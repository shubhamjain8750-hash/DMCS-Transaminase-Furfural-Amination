# S1–S3 descriptor extraction and DMCS scoring

## S1 — Extract raw descriptors

S1 reads the enzyme/source mapping in `S1_INPUTS.csv` and extracts per-system values from the original analysis folders. Required files are: prepared `complexN.pdb` containing protein, UNP, UNL and UNI; `cpptraj.in`, `md1.in` and `mmpbsa.in`; `rmsf_protein_calpha.dat`; the catalytic-residue–PLP distance file listed in `S1_INPUTS.csv`; `plp_unl.dat`; `plp_uni.dat`; `dmcs_cluster_summary.dat`; and `FINAL_RESULTS_UNL_MMPBSA.dat`.

S1 checks ligand heavy-atom inventory, common protein-only RMSF source, protein alignment before fluctuation calculation, residue-number mapping, production MD controls, 50,000-frame distance series, 50,000 total cluster frames and GB/PB energy rows. It derives the pocket independently from each system's prepared ternary structure using the 5.0 Å heavy-atom rule.

S1 writes the global raw descriptor table, canonical residue map, complete Cα RMSF table, cutoff sensitivity outputs and per-enzyme processed data.

## S2 — Normalize and calculate DMCS

S2 reads `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv`. It checks the exact 15-enzyme set and validates numeric inputs before calculating Dcat (three distance descriptors with subweights 0.50/0.25/0.25), Drig (inverse-normalized 5.0 Å pocket mean Cα RMSF), Dconf (positive normalization of the logarithm of the largest-cluster fraction) and Dene (positive normalization of the absolute signed GB ΔG).

The outer weights are Dcat 0.40, Drig 0.25, Dconf 0.15 and Dene 0.20.

## S3 — Validate and export ranking

S3 checks the full 15-system set, finite values and normalized score bounds, sorts by DMCS and writes `DMCS_Final_Ranking.csv`.

## Run from repository root

    python -m pip install -r 04_DMCS_Analysis/requirements.txt
    python 04_DMCS_Analysis/S2_DMCS_normalization.py
    python 04_DMCS_Analysis/S3_DMCS_ranking.py

These two steps reproduce normalized scores and ranking from the deposited raw descriptor matrix. To rerun S1, the original per-system analysis directories are required; they are not included in the public repository. See `DMCS_REPRODUCTION_GUIDE.md` for the expected files and command-line options.
