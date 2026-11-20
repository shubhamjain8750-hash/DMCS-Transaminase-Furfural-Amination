# Post-MD collection — quality-control record

## First-pass collection and issue

The first-pass classifier collected 690 DAT files across 15 systems and successfully verified their copies by SHA256. However, 45 `FINAL_RESULTS_*_MMPBSA.dat` energy-summary reports were incorrectly assigned to the SASA category. MMPBSA/MMGBSA summary reports are not SASA time-series outputs; the first-pass collection was rejected for publication.

The corrected collector explicitly excludes MMPBSA/MMGBSA reports before category assignment.

## Corrected collection inventory

| Category | DAT files |
|---|---:|
| RMSD | 165 |
| Rg | 150 |
| SASA | 150 |
| Hydrogen bonds | 180 |
| **Total** | **645** |

Numeric CSV conversions: 585. Sixty DAT outputs were not suitable for numeric-table CSV conversion and were retained as original DAT files.

## Final audit results

The corrected collection was scanned across all 15 specified enzyme directories. The final audit returned:

| Check | Result |
|---|---:|
| Systems found | 15/15 |
| DAT files collected | 645 |
| Source/copy SHA256 matches | 645/645 |
| Missing DAT copies | 0 |
| SHA256 mismatches | 0 |
| Duplicate checksum groups | 0 |
| Files with irregular/skipped numeric rows | 0 |
| MMPBSA/MMGBSA reports included | 0 |
| CSV conversions generated | 585 |
| Missing converted CSV files | 0 |
| Overall collection audit | **PASS** |

The copied DAT files were byte-for-byte verified against their source files using SHA256. No missing files, checksum mismatches, duplicate-content groups, irregular numeric rows or energy-summary reports were reported.

## Scope and limitations

This audit establishes collection integrity, source-copy identity and exclusion of the known MMPBSA/MMGBSA classification error. It does not independently validate that atom selections, reference structures, surface definitions, donor/acceptor selections, hydrogen-bond geometric cutoffs, sampling intervals and equilibration windows were identical across all systems. These methodological conditions must be confirmed before interpreting the files as directly comparable quantitative measurements.

No experimental HPLC/chromatogram data or supplementary figures are included in this public repository dataset.

## Release status

The corrected data collection passed its computational-server audit. The generated data files still need to be transferred into this repository and committed. The audit should be retained alongside the final manifest and per-system inventory.
