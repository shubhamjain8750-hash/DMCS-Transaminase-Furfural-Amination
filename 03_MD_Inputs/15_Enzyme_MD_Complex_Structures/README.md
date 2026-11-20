# Per-enzyme MD complex structures

This directory provides the protein–ligand/cofactor structures for all 15 enzyme systems.

## Files in each system folder

1. `complexN.pdb` — prepared unsolvated enzyme complex containing the protein and the three modeled molecular components:
   - `UNP`: pyridoxal-5'-phosphate (PLP)
   - `UNL`: furfural
   - `UNI`: isopropylamine

2. `complexN_equilibration2.pdb` (or the original source spelling `complexN_equilbration2.pdb`) — the solvated stage-2 equilibration coordinate snapshot retained in the source analysis folder.

The original source spelling is preserved. `PDB_STRUCTURE_MANIFEST.csv` identifies each file, source folder, atom/residue counts, ligand-residue atom counts and SHA256 checksum.

## Interpretation

The prepared `complexN.pdb` is the solute assembly used to prepare the explicit-solvent MD system. The stage-2 PDB is the corresponding solvated equilibration snapshot for structural inspection. Production `md1.in` is restart-based (`irest=1`, `ntx=5`) and uses the corresponding Amber restart and topology files; a PDB snapshot is not a replacement for those binary Amber inputs.
