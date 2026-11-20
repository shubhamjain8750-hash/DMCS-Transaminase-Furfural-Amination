# CV-TAm — harmonized DMCS data

This directory contains compact, processed data for this enzyme in the canonical 15-system DMCS comparison.

| File | Contents |
|---|---|
| `descriptor_summary.csv` | Raw distance means, frame counts, dominant-cluster information, signed GB/PB energies, protein/pocket sizes and residue lists |
| `active_site_rmsf.csv` | Residues in the canonical 5.0 Å structure-derived pocket, closest component, minimum distance and mapped Cα RMSF |
| `protein_ca_rmsf.csv` | Full protein-only per-residue Cα RMSF profile |
| `rmsf_protein_calpha.dat` | Plain-text two-column version of the protein Cα RMSF profile |
| `cutoff_sensitivity.csv` | System contribution to the 4.0, 5.0 and 6.0 Å cutoff sensitivity analysis |

The pocket is defined independently from this enzyme's prepared ternary complex: a protein residue is selected when any of its heavy atoms is within 5.0 Å of any heavy atom in PLP (UNP), furfural (UNL) or IPA (UNI). Residue numbers correspond to this system's structure and RMSF profile.

Descriptor definitions, scaling, weighting and reproduction instructions are provided in the parent `04_DMCS_Analysis/` documentation.
