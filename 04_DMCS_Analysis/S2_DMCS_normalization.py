#!/usr/bin/env python3
"""S2: Normalize the locked 15-system descriptor matrix and calculate DMCS."""

from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INPUT_FILE = HERE / "DMCS_RESULTS.csv"
OUTPUT_FILE = HERE / "DMCS_STANDARDIZED.csv"

EXPECTED_ENZYMES = {
    "ATA117-Rd11", "A0A2G0CFH8", "Lys-W-TA", "AspC", "AptA",
    "H-188", "G-188", "F-188", "AB-R-ATA", "A0A1B728H4",
    "A0A1Z5HPJ6", "S-omega-TA", "S-188", "CV-TAm", "W-188"
}
EXPECTED_SYSTEM_COUNT = 15
REQUIRED_COLUMNS = [
    "Enzyme", "Lys_PLP", "PLP_UNL", "PLP_UNI",
    "RMSF", "ClusterFraction", "MMGBSA"
]


def minmax(series, column_name):
    """Scale values to [0, 1], with larger values scoring higher."""
    minimum, maximum = series.min(), series.max()
    if maximum == minimum:
        raise ValueError(
            f"{column_name} has identical values; min-max normalization is undefined."
        )
    return (series - minimum) / (maximum - minimum)


def inverse_minmax(series, column_name):
    """Scale values to [0, 1], with smaller values scoring higher."""
    return 1.0 - minmax(series, column_name)


def main():
    df = pd.read_csv(INPUT_FILE)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df.empty or df["Enzyme"].isna().any():
        raise ValueError("Input is empty or contains missing enzyme identifiers.")

    df["Enzyme"] = df["Enzyme"].astype(str).str.strip()
    if df["Enzyme"].duplicated().any():
        duplicates = df.loc[df["Enzyme"].duplicated(), "Enzyme"].tolist()
        raise ValueError(f"Duplicate enzyme identifiers: {duplicates}")

    observed = set(df["Enzyme"])
    if len(df) != EXPECTED_SYSTEM_COUNT or observed != EXPECTED_ENZYMES:
        raise ValueError(
            "Input must match the defined 15-system analysis panel. "
            f"Missing={sorted(EXPECTED_ENZYMES - observed)}; "
            f"unexpected={sorted(observed - EXPECTED_ENZYMES)}"
        )

    numeric_columns = REQUIRED_COLUMNS[1:]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if not np.isfinite(df[numeric_columns].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite numerical descriptor values detected.")
    if (df["RMSF"] < 0).any():
        raise ValueError("RMSF cannot be negative.")
    if (df["ClusterFraction"] <= 0).any() or (df["ClusterFraction"] > 1).any():
        raise ValueError("ClusterFraction must be in the interval (0, 1].")

    # Catalytic readiness: inverse-normalized distance descriptors.
    df["Lys_PLP_norm"] = inverse_minmax(df["Lys_PLP"], "Lys_PLP")
    df["PLP_UNL_norm"] = inverse_minmax(df["PLP_UNL"], "PLP_UNL")
    df["PLP_UNI_norm"] = inverse_minmax(df["PLP_UNI"], "PLP_UNI")
    df["Dcat"] = (
        0.50 * df["Lys_PLP_norm"]
        + 0.25 * df["PLP_UNL_norm"]
        + 0.25 * df["PLP_UNI_norm"]
    )

    # Rigidity: lower mean active-site RMSF receives a higher score.
    df["Drig"] = inverse_minmax(df["RMSF"], "RMSF")

    # Conformational persistence: logarithm of the largest-cluster fraction.
    df["Cluster_log"] = np.log(df["ClusterFraction"])
    df["Dconf"] = minmax(df["Cluster_log"], "Cluster_log")

    # Energetic stabilization: magnitude of the signed GB binding free energy.
    df["MMGBSA_abs"] = df["MMGBSA"].abs()
    df["Dene"] = minmax(df["MMGBSA_abs"], "MMGBSA_abs")

    df["DMCS"] = (
        0.40 * df["Dcat"]
        + 0.25 * df["Drig"]
        + 0.15 * df["Dconf"]
        + 0.20 * df["Dene"]
    )
    df = df.sort_values("DMCS", ascending=False).reset_index(drop=True)
    df["Rank"] = np.arange(1, len(df) + 1)

    output_columns = [
        "Rank", "Enzyme", "Lys_PLP", "PLP_UNL", "PLP_UNI",
        "RMSF", "ClusterFraction", "MMGBSA",
        "Dcat", "Drig", "Dconf", "Dene", "DMCS"
    ]
    df[output_columns].to_csv(OUTPUT_FILE, index=False, float_format="%.9f")
    print("DMCS normalization completed.")
    print(f"Systems processed: {len(df)}")
    print(df[["Rank", "Enzyme", "DMCS"]].to_string(index=False))


if __name__ == "__main__":
    main()
