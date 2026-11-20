# Dynamic Mechanistic Conformation Scoring (DMCS)

## Research overview

This repository provides the computational data, input examples and analysis scripts accompanying the study of PLP-dependent transaminases for the conversion of biomass-derived furfural to furfurylamine.

The workflow combines sequential molecular docking, molecular-dynamics simulations and a descriptor-based comparative framework termed **Dynamic Mechanistic Conformation Scoring (DMCS)**. DMCS is a comparative prioritization metric; it is not an experimentally measured activity, kinetic parameter or absolute binding free energy.

## Repository map

| Directory | Purpose | Contents |
|---|---|---|
| [01_Enzyme_Screening](01_Enzyme_Screening/) | Candidate screening and panel definition | CSV versions of Supporting Information Tables S1–S4 |
| [02_Docking](02_Docking/) | Sequential docking strategy | Workflow documentation; score tables are in `01_Enzyme_Screening/` |
| [03_MD_Inputs](03_MD_Inputs/) | MD preparation/production and trajectory analysis inputs | AMBER input examples, CPPTRAJ templates and 30 PDB structures |
| [04_DMCS_Analysis](04_DMCS_Analysis/) | Canonical DMCS analysis | Raw/normalized tables, scripts, per-enzyme summaries, collected DAT outputs and provenance documentation |
| [05_Computational_Environment](05_Computational_Environment/) | Software and execution environment | Environment notes and Python dependency pointer |
| [06_Post_MD_Analysis_DAT_Files](06_Post_MD_Analysis_DAT_Files/) | Extended post-production analysis outputs | RMSD, Rg, SASA and hydrogen-bond time-series data; collection is undergoing final classification/QC |

## DMCS model

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`

- **Dcat — catalytic readiness:** weighted combination of catalytic-residue–PLP (0.50), PLP–furfural (0.25) and PLP–isopropylamine (0.25) distance descriptors.
- **Drig — active-site rigidity:** inverse-normalized mean Cα RMSF of a structure-derived catalytic pocket.
- **Dconf — conformational persistence:** positive min–max normalization of the natural logarithm of the dominant-cluster frame fraction.
- **Dene — energetic stabilization:** positive min–max normalization of the absolute magnitude of the signed GB binding-energy estimate.

Distances and pocket RMSF are inverse min–max normalized. Log dominant-cluster fraction and absolute GB energy magnitude are positive min–max normalized across the defined 15-system panel. The resulting score is therefore panel-dependent.

## Canonical 15-system result

Using the harmonized 5.0 Å structure-derived pocket definition, **ATA117-Rd11 ranks first (DMCS = 0.915409)**. The complete ranking is in [DMCS_Final_Ranking.csv](04_DMCS_Analysis/DMCS_Final_Ranking.csv). Pocket definition and cutoff sensitivity are documented in [DMCS_RMSF_METHOD.md](04_DMCS_Analysis/DMCS_RMSF_METHOD.md).

## Data availability and scope

### Included
- Screening CSV files corresponding to Supporting Information Tables S1–S4.
- AMBER minimization, heating, density/equilibration and production input examples.
- CPPTRAJ input examples for RMSD/RMSF/hydrogen-bond and Rg/SASA calculations.
- Prepared unsolvated enzyme–PLP–furfural–IPA structures and solvated stage-2 PDB snapshots for 15 systems.
- 199 collected numerical DAT outputs, including RMSF, catalytic distance, clustering and MMPBSA outputs where present.
- Harmonized per-enzyme DMCS descriptors, pocket residue maps, normalization/ranking scripts and audit documentation.

### Not included / pending
- Production MD trajectories and the complete set of binary AMBER restart/topology files.
- Complete per-enzyme docking pose/PDBQT/configuration packages.
- A fully validated, cross-system set of post-MD RMSD, Rg, SASA and hydrogen-bond result files. A preliminary 690-file collection passed byte-integrity checks, but the audit identified 45 MMPBSA summary reports incorrectly classified as SASA. That preliminary collection is not the publication dataset. The corrected collection must explicitly exclude MMPBSA/MMGBSA reports and be re-audited before deposit. See [06_Post_MD_Analysis_DAT_Files/README.md](06_Post_MD_Analysis_DAT_Files/README.md).
- Experimental chromatograms, HPLC data or supplementary figure files.

The absence of a result file must not be interpreted as a zero value or a failed analysis. Only analyses represented by deposited output files should be described as deposited results.

## Reproducibility

**Reproduce normalization and ranking from deposited descriptors:** install dependencies from [requirements.txt](04_DMCS_Analysis/requirements.txt) and follow [DMCS_REPRODUCTION_GUIDE.md](04_DMCS_Analysis/DMCS_REPRODUCTION_GUIDE.md). This route does not require trajectories.

**Re-extract descriptors from original MD analysis folders:** S1 requires original per-system folders and their distance, cluster, RMSF and MMPBSA files. These complete source folders and trajectories are not included. See [S1_INPUTS.csv](04_DMCS_Analysis/S1_INPUTS.csv) and the reproduction guide for the input contract.

The canonical Drig descriptor uses the protein-only `rmsf_protein_calpha.dat` source and a per-system, structure-derived 5.0 Å heavy-atom pocket. Legacy whole-complex or manually selected active-site RMSF files are retained as source records but are not substituted into the canonical cross-system calculation.

## Citation

Please cite the associated research article and its Supporting Information when using these data or methods. Add publication details and DOI here once available.

## Contact

For scientific questions, contact the corresponding authors listed in the associated manuscript.

## Repository

https://github.com/shubhamjain8750-hash/DMCS-Transaminase-Furfural-Amination
