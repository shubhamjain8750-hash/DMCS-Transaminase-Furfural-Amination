# 04 – Dynamic Mechanistic Conformation Scoring (DMCS) analysis

This directory contains the reproducible S1–S3 workflow for comparative evaluation of 15 PLP-dependent transaminase systems involved in furfural amination.

## DMCS model

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`.

Dcat is composed of catalytic-residue–PLP distance (0.50), PLP–furfural distance (0.25) and PLP–isopropylamine distance (0.25). Distances and pocket RMSF are inverse min–max normalized; ln(largest-cluster fraction) and |GB ΔG| are positive min–max normalized.

## Reproducible files

- `S1_INPUTS.csv`: system folders, catalytic residues and distance-output names.
- `S1_descriptor_extraction.py`: descriptor extraction, common RMSF pocket definition, validation and sensitivity analysis.
- `DMCS_RMSF_METHOD.md`: detailed scientific definition of the RMSF metric.
- `DMCS_DATA_PROVENANCE_AUDIT.md`: file inventory and QC summary.
- `DMCS_15_SYSTEMS_INPUTS_AND_PROTOCOLS.md`: per-system input definitions.
- `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv`: unnormalized mean distances, cluster and energy descriptors.
- `DMCS_ACTIVE_SITE_RESIDUES.csv`: full per-residue 5.0 Å pocket map.
- `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`: 4.0/5.0/6.0 Å sensitivity.
- `DMCS_RESULTS.csv`: raw descriptor matrix.
- `S2_DMCS_normalization.py`: component normalization and weighted DMCS calculation.
- `DMCS_STANDARDIZED.csv`: normalized component scores.
- `S3_DMCS_ranking.py`: final panel validation and ranking.
- `DMCS_Final_Ranking.csv`: canonical 5.0 Å ranking.
- `DMCS_Descriptor_Summary.csv`: compact descriptor summary.
- `requirements.txt`: Python dependencies.

## RMSF method

All 15 systems contain the same protein-only per-residue Cα RMSF output, `rmsf_protein_calpha.dat`, produced by the corresponding `cpptraj.in`. Other RMSF files, including `rmsf_complex_all_byres.dat`, `rmsf_byres_clean.dat` and legacy `active_site_rmsf.dat`, are retained as supplementary analysis records. Drig uses the common protein-only Cα source and a structure-defined pocket.

For each prepared ternary structure, a protein residue is included if any of its heavy atoms is within 5.0 Å of any heavy atom in the combined UNP (PLP), UNL (furfural) and UNI (isopropylamine) set. Drig is the arithmetic mean Cα RMSF of the selected residues. This selection is regenerated separately for each structure; no residue numbers are transferred between enzymes. The complete residue list and values are in `DMCS_ACTIVE_SITE_RESIDUES.csv`. Sensitivity at 4.0, 5.0 and 6.0 Å is also provided.

## Reproduction

Install dependencies:

```bash
python -m pip install -r 04_DMCS_Analysis/requirements.txt
```

With the 15 analysis directories under `$HOME/amber24`, run:

```bash
python 04_DMCS_Analysis/S1_descriptor_extraction.py \
  --analysis-root "$HOME/amber24" \
  --output-dir 04_DMCS_Analysis \
  --pocket-cutoff 5.0 \
  --sensitivity-cutoffs 4,5,6
python 04_DMCS_Analysis/S2_DMCS_normalization.py
python 04_DMCS_Analysis/S3_DMCS_ranking.py
```

S1 validates source files, the protein alignment/RMSF sequence, residue-number mapping, 50,000-frame distance outputs, cluster frame totals, GB/PB rows and production settings before writing tables.

## Current canonical result

The 5.0 Å pocket definition gives ATA117-Rd11 a DMCS score of **0.915409** (rank 1). This supersedes the earlier score produced from heterogeneous legacy RMSF masks. Use the updated score consistently in the manuscript, figures, Supporting Information and repository. The score is a comparative descriptor-based prioritization metric, not a direct activity prediction.


## Per-enzyme analysis data

The directory `15_Enzyme_Analysis_Data/` contains one subdirectory for each of the 15 evaluated enzyme systems. Each subdirectory provides the raw descriptor summary, canonical 5.0 Å pocket residue/RMSF table, complete protein Cα RMSF profile, CPPTRAJ-format `rmsf_protein_calpha.dat`, and the 4.0/5.0/6.0 Å cutoff-sensitivity rows. The parent directory README explains the common data contract and pocket definition.

The common protein Cα RMSF values are taken from `rmsf_protein_calpha.dat` in each original system folder. The residue-wise table `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv` now contains only this common source for all systems; it no longer mixes legacy active-site or whole-complex RMSF output files.

## Current canonical DMCS result

Using the 5.0 Å structure-defined catalytic pocket and the locked component weights, ATA117-Rd11 ranks first with DMCS = **0.915409**. The current ranking and 4.0/5.0/6.0 Å sensitivity results are included in the machine-readable outputs. The sensitivity analysis is documented in `DMCS_RMSF_METHOD.md`.

## Canonical 5.0 Å DMCS ranking

| Rank | Enzyme | DMCS |
|---:|---|---:|
| 1 | ATA117-Rd11 | 0.915409 |
| 2 | A0A2G0CFH8 | 0.822636 |
| 3 | G-188 | 0.568524 |
| 4 | AspC | 0.551479 |
| 5 | F-188 | 0.536944 |
| 6 | Lys-W-TA | 0.531666 |
| 7 | A0A1B728H4 | 0.526610 |
| 8 | H-188 | 0.526297 |
| 9 | AptA | 0.463306 |
| 10 | A0A1Z5HPJ6 | 0.455464 |
| 11 | S-188 | 0.454378 |
| 12 | AB-R-ATA | 0.449235 |
| 13 | CV-TAm | 0.288440 |
| 14 | W-188 | 0.216602 |
| 15 | S-omega-TA | 0.108260 |

These values are reproduced from the 5.0 Å structure-derived active-site RMSF descriptor and the locked descriptor weights. The 4.0/5.0/6.0 Å sensitivity data are provided in `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`.
