# Dynamic Mechanistic Conformation Scoring (DMCS)

## Research overview

This repository contains computational screening tables, prepared molecular structures, selected molecular-dynamics (MD) source outputs, the Dynamic Mechanistic Conformation Scoring (DMCS) descriptor workflow, and associated provenance documentation for the comparative study of PLP-dependent transaminases in furfural-to-furfurylamine biocatalysis.

DMCS is a panel-relative, descriptor-based prioritization framework. It is not an experimentally measured activity, catalytic rate, absolute binding free energy or substitute for biochemical validation.

## Repository map

| Directory | Purpose | Main contents |
|---|---|---|
| [01_Enzyme_Screening](01_Enzyme_Screening/) | Screening data | Machine-readable versions of Supporting Information Tables S1–S4 |
| [02_Docking](02_Docking/) | Sequential docking workflow | Docking-stage description and interpretation boundaries |
| [03_MD_Inputs](03_MD_Inputs/) | MD setup and analysis templates | AMBER control examples, CPPTRAJ templates and prepared PDB structures |
| [04_DMCS_Analysis](04_DMCS_Analysis/) | Canonical DMCS calculation | Raw descriptors, pocket/RMSF maps, normalization/ranking scripts, selected source DAT files and QC records |
| [05_Computational_Environment](05_Computational_Environment/) | Software and environment | Dependency list and reproduction notes |
| [06_Post_MD_Analysis_DAT_Files](06_Post_MD_Analysis_DAT_Files/) | Ancillary per-system post-MD output archive | RMSD, Rg, SASA and hydrogen-bond output series with source manifest and QC report |

## Canonical DMCS definition

`DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene`

- **Dcat — catalytic-geometry descriptor:** weighted combination of catalytic-residue–PLP (0.50), PLP–furfural (0.25) and PLP–IPA (0.25) mean-distance descriptors.
- **Drig — catalytic-pocket flexibility descriptor:** inverse min–max normalized mean protein Cα RMSF for the enzyme-specific structure-derived 5.0 Å pocket.
- **Dconf — conformational-persistence descriptor:** positive min–max normalization of the natural logarithm of the dominant-cluster frame fraction.
- **Dene — energetic descriptor:** positive min–max normalization of the absolute magnitude of the signed GB `DELTA TOTAL` value.

Distance and pocket-RMSF descriptors are inverse min–max normalized; log cluster fraction and absolute GB energy magnitude are positive min–max normalized. Scaling is performed across the defined 15-enzyme panel. Consequently, DMCS values and ranks are panel-dependent and can change if the panel or descriptor definitions change.

## Canonical 15-system result

For the documented 5.0 Å structure-derived pocket definition and weights, ATA117-Rd11 ranks first (DMCS = **0.915409**). The complete 15-system ranking is available in [DMCS_Final_Ranking.csv](04_DMCS_Analysis/DMCS_Final_Ranking.csv). The pocket definition, RMSF mapping and cutoff sensitivity are described in [DMCS_RMSF_METHOD.md](04_DMCS_Analysis/DMCS_RMSF_METHOD.md).

This ranking is the output of the defined DMCS descriptors only. The ancillary RMSD, Rg, SASA and hydrogen-bond series in directory 06 are **not additional DMCS terms** and were not used to calculate the deposited canonical DMCS scores.

## Data availability

### Screening and structural inputs
- Machine-readable screening tables corresponding to Supporting Information Tables S1–S4.
- AMBER minimization, heating, equilibration, production and MM/GBSA control examples.
- CPPTRAJ example inputs for RMSD/RMSF/hydrogen-bond and Rg/SASA analyses.
- Thirty PDB structures: prepared unsolvated complexes and solvated stage-2 coordinate snapshots for 15 systems, with a structure manifest.

### Canonical DMCS source and processed data
- Selected per-system distance, RMSF, clustering and MMPBSA source DAT outputs, with source manifest.
- Harmonized 15-system raw descriptor matrix, canonical pocket residue map, per-residue RMSF profiles, cutoff sensitivity, normalized components and final ranking.
- S1–S3 scripts and method/provenance documentation.

### Ancillary post-MD output archive
Directory [06_Post_MD_Analysis_DAT_Files](06_Post_MD_Analysis_DAT_Files/) contains 645 original DAT outputs (165 RMSD, 150 Rg, 150 SASA and 180 hydrogen-bond files) and 585 numeric CSV conversions. The collection passed a source-copy SHA256 audit (645/645 matches), with no missing copies, checksum mismatches, repeated checksum groups, irregular numeric rows or MMPBSA/MMGBSA reports. The manifest and per-system inventory are included.

These files are archived as per-system analysis outputs. They are not pooled into a harmonized comparative metric and are not inputs to the current DMCS formula/ranking. The `*_ns` subfolder files are time-axis re-expressions of corresponding frame-indexed series, not independent simulation replicas. The archive's integrity QC does not, by itself, establish that every system used identical atom masks, reference structures, surface settings or hydrogen-bond selections. See the directory README and QC report before reusing or comparing these series.

## Reproducibility boundaries

**Reproduce the deposited DMCS normalization and ranking:** install dependencies from [requirements.txt](04_DMCS_Analysis/requirements.txt), then run the S2 and S3 scripts as described in [DMCS_REPRODUCTION_GUIDE.md](04_DMCS_Analysis/DMCS_REPRODUCTION_GUIDE.md). This route uses the checked-in raw descriptor matrix and does not require MD trajectories.

**Re-extract raw descriptors (S1):** the S1 script is provided, but full re-extraction requires the original 15 per-system analysis directories and source files listed in `S1_INPUTS.csv`. The complete original analysis folders and production trajectories are not included in this repository.

**Re-run MD or docking:** PDB snapshots and example control files are not substitutes for the complete system-specific AMBER topology/restart/trajectory files or docking preparation/configuration/pose packages. Those materials are not fully deposited here. Do not infer missing settings from score tables or generic example templates.

## Important limitations

- Docking scores are scoring-function outputs for comparative filtering, not measured binding energies or catalytic rates.
- The DMCS score is relative to the chosen 15-system panel and its normalization scheme.
- A 5.0 Å pocket is defined independently for each enzyme from its own prepared ternary structure; residue numbering must not be transferred between systems.
- The post-MD output archive is not evidence that its different analysis selections are fully harmonized across all systems.
- Experimental chromatograms, HPLC results and supplementary figure files are not included in this public repository.

## Citation

Please cite the associated research article and its Supporting Information when using these methods or datasets. Publication details and DOI should be added here once available.

## Repository

https://github.com/shubhamjain8750-hash/DMCS-Transaminase-Furfural-Amination
