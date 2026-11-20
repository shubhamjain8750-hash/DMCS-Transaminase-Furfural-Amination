# 03 — Molecular-dynamics inputs and structures

## Purpose

This directory contains AMBER input examples defining minimization, heating, density/equilibration and production stages, together with CPPTRAJ analysis templates and the 15-system PDB structure collection.

## Input-file inventory

| File | Role |
|---|---|
| `min1.in` | Initial restrained energy minimization |
| `heat.in` | Explicit-solvent heating; supplied input ramps the temperature from 10 K to 300 K |
| `density.in` | Density/NPT equilibration stage |
| `equi1.in`, `equi2.in` | Subsequent equilibration stages |
| `md1.in` | Production MD control parameters |
| `mmpbsa.in` | GB/PB MM/GBSA calculation controls |
| `cpptraj.in` | Example RMSD, RMSF and hydrogen-bond analysis commands |
| `cpptraj_rg_sasa.in` | Example radius-of-gyration and SASA analysis commands |

## Production simulation settings

The supplied `md1.in` specifies a 2 fs time step (`dt=0.002 ps`) and 250,000,000 steps, corresponding to 500 ns. Coordinates are written every 5,000 steps (10 ps), giving 50,000 saved production frames when the complete run finishes. The input is restart-based (`irest=1`, `ntx=5`) and requires matching AMBER restart and topology files.

The MD setup documented for the study uses the protein ff19SB force field, GAFF2 for parameterized ligands and explicit TIP3P water. The complete system-specific topology and parameter files are not included here.

## Important: templates are not universal masks

The supplied CPPTRAJ and several AMBER input examples contain residue masks for a 330-residue protein and component labels `UNI`, `UNL` and `UNP`. The 15 enzyme systems do not all have the same protein length or residue numbering. **Do not run these example files unchanged for every system.** Inspect the relevant topology/PDB, update protein and ligand masks, confirm residue identifiers and use the matching restart and topology files.

The production input assumes that preceding preparation/equilibration stages have generated the restart files it reads. A PDB coordinate snapshot is not a replacement for an AMBER topology or restart.

## Structure collection

`15_Enzyme_MD_Complex_Structures/` contains 30 PDB files (two per system): the prepared unsolvated enzyme–PLP–furfural–IPA complex and the corresponding solvated stage-2 equilibration snapshot. The manifest records file provenance, size and SHA256 checksums. Original source directory and file spellings are retained for traceability.

## Analysis-output availability

The public DAT archive in `04_DMCS_Analysis/15_Enzyme_Analysis_DAT_Files/` includes RMSF, distance, clustering and MMPBSA outputs where collected. The CPPTRAJ files here are analysis **inputs**. The public package does not currently include result DAT files for a complete RMSD, Rg, SASA or hydrogen-bond analysis. See the DAT archive README for the deposited output inventory.

## Not deposited

Production trajectories, binary AMBER restart files, complete topology/parameter sets and complete per-enzyme docking preparation packages are not included. The repository supports inspection of the deposited structures, analysis inputs and processed DMCS data, but does not by itself provide every binary input required to restart or rerun each MD trajectory.
