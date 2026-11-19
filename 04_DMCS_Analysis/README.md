# 04 – Dynamic Mechanistic Conformation Scoring (DMCS) Analysis

## Overview

This directory contains the S1–S3 computational workflow for descriptor-based evaluation and prioritization of 15 PLP-dependent transaminase systems involved in furfural amination.

The analysis is organized into three stages:

1. **S1 – Raw descriptor extraction and compilation**
2. **S2 – Descriptor normalization and composite DMCS calculation**
3. **S3 – Final ranking and comparative summary generation**

The DMCS implementation is a weighted descriptor-normalization and ranking framework. It is **not a trained predictive machine-learning model**.

## Repository contents

| File | Purpose |
|---|---|
| `S1_INPUTS.csv` | 15-system manifest with analysis paths, catalytic distance filenames, RMSF/MMGBSA values and provenance statuses |
| `S1_descriptor_extraction.py` | Extracts CPPTRAJ distances and largest-cluster fraction; compiles supplied RMSF and MMGBSA |
| `README_S1_DESCRIPTOR_EXTRACTION.md` | S1 data contract, extraction details and execution instructions |
| `README_DATA_PROVENANCE.md` | Meaning of manifest provenance fields |
| `DMCS_DATA_PROVENANCE_AUDIT.md` | System-by-system data-quality findings and closure checklist |
| `DMCS_RESULTS.csv` | Current raw descriptor table used by S2 |
| `S2_DMCS_normalization.py` | Normalizes descriptors and calculates Dcat, Drig, Dconf, Dene and DMCS |
| `DMCS_STANDARDIZED.csv` | Current normalized descriptor table |
| `S3_DMCS_ranking.py` | Validates and ranks the 15 systems |
| `DMCS_Final_Ranking.csv` | Current ranked output |

## Locked analysis panel

The 15 retained systems are:

ATA117-Rd11, A0A2G0CFH8, Lys-W-TA, AspC, AptA, H-188, G-188, F-188, AB-R-ATA, A0A1B728H4, A0A1Z5HPJ6, S-omega-TA, S-188, CV-TAm and W-188.

Excluded systems: A0A1V0DD42 and A0A2L2XFE1.

For ATA117-Rd11, use the selected rerun folder `ATA-117-rd11_rerun_500ns`; do not use the older `rd11-500nss` run.

## DMCS scoring definition

Outer component weights:

| Component | Definition | Weight |
|---|---|---:|
| Dcat | Catalytic readiness | 0.40 |
| Drig | Active-site rigidity | 0.25 |
| Dconf | Conformational persistence | 0.15 |
| Dene | Energetic stabilization | 0.20 |

Catalytic subweights:

| Descriptor | Definition | Subweight |
|---|---|---:|
| Catalytic residue–PLP | Catalytic residue–PLP distance | 0.50 |
| PLP–UNL | PLP–furfural distance | 0.25 |
| PLP–UNI | PLP–isopropylamine distance | 0.25 |

S2 applies inverse min–max normalization to distance descriptors and RMSF. It applies positive min–max normalization to ln(largest-cluster fraction) and to the absolute magnitude of signed GB ΔG. The composite score is:

**DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene**

The legacy raw-distance column name `Lys_PLP` is retained for code compatibility; chemically, it represents catalytic-residue–PLP distance for all systems, including the Lys188 substitutions.

## Execution

Install dependencies:

```bash
pip install numpy pandas
```

Set the path containing the 15 analysis directories:

```bash
export DMCS_ANALYSIS_ROOT="$HOME/amber24"
```

Run in order:

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py
python 04_DMCS_Analysis/S2_DMCS_normalization.py
python 04_DMCS_Analysis/S3_DMCS_ranking.py
```

**Important:** S1 now requires both RMSF_Status and MMGBSA_Status to be `VERIFIED` for every system. Until the provenance audit is complete, exploratory output requires an explicit override:

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py --allow-provisional
```

The override allows exploratory compilation only. It does not make provisional values verified.

## Current ranking — provisional pending provenance audit

The currently committed ranking is arithmetically consistent with the committed DMCS_RESULTS.csv and current S2 formula. However, several RMSF selections/values and MM/GBSA source values still require raw-file verification. Therefore, the table below is retained as the **current provisional ranking**, not as a provenance-closed final ranking.

| Rank | Enzyme | DMCS |
|---:|---|---:|
| 1 | ATA117-Rd11 | 0.9063 |
| 2 | A0A2G0CFH8 | 0.8531 |
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
| 14 | CV-TAm | 0.2248 |
| 15 | W-188 | 0.1651 |

Do not mix the current 0.9063 score with the earlier 0.8394 score from a previous DMCS version/run.

## Reproducibility and data handling

S1 compiles existing CPPTRAJ outputs and manifest-supplied RMSF/MMGBSA values; it does not regenerate MD, RMSF, clustering or MM/GBSA calculations. Retain the corresponding system-specific CPPTRAJ inputs, distance time series, cluster summaries, RMSF masks/raw outputs and MMPBSA outputs.

Do not upload large NetCDF trajectories or bulky topology/coordinate files. Keep compact inputs, outputs, scripts, manifests and provenance records in version control; document external storage and checksums separately.

Complete the checklist in `DMCS_DATA_PROVENANCE_AUDIT.md` before freezing manuscript-reported DMCS scores.