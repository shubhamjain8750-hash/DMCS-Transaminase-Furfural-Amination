
#!/usr/bin/env python3

"""
Script S2: Descriptor Normalization and DMCS Calculation

Input:
    DMCS_RESULTS.csv

Required columns:
    Enzyme
    Lys_PLP
    PLP_UNL
    PLP_UNI
    RMSF
    ClusterFraction
    MMGBSA

Output:
    DMCS_STANDARDIZED.csv

DMCS weights:
    Dcat  = 0.40
    Drig  = 0.25
    Dconf = 0.15
    Dene  = 0.20
"""

import numpy as np
import pandas as pd

INPUT_FILE = "DMCS_RESULTS.csv"
OUTPUT_FILE = "DMCS_STANDARDIZED.csv"

REQUIRED_COLUMNS = [
    "Enzyme",
    "Lys_PLP",
    "PLP_UNL",
    "PLP_UNI",
    "RMSF",
    "ClusterFraction",
    "MMGBSA"
]


def minmax(series, column_name):
    """Normalize larger values to higher scores."""

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        raise ValueError(
            f"{column_name} has identical values; "
            "min-max normalization is undefined."
        )

    return (series - minimum) / (maximum - minimum)


def inverse_minmax(series, column_name):
    """Normalize smaller values to higher scores."""

    return 1.0 - minmax(series, column_name)


def main():

    df = pd.read_csv(INPUT_FILE)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df.empty:
        raise ValueError("Input dataset is empty.")

    if df["Enzyme"].isna().any():
        raise ValueError("Enzyme identifiers contain missing values.")

    numeric_columns = REQUIRED_COLUMNS[1:]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="raise")

    if not np.isfinite(
        df[numeric_columns].to_numpy(dtype=float)
    ).all():
        raise ValueError("Non-finite numerical values detected.")

    if (df["ClusterFraction"] <= 0).any():
        raise ValueError(
            "ClusterFraction must be greater than zero."
        )

    # 1. Catalytic readiness
    df["Lys_PLP_norm"] = inverse_minmax(
        df["Lys_PLP"], "Lys_PLP"
    )

    df["PLP_UNL_norm"] = inverse_minmax(
        df["PLP_UNL"], "PLP_UNL"
    )

    df["PLP_UNI_norm"] = inverse_minmax(
        df["PLP_UNI"], "PLP_UNI"
    )

    df["Dcat"] = (
        0.50 * df["Lys_PLP_norm"]
        + 0.25 * df["PLP_UNL_norm"]
        + 0.25 * df["PLP_UNI_norm"]
    )

    # 2. Active-site rigidity
    df["Drig"] = inverse_minmax(
        df["RMSF"], "RMSF"
    )

    # 3. Conformational persistence
    df["Cluster_log"] = np.log(df["ClusterFraction"])

    df["Dconf"] = minmax(
        df["Cluster_log"], "Cluster_log"
    )

    # 4. Energetic stabilization
    df["MMGBSA_abs"] = df["MMGBSA"].abs()

    df["Dene"] = minmax(
        df["MMGBSA_abs"], "MMGBSA_abs"
    )

    # 5. Composite DMCS score
    df["DMCS"] = (
        0.40 * df["Dcat"]
        + 0.25 * df["Drig"]
        + 0.15 * df["Dconf"]
        + 0.20 * df["Dene"]
    )

    # 6. Rank enzymes
    df = df.sort_values(
        by="DMCS",
        ascending=False
    ).reset_index(drop=True)

    df["Rank"] = np.arange(1, len(df) + 1)

    output_columns = [
        "Rank",
        "Enzyme",
        "Lys_PLP",
        "PLP_UNL",
        "PLP_UNI",
        "RMSF",
        "ClusterFraction",
        "MMGBSA",
        "Dcat",
        "Drig",
        "Dconf",
        "Dene",
        "DMCS"
    ]

    df[output_columns].to_csv(
        OUTPUT_FILE,
        index=False,
        float_format="%.6f"
    )

    print("DMCS calculation completed successfully.")
    print(df[["Rank", "Enzyme", "DMCS"]])


if __name__ == "__main__":
    main()
