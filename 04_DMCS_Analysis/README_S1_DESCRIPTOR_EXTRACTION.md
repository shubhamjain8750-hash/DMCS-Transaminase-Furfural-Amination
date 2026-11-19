# S1: Raw Descriptor Extraction for DMCS Analysis

## Overview

The S1 workflow describes the extraction and compilation of molecular dynamics-derived descriptors used in the Dynamic Mechanistic Conformation Scoring (DMCS) framework.

The workflow was applied to the 15 selected transaminase systems.

The extracted descriptors were obtained from cpptraj trajectory analyses and Amber MM/GBSA calculations. These values were subsequently compiled into `DMCS_RESULTS.csv`, which serves as the input for the normalization and scoring procedure implemented in S2.

## 1. Trajectory preparation

For each enzyme system, the production molecular dynamics trajectory was processed to generate a solvent-stripped trajectory for subsequent structural analyses.

The following operations were performed using cpptraj:

- Loading the corresponding topology and production trajectory.
- Applying periodic-boundary correction and imaging.
- Removing water and counterions.
- Saving the resulting trajectory in NetCDF format.

The resulting solvent-stripped trajectories were used consistently for the subsequent distance, clustering, and RMSF analyses.

## 2. Catalytic residue identification

The catalytic residue associated with PLP was identified by inspecting the corresponding complex structure and verifying residue numbering against the Amber topology.

For the canonical Lys-containing systems, the catalytic Lys residue was identified through its interaction with PLP.

For the Lys188 substitution systems, the corresponding substituted residue was used:

- H-188: Histidine
- G-188: Glycine
- F-188: Phenylalanine
- S-188: Serine
- W-188: Tryptophan

The corresponding residue-specific distance calculations were performed using the appropriate atom selections.

## 3. Distance descriptor extraction

Three distance descriptors were evaluated:

1. Catalytic residue–PLP distance.
2. PLP–furfural (UNL) distance.
3. PLP–isopropylamine (UNI) distance.

The distances were calculated using cpptraj and recorded as individual time-series output files.

The mean distance across the analysed trajectory frames was used as the corresponding raw descriptor.

## 4. Conformational clustering

Trajectory clustering was performed using cpptraj hierarchical agglomerative clustering.

The ligand-containing PLP, furfural, and IPA structural selections were used according to the system-specific clustering input.

The cluster summary output was used to identify the largest cluster and its corresponding fraction of analysed trajectory frames.

The largest-cluster fraction was retained as the conformational persistence descriptor.

## 5. Active-site RMSF

Active-site flexibility was evaluated using the atomic fluctuation analysis implemented in cpptraj.

The protein trajectory was structurally aligned before calculating the per-residue Cα fluctuations.

The active-site residue selections were defined for the corresponding enzyme systems based on their catalytic-site structural context and interaction analysis.

The mean RMSF across the selected active-site residues was used as the raw flexibility descriptor.

## 6. MM/GBSA energy extraction

Binding free-energy calculations were performed using the Amber MMPBSA workflow.

The generalized Born (GB) `DELTA TOTAL` value corresponding to the furfural-containing complex was extracted from the respective MM/GBSA output file.

The signed binding free-energy value was retained in the raw descriptor dataset. Its absolute magnitude was subsequently used by the existing S2 normalization procedure.

## 7. Raw descriptor compilation

The extracted descriptors were compiled into `DMCS_RESULTS.csv`.

The dataset contains the following fields:

| Descriptor      | Description                                                                               |
| --------------- | ----------------------------------------------------------------------------------------- |
| Enzyme          | Enzyme-system identifier                                                                  |
| Lys_PLP         | Catalytic residue–PLP distance descriptor, using the existing scoring-pipeline field name |
| PLP_UNL         | Mean PLP–furfural distance                                                                |
| PLP_UNI         | Mean PLP–isopropylamine distance                                                          |
| RMSF            | Mean active-site RMSF                                                                     |
| ClusterFraction | Largest-cluster fraction                                                                  |
| MMGBSA          | Signed GB binding free energy                                                             |

**Note:** `Lys_PLP` is retained as the existing column identifier for compatibility with the original DMCS scoring scripts. For Lys188 substitution systems, the corresponding substituted catalytic residue was used in the underlying distance calculation.

## 8. Downstream analysis

The compiled `DMCS_RESULTS.csv` file is supplied to S2, which performs descriptor normalization and calculates the composite DMCS score using the predefined weighting scheme.

S3 subsequently generates the final comparative ranking of the 15 enzyme systems.

The extraction, normalization, and ranking stages are maintained as separate computational steps to facilitate transparency and reproducibility.

S1 performs raw descriptor extraction and compilation; it does not independently normalize descriptors, train a machine-learning model, or calculate the final DMCS ranking.
