# DMCS reproduction guide

## 1. Reproduce deposited normalized scores and ranking

This route can be run using files already in the repository. It does not require the original cluster filesystem or production trajectories.

From the repository root, install dependencies and run:

    python -m pip install -r 04_DMCS_Analysis/requirements.txt
    python 04_DMCS_Analysis/S2_DMCS_normalization.py
    python 04_DMCS_Analysis/S3_DMCS_ranking.py

S2 reads `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv`, validates the 15-system panel, applies direction-specific min–max scaling and writes `DMCS_STANDARDIZED.csv`. S3 validates normalized component scores and writes `DMCS_Final_Ranking.csv`.

The canonical 5.0 Å score for ATA117-Rd11 is 0.915409.

## 2. Re-extract raw descriptors with S1

S1 requires the original 15 per-system analysis directories. The full directories and trajectories are not part of the public repository. Make those folders available separately, preserving the directory basenames listed in `S1_INPUTS.csv`.

Each source directory must contain at minimum: `complexN.pdb` with protein and UNP/UNL/UNI; `cpptraj.in`, `md1.in` and `mmpbsa.in`; `rmsf_protein_calpha.dat`; the catalytic-residue–PLP distance file in `S1_INPUTS.csv`; `plp_unl.dat`; `plp_uni.dat`; `dmcs_cluster_summary.dat`; and `FINAL_RESULTS_UNL_MMPBSA.dat`.

Run the following, replacing the example path with the parent directory containing all 15 source folders:

    python 04_DMCS_Analysis/S1_descriptor_extraction.py \
      --analysis-root /path/to/parent_of_15_system_folders \
      --output-dir 04_DMCS_Analysis \
      --pocket-cutoff 5.0 \
      --sensitivity-cutoffs 4,5,6
    python 04_DMCS_Analysis/S2_DMCS_normalization.py
    python 04_DMCS_Analysis/S3_DMCS_ranking.py

S1 validates required files, ligand heavy-atom inventory, protein alignment before RMSF, residue-number correspondence, 500 ns production settings, 50,000-frame distance series, cluster totals and GB/PB energy rows.

## 3. Canonical RMSF definition

For each enzyme, protein residues are selected independently from its prepared ternary structure when any protein heavy atom is within 5.0 Å of any heavy atom in PLP, furfural or IPA. Their residue identifiers are mapped to the corresponding values in the common protein-only `rmsf_protein_calpha.dat` profile. The arithmetic mean of selected Cα RMSF values is the Drig input. See `DMCS_RMSF_METHOD.md` for the complete procedure.

Do not substitute legacy whole-complex RMSF, ligand RMSF or a manually selected residue mask for this canonical metric.

## 4. DMCS definition

    Dcat  = 0.50 * inverse_minmax(catalytic-residue–PLP distance)
          + 0.25 * inverse_minmax(PLP–furfural distance)
          + 0.25 * inverse_minmax(PLP–IPA distance)
    Drig  = inverse_minmax(mean 5.0 Å pocket Cα RMSF)
    Dconf = minmax(ln(dominant-cluster frame fraction))
    Dene  = minmax(abs(signed GB DELTA TOTAL))
    DMCS  = 0.40*Dcat + 0.25*Drig + 0.15*Dconf + 0.20*Dene

All min–max operations are calculated over the same 15-system panel. The score is panel-dependent and is not an absolute biochemical activity prediction.

## 5. Outputs to inspect

- `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv`
- `DMCS_ACTIVE_SITE_RESIDUES.csv`
- `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv`
- `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`
- `DMCS_STANDARDIZED.csv`
- `DMCS_Final_Ranking.csv`
- `15_Enzyme_Analysis_Data/<enzyme>/`

For provenance and QC interpretation, also read `DMCS_DATA_PROVENANCE_AUDIT.md` and `DMCS_15_SYSTEMS_INPUTS_AND_PROTOCOLS.md`.
