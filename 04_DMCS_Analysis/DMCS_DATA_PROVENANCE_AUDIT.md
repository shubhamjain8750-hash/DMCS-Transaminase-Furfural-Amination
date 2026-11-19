# DMCS 15-System Data Provenance and Validation

## Scope

This audit covers the 15 retained systems. Excluded systems: **A0A1V0DD42** and **A0A2L2XFE1**. The lead selected for experimental follow-up remains **ATA117-Rd11**.

This document distinguishes arithmetic reproducibility of the committed scoring table from raw-data provenance of every descriptor. It does not claim that every value has been independently re-extracted from the selected 500 ns folders.

## Locked scoring definition

Outer component weights: Dcat = 0.40; Drig = 0.25; Dconf = 0.15; Dene = 0.20.

Catalytic subweights: catalytic-residue–PLP = 0.50; PLP–furfural (UNL) = 0.25; PLP–isopropylamine (UNI) = 0.25.

The current S2 implementation uses inverse min–max normalization for distances and RMSF; positive min–max normalization of ln(largest-cluster fraction); and positive min–max normalization of the absolute magnitude of signed GB binding free energy. DMCS = 0.40 Dcat + 0.25 Drig + 0.15 Dconf + 0.20 Dene.

The framework is descriptor-based normalization and ranking, **not a trained predictive machine-learning model**. Do not mix it with legacy scripts using a different five-term formula.

## Fifteen-system panel

ATA117-Rd11; A0A2G0CFH8; Lys-W-TA; AspC; AptA; H-188; G-188; F-188; AB-R-ATA; A0A1B728H4; A0A1Z5HPJ6; S-omega-TA; S-188; CV-TAm; W-188.

## Validation findings

### RMSF provenance

- ATA117-Rd11 selected rerun: six reported active-site residues (106, 115, 142, 188, 231, 249); mean = 1.476733 Å. Preserve the exact selection and source output. This residue mask must not be transferred unchanged to homologs.
- A0A2G0CFH8: previously reported 18-residue mean = 1.0853167 Å; verify the raw output and selection.
- Lys-W-TA: only one residue (136) was represented in the available RMSF summary (0.7051 Å). Treat as invalid/incomplete until the active-site residue set is reviewed.
- AspC: previously reported mean = 1.5606727 Å; verify raw selection and output.
- AptA: previously reported mean = 1.8177636 Å; verify raw selection and output.
- S-omega-TA: a previously described selection included residues 460–462 despite a reported protein length of 459; inspect topology numbering and repair the selection before accepting the value.
- H-188, G-188, F-188, AB-R-ATA, A0A1B728H4, A0A1Z5HPJ6, S-188, CV-TAm and W-188: current manifest values are historical inputs without verified raw RMSF selection/output provenance in the reviewed inventory.

Define active-site residues independently for each enzyme using structural alignment and catalytic-pocket context. Record exact residue IDs and atom selection. Do not copy ATA117-Rd11 residue numbering blindly.

### MM/GBSA provenance

Use the first generalized-Born (GB) DELTA TOTAL for the furfural-containing complex. Do not use the subsequent PB DELTA TOTAL row. Store signed GB ΔG in the manifest; S2 uses its absolute magnitude only for energetic normalization.

Selected ATA117-Rd11 rerun: GB ΔG = -12.4786 kcal/mol. The older rd11-500nss value (-12.8665) belongs to an obsolete run and must not be substituted.

Reported first-GB values for H-188, G-188, F-188, S-188 and W-188 are -2.3593, -4.4999, -2.9229, -1.4231 and -3.9323 kcal/mol, respectively. Verify against each corresponding final MMPBSA output before final freeze. Other system values remain marked unverified pending output-file inspection.

### Distance and clustering

S1 calculates the arithmetic mean of the second numeric column in each CPPTRAJ distance file. Confirm that each file contains time/frame followed by distance in Å and that atom selections refer to the corresponding chemical entities consistently.

The cluster parser selects the row with the maximum frame count, not simply the first row. For ATA117-Rd11 selected rerun, the largest cluster has 32,452 frames and fraction 0.649. Confirm consistent production-window and frame-sampling definitions across all systems.

## Current ranking: arithmetic versus provenance

The committed DMCS_RESULTS.csv, DMCS_STANDARDIZED.csv and DMCS_Final_Ranking.csv encode a ranking with ATA117-Rd11 at 0.9063. This score is arithmetically consistent with the committed raw descriptor table and current S2 formula.

Arithmetic reproducibility is not equivalent to raw-data provenance. Several RMSF entries remain unverified or incomplete, and multiple MM/GBSA values still require raw-output verification. Label this ranking **provisional pending descriptor provenance audit** until the outstanding checks are closed. Do not mix the 0.9063 15-system score with the earlier 0.8394 score from a previous DMCS version/run.

## Selected analysis folders

| System | Folder |
|---|---|
| ATA117-Rd11 | ATA-117-rd11_rerun_500ns |
| A0A2G0CFH8 | A0A2G0CFH8-500ns |
| Lys-W-TA | Lys-W-TA-500ns |
| AspC | AspC-500ns |
| AptA | AptA500ns |
| H-188 | H-188-500ns |
| G-188 | G-188-500ns |
| F-188 | F-188-500ns |
| AB-R-ATA | AB-R-ATA |
| A0A1B728H4 | A0A1B728H4-500ns |
| A0A1Z5HPJ6 | A0A1Z5HPJ6-500ns |
| S-omega-TA | S-omega-TA-500ns |
| S-188 | S-188-500ns |
| CV-TAm | CV-tam |
| W-188 | W-188-500ns |

Do not upload large NetCDF trajectories or bulky topology/coordinate files. Version compact analysis inputs, outputs, scripts, manifests and provenance records. Document external storage and checksums separately where needed.

## Reproducibility closure checklist

- [ ] Confirm the 15 folder names and selected production trajectories.
- [ ] Preserve per-system CPPTRAJ distance inputs and outputs.
- [ ] Verify catalytic residue identity, topology numbering and atom selections.
- [ ] Recompute/verify system-specific active-site RMSF using structurally mapped pocket residues; preserve masks and raw output.
- [ ] Verify the first GB DELTA TOTAL for every UNL-containing complex and retain signed values/units.
- [ ] Verify largest-cluster frame count and fraction against each cluster summary.
- [ ] Regenerate S1, S2 and S3 from the verified manifest.
- [ ] Confirm the 15-system set and document any score/rank changes.
- [ ] Freeze manuscript-reported scores only after all checks are complete.

## Provenance status vocabulary

- VERIFIED: source file, residue/atom selection and extraction have been checked.
- PROVISIONAL_REQUIRES_RAW_FILE_RECHECK: calculation description is known, but source needs reconfirmation.
- UNVERIFIED_HISTORICAL_VALUE: carried forward from an earlier script/table; raw provenance is not established.
- INVALID_SELECTION_REVIEW_REQUIRED: selection is incomplete or residue numbering is suspect; do not use in final scoring before correction.
- UNVERIFIED_IN_CURRENT_CONTEXT: raw output has not been checked in this audit.