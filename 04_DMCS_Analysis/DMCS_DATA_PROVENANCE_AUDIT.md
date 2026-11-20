# DMCS 15-system data provenance and validation report

## Scope

This report documents the source files and quality-control procedures for the 15-system comparative DMCS analysis. ATA117-Rd11 remains the lead system selected for experimental follow-up.

## Direct inspection of RMSF files

The folders were inspected using a broad RMSF filename inventory rather than assuming that all systems used a single name.

- All 15 systems contain `cpptraj.in`.
- All 15 systems contain `rmsf_protein_calpha.dat`.
- All 15 systems contain `rmsf_complex_all_byres.dat`.
- Nine systems additionally contain `rmsf_byres_clean.dat`.
- Six systems contain a separately named `active_site_rmsf.dat` and matching `active_site_rmsf.in`; four selections are multi-residue, while two are single-residue.
- The five Lys188 substitution folders contain residue-wise RMSF outputs and first-frame inspection structures/inputs (`check_*.in`, `check_*.pdb`).

The earlier assumption that variant folders lacked RMSF data was incorrect; the files were stored under different names. Those supplementary calculations are retained for traceability. The cross-system Drig descriptor now uses the common protein-only Cα source and a common structure-derived pocket rule.

## Protein Cα RMSF validation

Each `cpptraj.in` aligns the protein backbone to `md1.rst7` before calculating per-residue Cα RMSF. The common commands are:

```text
trajin md1.nc 1 last 10
autoimage
center :1-N mass origin
reference md1.rst7 parm solv_complexN.prmtop
rms reference :1-N@CA,C,N
atomicfluct \
  out rmsf_protein_calpha.dat \
  :1-N@CA byres
```

The 500 ns production settings are `dt=0.002 ps`, `nstlim=250000000`, `ntwx=5000`; the RMSF workflow analyses every tenth saved trajectory frame. All 15 systems passed the check that the protein residue endpoint in the CPPTRAJ mask, the protein residue identifiers in `complexN.pdb`, and the row identifiers in `rmsf_protein_calpha.dat` agree exactly.

CPPTRAJ's `atomicfluct` does not RMS-fit implicitly; the explicit preceding `rms reference` step is part of the method (AMBER-hub: https://amberhub.chpc.utah.edu/atomicfluct-rmsf/).

## Harmonized catalytic-pocket RMSF

The prepared structures contain UNP (PLP), UNL (furfural) and UNI (isopropylamine). For each system, protein residues with at least one heavy atom within 5.0 Å of any heavy atom in the combined UNP/UNL/UNI set are selected. The corresponding residue-wise Cα RMSF values are read from the common `rmsf_protein_calpha.dat` output using original residue identifiers. The arithmetic mean of those values is the Drig input.

This procedure creates a per-system residue set from the structure itself; residue numbers are not transferred between enzymes. The complete 5.0 Å pocket map is supplied in `DMCS_ACTIVE_SITE_RESIDUES.csv`. The 4.0/5.0/6.0 Å sensitivity results are supplied in `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`.

The 5.0 Å pocket contains 25–36 residues per system. The harmonized ATA117-Rd11 score is 0.915409 (rank 1). This replaces earlier score tables generated with non-uniform legacy RMSF masks. Values from different RMSF definitions must not be mixed.

## Distance, clustering and MM/GBSA provenance

All 45 distance time series (three for each system) contain 50,000 frames. S1 calculates the mean of the second numeric column. The catalytic residue identity and distance output filename are listed in `S1_INPUTS.csv`.

For every cluster summary, S1 selects the cluster with the greatest frame count and retains its fraction. Cluster frame counts sum to 50,000 for each system. For the UNL-containing MMPBSA result, the first `DELTA TOTAL` row is retained as GB and the second as PB. Signed GB ΔG is retained in the descriptor matrix; its absolute magnitude is used only for Dene.

## DMCS definition

Outer weights: Dcat 0.40, Drig 0.25, Dconf 0.15, Dene 0.20. Dcat subweights: catalytic-residue–PLP 0.50, PLP–furfural 0.25 and PLP–IPA 0.25. Distances and RMSF are inverse min–max normalized; ln(cluster fraction) and absolute GB ΔG are positive min–max normalized.

## Reproducibility outputs

- `S1_INPUTS.csv`: system-folder, catalytic-residue and distance-file manifest.
- `S1_descriptor_extraction.py`: raw descriptor extraction, structure-derived pocket mapping and sensitivity calculation.
- `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv`: frame counts, mean distances, dominant cluster, GB/PB and pocket summaries.
- `DMCS_ACTIVE_SITE_RESIDUES.csv`: canonical pocket membership and per-residue distance/RMSF data.
- `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`: sensitivity to the 4.0, 5.0 and 6.0 Å pocket boundary.
- `DMCS_RESULTS.csv`, `DMCS_STANDARDIZED.csv` and `DMCS_Final_Ranking.csv`: raw descriptor matrix, normalized scores and ranking.
- `DMCS_15_SYSTEMS_INPUTS_AND_PROTOCOLS.md`: collected per-system MD, CPPTRAJ, RMSF, clustering and MMPBSA definitions.

## Quality-control checklist

- [x] All 15 system folders and differently named RMSF outputs inspected.
- [x] Common Cα RMSF output present and residue-mapped in all systems.
- [x] Protein backbone RMS fit precedes `atomicfluct`.
- [x] Protein residue endpoint, prepared structure and Cα RMSF residue IDs agree.
- [x] All 45 distance series contain 50,000 frames.
- [x] Cluster frame totals sum to 50,000; dominant cluster selected by maximum count.
- [x] GB and PB energy rows extracted separately.
- [x] Common 5.0 Å pocket map and 4.0/5.0/6.0 Å sensitivity results generated.
- [x] Raw, normalized and ranked DMCS tables regenerated.

Production trajectories are not included. The public repository provides compact machine-readable descriptors, the residue-level pocket map, system-specific method inputs and scripts needed to reproduce the descriptor-level analysis.
