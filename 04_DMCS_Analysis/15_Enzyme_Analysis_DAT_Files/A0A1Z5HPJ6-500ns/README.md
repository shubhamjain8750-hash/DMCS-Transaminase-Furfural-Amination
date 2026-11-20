# A0A1Z5HPJ6 — collected analysis DAT outputs

**Original source analysis directory:** `A0A1Z5HPJ6-500ns`  
**Number of deposited DAT files:** 13

The files listed below are the original `.dat` outputs collected from this source directory. Original filenames and numeric contents are preserved. The parent `DAT_FILE_MANIFEST.csv` records source name, repository path, size and SHA256 checksum.

### Distance time series

- `lys_plp.dat`
- `plp_uni.dat`
- `plp_unl.dat`

### RMSF outputs

- `rmsf_byres_clean.dat`
- `rmsf_complex_all_byres.dat`
- `rmsf_ligands_all_byatom.dat`
- `rmsf_protein_calpha.dat`
- `rmsf_uni_byatom.dat`
- `rmsf_unl_byatom.dat`
- `rmsf_unp_byatom.dat`

### Clustering outputs

- `dmcs_cluster_summary.dat`
- `dmcs_clusters.dat`

### MM/GBSA report

- `FINAL_RESULTS_UNL_MMPBSA.dat`

## Interpretation

Distance files are time series used to extract the corresponding DMCS mean-distance descriptor. RMSF files have different atom/residue selections and must not be treated as interchangeable. The canonical cross-system Drig descriptor uses the protein-only `rmsf_protein_calpha.dat` profile with the structure-derived 5.0 Å pocket definition described in `04_DMCS_Analysis/DMCS_RMSF_METHOD.md`. Legacy active-site and whole-complex RMSF files are retained as source records only.

The MMPBSA report contains GB and PB sections; the descriptor workflow distinguishes the first and second `DELTA TOTAL` entries as GB and PB, respectively. Cluster outputs are interpreted using the frame counts recorded in the source summary.

This folder preserves DAT files that were actually present. It does not imply that every system contains an identical set of auxiliary outputs. The current public package does not contain a complete set of RMSD, Rg, SASA or hydrogen-bond result files.
