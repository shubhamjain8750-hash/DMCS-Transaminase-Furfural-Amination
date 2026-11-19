#!/usr/bin/env python3
"""S3: Validate and rank the locked 15-system DMCS panel."""

import numpy as np
import pandas as pd

INPUT_FILE = "DMCS_STANDARDIZED.csv"
OUTPUT_FILE = "DMCS_Final_Ranking.csv"
EXCLUDED_SYSTEMS = {"A0A1V0DD42", "A0A2L2XFE1"}
EXPECTED_ENZYMES = {
    "ATA117-Rd11", "A0A2G0CFH8", "Lys-W-TA", "AspC", "AptA",
    "H-188", "G-188", "F-188", "AB-R-ATA", "A0A1B728H4",
    "A0A1Z5HPJ6", "S-omega-TA", "S-188", "CV-TAm", "W-188"
}
REQUIRED_COLUMNS = ["Enzyme", "Dcat", "Drig", "Dconf", "Dene", "DMCS"]


def main():
    df = pd.read_csv(INPUT_FILE)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if df.empty or df["Enzyme"].isna().any():
        raise ValueError("Input is empty or contains missing enzyme identifiers.")

    df["Enzyme"] = df["Enzyme"].astype(str).str.strip()
    df = df.loc[~df["Enzyme"].isin(EXCLUDED_SYSTEMS)].copy()
    if df["Enzyme"].duplicated().any():
        duplicates = df.loc[df["Enzyme"].duplicated(), "Enzyme"].tolist()
        raise ValueError(f"Duplicate enzyme identifiers: {duplicates}")
    if len(df) != 15 or set(df["Enzyme"]) != EXPECTED_ENZYMES:
        raise ValueError(
            "Input must contain the locked 15-system panel. "
            f"Missing={sorted(EXPECTED_ENZYMES - set(df['Enzyme']))}; "
            f"unexpected={sorted(set(df['Enzyme']) - EXPECTED_ENZYMES)}"
        )

    numeric = REQUIRED_COLUMNS[1:]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if not np.isfinite(df[numeric].to_numpy(dtype=float)).all():
        raise ValueError("Non-finite component or DMCS values detected.")
    for col in ("Dcat", "Drig", "Dconf", "Dene", "DMCS"):
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} values must be within [0, 1].")

    df = df.sort_values("DMCS", ascending=False).reset_index(drop=True)
    df["Rank"] = np.arange(1, len(df) + 1)
    score_columns = ["Dcat", "Drig", "Dconf", "Dene", "DMCS"]
    df[score_columns] = df[score_columns].round(4)

    summary = df[[
        "Rank", "Enzyme", "Dcat", "Drig", "Dconf", "Dene", "DMCS"
    ]]
    summary.to_csv(OUTPUT_FILE, index=False)
    print(summary.to_string(index=False))
    print(f"\nDMCS ranking generated for {len(summary)} systems: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
