# Per-enzyme analysis DAT files

This directory is the public data location for the original numerical analysis outputs from the 15 enzyme systems.

## Organization

Each system has its own subfolder named after its analysis directory. The subfolders preserve the original DAT filenames and contents. Expected classes include:

- Catalytic-residue–PLP, PLP–furfural and PLP–isopropylamine distance time series.
- Protein C-alpha, active-site, residue-wise and ligand/complex RMSF outputs.
- Cluster membership/assignment and cluster summary files.
- UNL-containing MMPBSA results, including the GB and PB energy sections.
- Additional descriptor and structural-analysis outputs generated in the source folders.

The accompanying `DAT_FILE_MANIFEST.csv` records the original source folder, file size, SHA256 checksum and data category for every collected DAT file.

## Provenance

Files were copied from the corresponding 15 source analysis folders without changing their contents or original filenames. Use each system's matching CPPTRAJ/MMPBSA input definitions in the consolidated input/protocol documentation when interpreting or regenerating an output.

Large production trajectory files are not stored here.
