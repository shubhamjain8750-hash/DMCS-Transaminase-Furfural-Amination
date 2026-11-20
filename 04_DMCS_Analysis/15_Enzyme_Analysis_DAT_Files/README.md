# Original per-enzyme numerical analysis outputs (DAT)

## Scope

This directory preserves selected `.dat` files collected from the 15 supplied enzyme analysis folders. The original analysis-folder basenames, DAT filenames and file contents are retained. Each system subfolder contains a README inventory; `DAT_FILE_MANIFEST.csv` records source folder, filename, repository-relative path, byte size, SHA256 and a broad file category.

## Output classes represented

Depending on the system, the deposited outputs include catalytic distance series, protein/whole-complex/ligand RMSF profiles, legacy/system-specific active-site RMSF outputs, clustering summaries and membership/assignment outputs, and UNL-containing MM/GBSA/PB reports.

Not every individual system has an identical set of auxiliary DAT files. The manifest and per-system inventories define what is present; a missing file must not be interpreted as a zero-valued result.

## Relationship to the post-MD output archive

Additional RMSD, radius-of-gyration (Rg), solvent-accessible surface area (SASA) and hydrogen-bond time series are archived separately under [`06_Post_MD_Analysis_DAT_Files/`](../../06_Post_MD_Analysis_DAT_Files/README.md). That collection contains 645 original DAT outputs and 585 numeric CSV conversions across the 15 systems. Its `*_ns` files are time-axis re-expressions of corresponding frame-indexed series, not independent replicas. Hydrogen-bond `*_avg.dat` files are text summaries and are preserved without numeric CSV conversion.

The 06 output archive is ancillary to the canonical DMCS analysis. Its RMSD/Rg/SASA/hydrogen-bond outputs do not enter the current DMCS equation or S1–S3 descriptor calculation. Its SHA256 audit validates file-copy integrity and classification, not cross-system equivalence of atom masks, reference structures or calculation settings.

## Use and integrity

Use each folder's README and `DAT_FILE_MANIFEST.csv` to identify source outputs. Distance and RMSF files are plain-text numeric outputs; MMPBSA files are text reports and should be interpreted using their GB/PB sections. Recompute SHA256 locally to verify an individual source file. The manifest is an integrity aid, not a substitute for original simulation files or trajectory provenance.
