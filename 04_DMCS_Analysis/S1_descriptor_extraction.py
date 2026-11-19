#!/usr/bin/env python3
"""S1: Compile raw DMCS descriptors from per-enzyme output folders.

Each folder must contain lys_plp.dat, plp_unl.dat, plp_uni.dat and
dmcs_cluster_summary.dat. S1_INPUTS.csv must contain:
Enzyme,Directory,RMSF,MMGBSA

RMSF and MMGBSA are read per enzyme because the recovered historical
dmcs_HOMO1_v2.py hardcoded these descriptors. This script does not run
CPPTRAJ or MM/GBSA. Output: DMCS_RESULTS.csv for S2.
"""
from pathlib import Path
import numpy as np
import pandas as pd

INPUT = Path("S1_INPUTS.csv")
OUTPUT = Path("DMCS_RESULTS.csv")
EXPECTED = 15
EXCLUDED = {"A0A1V0DD42", "A0A2L2XFE1"}
REQUIRED = {"Enzyme", "Directory", "RMSF", "MMGBSA"}

def mean_second_column(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    arr = np.loadtxt(path, comments="#", ndmin=2)
    if arr.shape[1] < 2:
        raise ValueError(f"{path}: expected at least two columns")
    vals = arr[:, 1]
    vals = vals[np.isfinite(vals)]
    if not len(vals):
        raise ValueError(f"{path}: no finite distance values")
    return float(np.mean(vals))

def largest_cluster(path):
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open() as handle:
        for line in handle:
            cols = line.split()
            if not cols or line.lstrip().startswith("#"):
                continue
            if len(cols) < 3:
                raise ValueError(f"Unexpected row in {path}: {line.strip()}")
            frames, fraction = int(float(cols[1])), float(cols[2])
            if frames < 0 or not np.isfinite(fraction) or not 0 <= fraction <= 1:
                raise ValueError(f"Invalid cluster data in {path}: {line.strip()}")
            return frames, fraction
    raise ValueError(f"No data rows in {path}")

def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            "S1_INPUTS.csv missing. Copy S1_INPUTS_TEMPLATE.csv to "
            "S1_INPUTS.csv and fill in the 15 enzyme rows."
        )
    df = pd.read_csv(INPUT)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing input columns: {sorted(missing)}")
    df["Enzyme"] = df["Enzyme"].astype(str).str.strip()
    df["Directory"] = df["Directory"].astype(str).str.strip()
    df = df.loc[~df["Enzyme"].isin(EXCLUDED)].copy()
    if len(df) != EXPECTED:
        raise ValueError(f"Expected {EXPECTED} systems after exclusions; found {len(df)}")
    if df["Enzyme"].duplicated().any():
        raise ValueError("Duplicate enzyme identifiers in S1_INPUTS.csv")
    for col in ("RMSF", "MMGBSA"):
        df[col] = pd.to_numeric(df[col], errors="raise")
    if not np.isfinite(df[["RMSF", "MMGBSA"]].to_numpy(float)).all():
        raise ValueError("RMSF/MMGBSA contains non-finite values")

    rows = []
    for r in df.to_dict("records"):
        folder = Path(r["Directory"]).expanduser()
        if not folder.is_absolute():
            folder = Path.cwd() / folder
        cluster_frames, cluster_fraction = largest_cluster(folder / "dmcs_cluster_summary.dat")
        rows.append({
            "Enzyme": r["Enzyme"],
            "Lys_PLP": mean_second_column(folder / "lys_plp.dat"),
            "PLP_UNL": mean_second_column(folder / "plp_unl.dat"),
            "PLP_UNI": mean_second_column(folder / "plp_uni.dat"),
            "RMSF": float(r["RMSF"]),
            "ClusterFraction": cluster_fraction,
            "MMGBSA": float(r["MMGBSA"]),
        })
        print(f"Processed {r['Enzyme']} (largest cluster frames: {cluster_frames})")

    pd.DataFrame(rows).to_csv(OUTPUT, index=False, float_format="%.6f")
    print(f"Created {OUTPUT} with {len(rows)} systems.")

if __name__ == "__main__":
    main()
