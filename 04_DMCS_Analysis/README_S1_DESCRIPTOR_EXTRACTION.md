# S1: Raw descriptor extraction and harmonized catalytic-pocket RMSF

S1 reads `S1_INPUTS.csv` and the 15 per-system analysis folders.

## Required source files

- `complexN.pdb`: prepared ternary structure with UNP (PLP), UNL (furfural) and UNI (isopropylamine).
- `cpptraj.in`, `md1.in` and `mmpbsa.in`: method and production inputs.
- `rmsf_protein_calpha.dat`: common protein-only Cα RMSF output.
- Catalytic-residue–PLP distance file named in `S1_INPUTS.csv`.
- `plp_unl.dat`, `plp_uni.dat`, `dmcs_cluster_summary.dat`.
- `FINAL_RESULTS_UNL_MMPBSA.dat`.

## RMSF definition

S1 derives the 5.0 Å catalytic pocket separately from each `complexN.pdb`: protein residues with at least one heavy atom within 5.0 Å of the combined UNP/UNL/UNI heavy-atom set. It retrieves per-residue Cα RMSF by original residue number and averages these values to give Drig's raw input.

The source `cpptraj.in` performs a protein backbone RMS fit to `md1.rst7` before `atomicfluct`. CPPTRAJ does not align coordinates implicitly inside `atomicfluct`; this preceding fit is essential. Details and sensitivity analysis are in `DMCS_RMSF_METHOD.md`.

## Other descriptors

- Distance means: mean of column 2 for catalytic-residue–PLP, PLP–furfural and PLP–IPA time series. Each file must contain 50,000 frames.
- Conformational persistence: fraction of the cluster with the greatest frame count; cluster frame counts must sum to 50,000.
- Energetic stabilization: first `DELTA TOTAL` row in the UNL MMPBSA output (GB); the second row is retained separately as PB. Keep signed GB ΔG in the raw table; use its absolute magnitude only for Dene.

## Run

```bash
python -m pip install -r 04_DMCS_Analysis/requirements.txt
python 04_DMCS_Analysis/S1_descriptor_extraction.py \
  --analysis-root "$HOME/amber24" \
  --output-dir 04_DMCS_Analysis \
  --pocket-cutoff 5.0 \
  --sensitivity-cutoffs 4,5,6
```

S1 generates raw source descriptors, the canonical pocket map, cutoff sensitivity, the S2 input matrix and updated score/ranking tables. It stops if source files, residue mappings, frame counts or production/RMSF settings fail validation.
