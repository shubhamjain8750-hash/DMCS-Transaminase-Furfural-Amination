
# Dynamic Mechanistic Conformation Scoring (DMCS)

## Project Overview

This repository accompanies the research study:

**Dynamic Mechanistic Conformation Scoring-Guided Identification and Experimental Validation of a Transaminase for Biomass-Derived Furfural Amination**

This study introduces Dynamic Mechanistic Conformation Scoring (DMCS), a molecular dynamics-based computational framework for the systematic prioritization of PLP-dependent transaminases for the biocatalytic conversion of biomass-derived furfural into furfurylamine.

## DMCS Framework

The DMCS framework integrates four trajectory-derived descriptors:

1. Catalytic Readiness (Dcat)
2. Active-Site Rigidity (Drig)
3. Conformational Persistence (Dconf)
4. Energetic Stabilization (Dene)

The composite DMCS score is calculated using:

DMCS = 0.40(Dcat) + 0.25(Drig) + 0.15(Dconf) + 0.20(Dene)

## Research Objectives

- Computational screening of PLP-dependent enzymes.
- Sequential molecular docking of PLP, furfural and isopropylamine.
- Molecular dynamics-based assessment of enzyme systems.
- Development and implementation of the DMCS framework.
- Comparative evaluation of enzyme homologs and catalytic-site variants.
- Experimental evaluation of ATA117-Rd11 for furfural amination.

## Repository Contents

This repository is being organized to provide the computational scripts, machine-readable datasets, simulation preparation files, processed results and experimental data supporting the study.

The repository will include:

- Enzyme screening datasets.
- Molecular docking inputs and results.
- Molecular dynamics preparation files and parameters.
- DMCS descriptor extraction and scoring scripts.
- Processed computational datasets.
- Experimental source data.
- Software versions and reproducibility documentation.

## Computational Software

The computational workflow uses:

- AMBER
- CPPTRAJ
- AutoDock Vina
- Python
- Molecular visualization and structural analysis tools

Exact software versions and computational dependencies will be documented in the repository.

## Reproducibility

The repository is intended to provide the scripts, input information and machine-readable datasets necessary to reproduce the essential computational analyses and DMCS-based enzyme prioritization described in the associated study.

Molecular dynamics trajectories are not included.

## Citation

Please cite the associated research article when using this repository.

Full publication details and DOI will be added following publication.

## Contact

For questions regarding the computational methodology and associated research, please refer to the corresponding authors listed in the manuscript.
