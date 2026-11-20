# 01 — Enzyme screening datasets

## Purpose

This directory contains machine-readable CSV transcriptions of the screening tables in the study's Supporting Information. The tables document the candidate panel and staged computational selection workflow before the 15-system MD/DMCS comparison.

## Files

| File | Contents |
|---|---|
| `Table_S1_Initial_Enzyme_Screening.csv` | Initial 22-enzyme screening panel and sequential docking scores |
| `Table_S2_Homolog_Screening.csv` | Ten homologous candidates, sequence similarity relative to ATA117-Rd11 and sequential docking scores |
| `Table_S3_Benchmark_Enzymes.csv` | Benchmark results for AB-R-ATA and CV-TAm |
| `Table_S4_Lys188_Variants.csv` | Ten Lys188 substitution variants and sequential docking scores |

## Column interpretation

The staged score columns represent the docking score after addition of the indicated component: protein + PLP; PLP + furfural; and PLP + furfural + isopropylamine (IPA). Values are docking scores in kcal/mol as reported in the Supporting Information; they are not experimental binding free energies, catalytic rates or direct measures of enzyme activity.

The homolog table additionally reports sequence similarity to ATA117-Rd11. Similarity values are percentages and should be interpreted alongside, not as a replacement for, structural and functional evaluation.

## Data handling and scope

The CSV files preserve the reported numerical values and candidate identities while using machine-readable column headings. For formal interpretation, the manuscript and original Supporting Information remain authoritative.

This directory contains the screening tables, not a full docking project archive. Prepared receptor/ligand PDBQT files, all Vina configuration files, search-box coordinates and docking pose files are not deposited here. The staged protocol is described in [02_Docking](../02_Docking/README.md).
