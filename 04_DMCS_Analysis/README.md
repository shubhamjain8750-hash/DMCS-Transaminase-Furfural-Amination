# 04 – Dynamic Mechanistic Conformation Scoring (DMCS) Analysis

## Overview

This directory contains the S1–S3 workflow for the comparative evaluation of 15 PLP-dependent transaminase systems involved in furfural amination.

The workflow is organized into:
1. **S1 – Raw descriptor extraction and compilation**
2. **S2 – Descriptor normalization and DMCS calculation**
3. **S3 – Comparative ranking and summary generation**

DMCS is a weighted descriptor-normalization and ranking framework; it is not a trained predictive machine-learning model.

## Repository contents

| File | Purpose |
|---|---|
| `S1_INPUTS.csv` | 15-system manifest, including raw-data paths and RMSF/MMGBSA provenance statuses |
| `S1_descriptor_extraction.py` | Extracts distance and largest-cluster descriptors; compiles the manifest RMSF and GB-energy values |
| `README_S1_DESCRIPTOR_EXTRACTION.md` | S1 data contract and execution guide |
| `README_DATA_PROVENANCE.md` | Explanation of descriptor provenance fields |
| `DMCS_DATA_PROVENANCE_AUDIT.md` | Raw-data validation findings and reproducibility checklist |
| `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv` | Exact distance means, frame counts, cluster metrics and GB/PB energy values parsed from the uploaded system outputs |
| `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv` | Residue-wise RMSF output retained for active-site mapping and audit |
| `DMCS_15_SYSTEMS_INPUTS_AND_PROTOCOLS.md` | Consolidated system-specific CPPTRAJ, RMSF, MD and MMPBSA inputs |
| `DMCS_RESULTS.csv` | S1-compatible raw descriptor matrix |
| `DMCS_Descriptor_Summary.csv` | Compact raw descriptor summary |
| `S2_DMCS_normalization.py` | Calculates normalized component scores and composite DMCS |
| `DMCS_STANDARDIZED.csv` | Normalized descriptor table |
| `S3_DMCS_ranking.py` | Validates and sorts the 15-system panel |
| `DMCS_Final_Ranking.csv` | Current provisional ranked output |

## Analysis panel

The 15 evaluated systems are:

ATA117-Rd11, A0A2G0CFH8, Lys-W-TA, AspC, AptA, H-188, G-188, F-188, AB-R-ATA, A0A1B728H4, A0A1Z5HPJ6, S-omega-TA, S-188, CV-TAm and W-188.

For ATA117-Rd11, the selected production analysis folder is `ATA-117-rd11_rerun_500ns`.

## DMCS scoring definition

| Component | Definition | Weight |
|---|---|---:|
| Dcat | Catalytic readiness | 0.40 |
| Drig | Active-site rigidity | 0.25 |
| Dconf | Conformational persistence | 0.15 |
| Dene | Energetic stabilization | 0.20 |

Catalytic-readiness subweights:

| Descriptor | Weight |
|---|---:|
| Catalytic-residue–PLP distance | 0.50 |
| PLP–furfural distance | 0.25 |
| PLP–isopropylamine distance | 0.25 |

S2 uses inverse min–max normalization for distance descriptors and RMSF, and positive min–max normalization for the logarithm of the largest-cluster fraction and the absolute magnitude of signed GB ΔG.

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`

The legacy column name `Lys_PLP` is retained for code compatibility. Chemically, it represents the catalytic-residue–PLP distance for every system.

## Execution

Install the Python dependencies:

```bash
pip install numpy pandas
```

Set the analysis root (the parent directory containing the 15 system folders):

```bash
export DMCS_ANALYSIS_ROOT="$HOME/amber24"
```

Run the scripts in sequence:

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py
python 04_DMCS_Analysis/S2_DMCS_normalization.py
python 04_DMCS_Analysis/S3_DMCS_ranking.py
```

S1 requires `RMSF_Status` and `MMGBSA_Status` to be `VERIFIED` for every row by default. While RMSF mapping remains under review, an exploratory compilation can be explicitly requested with:

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py --allow-provisional
```

This override does not promote provisional values to verified values.

## Current provisional ranking

The current ranking was recalculated using exact mean distances, largest-cluster fractions and the first GB `DELTA TOTAL` values extracted from the uploaded raw outputs. Historical RMSF values are retained where the archive did not contain a system-specific active-site selection, and two available RMSF selections contain only a single residue. Therefore, the numerical ranking is **provisional pending completion of consistent active-site RMSF mapping**.

| Rank | Enzyme | DMCS |
|---:|---|---:|
| 1 | ATA117-Rd11 | 0.9063 |
| 2 | A0A2G0CFH8 | 0.8532 |
| 3 | Lys-W-TA | 0.6291 |
| 4 | AspC | 0.5955 |
| 5 | AptA | 0.5800 |
| 6 | H-188 | 0.4556 |
| 7 | G-188 | 0.4292 |
| 8 | F-188 | 0.4250 |
| 9 | AB-R-ATA | 0.3974 |
| 10 | A0A1B728H4 | 0.3863 |
| 11 | A0A1Z5HPJ6 | 0.3821 |
| 12 | S-omega-TA | 0.3562 |
| 13 | S-188 | 0.3091 |
| 14 | CV-TAm | 0.2247 |
| 15 | W-188 | 0.1651 |

## Data handling

The raw descriptor table retains 50,000-frame distance-series statistics, largest-cluster frame counts/fractions and signed GB/PB energy values. The residue-wise RMSF table preserves the data needed to audit active-site selections. Production trajectory files are not included.

Complete the checks in `DMCS_DATA_PROVENANCE_AUDIT.md` before treating manuscript-reported scores as provenance-closed final values.
