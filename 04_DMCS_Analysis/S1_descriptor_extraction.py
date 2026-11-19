
#!/usr/bin/env python3

"""
S1: Raw DMCS Descriptor Compilation

Purpose:
    Compile molecular dynamics-derived descriptors from individual
    enzyme-system analysis folders into a single dataset.

Input:
    S1_INPUTS.csv

Required columns:
    Enzyme
    Directory
    RMSF
    MMGBSA
    CatalyticDistanceFile

Per-system files:
    Catalytic-residue–PLP distance file
    plp_unl.dat
    plp_uni.dat
    dmcs_cluster_summary.dat

RMSF and MMGBSA:
    Previously calculated descriptor values are supplied through
    S1_INPUTS.csv. This script does not rerun RMSF or MM/GBSA.

Output:
    DMCS_RESULTS.csv

The output schema is retained for compatibility with S2.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT = Path("S1_INPUTS.csv")
OUTPUT = Path("DMCS_RESULTS.csv")

EXPECTED_SYSTEMS = 15

REQUIRED_COLUMNS = {
    "Enzyme",
    "Directory",
    "CatalyticDistanceFile",
    "RMSF",
    "MMGBSA"
}


# --------------------------------------------------
# DISTANCE EXTRACTION
# --------------------------------------------------

def mean_second_column(path):
    """Calculate the mean of the second column of a cpptraj distance file."""

    if not path.is_file():
        raise FileNotFoundError(f"Missing distance file: {path}")

    arr = np.loadtxt(path, comments="#", ndmin=2)

    if arr.shape[1] < 2:
        raise ValueError(
            f"{path}: expected at least two numerical columns."
        )

    values = arr[:, 1]
    values = values[np.isfinite(values)]

    if len(values) == 0:
        raise ValueError(
            f"{path}: no finite distance values found."
        )

    return float(np.mean(values))


# --------------------------------------------------
# CLUSTER EXTRACTION
# --------------------------------------------------

def largest_cluster(path):
    """
    Identify the largest cluster using its frame count.

    Expected columns:
        Column 1: Cluster identifier
        Column 2: Number of frames
        Column 3: Cluster fraction
    """

    if not path.is_file():
        raise FileNotFoundError(f"Missing cluster file: {path}")

    clusters = []

    with path.open() as handle:

        for line in handle:

            if not line.strip() or line.lstrip().startswith("#"):
                continue

            columns = line.split()

            if len(columns) < 3:
                raise ValueError(
                    f"Unexpected cluster-summary row: {line.strip()}"
                )

            frames = int(float(columns[1]))
            fraction = float(columns[2])

            if (
                frames < 0
                or not np.isfinite(fraction)
                or not 0 <= fraction <= 1
            ):
                raise ValueError(
                    f"Invalid cluster data: {line.strip()}"
                )

            clusters.append((frames, fraction))

    if not clusters:
        raise ValueError(
            f"No cluster data rows found in {path}"
        )

    # Select the cluster containing the maximum number of frames.
    frames, fraction = max(clusters, key=lambda item: item[0])

    if frames == 0 or fraction <= 0:
        raise ValueError(
            f"Invalid largest-cluster result in {path}"
        )

    return frames, fraction


# --------------------------------------------------
# MAIN WORKFLOW
# --------------------------------------------------

def main():

    if not INPUT.is_file():
        raise FileNotFoundError(
            "S1_INPUTS.csv not found. "
            "Prepare the input manifest before running S1."
        )

    df = pd.read_csv(INPUT)

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing input columns: {sorted(missing)}"
        )

    # Validate identifiers and paths.
    for column in ("Enzyme", "Directory", "CatalyticDistanceFile"):
        df[column] = df[column].astype(str).str.strip()

    if df[["Enzyme", "Directory", "CatalyticDistanceFile"]].isna().any().any():
        raise ValueError("Missing enzyme, directory, or distance filename.")

    if df["Enzyme"].duplicated().any():
        raise ValueError(
            "Duplicate enzyme identifiers in S1_INPUTS.csv."
        )

    if len(df) != EXPECTED_SYSTEMS:
        raise ValueError(
            f"Expected {EXPECTED_SYSTEMS} enzyme systems; "
            f"found {len(df)}."
        )

    # Validate previously calculated descriptors.
    for column in ("RMSF", "MMGBSA"):
        df[column] = pd.to_numeric(df[column], errors="raise")

    if not np.isfinite(
        df[["RMSF", "MMGBSA"]].to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "RMSF or MMGBSA contains non-finite values."
        )

    if (df["RMSF"] < 0).any():
        raise ValueError("RMSF cannot be negative.")

    results = []

    # Process each enzyme system.
    for record in df.to_dict("records"):

        enzyme = record["Enzyme"]

        folder = Path(record["Directory"]).expanduser()

        if not folder.is_absolute():
            folder = Path.cwd() / folder

        if not folder.is_dir():
            raise FileNotFoundError(
                f"Analysis directory not found for {enzyme}: {folder}"
            )

        catalytic_file = (
            folder / record["CatalyticDistanceFile"]
        )

        unl_file = folder / "plp_unl.dat"
        uni_file = folder / "plp_uni.dat"
        cluster_file = folder / "dmcs_cluster_summary.dat"

        # Raw distance descriptors.
        catalytic_distance = mean_second_column(catalytic_file)
        plp_unl = mean_second_column(unl_file)
        plp_uni = mean_second_column(uni_file)

        # Largest-cluster descriptor.
        cluster_frames, cluster_fraction = largest_cluster(
            cluster_file
        )

        results.append({
            "Enzyme": enzyme,

            # Retained field name for compatibility with S2.
            "Lys_PLP": catalytic_distance,

            "PLP_UNL": plp_unl,
            "PLP_UNI": plp_uni,
            "RMSF": float(record["RMSF"]),
            "ClusterFraction": cluster_fraction,
            "MMGBSA": float(record["MMGBSA"])
        })

        print(
            f"Processed {enzyme}: "
            f"largest cluster = {cluster_frames} frames"
        )

    # Compile and validate final raw descriptor dataset.
    output = pd.DataFrame(results)

    numeric_columns = [
        "Lys_PLP",
        "PLP_UNL",
        "PLP_UNI",
        "RMSF",
        "ClusterFraction",
        "MMGBSA"
    ]

    if not np.isfinite(
        output[numeric_columns].to_numpy(dtype=float)
    ).all():
        raise ValueError(
            "Non-finite values detected in final descriptor dataset."
        )

    if (output["ClusterFraction"] <= 0).any():
        raise ValueError(
            "Cluster fractions must be greater than zero."
        )

    output.to_csv(
        OUTPUT,
        index=False,
        float_format="%.6f"
    )

    print("\nS1 descriptor compilation completed successfully.")
    print(f"Enzyme systems processed: {len(output)}")
    print(f"Output generated: {OUTPUT}")


if __name__ == "__main__":
    main()
