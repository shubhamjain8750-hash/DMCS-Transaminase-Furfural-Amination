#!/usr/bin/env python3
"""S1: Compile raw DMCS descriptors from 15 enzyme-system analysis folders.

RMSF and MM/GBSA are supplied by S1_INPUTS.csv and are not recalculated here.
By default, S1 requires both provenance status fields to be VERIFIED.
Use --allow-provisional only for exploratory regeneration while the provenance
audit is open. See DMCS_DATA_PROVENANCE_AUDIT.md.
"""

from argparse import ArgumentParser
from pathlib import Path
import os
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUT = HERE / "S1_INPUTS.csv"
OUTPUT = HERE / "DMCS_RESULTS.csv"
EXPECTED_SYSTEMS = 15
REQUIRED_COLUMNS = {
    "Enzyme", "Directory", "CatalyticDistanceFile", "RMSF", "MMGBSA",
    "RMSF_Status", "MMGBSA_Status"
}
EXPECTED_ENZYMES = {
    "ATA117-Rd11", "A0A2G0CFH8", "Lys-W-TA", "AspC", "AptA",
    "H-188", "G-188", "F-188", "AB-R-ATA", "A0A1B728H4",
    "A0A1Z5HPJ6", "S-omega-TA", "S-188", "CV-TAm", "W-188"
}


def mean_second_column(path: Path) -> float:
    """Return the mean of the second numeric column in a CPPTRAJ output."""
    if not path.is_file():
        raise FileNotFoundError(f"Missing distance file: {path}")
    arr = np.loadtxt(path, comments="#", ndmin=2)
    if arr.shape[1] < 2:
        raise ValueError(f"{path}: expected at least two numeric columns.")
    values = arr[:, 1]
    values = values[np.isfinite(values)]
    if values.size == 0:
        raise ValueError(f"{path}: no finite distance values found.")
    return float(np.mean(values))


