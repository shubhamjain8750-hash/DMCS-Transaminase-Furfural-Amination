# S1–S3: Reproducible descriptor extraction and DMCS scoring

## S1: Source-data extraction and validation

S1 reads \`S1_INPUTS.csv\` and the 15 system analysis directories.

Required per-system files:
- \`complexN.pdb\`: ternary prepared structure containing UNP (PLP), UNL (furfural) and UNI (IPA)
- \`cpptraj.in\`, \`md1.in\`, and \`mmpbsa.in\`
- \`rmsf_protein_calpha.dat\`: common protein-only Cα RMSF output
- the catalytic-residue–PLP distance file named in \`S1_INPUTS.csv\`
- \`plp_unl.dat\`, \`plp_uni.dat\`, \`dmcs_cluster_summary.dat\`
- \`FINAL_RESULTS_UNL_MMPBSA.dat\`

For RMSF, S1 selects protein residues whose heavy atoms contact any heavy atom in PLP, furfural or IPA within 5.0 Å in that system's own \`complexN.pdb\`. It then reads the corresponding residue Cα RMSF from the common \`rmsf_protein_calpha.dat\` file. The active-site RMSF descriptor is the arithmetic mean over these residues. The residue numbering is system-specific; no fixed residue mask is copied across enzymes.

S1 validates the PDB/RMSF residue mapping, protein-alignment-before-fluctuation CPPTRAJ protocol, 500 ns production settings, 50,000-frame distance series, 50,000 total cluster frames, and GB/PB energy rows.

S1 generates:
- \`DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv\`
- \`DMCS_ACTIVE_SITE_RESIDUES.csv\`
- \`DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv\`
- \`DMCS_RESULTS.csv\`
- \`DMCS_RMSF_CUTOFF_SENSITIVITY.csv\`
- \`DMCS_Descriptor_Summary.csv\`
- \`DMCS_STANDARDIZED.csv\` and \`DMCS_Final_Ranking.csv\`
- per-enzyme outputs in \`15_Enzyme_Analysis_Data/<enzyme>/\`

## S2: Normalization and DMCS calculation

The outer weights are Dcat = 0.40, Drig = 0.25, Dconf = 0.15 and Dene = 0.20. The Dcat subweights are catalytic-residue–PLP = 0.50, PLP–furfural = 0.25 and PLP–IPA = 0.25.

Distances and pocket RMSF use inverse min–max scaling. Conformational persistence uses positive min–max scaling of the logarithm of the dominant-cluster fraction. Energetic stabilization uses positive min–max scaling of the absolute magnitude of signed GB ΔG.

## S3: Ranking

S3 validates the 15-system identifier set, numeric bounds and score columns, then sorts by DMCS and writes \`DMCS_Final_Ranking.csv\`.

## Reproduce

\`\`\`bash
python -m pip install -r 04_DMCS_Analysis/requirements.txt
python 04_DMCS_Analysis/S1_descriptor_extraction.py --analysis-root "$HOME/amber24" --output-dir 04_DMCS_Analysis --pocket-cutoff 5.0 --sensitivity-cutoffs 4,5,6
python 04_DMCS_Analysis/S2_DMCS_normalization.py
python 04_DMCS_Analysis/S3_DMCS_ranking.py
\`\`\`

The currently reported 5.0 Å pocket score for ATA117-Rd11 is 0.915409. The 4.0/5.0/6.0 Å sensitivity table is supplied separately.
