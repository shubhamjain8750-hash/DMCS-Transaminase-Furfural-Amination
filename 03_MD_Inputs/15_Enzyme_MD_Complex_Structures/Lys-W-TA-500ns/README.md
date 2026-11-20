# Lys-W-TA: MD complex structures

- `complexN.pdb`: prepared unsolvated enzyme–PLP–furfural–isopropylamine complex. The three components are encoded as residues UNP (PLP), UNL (furfural) and UNI (isopropylamine).
- `complexN_equilbration2.pdb`: solvated stage-2 equilibration coordinate snapshot retained from the MD preparation workflow.

The stage-2 PDB is a visualization/coordinate snapshot; production `md1.in` is restart-based (`irest=1`, `ntx=5`) and reads the corresponding Amber restart/topology files. A PDB snapshot is not a replacement for the binary Amber restart or topology.
