
# 02 - Molecular Docking

## Overview

This directory contains the molecular docking workflows and associated datasets used for computational screening of PLP-dependent enzymes for furfural amination.

## Sequential Docking Protocol

A sequential docking strategy was employed to construct comparable catalytic assemblies across the selected enzyme systems.

The workflow involved:

1. Docking pyridoxal-5'-phosphate (PLP) into the predicted active site.
2. Docking furfural into the PLP-containing enzyme complex.
3. Docking isopropylamine (IPA) into the resulting assembly.

## Docking Software

- AutoDock Vina

## Docking Parameters

- Exhaustiveness: 8
- Grid dimensions: To be documented from the original configuration files.
- Grid centre: To be documented from the original configuration files.

## Expected Files

- Docking score datasets in CSV format.
- Prepared receptor structures.
- Prepared ligand structures.
- Docking configuration files.
- Representative docking poses.
- Supporting preparation scripts.

## Associated Manuscript Sections

- Section 2.2: Ligand and Protein Preparation
- Section 2.3: Docking Protocol
- Supporting Information: Tables S1-S4
