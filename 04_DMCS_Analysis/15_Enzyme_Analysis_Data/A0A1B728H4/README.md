# A0A1B728H4

The files in this directory are the per-enzyme machine-readable analysis outputs used by the harmonized 15-system DMCS workflow.

- `descriptor_summary.csv`: raw distance means, frame counts, cluster data and signed GB/PB energies.
- `active_site_rmsf.csv`: 5.0 Å structure-defined catalytic-pocket residue membership, nearest ligand/cofactor and per-residue Cα RMSF.
- `protein_ca_rmsf.csv`: complete protein Cα RMSF profile from the common CPPTRAJ output.
- `rmsf_protein_calpha.dat`: CPPTRAJ-style two-column RMSF profile.
- `cutoff_sensitivity.csv`: DMCS component values and rank/score at 4.0, 5.0 and 6.0 Å pocket cutoffs.

The canonical pocket is calculated independently from this enzyme's prepared ternary complex. Its protein residues are selected by a 5.0 Å heavy-atom contact to PLP, furfural or isopropylamine. Residues are mapped by their own Amber/CPPTRAJ numbering.
