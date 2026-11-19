
# 03 - Molecular Dynamics Inputs

## Overview

This directory contains the molecular dynamics preparation workflows, simulation parameters and associated input files used in the computational evaluation of PLP-dependent transaminases.

## Molecular Dynamics Methodology

Molecular dynamics simulations were performed using AMBER24.

The computational systems were prepared using:

- Protein force field: ff19SB
- Ligand force field: GAFF2
- Explicit solvent: TIP3P water
- Simulation ensemble: NPT
- Temperature: 300 K
- Integration time step: 2 fs
- Production simulation duration: 500 ns

## Expected Files

- Initial protein and ligand structures.
- Molecular system preparation scripts.
- tleap input files.
- Ligand parameter and topology files.
- Energy minimization input files.
- Heating and equilibration input files.
- Production MD input files.
- MM/GBSA calculation parameters.

## Reproducibility

The directory is intended to provide the necessary simulation preparation files and computational parameters for reconstructing the molecular dynamics systems described in the manuscript.

Large production trajectories and trajectory output files are not included.

## Associated Manuscript Sections

- Section 2.4: Molecular Dynamics Simulations
- Section 2.5: MM/GBSA Binding Energy Calculations
- Supporting Information: Method 1 and Workflows 1-3
