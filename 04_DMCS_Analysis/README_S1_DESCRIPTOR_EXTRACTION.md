## S1: Raw descriptor compilation

Use `S1_INPUTS_TEMPLATE.csv` to create `S1_INPUTS.csv` with one row per
retained enzyme. Supply the enzyme ID, its output directory, its own
previously determined active-site RMSF, and its furfural (UNL) MM/GBSA
binding energy in kcal/mol.

Each output directory must contain:
- `lys_plp.dat`
- `plp_unl.dat`
- `plp_uni.dat`
- `dmcs_cluster_summary.dat`

Run `python S1_descriptor_extraction.py`. The script calculates the mean
of the second column in each distance file, reads the largest-cluster
fraction from the first non-comment row of the cluster summary, and writes
`DMCS_RESULTS.csv` for S2.

**Historical-method limitation:** The recovered `dmcs_HOMO1_v2.py` hardcoded
RMSF and MM/GBSA values. Accordingly, S1 reads these two values from the
per-enzyme input table; it does not calculate them. Never copy one enzyme's
RMSF or MM/GBSA value to other systems. S1 does not launch CPPTRAJ or
perform MM/GBSA calculations.

The script requires exactly 15 retained systems and excludes
`A0A1V0DD42` and `A0A2L2XFE1`.
