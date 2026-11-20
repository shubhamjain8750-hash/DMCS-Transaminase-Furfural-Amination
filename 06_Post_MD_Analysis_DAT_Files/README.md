# 06 — Post-MD analysis outputs

This directory is reserved for the per-system post-production analysis outputs for RMSD, radius of gyration (Rg), solvent-accessible surface area (SASA) and hydrogen-bond analysis.

## Planned data organization

Each of the 15 DMCS enzyme systems will have a subfolder named after its original source analysis directory. Within each system, output files will be grouped by analysis type:

- `RMSD/`
- `Rg/`
- `SASA/`
- `Hydrogen_Bonds/`

Original `.dat` output files will be retained unchanged. Where a file contains a parseable numeric table, a matching `.csv` export will also be provided. CSV conversion is a format transformation only; it does not recalculate the underlying data.

## Provenance and validation files

The completed folder is expected to include:

- `POST_MD_DAT_MANIFEST.csv`: original source path, copied path, converted CSV path, file size, SHA256 checksum, row/column counts and conversion status.
- `POST_MD_SYSTEM_INVENTORY.csv`: output counts by enzyme and analysis category.
- `README.md`: deposited-file inventory and interpretation notes.

## Scope and interpretation

This folder must contain only result files actually found in the source analysis directories. A missing RMSD/Rg/SASA/hydrogen-bond file must not be represented as a zero value or described as a completed analysis. Before cross-system comparison, confirm that the atom masks, reference structures, surface definitions, donor/acceptor selections and geometric cutoffs are consistent.

**Status:** directory documentation is in place. The per-system result files are not yet deposited; they will be added after extraction and validation on the computational cluster.
