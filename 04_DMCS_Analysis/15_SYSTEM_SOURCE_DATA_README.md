# Source-data package map and provenance

Two original-source collections are deposited in the repository:

| Repository path | Contents | Manifest |
|---|---|---|
| `03_MD_Inputs/15_Enzyme_MD_Complex_Structures/` | Two PDB structures per system: prepared unsolvated ternary complex and solvated stage-2 coordinate snapshot | `PDB_STRUCTURE_MANIFEST.csv` |
| `04_DMCS_Analysis/15_Enzyme_Analysis_DAT_Files/` | Original collected numerical DAT outputs, grouped by original source analysis-folder basename | `DAT_FILE_MANIFEST.csv` |

The source folder basenames are deliberately preserved for traceability. Enzyme labels used in the canonical DMCS data tables may use normalized display names; see `S1_INPUTS.csv` for the mapping between display label and original source analysis directory.

The PDB and DAT collections are selected source outputs, not full backups of the MD work directories. Production trajectories, binary restart/topology files and complete per-enzyme docking preparation packages are not included.