def largest_cluster(path: Path):
    """Return (frame_count, fraction) for the cluster with most frames."""
    if not path.is_file():
        raise FileNotFoundError(f"Missing cluster file: {path}")
    clusters = []
    with path.open() as handle:
        for line in handle:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split()
            if len(fields) < 3:
                raise ValueError(f"Unexpected cluster row in {path}: {line.strip()}")
            frames = int(float(fields[1]))
            fraction = float(fields[2])
            if frames < 0 or not np.isfinite(fraction) or not 0 <= fraction <= 1:
                raise ValueError(f"Invalid cluster row in {path}: {line.strip()}")
            clusters.append((frames, fraction))
    if not clusters:
        raise ValueError(f"No cluster data rows found in {path}")
    frames, fraction = max(clusters, key=lambda item: item[0])
    if frames <= 0 or fraction <= 0:
        raise ValueError(f"Invalid largest-cluster result in {path}")
    return frames, fraction


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-provisional",
        action="store_true",
        help="Allow RMSF/MMGBSA values whose manifest provenance status is not VERIFIED.",
    )
    parser.add_argument(
        "--analysis-root",
        default=os.environ.get("DMCS_ANALYSIS_ROOT", "."),
        help="Root containing the 15 enzyme analysis folders (default: DMCS_ANALYSIS_ROOT or current directory).",
    )
    args = parser.parse_args()

    if not INPUT.is_file():
        raise FileNotFoundError(f"Input manifest not found: {INPUT}")
    df = pd.read_csv(INPUT)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing manifest columns: {sorted(missing)}")

    for col in ("Enzyme", "Directory", "CatalyticDistanceFile",
                "RMSF_Status", "MMGBSA_Status"):
        if df[col].isna().any():
            raise ValueError(f"Missing values in {col}.")
        df[col] = df[col].astype(str).str.strip()
        if (df[col] == "").any():
            raise ValueError(f"Empty values in {col}.")

    if df["Enzyme"].duplicated().any():
        raise ValueError("Duplicate enzyme identifiers in S1_INPUTS.csv.")
    if len(df) != EXPECTED_SYSTEMS:
        raise ValueError(f"Expected {EXPECTED_SYSTEMS} systems; found {len(df)}.")
    observed = set(df["Enzyme"])
    if observed != EXPECTED_ENZYMES:
        raise ValueError(
            "Input enzyme panel does not match the locked 15-system panel. "
            f"Missing={sorted(EXPECTED_ENZYMES - observed)}; "
            f"unexpected={sorted(observed - EXPECTED_ENZYMES)}"
        )

    for col in ("RMSF", "MMGBSA"):
        df[col] = pd.to_numeric(df[col], errors="raise")
    if not np.isfinite(df[["RMSF", "MMGBSA"]].to_numpy(dtype=float)).all():
        raise ValueError("RMSF or MMGBSA contains non-finite values.")
    if (df["RMSF"] < 0).any():
        raise ValueError("RMSF cannot be negative.")

    unverified = df.loc[
        (df["RMSF_Status"] != "VERIFIED")
        | (df["MMGBSA_Status"] != "VERIFIED"),
        ["Enzyme", "RMSF_Status", "MMGBSA_Status"]
    ]
    if not unverified.empty and not args.allow_provisional:
        print(
            "S1 stopped: unverified/provisional RMSF or MMGBSA entries remain.\n"
            + unverified.to_string(index=False)
            + "\nVerify the source files and mark both fields VERIFIED, or use "
              "--allow-provisional for exploratory output.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if not unverified.empty:
        print(
            "WARNING: proceeding with provisional descriptors by explicit request.\n"
            + unverified.to_string(index=False),
            file=sys.stderr,
        )

    analysis_root = Path(args.analysis_root).expanduser().resolve()
    results = []
    for record in df.to_dict("records"):
        folder = Path(record["Directory"]).expanduser()
        if not folder.is_absolute():
            folder = analysis_root / folder
        if not folder.is_dir():
            raise FileNotFoundError(
                f"Analysis directory not found for {record['Enzyme']}: {folder}"
            )

        catalytic = mean_second_column(folder / record["CatalyticDistanceFile"])
        plp_unl = mean_second_column(folder / "plp_unl.dat")
        plp_uni = mean_second_column(folder / "plp_uni.dat")
        cluster_frames, cluster_fraction = largest_cluster(
            folder / "dmcs_cluster_summary.dat"
        )

        results.append({
            "Enzyme": record["Enzyme"],
            # Legacy column label retained for compatibility with S2.
            # It represents catalytic-residue–PLP distance for every system.
            "Lys_PLP": catalytic,
            "PLP_UNL": plp_unl,
            "PLP_UNI": plp_uni,
            "RMSF": float(record["RMSF"]),
            "ClusterFraction": cluster_fraction,
            "MMGBSA": float(record["MMGBSA"]),
        })
        print(
            f"Processed {record['Enzyme']}: "
            f"largest cluster = {cluster_frames} frames "
            f"(fraction {cluster_fraction:.6f})"
        )

    output = pd.DataFrame(results)
    numeric = ["Lys_PLP", "PLP_UNL", "PLP_UNI", "RMSF",
               "ClusterFraction", "MMGBSA"]
    if not np.isfinite(output[numeric].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite values found in compiled descriptors.")
    if (output["ClusterFraction"] <= 0).any():
        raise ValueError("Cluster fractions must be greater than zero.")

    output = output[
        ["Enzyme", "Lys_PLP", "PLP_UNL", "PLP_UNI",
         "RMSF", "ClusterFraction", "MMGBSA"]
    ]
    output.to_csv(OUTPUT, index=False, float_format="%.7f")
    print(f"\nS1 completed: {len(output)} systems -> {OUTPUT}")
    if not unverified.empty:
        print("OUTPUT STATUS: PROVISIONAL. Do not describe as final/validated.")


if __name__ == "__main__":
    main()
