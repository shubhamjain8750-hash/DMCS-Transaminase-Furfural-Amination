# Source-data package map and provenance

The repository contains three distinct source-data collections. They serve different purposes and must not be conflated.

| Repository path | Contents | Manifest / documentation |
|---|---|---|
| `03_MD_Inputs/15_Enzyme_MD_Complex_Structures/` | Two PDB structures per system: prepared unsolvated ternary complex and solvated stage-2 coordinate snapshot | `PDB_STRUCTURE_MANIFEST.csv` |
| `04_DMCS_Analysis/15_Enzyme_Analysis_DAT_Files/` | Selected original DAT outputs used for canonical DMCS descriptor provenance: distance, RMSF, clustering and MMPBSA records where present | `DAT_FILE_MANIFEST.csv` |
| `06_Post_MD_Analysis_DAT_Files/` | Ancillary post-production RMSD, Rg, SASA and hydrogen-bond series collected from the 15 system folders; includes original DAT and numeric CSV representations | `POST_MD_DAT_MANIFEST.csv`, `POST_MD_SYSTEM_INVENTORY.csv`, `POST_MD_COLLECTION_QC.md` |

The source folder basenames are deliberately preserved for traceability. Enzyme labels used in the canonical DMCS data tables may use normalized display names; see `04_DMCS_Analysis/S1_INPUTS.csv` for the mapping between display label and original source analysis directory.

The PDB and DAT collections are selected source outputs, not full backups of the MD work directories. Production trajectories, binary restart/topology files and complete per-enzyme docking preparation packages are not included.

## Scope distinction

The directory 04 source DAT collection supplies input provenance for the deposited DMCS descriptors. The directory 06 post-MD archive is supplementary to that calculation: its RMSD, Rg, SASA and hydrogen-bond series are not inputs to the current DMCS equation or ranking. The 06 archive passed file-integrity and classification checks; its audit does not, by itself, demonstrate that all system-specific selections and analysis parameters were methodologically identical.
