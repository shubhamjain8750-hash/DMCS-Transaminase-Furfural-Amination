# S1: Raw Descriptor Extraction and Compilation for DMCS Analysis

## Overview

The S1 workflow describes the extraction and compilation of molecular dynamics-derived descriptors used in the Dynamic Mechanistic Conformation Scoring (DMCS) framework.

The workflow was applied to 15 selected transaminase systems. Molecular dynamics-derived distance, conformational clustering, and active-site flexibility descriptors, together with previously calculated MM/GBSA binding energies, were compiled into a unified dataset.

The resulting `DMCS_RESULTS.csv` file serves as the input for descriptor normalization and DMCS calculation in S2.

The S1 workflow is implemented in `S1_descriptor_extraction.py`.

## 1. Input organization

The extraction workflow uses `S1_INPUTS.csv` as its input manifest.

The manifest contains the following fields:

| Field | Description |
|---|---|
| `Enzyme` | Enzyme-system identifier |
| `Directory` | Directory containing the corresponding analysis outputs |
| `CatalyticDistanceFile` | System-specific catalytic residue–PLP distance file |
| `RMSF` | Previously calculated mean active-site RMSF |
| `MMGBSA` | Previously calculated signed GB binding free energy |

The `CatalyticDistanceFile` field allows the extraction script to accommodate different catalytic-residue distance filenames across enzyme systems.

Each analysis directory is expected to contain the corresponding catalytic-residue–PLP distance file, `plp_unl.dat`, `plp_uni.dat`, and `dmcs_cluster_summary.dat`.

The RMSF and MMGBSA values are supplied through the input manifest because these descriptors were calculated previously. S1 compiles these values with the corresponding trajectory-derived descriptors rather than rerunning the underlying simulations or energy calculations.

## 2. Trajectory preparation

For each enzyme system, the production molecular dynamics trajectory was processed to generate a solvent-stripped trajectory for subsequent structural analyses.

The following operations were performed using cpptraj:

- Loading the corresponding topology and production trajectory.
- Applying periodic-boundary correction and imaging.
- Removing water molecules and counterions.
- Saving the resulting trajectory in NetCDF format.

The resulting solvent-stripped trajectories were used for subsequent distance, clustering, and RMSF analyses.

## 3. Catalytic residue identification

The catalytic residue associated with PLP was identified by inspecting the corresponding complex structure and verifying residue numbering against the Amber topology.

For canonical Lys-containing systems, the catalytic Lys residue was identified based on its interaction with PLP.

For the Lys188 substitution systems, the corresponding substituted residue was used:

- H-188: Histidine
- G-188: Glycine
- F-188: Phenylalanine
- S-188: Serine
- W-188: Tryptophan

The corresponding residue-specific distance files were used for descriptor extraction. Their filenames are specified individually in `S1_INPUTS.csv`.

## 4. Distance descriptor extraction

Three distance descriptors were evaluated:

1. Catalytic residue–PLP distance.
2. PLP–furfural (UNL) distance.
3. PLP–isopropylamine (UNI) distance.

The distances were calculated using cpptraj and recorded as individual time-series output files.

The mean distance across the analysed trajectory frames was calculated using the second numerical column of the corresponding cpptraj output file.

The extraction script processes the catalytic-residue–PLP distance using the filename specified in the input manifest, while the PLP–furfural and PLP–IPA distances are read from `plp_unl.dat` and `plp_uni.dat`, respectively.

## 5. Conformational clustering

Trajectory clustering was performed using cpptraj hierarchical agglomerative clustering.

The ligand-containing PLP, furfural, and IPA structural selections were used according to the corresponding system-specific clustering input.

The cluster summary output, `dmcs_cluster_summary.dat`, was used to identify the cluster containing the maximum number of trajectory frames.

The corresponding cluster fraction was retained as the conformational persistence descriptor.

The extraction script identifies the largest cluster based on its frame count rather than assuming that a particular row represents the largest cluster.

## 6. Active-site RMSF

Active-site flexibility was evaluated using the atomic fluctuation analysis implemented in cpptraj.

The protein trajectory was structurally aligned before calculating the per-residue Cα fluctuations.

Active-site residue selections were defined for the corresponding enzyme systems based on their catalytic-site structural context and interaction analysis.

The mean RMSF across the selected active-site residues was used as the raw flexibility descriptor.

These previously calculated RMSF values are supplied through `S1_INPUTS.csv` and incorporated into the final descriptor dataset.

## 7. MM/GBSA energy extraction

Binding free-energy calculations were performed using the Amber MMPBSA workflow.

The generalized Born (GB) `DELTA TOTAL` value corresponding to the furfural-containing complex was obtained from the respective MM/GBSA output.

The signed binding free-energy value was retained in `S1_INPUTS.csv` and incorporated into the raw descriptor dataset.

The absolute magnitude of the signed MM/GBSA value is subsequently used by the existing S2 normalization procedure to represent the energetic descriptor.

## 8. Raw descriptor compilation

The extracted descriptors were compiled into `DMCS_RESULTS.csv`.

The output dataset contains the following fields:

| Descriptor | Description |
|---|---|
| `Enzyme` | Enzyme-system identifier |
| `Lys_PLP` | Catalytic residue–PLP distance descriptor, retaining the existing scoring-pipeline column name |
| `PLP_UNL` | Mean PLP–furfural distance |
| `PLP_UNI` | Mean PLP–isopropylamine distance |
| `RMSF` | Mean active-site RMSF |
| `ClusterFraction` | Fraction of trajectory frames belonging to the largest cluster |
| `MMGBSA` | Signed GB binding free energy |

**Column naming note:** The `Lys_PLP` identifier is retained for compatibility with the existing DMCS normalization script. For Lys188 substitution systems, the corresponding substituted catalytic residue was used in the underlying distance calculation. Thus, the column represents the catalytic residue–PLP distance descriptor across the enzyme panel.

The S1 script performs input validation, checks the availability of the required analysis files, extracts the numerical descriptors, and compiles the resulting values into the unified CSV dataset.

## 9. Downstream normalization and ranking

The compiled `DMCS_RESULTS.csv` file is supplied to S2 for descriptor normalization and composite DMCS calculation.

The predefined weighting scheme is retained:

- Catalytic readiness (Dcat): 0.40
- Active-site rigidity (Drig): 0.25
- Conformational persistence (Dconf): 0.15
- Energetic stabilization (Dene): 0.20

The catalytic readiness component retains its established subweights:

- Catalytic residue–PLP distance: 0.50
- PLP–furfural distance: 0.25
- PLP–isopropylamine distance: 0.25

S3 subsequently ranks the enzyme systems according to their calculated DMCS scores and generates the final comparative ranking table.

The extraction, normalization, and ranking stages are maintained as separate computational steps to facilitate transparency and reproducibility.

## 10. Reproducibility and implementation

The complete S1–S3 workflow is organized into independent scripts:

| Script | Function |
|---|---|
| `S1_descriptor_extraction.py` | Compiles raw descriptors from individual analysis folders and the input manifest |
| `S2_DMCS_normalization.py` | Performs descriptor normalization and calculates the composite DMCS score |
| `S3_DMCS_ranking.py` | Generates the final comparative ranking and summary table |

S1 performs raw descriptor compilation and validation. It does not independently normalize descriptors, train a predictive machine-learning model, or calculate the final DMCS ranking.

For reproducibility, the input manifest, analysis output files, software inputs, and corresponding descriptor values should be retained alongside the analysis scripts.

The workflow therefore provides a transparent separation between molecular dynamics-derived descriptor extraction, normalization, and final DMCS-based enzyme ranking.
