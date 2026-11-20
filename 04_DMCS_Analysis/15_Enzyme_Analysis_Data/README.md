# Harmonized per-enzyme DMCS data

## Purpose

This directory contains compact, machine-readable per-enzyme outputs used in the canonical 15-system DMCS comparison. It is distinct from `15_Enzyme_Analysis_DAT_Files/`, which preserves original collected source DAT files. This directory contains harmonized tables used for descriptor calculation and audit.

Each enzyme folder contains:

| File | Definition |
|---|---|
| `descriptor_summary.csv` | Source means, frame counts, cluster statistics, signed GB/PB energies, protein/pocket counts and residue lists |
| `active_site_rmsf.csv` | Residues selected by the canonical 5.0 Å structure-derived pocket rule, nearest component, minimum distance and Cα RMSF |
| `protein_ca_rmsf.csv` | Complete protein-only per-residue Cα RMSF profile |
| `rmsf_protein_calpha.dat` | Plain-text CPPTRAJ-style version of the same Cα RMSF profile |
| `cutoff_sensitivity.csv` | Per-enzyme scores/ranks and RMSF means at 4.0, 5.0 and 6.0 Å |

## Common pocket rule

For each system, protein residues having at least one heavy atom within 5.0 Å of any heavy atom belonging to PLP (UNP), furfural (UNL) or IPA (UNI) in that system's own prepared `complexN.pdb` are selected. Their Cα RMSF values are read from the common protein-only `rmsf_protein_calpha.dat` output and averaged arithmetically. Each enzyme's own residue identifiers are used.

## Frame, cluster and energy conventions

The three distance series contain 50,000 frames per system. The dominant conformational cluster is the cluster with the highest frame count. The first `DELTA TOTAL` entry from the UNL-containing MMPBSA report is retained as GB and the second as PB. The signed GB value is retained in the raw table; only its absolute magnitude is used for Dene.

## Reproduction

See [DMCS_REPRODUCTION_GUIDE.md](../DMCS_REPRODUCTION_GUIDE.md), [DMCS_RMSF_METHOD.md](../DMCS_RMSF_METHOD.md) and the S1–S3 scripts in the parent directory. S2/S3 reproduce normalization and ranking from the deposited raw descriptor matrix. Re-extracting S1 descriptors requires the original analysis directories described in the reproduction guide.
