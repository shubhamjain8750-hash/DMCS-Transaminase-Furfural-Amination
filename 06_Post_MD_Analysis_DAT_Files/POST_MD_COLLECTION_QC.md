# Post-MD collection — quality-control record

## First-pass collection and correction

The first-pass collector found 690 DAT files across 15 systems and verified the copied files by SHA256. During classification review, 45 `FINAL_RESULTS_*_MMPBSA.dat` energy-summary reports were found under the SASA category. These are MM/GBSA/PB summary reports, not SASA time-series outputs. The first-pass collection was therefore rejected.

The corrected collector explicitly excludes MMPBSA/MMGBSA reports before category assignment.

## Corrected collection inventory

| Category | DAT files |
|---|---:|
| RMSD | 165 |
| Rg | 150 |
| SASA | 150 |
| Hydrogen bonds | 180 |
| **Total** | **645** |

The 645 files comprise 585 per-frame numeric time-series files and 60 hydrogen-bond average-summary text files. Numeric CSV conversions: 585. The 60 non-tabular `*_avg.dat` outputs are preserved as DAT without a CSV counterpart.

## Final file-integrity and classification audit

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
| Numeric CSV conversions generated | 585 |
| Missing converted CSV files | 0 |
| Overall collection audit | **PASS** |

The copied DAT files were byte-for-byte verified against their source files using SHA256. The manifest and inventory are deposited beside this report.

## Time-axis representation

The ordinary time-series files use frame indices. The files under `ns_files/` use an explicit time-in-nanoseconds x-axis and are alternative representations of corresponding series, not independent trajectories or replicates. The deposited series have 5,000 rows; the production control writes frames every 10 ps and the supplied analysis templates read every tenth saved frame, corresponding to 0.1 ns sampling. Check the system-specific input/log before assigning these example settings universally.

## Scope and limitations of this audit

This audit establishes collection integrity, source-copy identity and exclusion of the identified MMPBSA/MMGBSA classification error. It does **not** independently verify that all 15 systems used identical atom masks, RMSD alignment references, Rg/SASA atom selections, hydrogen-bond donor/acceptor selections, geometric cutoffs, equilibration windows or trajectory preprocessing. The supplied CPPTRAJ templates are examples with system-specific masks, not universal validated protocols.

Accordingly, the files are archived as per-system outputs. Do not infer cross-system methodological equivalence from the uniform file counts, successful checksums or matching row counts. The time-series data are not additional DMCS descriptors and were not used to calculate the canonical DMCS scores.

No experimental HPLC/chromatogram data or supplementary figures are included in this public repository dataset.

## Repository record

The corrected collection (DAT files, CSV exports, manifest, inventory and this QC record) is committed to the public `main` branch in commit [945ba04](https://github.com/shubhamjain8750-hash/DMCS-Transaminase-Furfural-Amination/commit/945ba04b48d8dca2afc46b4604a927e625d8776e).
