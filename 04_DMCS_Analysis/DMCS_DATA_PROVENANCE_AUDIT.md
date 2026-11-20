# DMCS 15-System Data Provenance and Validation

## Scope

This audit documents the 15-system comparison and the raw files collected from the selected 500 ns analysis folders. ATA117-Rd11 remains the lead system prioritized for experimental assessment.

The audit distinguishes direct extraction from the uploaded files from historical inputs that still require a reproducible active-site residue mapping.

## Locked scoring definition

Outer component weights:
- Dcat = 0.40
- Drig = 0.25
- Dconf = 0.15
- Dene = 0.20

Catalytic-readiness subweights:
- Catalytic-residue–PLP = 0.50
- PLP–furfural = 0.25
- PLP–isopropylamine = 0.25

S2 applies inverse min–max normalization to distances and RMSF; positive min–max normalization to ln(largest-cluster fraction); and positive min–max normalization to the absolute value of signed GB ΔG.

DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene.

This is a descriptor-based ranking framework, not a trained predictive machine-learning model.

## Raw-data extraction results

The uploaded analysis archive contained 15 system folders and 771 files. The extracted distance time series contain 50,000 frames per descriptor for every system. The largest cluster was selected by maximum frame count from each `dmcs_cluster_summary.dat`.

For every system, the MM/GBSA value was extracted from the first `DELTA TOTAL` row in the GB section of `FINAL_RESULTS_UNL_MMPBSA.dat`. The PB `DELTA TOTAL` value is retained separately in the raw-descriptor CSV for traceability and is not used for Dene.

The complete numerical results are in:
- `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv`
- `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv`

The complete set of selected input definitions is consolidated in `DMCS_15_SYSTEMS_INPUTS_AND_PROTOCOLS.md`.

## RMSF provenance

The archive contains different levels of RMSF evidence:

- ATA117-Rd11: six-residue active-site output; mean = 1.476733 Å; residues 106, 115, 142, 188, 231 and 249.
- A0A2G0CFH8: 18-residue active-site output; mean = 1.085317 Å; the exact residue list is preserved in the raw descriptor CSV.
- AspC: 11-residue active-site output; mean = 1.560673 Å.
- AptA: 11-residue active-site output; mean = 1.817764 Å.
- Lys-W-TA: the active-site RMSF file contains one residue (136; 0.7051 Å). This is a single-residue value and should not be interpreted as a multi-residue active-site mean without an explicit methodological justification.
- S-omega-TA: the active-site RMSF file contains one protein residue (288; 0.8765 Å). The input mask also names ligand/cofactor residue numbers, but those do not yield additional Cα RMSF rows.
- H-188, G-188, F-188, AB-R-ATA, A0A1B728H4, A0A1Z5HPJ6, S-188, CV-TAm and W-188: residue-wise RMSF output is present, but a matching active-site residue selection/output was not present in the uploaded bundle.

The RMSF-by-residue series for systems without an active-site output have been preserved in `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv`. A comparable active-site mean must be calculated only after residues are mapped to the catalytic pocket for each system. Do not transfer one enzyme's residue numbering to another without structural alignment and verification.

The historical RMSF values in `S1_INPUTS.csv` remain marked unverified where a source active-site mask/output was not available. Two single-residue selections are also explicitly flagged for review. The S1 script blocks standard extraction while these statuses remain unresolved; `--allow-provisional` is available only for exploratory table regeneration.

## Distance descriptor validation

The following fields are included in the raw-descriptor CSV:
- Catalytic residue–PLP mean distance (Å)
- PLP–furfural mean distance (Å)
- PLP–isopropylamine mean distance (Å)
- Number of frames used for each mean
- Catalytic residue identity and distance-file name

Means were computed from the second numeric column of each CPPTRAJ distance series. The catalytic distance file mapping is listed per system in the raw-descriptor table and the corresponding input file is included in the consolidated input documentation.

## Clustering validation

For each system, the row with the greatest frame count was selected from `dmcs_cluster_summary.dat`. The raw-descriptor table records the dominant cluster frame count, cluster fraction and total number of clusters.

## MM/GBSA validation

The signed GB `DELTA TOTAL` was extracted from the first `DELTA TOTAL` row in the GB section of each UNL-containing MMPBSA output. The PB value is recorded separately for traceability. S2 uses the absolute value of the signed GB result for energetic normalization.

For ATA117-Rd11, the selected rerun gives GB ΔG = -12.4786 kcal/mol. Do not substitute values from an earlier run.

## Current ranking

The current provisional ranking was recalculated from exact raw distance means, dominant-cluster fractions and GB energy values, combined with the RMSF inputs currently recorded in the manifest.

ATA117-Rd11 remains rank 1 with DMCS = 0.9063. The ranking remains provisional because active-site RMSF residue mapping is not yet complete and consistent for all 15 systems. The current CSVs preserve the exact inputs and normalization outputs used to obtain this provisional ranking.

## Reproducibility closure checklist

- [x] Confirmed all 15 analysis folders are represented in the uploaded archive.
- [x] Extracted all three distance-series means for each system (50,000 frames per series).
- [x] Selected the largest cluster by frame count for each system.
- [x] Extracted the first GB `DELTA TOTAL` value from each UNL-containing MMPBSA output.
- [x] Preserved system-specific distance, cluster, RMSF, MD and MMPBSA input definitions in a consolidated file.
- [x] Preserved residue-wise RMSF data available in the archive.
- [ ] Establish and document a structurally mapped active-site residue set for every system.
- [ ] Recalculate the active-site RMSF means from those finalized selections.
- [ ] Regenerate S1–S3 after all RMSF statuses are finalized.
- [ ] Freeze manuscript-reported numerical scores after the RMSF checks are complete.

## File-handling note

Large production NetCDF trajectories are not included. The repository contains machine-readable processed descriptors and the compact analysis inputs needed to inspect the reported descriptor and scoring workflow.
