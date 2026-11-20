# Harmonized catalytic-pocket RMSF procedure

## Purpose and source-file audit

This document defines the residue-level RMSF procedure used to calculate Drig consistently across the 15 PLP-dependent transaminase systems. Each system's pocket is identified independently from its own prepared ternary-complex structure; residue numbers are not transferred between enzymes.

A filename-wide inspection found that all 15 system folders contain `cpptraj.in`, `rmsf_protein_calpha.dat` and `rmsf_complex_all_byres.dat`. Nine also contain `rmsf_byres_clean.dat`. Six contain a separately named `active_site_rmsf.dat` with matching `active_site_rmsf.in` (four multi-residue selections and two single-residue selections). The variant folders additionally contain residue-wise RMSF products and `check_*.in` / `check_*.pdb` inspection files. These supplementary analyses are retained for traceability. The common cross-system source is `rmsf_protein_calpha.dat`, which is present in every system and has the same protein-only Cα definition.

## CPPTRAJ Cα RMSF workflow

The system-specific `cpptraj.in` files share this pattern; N is the protein residue endpoint for that system:

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

Production parameters are `dt=0.002 ps`, `nstlim=250000000` and `ntwx=5000`, corresponding to 500 ns with 50,000 saved frames. The CPPTRAJ RMSF calculation samples every tenth saved frame. The explicit `rms reference` action aligns the protein backbone (Cα, C and N) to `md1.rst7` before `atomicfluct`. CPPTRAJ's `atomicfluct` does not perform RMS fitting implicitly; the prior RMS fit removes global translation and rotation before positional fluctuations are measured (AMBER-hub documentation: https://amberhub.chpc.utah.edu/atomicfluct-rmsf/).

For every system, the protein residue endpoint in the CPPTRAJ mask, the protein residue identifiers in `complexN.pdb`, and the row identifiers in `rmsf_protein_calpha.dat` match exactly.

## Structure-derived pocket definition

The prepared `complexN.pdb` files contain UNP (PLP), UNL (furfural) and UNI (isopropylamine). For each system independently:

1. Select the heavy atoms (exclude H and D) in UNP, UNL and UNI.
2. For every protein residue R, calculate the minimum Euclidean distance between any protein heavy atom in R and any heavy atom in the combined UNP/UNL/UNI set: `d(R) = min ||x_i - x_j||`.
3. Define the catalytic pocket as protein residues with `d(R) <= 5.0 Å`.
4. Retrieve each selected residue's Cα RMSF from `rmsf_protein_calpha.dat` using its original residue number.
5. Calculate the pocket RMSF as the arithmetic mean of those residue-wise Cα RMSF values: `RMSF_pocket = sum(RMSF_CA,R) / N_pocket`.

The 5.0 Å heavy-atom shell is the canonical Drig definition. It is generated independently from each enzyme's prepared ternary structure. The full machine-readable residue map, including residue name, nearest ligand/cofactor, minimum distance and Cα RMSF, is supplied in `DMCS_ACTIVE_SITE_RESIDUES.csv`.

## Cutoff sensitivity

The pocket was recalculated at 4.0, 5.0 and 6.0 Å. Pocket means, component scores and DMCS ranks are in `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`. The leading two systems and bottom two systems retain their positions across these cutoffs; intermediate rankings change modestly. This sensitivity analysis makes the operational pocket boundary explicit.

## Other descriptors and DMCS

- Catalytic-residue–PLP, PLP–furfural and PLP–IPA distances are arithmetic means of column 2 in their CPPTRAJ time-series files. All 45 series contain 50,000 frames.
- Conformational persistence is the frame fraction of the cluster with the maximum frame count in `dmcs_cluster_summary.dat`.
- Energetic stabilization uses the first `DELTA TOTAL` row from the UNL-containing MMPBSA output (GB). The second row is PB. Signed GB ΔG is retained; its absolute magnitude is used only for Dene.

Weights: Dcat = 0.40, Drig = 0.25, Dconf = 0.15, Dene = 0.20. Dcat subweights: catalytic-residue–PLP = 0.50, PLP–furfural = 0.25, PLP–IPA = 0.25. Distances and pocket RMSF are inverse min–max normalized; ln(largest-cluster fraction) and |GB ΔG| are positive min–max normalized.

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`.

## S1 quality-control checks

S1 checks the 15-system manifest, required source files, 50,000-frame distances, cluster frame totals, GB/PB energy rows, ligand heavy-atom inventory, protein RMS-fit-before-RMSF sequence, production MD parameters, protein residue endpoint and exact structure/RMSF residue-number correspondence. It writes the raw descriptor matrix, canonical pocket residue map, cutoff sensitivity, normalized table and final ranking.
