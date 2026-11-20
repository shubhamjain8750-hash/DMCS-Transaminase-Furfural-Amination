# 06 — Ancillary post-MD analysis output archive

## Purpose and relationship to DMCS

This directory archives per-system post-production molecular-dynamics analysis outputs collected from the 15-enzyme panel. It is a source-output archive, not a harmonized comparative analysis and not an extension of the current DMCS equation.

The canonical DMCS score is calculated only from Dcat, Drig, Dconf and Dene as defined in `../04_DMCS_Analysis/`. The RMSD, Rg, SASA and hydrogen-bond series in this directory were **not used as inputs to the deposited DMCS score or ranking**. They must not be described as additional DMCS descriptors or as evidence that the ranking was independently validated by these analyses.

## Deposited inventory

| Category | DAT files | Description |
|---|---:|---|
| RMSD | 165 | Protein, complex and component-specific RMSD series |
| Radius of gyration (Rg) | 150 | Protein, complex and component-containing Rg series |
| SASA | 150 | Protein, complex and component-containing surface-area series |
| Hydrogen bonds | 180 | Per-frame hydrogen-bond series and CPPTRAJ average-summary reports |
| **Total** | **645** | **15 systems** |

There are 585 numeric CSV exports. The repository contains 587 CSV files in this directory when the manifest and per-system inventory are included. Sixty hydrogen-bond `*_avg.dat` files are text-formatted CPPTRAJ summary reports rather than numeric time-series tables; they are retained in original DAT form and have no CSV counterpart.

## Time axis and duplicate representations

The ordinary files use a frame-index x-axis. The corresponding files under `ns_files/` use an explicit time-in-nanoseconds x-axis. Inspection of the series and manifest shows 5,000 data rows per time-series file; the supplied production input writes coordinates every 10 ps and the example CPPTRAJ analysis reads every tenth saved frame, corresponding to a 0.1 ns interval over a 500 ns run.

The `*_ns` files are alternate time-axis representations of corresponding series, not separate simulation replicas or independent data. Do not pool both representations as independent observations or count them as replicate trajectories. Use one representation consistently and retain its units.

## File categories and interpretation

- **RMSD:** the source files distinguish protein Cα, complete complex, individual ligand/cofactor and combined ligand selections where available. RMSD depends on the alignment/reference and atom mask.
- **Rg:** the source files distinguish protein, full assembly and protein-plus-one-component masks where available. Rg values depend on the atom selection.
- **SASA:** the source files distinguish protein, full assembly and protein-plus-one-component masks where available. SASA values depend on the atom selection and surface calculation settings.
- **Hydrogen bonds:** the time-series files report per-frame counts for UNI, UNL, UNP and the complete assembly where available. The `*_avg.dat` files are separate CPPTRAJ text summaries, not per-frame occupancy time series.

MMPBSA/MMGBSA energy-summary reports are excluded from this directory. They belong to the selected source DAT archive in `../04_DMCS_Analysis/15_Enzyme_Analysis_DAT_Files/` and are handled separately in the canonical energetic descriptor workflow.

## Provenance and integrity files

- `POST_MD_DAT_MANIFEST.csv` records the source directory/path, category, copied path, file size, SHA256, CSV path and conversion status for each DAT file.
- `POST_MD_SYSTEM_INVENTORY.csv` gives per-system counts by category.
- `POST_MD_COLLECTION_QC.md` records the first-pass classification issue and the corrected final audit.

The corrected collection contains 645 DAT files from 15 systems. The audit reported 645/645 source-copy SHA256 matches, zero missing copies, zero mismatches, zero repeated checksum groups, zero irregular/skipped numeric rows, zero MMPBSA/MMGBSA reports in the collection, 585 generated numeric CSV exports and zero missing converted CSV files.

## Methodological limits — read before comparing systems

The supplied CPPTRAJ templates in `03_MD_Inputs/` are examples, not proof that identical settings were used for every deposited per-system series. For example, the RMSD/hydrogen-bond template and the Rg/SASA template contain a 330-residue protein mask and are labelled for specific validation workflows. The mask and residue/component selections must be checked against each system's topology and original analysis input.

The example hydrogen-bond commands use a 3.5 Å distance criterion and 120° angle criterion. Do not attribute those settings to all 15 systems unless the corresponding per-system inputs/logs verify them. Similarly, confirm RMSD alignment/reference, Rg/SASA masks, trajectory window, frame stride and any time-axis conversion before performing quantitative cross-system comparison.

The collection QC establishes file provenance, source-copy identity and exclusion of the known MMPBSA/SASA classification error. It does **not** establish methodological equivalence, validate the scientific interpretation of every trajectory, or provide statistical replicates.

## Reproduction boundary

The original production trajectories, binary AMBER restart/topology files and full per-system analysis directories are not included. Therefore, the archived series can be inspected and re-plotted, but the complete original calculations cannot be regenerated from this directory alone. Consult the manifest and preserve the original source and unit conventions when using any series.
