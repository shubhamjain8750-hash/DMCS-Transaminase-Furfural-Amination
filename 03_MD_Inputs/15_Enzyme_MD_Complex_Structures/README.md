# Prepared MD complex structures — 15 enzyme systems

This folder contains 30 PDB structures organized into 15 enzyme-specific subfolders. Each system has:

- `complexN.pdb`: prepared, unsolvated protein–ligand/cofactor assembly.
- A source-named `complexN_equilibration2.pdb` or `complexN_equilbration2.pdb`: solvated stage-2 equilibration coordinate snapshot. The original spelling is retained.

## Residue identifiers

| Residue name | Component |
|---|---|
| `UNP` | Pyridoxal-5′-phosphate (PLP) |
| `UNL` | Furfural |
| `UNI` | Isopropylamine (IPA) |

## Interpretation

The unsolvated PDB is the prepared solute assembly. The stage-2 PDB is a coordinate snapshot for structural inspection. It is **not** the binary production restart file. Production MD uses the corresponding AMBER restart and topology files, which are not included here.

## Integrity and provenance

`PDB_STRUCTURE_MANIFEST.csv` lists enzyme label, original source directory, original filename, repository-relative path, file size, SHA256 checksum, atom count, protein-residue count and UNP/UNL/UNI atom counts. Source directory names have been kept intact to preserve traceability.
