# Input manifest provenance fields

The original five columns are the S1 input contract. Additional documentary columns in S1_INPUTS.csv are ignored by the current extraction script:

- RMSF_Status
- MMGBSA_Status
- Notes

Do not change a status to VERIFIED until the corresponding raw source file, residue/atom selection and extraction calculation have been checked. RMSF must represent a structurally mapped active-site residue set, not an arbitrary single residue or a mask copied from ATA117-Rd11. MMGBSA must be the signed first GB DELTA TOTAL for the UNL-containing complex, not the PB row.

See DMCS_DATA_PROVENANCE_AUDIT.md for system-by-system limitations and the closure checklist.