# 04 — Dynamic Mechanistic Conformation Scoring (DMCS)

## Purpose and scope

This directory contains the canonical 15-system DMCS analysis: source descriptor tables, per-enzyme processed outputs, normalization/ranking scripts, RMSF pocket definition, provenance audit and collected numerical DAT files.

DMCS is a comparative, descriptor-based prioritization framework. It integrates catalytic geometry, active-site flexibility, conformational persistence and an MM/GBSA-derived energetic descriptor. It is not an experimentally calibrated activity predictor.

## DMCS equation and weights

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`

Dcat is assembled from three distance components: catalytic residue–PLP (0.50), PLP–furfural (0.25) and PLP–IPA (0.25).

Distances and catalytic-pocket RMSF are inverse min–max normalized. Dconf is positive min–max normalized from the natural logarithm of the dominant-cluster frame fraction. Dene is positive min–max normalized from the absolute value of signed GB `DELTA TOTAL`. Normalization is performed across the defined 15-enzyme panel.

## Canonical RMSF/Drig definition

All 15 systems have a common protein-only per-residue Cα RMSF file, `rmsf_protein_calpha.dat`. For each enzyme separately, protein residues with at least one heavy atom within 5.0 Å of any heavy atom in the prepared PLP (UNP) + furfural (UNL) + IPA (UNI) assembly are selected. Drig is the arithmetic mean of the selected residue-wise Cα RMSF values. Residue numbering is system-specific and is not transferred between enzymes.

The full residue map is `DMCS_ACTIVE_SITE_RESIDUES.csv`; the 4.0/5.0/6.0 Å sensitivity analysis is `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`. See [DMCS_RMSF_METHOD.md](DMCS_RMSF_METHOD.md) for the complete procedure.

## Main files

| File/folder | Purpose |
|---|---|
| `S1_INPUTS.csv` | 15-system source manifest: enzyme label, source directory, catalytic residue and distance filename |
| `S1_descriptor_extraction.py` | Source descriptor extraction, validation, structure-derived pocket map and cutoff sensitivity |
| `S2_DMCS_normalization.py` | Normalization and weighted score calculation from the raw descriptor table |
| `S3_DMCS_ranking.py` | Validation and export of the final ranked panel |
| `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv` | Extracted raw descriptors and provenance fields |
| `DMCS_ACTIVE_SITE_RESIDUES.csv` | Per-residue canonical 5.0 Å pocket map |
| `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv` | Common protein Cα RMSF profile for all systems |
| `DMCS_RMSF_CUTOFF_SENSITIVITY.csv` | 4.0/5.0/6.0 Å sensitivity results |
| `DMCS_RESULTS.csv` | Raw descriptor matrix supplied to normalization |
| `DMCS_STANDARDIZED.csv` | Normalized components and DMCS |
| `DMCS_Final_Ranking.csv` | Final canonical 15-system ranking |
| `15_Enzyme_Analysis_Data/` | Harmonized per-enzyme processed tables and RMSF data |
| `15_Enzyme_Analysis_DAT_Files/` | Original collected per-enzyme numerical DAT outputs |
| `DMCS_DATA_PROVENANCE_AUDIT.md` | Source inventory and quality-control record |
| `DMCS_REPRODUCTION_GUIDE.md` | Reproduction routes and required files |
| `DMCS_15_SYSTEMS_INPUTS_AND_PROTOCOLS.md` | Per-system residue and input-file mapping |

## Canonical 5.0 Å ranking

| Rank | Enzyme | DMCS |
|---:|---|---:|
| 1 | ATA117-Rd11 | 0.915409 |
| 2 | A0A2G0CFH8 | 0.822636 |
| 3 | G-188 | 0.568524 |
| 4 | AspC | 0.551479 |
| 5 | F-188 | 0.536944 |
| 6 | Lys-W-TA | 0.531666 |
| 7 | A0A1B728H4 | 0.526610 |
| 8 | H-188 | 0.526297 |
| 9 | AptA | 0.463306 |
| 10 | A0A1Z5HPJ6 | 0.455464 |
| 11 | S-188 | 0.454378 |
| 12 | AB-R-ATA | 0.449235 |
| 13 | CV-TAm | 0.288440 |
| 14 | W-188 | 0.216602 |
| 15 | S-omega-TA | 0.108260 |

This is the canonical ranking for the 5.0 Å structure-derived pocket definition and the weights stated above. It supersedes provisional values calculated using heterogeneous legacy RMSF selections.

## Reproduction boundary

S2 and S3 can be run from the descriptor matrix included in this repository. Full S1 source re-extraction requires the original per-system analysis directories and all files listed in `DMCS_REPRODUCTION_GUIDE.md`; the complete source directories and production trajectories are not included. The repository distinguishes reproducing normalized ranking from deposited descriptors from regenerating descriptors from trajectories/source data.
