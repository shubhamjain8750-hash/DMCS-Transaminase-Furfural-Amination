# S1: Raw Descriptor Extraction and Compilation

## Purpose and data contract

S1 reads `S1_INPUTS.csv` and compiles trajectory-derived distance and clustering descriptors from the corresponding system folders. The manifest supplies active-site RMSF and signed GB binding free energy. S1 does not rerun MD, RMSF or MMPBSA calculations.

Required manifest fields:
- `Enzyme`: system identifier
- `Directory`: absolute path or path relative to the analysis root
- `CatalyticDistanceFile`: catalytic-residue–PLP distance series
- `RMSF`: mean active-site RMSF (Å)
- `MMGBSA`: signed GB ΔG (kcal/mol)
- `RMSF_Status` and `MMGBSA_Status`: descriptor provenance
- `Notes`: optional source and residue-selection details

The script validates the 15-system panel and checks provenance statuses. It stops by default unless both descriptor statuses are `VERIFIED` for every row. Use `--allow-provisional` only to explicitly regenerate an exploratory matrix while any RMSF values remain under review.

## Required files in each analysis folder

- System-specific catalytic-residue–PLP distance output.
- `plp_unl.dat`: PLP–furfural distance.
- `plp_uni.dat`: PLP–isopropylamine distance.
- `dmcs_cluster_summary.dat`: cluster frame counts and fractions.
- RMSF output and its matching selection input.
- `FINAL_RESULTS_UNL_MMPBSA.dat`: MMPBSA output for the UNL-containing complex.

## Distance extraction

S1 calculates the arithmetic mean of the second numeric column in each CPPTRAJ distance file. The collected series contain 50,000 frames per descriptor. Check the associated input file for residue and atom selections; catalytic substitutions use the matching residue-specific file. The output retains the legacy column name `Lys_PLP` for compatibility, although the field represents catalytic-residue–PLP distance in every system.

## Clustering

S1 selects the cluster-summary row with the maximum frame count and stores its frame fraction. It does not assume that the first row is the largest cluster.

## RMSF policy

The active-site residue set must be documented for each system. Four systems have multi-residue `active_site_rmsf.dat` files with corresponding CPPTRAJ selection inputs in the collected bundle. Two systems have single-residue active-site RMSF outputs requiring definition review. The remaining systems have residue-wise RMSF data but no corresponding active-site selection in the collected input bundle.

Do not use whole-protein residue-wise RMSF as a substitute for an active-site mean. Establish each active-site selection through structure/sequence alignment and catalytic-pocket context, then record the exact residue IDs and atom selection in the input files and manifest.

## MM/GBSA extraction

Use the first GB `DELTA TOTAL` value for the UNL-containing complex. Do not use the PB `DELTA TOTAL` row that follows. The signed GB ΔG is retained in the manifest; S2 uses its absolute magnitude only for energetic normalization. All 15 GB values in the current manifest were extracted from the corresponding raw MMPBSA output.

## Execution

Set the analysis root to the parent directory containing all system folders:

```bash
export DMCS_ANALYSIS_ROOT="$HOME/amber24"
```

Standard execution (requires all RMSF and MMGBSA statuses to be VERIFIED):

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py
```

Exploratory execution while some RMSF statuses remain provisional:

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py --allow-provisional
```

The exploratory flag does not validate the manifest values. It only permits S1 to compile the current inputs for review.

## Output

S1 writes `DMCS_RESULTS.csv` with:
`Enzyme, Lys_PLP, PLP_UNL, PLP_UNI, RMSF, ClusterFraction, MMGBSA`.

Proceed to S2 and S3 only when the provenance status is appropriate for the intended analysis. The present published ranking is provisional pending completion of active-site RMSF mapping.
