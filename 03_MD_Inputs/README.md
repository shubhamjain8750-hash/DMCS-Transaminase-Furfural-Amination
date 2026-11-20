# 03 — Molecular-dynamics inputs and structures

## Purpose

This directory contains AMBER control-file examples for minimization, heating, equilibration and production MD; CPPTRAJ analysis templates; and the prepared PDB structure collection for the 15-system comparison.

## Input-file inventory

| File | Role |
|---|---|
| `min1.in` | Initial restrained energy minimization example |
| `heat.in` | Explicit-solvent heating example; ramps from 10 K to 300 K |
| `density.in` | Density/NPT equilibration example |
| `equi1.in`, `equi2.in` | Subsequent equilibration examples |
| `md1.in` | 500 ns production control example |
| `mmpbsa.in` | GB/PB MM/GBSA calculation controls |
| `cpptraj.in` | Example RMSD, RMSF and hydrogen-bond analysis commands |
| `cpptraj_rg_sasa.in` | Example radius-of-gyration and SASA analysis commands |

## Production simulation settings

The supplied `md1.in` specifies a 2 fs time step (`dt=0.002 ps`) and 250,000,000 steps, corresponding to 500 ns. Coordinates are written every 5,000 steps (10 ps), giving 50,000 saved coordinate frames for a completed trajectory. The input is restart-based (`irest=1`, `ntx=5`) and requires matching system-specific AMBER restart and topology files.

The documented setup uses protein ff19SB, GAFF2 for parameterized ligands and explicit TIP3P water. The system-specific topology, parameter and trajectory files are not bundled here.

## CPPTRAJ templates: examples, not universal protocols

The supplied `cpptraj.in` and `cpptraj_rg_sasa.in` are example inputs. They contain a 1–330 protein-residue mask and component residue names UNI, UNL and UNP. The first file is labelled for a Lys188-mutant validation workflow; the Rg/SASA file is labelled for a CV-TAm validation workflow. Enzyme length, numbering, topology masks and ligand residue identifiers differ across the panel. **Do not run either template unchanged for every enzyme.** Check each system's topology and PDB and adapt the masks before analysis.

The example hydrogen-bond commands use a 3.5 Å distance criterion and 120° angle criterion. These values describe the supplied example template; they should not be assumed to prove that every archived system-specific output was generated with identical selections unless the corresponding per-system input/log is available.

The example CPPTRAJ files use `trajin md1.nc 1 last 10`, i.e. every tenth saved coordinate frame. With the production output interval above, this corresponds to a 0.1 ns sampling interval and 5,000 analysis points over 500 ns. The deposited `*_ns` files in directory 06 express the x-axis in ns; corresponding frame-indexed files are also retained. These are alternate time-axis representations, not independent replicas.

## Structure collection

`15_Enzyme_MD_Complex_Structures/` contains 30 PDB files (two per system): the prepared unsolvated enzyme–PLP–furfural–IPA complex and the corresponding solvated stage-2 equilibration coordinate snapshot. The structure manifest records source filename, size, atom/residue and component counts, and SHA256. Original source folder and filename spellings are retained for traceability.

A solvated stage-2 PDB is a coordinate snapshot for inspection. It is **not** a substitute for the binary AMBER production restart or topology.

## Analysis-output availability

Two separate data locations must be distinguished:

1. `04_DMCS_Analysis/15_Enzyme_Analysis_DAT_Files/` contains the selected source DAT files used for the canonical DMCS descriptor workflow, including distance, RMSF, clustering and MMPBSA outputs where collected.
2. [`06_Post_MD_Analysis_DAT_Files/`](../06_Post_MD_Analysis_DAT_Files/README.md) contains the additional per-system RMSD, Rg, SASA and hydrogen-bond output series (645 original DAT files and 585 numeric CSV conversions across 15 systems).

The directory 06 is an ancillary output archive, not an additional DMCS scoring module. Its files have passed source-copy and classification checks, but those checks do not establish cross-system methodological equivalence. The `*_ns` variants provide an ns time axis for the corresponding frame-indexed series; they must not be counted as independent simulation runs. Hydrogen-bond `*_avg.dat` files are CPPTRAJ text summaries and are retained as DAT without numeric CSV conversion.

## Not deposited

Production trajectories, binary AMBER restart files, complete system-specific topology/parameter sets and complete per-enzyme docking preparation packages are not included. The repository supports inspection of deposited structures, templates, selected source outputs and processed DMCS data, but it does not by itself provide every binary input required to restart or rerun MD.
