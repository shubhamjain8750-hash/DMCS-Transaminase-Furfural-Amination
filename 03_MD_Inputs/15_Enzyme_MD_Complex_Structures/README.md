# 15-enzyme MD complex structures

Each enzyme folder contains two PDB structures:

1. `complexN.pdb`: prepared enzyme–PLP–furfural–isopropylamine solute assembly before solvation.
2. `complexN_equil...2.pdb`: the corresponding solvated stage-2 equilibration snapshot (the original source filename is preserved, including source spelling).

In these files the ligand/cofactor residue identifiers are UNP (PLP), UNL (furfural) and UNI (isopropylamine). The PDB files support structural inspection and reconstruction of the starting solute assembly. Production MD is restart-based and depends on the matching Amber topology/restart files; PDB snapshots are not substitutes for those binary inputs.
