# Dynamic Mechanistic Conformation Scoring (DMCS)

## Project Overview

This repository accompanies the research study:

**Dynamic Mechanistic Conformation Scoring-Guided Identification and Experimental Validation of a Transaminase for Biomass-Derived Furfural Amination**

The study introduces Dynamic Mechanistic Conformation Scoring (DMCS), a molecular-dynamics-based descriptor framework for systematic prioritization of PLP-dependent transaminases for the biocatalytic conversion of biomass-derived furfural into furfurylamine.

## DMCS Framework

The DMCS framework integrates four descriptor components:

1. Catalytic readiness (Dcat)
2. Active-site rigidity (Drig)
3. Conformational persistence (Dconf)
4. Energetic stabilization (Dene)

The composite score is:

`DMCS = 0.40(Dcat) + 0.25(Drig) + 0.15(Dconf) + 0.20(Dene)`

The catalytic-readiness component uses catalytic-residue–PLP, PLP–furfural and PLP–isopropylamine distance descriptors with subweights of 0.50, 0.25 and 0.25, respectively.

## Repository Contents

- Enzyme screening datasets.
- Sequential molecular-docking methodology and supporting data.
- Molecular-dynamics and MM/GBSA input parameters.
- System-specific DMCS distance and clustering input files.
- Machine-readable raw descriptor tables and residue-wise RMSF data.
- Descriptor extraction, normalization and ranking scripts.
- Processed computational datasets and reproducibility documentation.

The 15-system DMCS analysis and its supporting inputs are documented in `04_DMCS_Analysis/`.

## Computational Software

- AMBER24
- CPPTRAJ
- AutoDock Vina
- Python (NumPy and pandas)
- PyMOL and other molecular-visualization tools

## Reproducibility

The repository provides the S1–S3 analysis scripts, machine-readable descriptor data, the per-enzyme data directory (`04_DMCS_Analysis/15_Enzyme_Analysis_Data/`), system-specific analysis inputs, and the source tables used to inspect distance, clustering, RMSF and MM/GBSA descriptors. Molecular-dynamics trajectory files are not included.

The canonical rigidity descriptor is generated for all 15 systems from the common protein-only Cα RMSF output and a structure-derived 5.0 Å catalytic-pocket definition. The residue mapping, per-system source tables and 4.0/5.0/6.0 Å sensitivity analysis are documented in `04_DMCS_Analysis/`.

## Data and Software Availability

The computational scripts, machine-readable descriptor datasets, per-enzyme analysis outputs for all 15 systems, structure-derived catalytic-pocket RMSF maps, system-specific analysis inputs and supporting reproducibility documentation are publicly available in this GitHub repository:

https://github.com/shubhamjain8750-hash/DMCS-Transaminase-Furfural-Amination

The Supporting Information provides the detailed computational methodology and supplementary results. Molecular-dynamics trajectories are not included.

## Citation

Please cite the associated research article when using this repository. Publication details and DOI will be added following publication.

## Contact

For questions regarding the computational methodology and associated research, please refer to the corresponding authors listed in the manuscript.

## Current 15-system DMCS analysis

The harmonized 5.0 Å structure-derived catalytic-pocket RMSF analysis ranks **ATA117-Rd11** first (DMCS = **0.915409**). The complete 15-system ranking, component scores, residue maps, per-enzyme data and cutoff-sensitivity results are maintained in [`04_DMCS_Analysis/`](04_DMCS_Analysis/README.md).
