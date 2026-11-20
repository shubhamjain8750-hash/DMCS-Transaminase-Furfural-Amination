# 06 — Post-MD analysis outputs

This directory contains the corrected per-system post-production MD outputs collected from the 15-enzyme DMCS panel.

## Collection scope

The collection contains four categories:

- `RMSD/` — structural deviation outputs
- `Rg/` — radius-of-gyration outputs
- `SASA/` — solvent-accessible surface area outputs
- `Hydrogen_Bonds/` — hydrogen-bond outputs

RMSF is maintained separately in the DMCS analysis data. MMPBSA/MMGBSA energy-summary reports are excluded and must not be categorized as SASA.

## Final collected inventory

| Category | Original DAT files |
|---|---:|
| RMSD | 165 |
| Rg | 150 |
| SASA | 150 |
| Hydrogen bonds | 180 |
| **Total** | **645** |

A total of 585 numeric CSV exports were generated. Sixty DAT files, primarily hydrogen-bond average reports, did not contain tabular numeric rows suitable for CSV conversion and are retained in their original DAT form. CSV conversion is a format transformation only; it does not recalculate underlying values.

## Organization and provenance

Each system is stored under its original source-directory name, with results grouped by category and original relative subfolder. Original `.dat` files are retained unchanged.

- `POST_MD_DAT_MANIFEST.csv` records the source and copied paths, category, file size, SHA256, CSV path and conversion status.
- `POST_MD_SYSTEM_INVENTORY.csv` records per-enzyme output counts.
- `POST_MD_COLLECTION_QC.md` records the first-pass classification issue and the corrected final audit.

## Final collection audit

The corrected collection was run across all 15 specified systems. The final audit reported:

- 645 DAT files verified against their original source by SHA256.
- 0 missing DAT files and 0 checksum mismatches.
- 0 duplicate-content checksum groups.
- 0 files with irregular or skipped numeric rows.
- 0 MMPBSA/MMGBSA reports in the collection.
- 585 CSV conversions, with 0 missing converted CSV files.

The collection passed its file-integrity and classification checks on the computational server. The audit verifies file provenance and collection logic; it does not independently establish uniformity of atom selections, reference structures, SASA definitions or hydrogen-bond geometric criteria across all systems.

## Interpretation cautions

Before quantitative cross-system comparison, confirm consistent atom masks, reference structures, surface definitions, donor/acceptor selections, hydrogen-bond geometric cutoffs, trajectory sampling intervals and equilibration windows. A matching file count alone does not establish methodological comparability.

**Repository status:** the corrected collection has passed its computational-server audit. Transfer of the generated files into this GitHub directory and commit to the public repository are the remaining publication steps.
