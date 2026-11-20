# 02 — Sequential molecular docking

## Objective

Molecular docking was used as a staged computational filter to compare PLP-dependent transaminases for assembly of a plausible catalytic complex containing PLP, furfural and isopropylamine (IPA).

## Sequential workflow

1. **PLP placement:** dock pyridoxal-5′-phosphate (PLP) into the enzyme active site.
2. **Furfural placement:** retain the PLP-containing assembly and dock furfural.
3. **IPA placement:** retain the PLP–furfural assembly and dock isopropylamine.

The staged score columns are reported in the CSV tables in [01_Enzyme_Screening](../01_Enzyme_Screening/README.md). The sequence is intended to assess whether the required components can be accommodated in a comparable active-site arrangement.

## Software and interpretation

AutoDock Vina was used for docking. The reported docking scores are scoring-function estimates for comparative screening only. They should not be equated with experimental binding free energies, turnover rates or catalytic efficiencies. Docking alone does not establish a productive catalytic geometry or reaction mechanism; downstream MD and DMCS descriptors provide additional dynamic and mechanistic context.

## Data availability and reproducibility boundary

The public repository includes machine-readable screening score tables in `01_Enzyme_Screening/` and MD starting structures in `03_MD_Inputs/15_Enzyme_MD_Complex_Structures/`. It does **not** currently include the complete per-enzyme docking package (prepared receptor/ligand PDBQT files, all Vina configuration files, search-box coordinates and pose files). The score tables can be inspected, but docking calculations cannot be independently rerun from this directory alone.

Do not infer missing search-box coordinates, exhaustiveness settings or pose-selection rules from the score tables. For exact reproduction, use the parameter values and preparation details stated in the final manuscript/Supporting Information and retain the original configuration files as a separate archive.
