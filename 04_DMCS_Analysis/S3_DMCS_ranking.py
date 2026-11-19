
#!/usr/bin/env python3

"""
Script S3: DMCS Ranking and Summary Table Generation

Input:
    DMCS_STANDARDIZED.csv

Output:
    DMCS_Final_Ranking.csv

Purpose:
    Rank enzyme systems according to their DMCS scores
    and generate the final comparative descriptor table.
"""

import numpy as np
import pandas as pd

INPUT_FILE = "DMCS_STANDARDIZED.csv"
OUTPUT_FILE = "DMCS_Final_Ranking.csv"

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

    if not np.isfinite(
        df[REQUIRED_COLUMNS[1:]].to_numpy(dtype=float)
    ).all():
        raise ValueError("Non-finite descriptor values detected.")

    # Rank enzymes by DMCS score
    df = df.sort_values(
        by="DMCS",
        ascending=False
    ).reset_index(drop=True)

    df["Rank"] = np.arange(1, len(df) + 1)

    # Round normalized descriptor values
    numeric_columns = [
        "Dcat",
        "Drig",
        "Dconf",
        "Dene",
        "DMCS"
    ]

    df[numeric_columns] = df[numeric_columns].round(4)

    # Generate final ranking table
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

    summary.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(summary)

    print(
        "\nDMCS summary table generated successfully."
    )


if __name__ == "__main__":
    main()
