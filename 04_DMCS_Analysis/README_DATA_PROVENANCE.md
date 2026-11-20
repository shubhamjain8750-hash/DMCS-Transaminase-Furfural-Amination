# DMCS data dictionary and provenance

| File | Meaning |
|---|---|
| `S1_INPUTS.csv` | Enzyme display label, original source directory, catalytic residue and catalytic-residue–PLP DAT filename |
| `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv` | Raw means, frame counts, largest-cluster data, signed GB/PB results and per-cutoff pocket fields |
| `DMCS_ACTIVE_SITE_RESIDUES.csv` | Per-residue 5.0 Å pocket membership, residue name, minimum distance to UNP/UNL/UNI, nearest component and Cα RMSF |
| `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv` | Common protein-only Cα RMSF values and source filename for every system |
| `DMCS_RESULTS.csv` | Compact raw descriptor matrix passed to S2 |
| `DMCS_STANDARDIZED.csv` | Normalized descriptor components and composite DMCS scores |
| `DMCS_Final_Ranking.csv` | Ranked 15-system DMCS table |
| `DMCS_RMSF_CUTOFF_SENSITIVITY.csv` | 4.0/5.0/6.0 Å pocket sensitivity results |
| `DMCS_Descriptor_Summary.csv` | Compact descriptor summary |

## Units and conventions

- Distances: Å.
- RMSF: Å.
- MMPBSA energies: kcal/mol.
- Cluster fraction: unitless fraction from 0 to 1.
- Scores: normalized unitless values from 0 to 1.
- Rank: 1 is the largest composite DMCS value.

The common RMSF source is `rmsf_protein_calpha.dat`, after protein-backbone alignment. The Drig pocket is defined from the prepared ternary structure using a 5.0 Å heavy-atom contact to PLP (UNP), furfural (UNL) or IPA (UNI). Full definitions are in `DMCS_RMSF_METHOD.md`.
