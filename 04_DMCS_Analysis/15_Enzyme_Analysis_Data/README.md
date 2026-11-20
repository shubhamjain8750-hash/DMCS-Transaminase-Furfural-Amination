# 15-Enzyme Analysis Data

This directory contains a per-enzyme, machine-readable record of the data used in the harmonized DMCS comparison.

Each enzyme subdirectory contains:
- `descriptor_summary.csv`: the catalytic-residue–PLP, PLP–furfural and PLP–isopropylamine mean distances, frame counts, dominant-cluster statistics, and signed GB/PB binding-energy outputs.
- `active_site_rmsf.csv`: residue-level membership and Cα RMSF values for the canonical 5.0 Å catalytic-pocket definition.
- `protein_ca_rmsf.csv`: the complete per-residue Cα RMSF series extracted from the common `rmsf_protein_calpha.dat` source.
- `rmsf_protein_calpha.dat`: a plain-text CPPTRAJ-format rendering of the same per-residue Cα RMSF values.
- `cutoff_sensitivity.csv`: the system's contribution to the 4.0, 5.0 and 6.0 Å pocket-cutoff sensitivity analysis.

## Harmonized RMSF definition

The protein backbone is aligned using the common CPPTRAJ protocol, then Cα RMSF is calculated for every protein residue. For each prepared ternary complex, protein residues with at least one heavy atom within 5.0 Å of a heavy atom from PLP (UNP), furfural (UNL) or isopropylamine (UNI) are selected. The active-site RMSF descriptor is the arithmetic mean of their residue-wise Cα RMSF values. Each enzyme's own residue numbering and structure are used; no fixed residue mask is transferred between enzymes.

## Frame and energy provenance

All three distance series contain 50,000 frames per system. The dominant conformational cluster is selected by maximum frame count. The first `DELTA TOTAL` row from the UNL-containing MMPBSA output is retained as the GB result; the following PB result is retained separately for traceability.

## Reproduce the complete workflow

See the parent folder's `S1_descriptor_extraction.py`, `DMCS_RMSF_METHOD.md`, and `DMCS_DATA_PROVENANCE_AUDIT.md`. The full collected per-system `.dat`, `.in`, `.sh`, and `.log` files can be kept as the downloadable source archive alongside these compact tables.
