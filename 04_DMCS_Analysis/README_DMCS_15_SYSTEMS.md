# DMCS Analysis

This folder contains the input descriptor table, normalized DMCS output,
final ranking, and scripts for the 15-system DMCS analysis.

## Analysis set
The analysis includes 15 enzyme systems. `A0A1V0DD42` and `A0A2L2XFE1`
are excluded before descriptor normalization.

## Workflow
1. `DMCS_RESULTS.csv` — descriptor input used by S2.
2. `S2_DMCS_normalization.py` — descriptor normalization and DMCS calculation;
   generates `DMCS_STANDARDIZED.csv`.
3. `S3_DMCS_ranking.py` — ranking and summary generation;
   generates `DMCS_Final_Ranking.csv`.

## DMCS weights
- Catalytic readiness (Dcat): 0.40
- Active-site rigidity (Drig): 0.25
- Conformational persistence (Dconf): 0.15
- Energetic stabilization (Dene): 0.20

Catalytic readiness subweights:
- Lys_PLP: 0.50
- PLP_UNL: 0.25
- PLP_UNI: 0.25

## Reproducibility
Run from this directory:
```bash
python S2_DMCS_normalization.py
python S3_DMCS_ranking.py
```

The scripts validate that exactly 15 unique systems remain after exclusions.
This is a descriptor-normalization and ranking workflow, not a predictive
machine-learning model training procedure.
