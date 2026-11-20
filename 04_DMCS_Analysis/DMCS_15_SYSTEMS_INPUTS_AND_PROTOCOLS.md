# 15-system input and protocol manifest

## Enzyme/source mapping

The following table is the authoritative mapping used by S1. Directory names are the original source-folder basenames and are preserved for traceability.

| DMCS enzyme label | Original source directory | Catalytic residue | Catalytic-distance output |
|---|---|---|---|
| ATA117-Rd11 | `ATA-117-rd11_rerun_500ns` | Lys188 | `lys_plp.dat` |
| A0A2G0CFH8 | `A0A2G0CFH8-500ns` | Lys240 | `lys_plp.dat` |
| Lys-W-TA | `Lys-W-TA-500ns` | Lys136 | `lys_plp.dat` |
| AspC | `AspC-500ns` | Lys234 | `lys_plp.dat` |
| AptA | `AptA500ns` | Lys281 | `lys_plp.dat` |
| H-188 | `H-188-500ns` | His188 | `his_plp.dat` |
| G-188 | `G-188-500ns` | Gly188 | `gly_plp.dat` |
| F-188 | `F-188-500ns` | Phe188 | `phe_plp.dat` |
| AB-R-ATA | `AB-R-ATA` | Lys180 | `lys_plp.dat` |
| A0A1B728H4 | `A0A1B728H4-500ns` | Lys147 | `lys_plp.dat` |
| A0A1Z5HPJ6 | `A0A1Z5HPJ6-500ns` | Lys140 | `lys_plp.dat` |
| S-omega-TA | `S-omega-TA-500ns` | Lys288 | `lys_plp.dat` |
| S-188 | `S-188-500ns` | Ser188 | `ser_plp.dat` |
| CV-TAm | `CV-tam` | Lys288 | `lys_plp.dat` |
| W-188 | `W-188-500ns` | Trp188 | `trp_plp.dat` |

The machine-readable equivalent is `S1_INPUTS.csv`.

## MD production settings

The supplied `03_MD_Inputs/md1.in` uses a 2 fs integration step and 250,000,000 steps (500 ns). Coordinates are written every 5,000 steps (10 ps), equivalent to 50,000 saved frames over a completed 500 ns production run. The input is restart-based and requires the system-specific preceding restart and topology.

## Common descriptor inputs

| Input | Purpose |
|---|---|
| `complexN.pdb` | Prepared ternary structure for structure-derived pocket selection |
| `cpptraj.in` | Protein alignment and Cα RMSF calculation protocol |
| `md1.in` | Production MD settings |
| `mmpbsa.in` | MM/GBSA calculation settings |
| `rmsf_protein_calpha.dat` | Common protein-only per-residue Cα RMSF source |
| Catalytic-distance file from mapping table | Catalytic residue–PLP distance series |
| `plp_unl.dat` | PLP–furfural distance series |
| `plp_uni.dat` | PLP–IPA distance series |
| `dmcs_cluster_summary.dat` | Cluster identifiers and frame counts |
| `FINAL_RESULTS_UNL_MMPBSA.dat` | GB/PB energy summary |

## Data availability note

The public repository contains the mapping, selected PDB structures, collected DAT outputs and harmonized descriptor tables. It does not contain all original per-system analysis directories, trajectories or binary AMBER restart/topology files. This manifest defines the input contract for full S1 re-extraction; it does not imply that every required S1 source file is present in the public repository.
