# 05 — Computational environment

## Software used

| Software | Role | Repository availability |
|---|---|---|
| AMBER24 | System preparation and molecular-dynamics calculations | Input examples are provided; AMBER executables and binary topology/restart files are not bundled |
| CPPTRAJ | Trajectory imaging, alignment, RMSF and other trajectory analyses | Analysis input examples are provided |
| AutoDock Vina | Sequential docking | Score tables are supplied; complete receptor/ligand preparation and pose/configuration sets are not bundled |
| Python | Descriptor extraction, normalization, validation and ranking | S1–S3 scripts are provided |
| NumPy and pandas | Numerical and tabular processing | Dependencies are listed in `04_DMCS_Analysis/requirements.txt` |

## Python setup

From the repository root:

    python -m pip install -r 04_DMCS_Analysis/requirements.txt

The dependency file specifies NumPy below version 2 and pandas. The repository does not currently pin a complete operating-system image, compiler stack, GPU driver, CUDA toolkit or exact versions of every third-party program. Researchers should record their installed versions when reproducing calculations.

## Hardware and trajectory execution

GPU models, driver versions and cluster-specific modules depend on the execution environment and are not encoded as universal requirements by the input files. The supplied `md1.in` defines simulation controls but does not provide the corresponding AMBER executable, topology, restart or production trajectory.

## Reproducibility recommendation

For independent reproduction, archive exact AMBER/CPPTRAJ build information, docking version, Python/NumPy/pandas versions, hardware/driver details, system-specific topology and restart files, random seeds and full execution logs alongside the analysis outputs.
