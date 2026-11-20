# Original per-enzyme numerical analysis outputs (DAT)

## Scope

This directory preserves the `.dat` files collected from the 15 supplied enzyme analysis folders. The original analysis-folder basenames, DAT filenames and file contents are retained. Each subfolder contains a README inventory; `DAT_FILE_MANIFEST.csv` records source folder, filename, repository-relative path, byte size, SHA256 and a broad file category.

## Output classes represented

Depending on the system, the deposited outputs include catalytic distance series, protein/whole-complex/ligand RMSF profiles, legacy/system-specific active-site RMSF outputs, clustering summaries and membership/assignment outputs, and UNL-containing MM/GBSA/PB reports.

Not every individual system has an identical set of auxiliary DAT files. The manifest and per-system inventories define what is present; a missing file must not be interpreted as a zero-valued result.

## Important analysis-coverage note

The current public DAT collection includes RMSF output for all 15 systems, but it does **not** include result DAT files for a complete cross-system RMSD, radius-of-gyration, SASA or hydrogen-bond occupancy analysis. CPPTRAJ input examples are available under `03_MD_Inputs/`; input templates are not analysis results. These result series should only be added once actual outputs have been generated, checked and associated with the correct topology and trajectory.

## Use and integrity

Use each folder's README and `DAT_FILE_MANIFEST.csv` to identify the source output. Distance and RMSF files are plain-text numeric outputs; MMPBSA files are text reports and should be interpreted using their GB/PB sections. Recompute SHA256 locally to verify an individual source file. The manifest is an integrity aid, not a substitute for original simulation files or trajectory provenance.
