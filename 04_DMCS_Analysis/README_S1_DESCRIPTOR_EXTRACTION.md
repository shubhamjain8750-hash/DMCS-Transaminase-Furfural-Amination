# S1: Raw Descriptor Extraction and Compilation

## Purpose and data contract

S1 reads `S1_INPUTS.csv` and compiles distance and cluster descriptors from the selected system folders. The manifest supplies the mean active-site RMSF and signed MM/GBSA GB binding free energy. S1 does **not** recalculate MD, RMSF or MM/GBSA.

Required manifest fields:
- `Enzyme`: system identifier
- `Directory`: path relative to the analysis root, or an absolute path
- `CatalyticDistanceFile`: system-specific catalytic-residue–PLP distance file
- `RMSF`: mean active-site RMSF in Å
- `MMGBSA`: signed GB ΔG in kcal/mol
- `RMSF_Status` and `MMGBSA_Status`: provenance status fields
- `Notes`: optional free-text provenance note

The S1 script requires the 15-system panel and exact enzyme identifiers. It will stop by default unless both RMSF and MMGBSA status fields are `VERIFIED`. For exploratory recalculation while the audit is open, explicitly pass `--allow-provisional`. This flag does not validate the supplied values; it only permits provisional processing.

## Per-system files

Each analysis directory must contain:
- The catalytic-residue–PLP distance file named in `CatalyticDistanceFile`
- `plp_unl.dat` (PLP–furfural)
- `plp_uni.dat` (PLP–isopropylamine)
- `dmcs_cluster_summary.dat`

S1 calculates the mean of the second numeric column in each CPPTRAJ distance file. Confirm that the file columns are frame/time followed by distance in Å and that atom selections are correct for the relevant system.

For clustering, S1 selects the row with the greatest number of frames and retains its cluster fraction. It does not assume that the first row is the dominant cluster.

## Catalytic-residue assignment

The five Lys188 substitution systems use their residue-specific distance files:
- H-188: `his_plp.dat`
- G-188: `gly_plp.dat`
- F-188: `phe_plp.dat`
- S-188: `ser_plp.dat`
- W-188: `trp_plp.dat`

The other systems currently map to `lys_plp.dat`; verify each mapping against the corresponding CPPTRAJ input and Amber topology. The output retains the legacy column name `Lys_PLP` for compatibility with S2, but it represents catalytic-residue–PLP distance in all systems.

## RMSF policy

Active-site residues must be defined independently for each enzyme using structural alignment and the catalytic-pocket context. Do not transfer a fixed residue-number mask from ATA117-Rd11 to another homolog. Preserve the exact residue/atom selection and raw per-residue output used to calculate each mean.

Values currently marked historical, provisional or requiring selection review must not be treated as final. See `DMCS_DATA_PROVENANCE_AUDIT.md`.

## MM/GBSA policy

Use the first GB `DELTA TOTAL` value for the UNL-containing complex. Do not use the PB result that may follow it. Preserve the signed GB ΔG in the manifest; S2 uses its absolute magnitude for energetic normalization. Confirm source output and units before setting the manifest status to `VERIFIED`.

## Running S1

From the repository folder, set the analysis root to the directory containing the 15 enzyme folders:

```bash
export DMCS_ANALYSIS_ROOT="$HOME/amber24"
python 04_DMCS_Analysis/S1_descriptor_extraction.py
```

The command above intentionally stops until both descriptor provenance statuses are VERIFIED.

For exploratory processing only:

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py --analysis-root "$HOME/amber24" --allow-provisional
```

The output is `DMCS_RESULTS.csv` in this script's directory. It contains the S2-compatible columns:
`Enzyme, Lys_PLP, PLP_UNL, PLP_UNI, RMSF, ClusterFraction, MMGBSA`.

## S1 limitations

S1 compiles existing analysis results. It does not generate MD trajectories, CPPTRAJ distance outputs, RMSF values, clustering outputs or MM/GBSA energies. The optional flag `--allow-provisional` is an explicit acknowledgement that some supplied descriptors have not yet passed provenance checks; it is not a substitute for completing the audit.
