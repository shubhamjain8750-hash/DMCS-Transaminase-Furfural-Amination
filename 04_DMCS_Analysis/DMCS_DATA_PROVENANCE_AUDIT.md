# DMCS 15-system data provenance and quality-control report

## Scope

This audit records the source-file checks and consistency rules used to build the canonical 15-system DMCS descriptor dataset. The canonical output is the 5.0 Å structure-derived pocket analysis and its 15-system ranking.

## Source inventory

The supplied source archive was inspected across 15 enzyme analysis directories. Each system contained the common protein-only `rmsf_protein_calpha.dat` and a CPPTRAJ input. Whole-complex RMSF outputs, `rmsf_byres_clean.dat` in a subset, and separately named `active_site_rmsf.dat` outputs in a subset were also found. These differently defined legacy files are retained as provenance records but are not mixed into the canonical cross-system Drig descriptor.

The public repository contains the 15-system prepared PDB structures and stage-2 PDB snapshots; collected per-system DAT files and their SHA256 manifest; harmonized raw descriptor matrix, pocket residue map, RMSF profiles, normalized values and ranking; and S1–S3 scripts and method documentation.

The complete original per-system analysis directories, production trajectory files and binary AMBER restart/topology files are not included. Full S1 extraction from original source folders therefore requires a separate copy of those source directories.

## Common Cα RMSF source and alignment

The common RMSF source is `rmsf_protein_calpha.dat` for each system. It is a protein-only, per-residue Cα RMSF profile. In the source workflow the protein backbone is aligned before `atomicfluct` is applied. Whole-complex or ligand RMSF outputs are not interchangeable with this metric.

The 500 ns production control is defined by `dt=0.002 ps` and `nstlim=250000000`. Coordinates are saved every 5,000 steps, equivalent to 10 ps and 50,000 saved frames for a completed trajectory. The supplied common CPPTRAJ examples include a 330-residue protein mask; because the evaluated enzymes have different lengths and residue numbering, the mask must be system-adjusted before reuse.

## Structure-derived catalytic pocket

The prepared `complexN.pdb` structures contain UNP (PLP), UNL (furfural) and UNI (isopropylamine). For each enzyme independently: (1) exclude hydrogen/deuterium atoms from the contact calculation; (2) calculate the minimum distance between any protein heavy atom in a residue and any heavy atom in the combined UNP/UNL/UNI set; (3) include residues at or below 5.0 Å; (4) map each residue's Cα RMSF from the common `rmsf_protein_calpha.dat` using that system's residue identifier; and (5) calculate the arithmetic mean of the selected residue-wise values.

The full residue membership, minimum distances and mapped RMSF values are in `DMCS_ACTIVE_SITE_RESIDUES.csv`. The 4.0, 5.0 and 6.0 Å cutoff sensitivity results are in `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`.

## Other descriptor provenance

- Catalytic-residue–PLP, PLP–furfural and PLP–IPA distance descriptors are means of their respective CPPTRAJ time series. Each of the 45 inspected series contains 50,000 frames.
- The dominant cluster is selected by maximum frame count in `dmcs_cluster_summary.dat`; source cluster frame totals sum to 50,000 per system.
- The first `DELTA TOTAL` entry in the UNL-containing MMPBSA report is treated as GB and the second as PB. Signed GB is retained; its absolute magnitude is used only for Dene.

## DMCS weights and scaling

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`.

Dcat subweights: catalytic-residue–PLP 0.50, PLP–furfural 0.25 and PLP–IPA 0.25. Distance and pocket-RMSF descriptors are inverse min–max scaled. The natural logarithm of the dominant-cluster fraction and the absolute GB ΔG magnitude are positive min–max scaled over the defined 15-system panel.

## Publicly reproducible components

- S2 normalization and S3 ranking can be run from the checked-in raw descriptor matrix.
- S1 is provided for independent source-data extraction, but requires the original per-system analysis folders specified in `S1_INPUTS.csv`.
- The repository does not include production trajectories and cannot reproduce a new MD trajectory from PDB snapshots alone.

## Quality-control summary

- [x] Fifteen source systems inventoried.
- [x] Common protein-only Cα RMSF source identified for each system.
- [x] Structure-to-RMSF residue correspondence checked.
- [x] 45 catalytic-distance series checked for 50,000 frames each.
- [x] Dominant cluster selected by frame count; cluster totals checked.
- [x] GB and PB `DELTA TOTAL` entries distinguished.
- [x] Structure-derived 5.0 Å pocket map generated separately for each enzyme.
- [x] 4.0/5.0/6.0 Å cutoff sensitivity calculated.
- [x] Raw descriptors, normalized scores and final ranking generated.

## Interpretation and limitations

The score is a relative prioritization metric over this specific panel and descriptor set. It is not an absolute estimate of catalytic rate, substrate conversion or experimentally measured binding affinity. Missing RMSD, Rg, SASA or hydrogen-bond result files are not treated as zeros and are not claimed as deposited analyses.
