# DMCS reproduction guide

## Repository data layout

The machine-readable, processed data for the 15-system DMCS analysis are provided under \`04_DMCS_Analysis/\`. The per-enzyme directory \`15_Enzyme_Analysis_Data/\` contains one directory per evaluated enzyme, with:
- descriptor summary, including distance means, frame counts, cluster statistics and GB/PB energies;
- the canonical 5.0 Å catalytic-pocket residue map and residue-wise Cα RMSF values;
- the complete protein Cα RMSF profile in CSV and CPPTRAJ-style DAT formats;
- per-enzyme 4.0/5.0/6.0 Å cutoff-sensitivity results.

The global source tables are \`DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv\`, \`DMCS_ACTIVE_SITE_RESIDUES.csv\`, \`DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv\`, \`DMCS_RESULTS.csv\` and \`DMCS_RMSF_CUTOFF_SENSITIVITY.csv\`.

## Reproduce the normalized scores and ranking from the public data

This route uses the complete machine-readable descriptor matrix supplied in the repository and does not require MD trajectories or the original cluster filesystem:

\`\`\`bash
python -m pip install -r 04_DMCS_Analysis/requirements.txt
python 04_DMCS_Analysis/S2_DMCS_normalization.py
python 04_DMCS_Analysis/S3_DMCS_ranking.py
\`\`\`

S2 reads \`DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv\`, performs the descriptor normalization and calculates Dcat, Drig, Dconf, Dene and DMCS. S3 validates the full 15-system panel and exports \`DMCS_Final_Ranking.csv\`.

## Re-extract descriptors from the original analysis directories

For a full source-file re-extraction, make the original 15 per-system analysis directories available on the machine running S1. The expected directory names and catalytic distance output names are recorded in \`S1_INPUTS.csv\`. Required per-system inputs include:
- prepared \`complexN.pdb\`;
- \`cpptraj.in\`, \`md1.in\`, \`mmpbsa.in\`;
- \`rmsf_protein_calpha.dat\`;
- the catalytic-residue–PLP distance series, \`plp_unl.dat\`, \`plp_uni.dat\`;
- \`dmcs_cluster_summary.dat\`;
- \`FINAL_RESULTS_UNL_MMPBSA.dat\`.

Run:

\`\`\`bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py \\
  --analysis-root /path/to/parent_of_15_system_folders \\
  --output-dir 04_DMCS_Analysis \\
  --pocket-cutoff 5.0 \\
  --sensitivity-cutoffs 4,5,6
python 04_DMCS_Analysis/S2_DMCS_normalization.py
python 04_DMCS_Analysis/S3_DMCS_ranking.py
\`\`\`

S1 validates the common protein Cα RMSF protocol, residue-number correspondence, structure/ligand heavy-atom inventory, 500 ns production settings, distance-series frame counts, cluster frame totals and GB/PB energy rows before regenerating the machine-readable outputs.

## Canonical RMSF definition

For each enzyme, S1 identifies protein residues with at least one heavy atom within 5.0 Å of any PLP, furfural or IPA heavy atom in that enzyme's prepared ternary complex. It maps those structure-specific residues to the protein-only Cα RMSF profile produced after common backbone fitting and averages the residue-wise values. The procedure is structure-derived and uses each enzyme's own residue numbering.

The 4.0 and 6.0 Å analyses provide cutoff sensitivity. See \`DMCS_RMSF_METHOD.md\` for the full mathematical and CPPTRAJ definition.

## DMCS weights

\`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene\`

Dcat subweights: catalytic-residue–PLP = 0.50, PLP–furfural = 0.25 and PLP–IPA = 0.25.

The canonical 5.0 Å analysis gives ATA117-Rd11 a DMCS score of 0.915409 (rank 1).
