# S-188 — MD complex structures

**Original source directory:** `S-188-500ns`

## Structures deposited

- `complexN.pdb`: prepared unsolvated enzyme–PLP–furfural–IPA complex
- `complexN_equilbration2.pdb`: solvated stage-2 equilibration coordinate snapshot

The molecular components are identified by residue names UNP (PLP), UNL (furfural) and UNI (isopropylamine). The prepared `complexN.pdb` is the unsolvated solute assembly. The stage-2 PDB is a coordinate snapshot for inspection; it is not the production AMBER restart file.

Use the parent `PDB_STRUCTURE_MANIFEST.csv` for file sizes, atom counts, protein-residue counts, component atom counts and SHA256 checksums. Original filenames and source directory spelling are preserved for traceability.

**Reproduction note:** production MD is restart-based and also requires the matching AMBER topology and restart files. Those binary files and production trajectories are not included in this repository.
