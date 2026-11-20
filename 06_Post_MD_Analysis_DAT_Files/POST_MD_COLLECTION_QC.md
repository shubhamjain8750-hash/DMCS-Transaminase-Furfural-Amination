# Post-MD collection — quality-control record

## First-pass collection

- Systems scanned: 15 of 15
- DAT files collected: 690
- Numeric CSV conversions: 585
- Original-copy checksum verification: 690 of 690 passed
- Missing copied DAT files: 0
- SHA256 mismatches: 0
- Duplicate SHA256 groups: 0
- Files with irregular/skipped numeric lines: 0

## Classification issue identified

The first-pass classifier included 45 files named `FINAL_RESULTS_UNI_MMPBSA.dat`, `FINAL_RESULTS_UNL_MMPBSA.dat` and `FINAL_RESULTS_UNP_MMPBSA.dat` under the SASA category. These are MMPBSA energy summaries, not solvent-accessible surface area time-series outputs. The first-pass collection must not be used as the final post-MD dataset.

A corrected collector has been prepared to exclude any MMPBSA/MMGBSA report before category assignment.

## Expected corrected inventory

| Category | Expected DAT files |
|---|---:|
| RMSD | 165 |
| Rg | 150 |
| SASA | 150 |
| Hydrogen bonds | 180 |
| **Total** | **645** |

Expected numeric CSV exports: 585. Sixty hydrogen-bond average files were not tabular numeric series in the first-pass conversion and should remain as source DAT files without a CSV export.

## Release gate

This quality-control record documents the first-pass audit, not a completed corrected collection. Before release:

1. Run the corrected collector across the same 15 source directories.
2. Confirm all 645 DAT files have matching source SHA256 values.
3. Confirm the inventory counts and review any deviations from the expected counts above.
4. Confirm no MMPBSA/MMGBSA summaries appear in the SASA category.
5. Confirm the generated CSV conversions and manifest paths resolve.
6. Only then publish the corrected data folder and change the repository status to completed.

No experimental HPLC/chromatogram data or supplementary figures are part of this public repository collection.
