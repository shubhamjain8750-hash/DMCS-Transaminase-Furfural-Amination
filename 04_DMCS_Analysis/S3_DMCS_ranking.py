#!/usr/bin/env python3

"""
Script S3: DMCS Ranking and Summary Table Generation

Input:
    DMCS_STANDARDIZED.csv

Output:
    DMCS_Final_Ranking.csv

Purpose:
    Rank the 15 retained enzyme systems according to their DMCS scores
    and generate the final comparative descriptor table.

Excluded systems:
    A0A1V0DD42
    A0A2L2XFE1

Note:
    This script ranks DMCS scores; it does not train a predictive
    machine-learning model.
"""

import numpy as np
import pandas as pd

INPUT_FILE = "DMCS_STANDARDIZED.csv"
OUTPUT_FILE = "DMCS_Final_Ranking.csv"

EXCLUDED_SYSTEMS = {
    "A0A1V0DD42",
    "A0A2L2XFE1"
}
EXPECTED_SYSTEM_COUNT = 15

REQUIRED_COLUMNS = [
    "Enzyme",
    "Dcat",
    "Drig",
    "Dconf",
    "Dene",
    "DMCS"
]


def main():
    df = pd.read_csv(INPUT_FILE)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if df.empty:
        raise ValueError("Input dataset is empty.")

    df["Enzyme"] = df["Enzyme"].astype(str).str.strip()

    # Safety filter: ensure excluded systems cannot enter the final ranking.
    df = df.loc[~df["Enzyme"].isin(EXCLUDED_SYSTEMS)].copy()

    if len(df) != EXPECTED_SYSTEM_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_SYSTEM_COUNT} systems after exclusions; "
            f"found {len(df)}. Check DMCS_STANDARDIZED.csv."
        )

    if df["Enzyme"].duplicated().any():
        duplicates = df.loc[
            df["Enzyme"].duplicated(), "Enzyme"
        ].tolist()
        raise ValueError(f"Duplicate enzyme identifiers: {duplicates}")

    numeric_columns = REQUIRED_COLUMNS[1:]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="raise")

    if not np.isfinite(
        df[numeric_columns].to_numpy(dtype=float)
    ).all():
        raise ValueError("Non-finite descriptor values detected.")

    # Rank enzymes by DMCS score
    df = df.sort_values(
        by="DMCS", ascending=False
    ).reset_index(drop=True)
    df["Rank"] = np.arange(1, len(df) + 1)

    # Round normalized descriptor values
    score_columns = [
        "Dcat", "Drig", "Dconf", "Dene", "DMCS"
    ]
    df[score_columns] = df[score_columns].round(4)

    summary = df[
        [
            "Rank",
            "Enzyme",
            "Dcat",
            "Drig",
            "Dconf",
            "Dene",
            "DMCS"
        ]
    ]

    summary.to_csv(OUTPUT_FILE, index=False)

    print(summary.to_string(index=False))
    print(
        f"\nDMCS summary table generated successfully "
        f"for {len(summary)} enzyme systems."
    )


if __name__ == "__main__":
    main()
