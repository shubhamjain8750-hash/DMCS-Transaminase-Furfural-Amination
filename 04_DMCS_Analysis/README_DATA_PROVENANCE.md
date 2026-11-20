# Input manifest provenance fields

The five original S1 input fields define the required data contract. The manifest also records:

- `RMSF_Status`: provenance status of the active-site RMSF value.
- `MMGBSA_Status`: provenance status of the signed GB binding free energy.
- `Notes`: supporting explanation and residue-selection information.

`VERIFIED` means that the source output and extraction calculation are present and checked. `UNVERIFIED_HISTORICAL_VALUE` means that a value was retained from an earlier analysis but its active-site residue selection is not present in the collected input bundle. `SINGLE_RESIDUE_ONLY_REQUIRES_REVIEW` flags an RMSF output containing a single residue, rather than a multi-residue active-site mean.

The MMPBSA value in the manifest is the signed first GB `DELTA TOTAL` from the UNL-containing complex output. The subsequent PB row is not used for DMCS energetic normalization.

See `DMCS_DATA_PROVENANCE_AUDIT.md` and `DMCS_15_SYSTEMS_INPUTS_AND_PROTOCOLS.md` for system-specific evidence and input files.
