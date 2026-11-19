
# 04 - Dynamic Mechanistic Conformation Scoring (DMCS) Analysis

## Overview

This directory contains the computational implementation of the Dynamic Mechanistic Conformation Scoring (DMCS) framework developed for the prioritization of PLP-dependent transaminases.

## DMCS Descriptors

The framework integrates four trajectory-derived descriptors:

1. Catalytic Readiness (Dcat)
2. Active-Site Rigidity (Drig)
3. Conformational Persistence (Dconf)
4. Energetic Stabilization (Dene)

## Computational Workflows

### Workflow 1: Descriptor Extraction

Extraction of trajectory-derived catalytic distances, active-site RMSF, conformational cluster occupancy and MM/GBSA energetic contributions.

### Workflow 2: Descriptor Normalization and Scoring

Normalization of individual descriptors and calculation of the composite DMCS score using the predefined weighting scheme:

DMCS = 0.40(Dcat) + 0.25(Drig) + 0.15(Dconf) + 0.20(Dene)

### Workflow 3: Ranking and Visualization

Generation of normalized descriptor tables, comparative enzyme rankings and datasets for visualization.

## Expected Files

- S1_descriptor_extraction.py
- S2_DMCS_normalization.py
- S3_DMCS_ranking.py
- DMCS_raw_descriptors.csv
- DMCS_standardized.csv
- DMCS_final_ranking.csv
- active_site_residues.csv

## Reproducibility

The scripts and machine-readable datasets will provide the computational implementation and data required to reproduce the DMCS calculations and comparative enzyme prioritization.

## Associated Manuscript Sections

- Section 2.6: Dynamic Mechanistic Conformation Scoring
- Supporting Information: Methods 1-3 and Workflows 1-3
