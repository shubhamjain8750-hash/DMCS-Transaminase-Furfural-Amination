# 04 — Dynamic Mechanistic Conformation Scoring (DMCS)

## Purpose and scope

This directory contains the canonical 15-system DMCS analysis: source descriptor tables, harmonized per-enzyme processed outputs, normalization/ranking scripts, the structure-derived catalytic-pocket/RMSF method and source provenance records.

DMCS is a comparative, descriptor-based prioritization framework. It integrates catalytic geometry, catalytic-pocket flexibility, conformational persistence and a GB-derived energetic descriptor. It is not an experimentally calibrated activity predictor.

## DMCS equation and weights

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`

Dcat is assembled from three distance components: catalytic residue–PLP (0.50), PLP–furfural (0.25) and PLP–IPA (0.25).

Distances and catalytic-pocket RMSF are inverse min–max normalized. Dconf is positive min–max normalized from the natural logarithm of the dominant-cluster frame fraction. Dene is positive min–max normalized from the absolute value of signed GB `DELTA TOTAL`. All normalization is performed across the defined 15-enzyme panel.

## Canonical RMSF/Drig definition

All 15 systems have a common protein-only per-residue Cα RMSF source, `rmsf_protein_calpha.dat`. For each enzyme separately, protein residues with at least one heavy atom within 5.0 Å of any heavy atom in the prepared PLP (UNP) + furfural (UNL) + IPA (UNI) assembly are selected. Drig is the arithmetic mean of the selected residue-wise Cα RMSF values. Residue numbering is system-specific and is not transferred between enzymes.

The complete residue map is `DMCS_ACTIVE_SITE_RESIDUES.csv`; the 4.0/5.0/6.0 Å cutoff sensitivity analysis is `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`. See [DMCS_RMSF_METHOD.md](DMCS_RMSF_METHOD.md) for the complete method.

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

This ranking is specific to the 5.0 Å pocket definition, descriptor transformations, weights and 15-system panel. It supersedes provisional values generated using heterogeneous legacy RMSF selections.

## Main files

| File/folder | Purpose |
|---|---|
| `S1_INPUTS.csv` | Mapping of DMCS labels, original source directories, catalytic residues and distance filenames |
| `S1_descriptor_extraction.py` | Raw descriptor extraction, input validation, pocket mapping and cutoff sensitivity |
| `S2_DMCS_normalization.py` | Normalization and weighted score calculation from the raw descriptor matrix |
| `S3_DMCS_ranking.py` | Validation and export of the final ranked panel |
| `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv` | Raw descriptor matrix and provenance fields |
| `DMCS_ACTIVE_SITE_RESIDUES.csv` | Per-residue canonical 5.0 Å pocket map |
| `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv` | Common protein Cα RMSF profiles |
| `DMCS_RMSF_CUTOFF_SENSITIVITY.csv` | 4.0/5.0/6.0 Å sensitivity results |
| `DMCS_STANDARDIZED.csv` | Normalized components and DMCS |
| `DMCS_Final_Ranking.csv` | Final canonical 15-system ranking |
| `15_Enzyme_Analysis_Data/` | Harmonized per-enzyme descriptor and RMSF tables |
| `15_Enzyme_Analysis_DAT_Files/` | Selected original source DAT outputs used for descriptor provenance |
| `DMCS_DATA_PROVENANCE_AUDIT.md` | DMCS source inventory and quality-control record |
| `DMCS_REPRODUCTION_GUIDE.md` | Reproduction routes and required files |

## Relationship to the separate post-MD output archive

The repository also contains [`06_Post_MD_Analysis_DAT_Files/`](../06_Post_MD_Analysis_DAT_Files/README.md), which archives per-system RMSD, Rg, SASA and hydrogen-bond output series. These series are provided as ancillary source outputs. They are **not terms in the current DMCS equation**, are not inputs to S1–S3, and were not used to generate the canonical scores above. The `*_ns` files are alternate x-axis representations of corresponding frame-indexed series, not separate simulation replicas.

The archive's SHA256 audit verifies source-copy integrity and category classification. It does not by itself prove identical atom masks, reference structures, surface parameters or hydrogen-bond definitions across systems. Therefore, these archived series must not be treated as a harmonized cross-system comparative dataset without additional per-system method verification.

## Reproduction boundary

S2 and S3 can be run from the checked-in raw descriptor matrix. Full S1 source re-extraction requires the original per-system analysis directories and all required files listed in [DMCS_REPRODUCTION_GUIDE.md](DMCS_REPRODUCTION_GUIDE.md); the complete original source directories and production trajectories are not included. Reproducing the deposited ranking from descriptors is distinct from regenerating those descriptors from trajectories.
