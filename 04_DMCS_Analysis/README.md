# 04 – Dynamic Mechanistic Conformation Scoring (DMCS) Analysis

## 1. Overview

This directory contains the computational implementation of the Dynamic Mechanistic Conformation Scoring (DMCS) framework developed for the comparative evaluation and prioritization of PLP-dependent transaminases involved in the conversion of biomass-derived furfural to furfurylamine.

The DMCS workflow integrates molecular dynamics-derived catalytic, conformational, and energetic descriptors into a composite scoring framework. The analysis was applied to 15 selected transaminase systems to facilitate their comparative evaluation and prioritization.

The computational workflow is organized into three sequential stages:

1. **S1 – Raw descriptor extraction and compilation**
2. **S2 – Descriptor normalization and DMCS calculation**
3. **S3 – Final ranking and comparative summary generation**

Each stage is implemented independently to maintain a transparent and traceable analysis workflow.

---

## 2. Repository Contents

| File | Description |
|---|---|
| `S1_INPUTS.csv` | Input manifest containing enzyme identifiers, analysis directories, catalytic distance filenames, RMSF values, and MM/GBSA values |
| `S1_descriptor_extraction.py` | Compiles raw descriptors from the individual enzyme analysis directories |
| `README_S1_DESCRIPTOR_EXTRACTION.md` | Detailed description of the S1 extraction methodology |
| `DMCS_RESULTS.csv` | Compiled raw descriptor dataset used as input for S2 |
| `DMCS_Descriptor_Summary.csv` | Descriptive summary of the raw DMCS descriptors |
| `S2_DMCS_normalization.py` | Performs descriptor normalization and calculates the composite DMCS score |
| `DMCS_STANDARDIZED.csv` | Contains normalized descriptor components and calculated DMCS scores |
| `S3_DMCS_ranking.py` | Generates the final comparative ranking |
| `DMCS_Final_Ranking.csv` | Final ranked output for the 15 enzyme systems |

---

## 3. Computational Workflow

### S1. Raw Descriptor Extraction and Compilation

The first stage compiles molecular dynamics-derived descriptors and previously calculated energy and flexibility measurements into a unified dataset.

The extraction workflow uses:

- Production molecular dynamics trajectories and their corresponding Amber topology files.
- CPPTRAJ-generated catalytic residue–PLP, PLP–furfural, and PLP–IPA distance time series.
- CPPTRAJ conformational clustering summaries.
- Previously calculated active-site RMSF values.
- Amber MM/GBSA generalized Born binding free-energy results.

The `S1_INPUTS.csv` file specifies the analysis directory and the appropriate catalytic residue–PLP distance filename for each enzyme system.

System-specific catalytic residue assignments are accommodated through the `CatalyticDistanceFile` field. This allows the same extraction workflow to process canonical Lys-containing systems and systems containing substitutions at the corresponding catalytic position.

The S1 script calculates mean distance descriptors, identifies the largest cluster from the cluster summary, and incorporates the supplied RMSF and MM/GBSA values.

The resulting dataset is saved as:

`DMCS_RESULTS.csv`

A detailed description of the extraction procedure is available in `README_S1_DESCRIPTOR_EXTRACTION.md`.

### S2. Descriptor Normalization and DMCS Calculation

The second stage performs min–max normalization of the raw descriptors and calculates the four component scores.

The analysis considers four descriptor categories:

| Component | Description | Weight |
|---|---|---:|
| Dcat | Catalytic readiness | 0.40 |
| Drig | Active-site rigidity | 0.25 |
| Dconf | Conformational persistence | 0.15 |
| Dene | Energetic stabilization | 0.20 |

The catalytic readiness component integrates three distance descriptors:

| Descriptor | Description | Subweight |
|---|---|---:|
| Lys_PLP | Catalytic residue–PLP distance | 0.50 |
| PLP_UNL | PLP–furfural distance | 0.25 |
| PLP_UNI | PLP–isopropylamine distance | 0.25 |

The existing `Lys_PLP` column name is retained for compatibility with the scoring implementation. For catalytic-residue substitution systems, the corresponding substituted residue–PLP distance is used.

The component scores are calculated as follows.

**Catalytic readiness:**

\[
D_{\mathrm{cat}} =
0.50N_{\mathrm{Lys-PLP}}+
0.25N_{\mathrm{PLP-UNL}}+
0.25N_{\mathrm{PLP-UNI}}
\]

**Active-site rigidity:**

\[
D_{\mathrm{rig}}=1-N_{\mathrm{RMSF}}
\]

**Conformational persistence:**

\[
D_{\mathrm{conf}}=
N_{\ln(\mathrm{ClusterFraction})}
\]

**Energetic stabilization:**

\[
D_{\mathrm{ene}}=
N_{|\Delta G_{\mathrm{GB}}|}
\]

Here, \(N\) denotes min–max normalization across the 15 enzyme systems. Distance and RMSF descriptors are inversely normalized, whereas cluster persistence and the absolute magnitude of the GB binding free energy are positively normalized.

The composite DMCS score is calculated using:

\[
\boxed{
DMCS =
0.40D_{\mathrm{cat}}+
0.25D_{\mathrm{rig}}+
0.15D_{\mathrm{conf}}+
0.20D_{\mathrm{ene}}
}
\]

The normalized descriptor dataset and component scores are saved as:

`DMCS_STANDARDIZED.csv`

### S3. Final Ranking and Comparative Analysis

The third stage ranks the enzyme systems in descending order of their calculated DMCS scores.

The script reads `DMCS_STANDARDIZED.csv`, validates the enzyme identifiers and numerical values, and generates the final comparative ranking.

The output is saved as:

`DMCS_Final_Ranking.csv`

The final ranking provides the relative prioritization of the 15 evaluated enzyme systems based on their composite DMCS scores.

---

## 4. Execution Instructions

### Software requirements

The descriptor compilation and scoring scripts require:

- Python 3
- NumPy
- pandas

Install the Python dependencies using:

```bash
pip install numpy pandas
```

CPPTRAJ and Amber MMPBSA are used in the upstream trajectory and energy-analysis workflows. They are not invoked directly by the S2 or S3 scoring scripts.

### Running the workflow

Execute the scripts from this directory in the following order:

**Step 1 – Raw descriptor compilation**

```bash
python S1_descriptor_extraction.py
```

Input:
- `S1_INPUTS.csv`
- Corresponding per-enzyme analysis directories and required CPPTRAJ output files.

Output:
- `DMCS_RESULTS.csv`

**Step 2 – Descriptor normalization and DMCS calculation**

```bash
python S2_DMCS_normalization.py
```

Input:
- `DMCS_RESULTS.csv`

Output:
- `DMCS_STANDARDIZED.csv`

**Step 3 – Final ranking**

```bash
python S3_DMCS_ranking.py
```

Input:
- `DMCS_STANDARDIZED.csv`

Output:
- `DMCS_Final_Ranking.csv`

The S2 and S3 scripts validate the expected number of retained systems, enzyme identifiers, duplicate entries, and numerical descriptor values before generating their respective outputs.

---

## 5. Analysis Set and Data Integrity

The final comparative analysis contains 15 enzyme systems.

The S2 and S3 scripts enforce the expected system count and check for duplicate enzyme identifiers and invalid numerical values.

The raw descriptor dataset, normalized dataset, and final ranking are maintained as separate outputs to preserve traceability between the input measurements and the final composite scores.

The existing scoring implementation and descriptor weights are retained consistently across the normalization and ranking stages.

---

## 6. Final DMCS Ranking

The final analysis identifies ATA117-Rd11 as the top-ranked transaminase among the 15 evaluated systems.

| Rank | Enzyme | DMCS |
|---:|---|---:|
| 1 | ATA117-Rd11 | 0.9063 |
| 2 | A0A2G0CFH8 | 0.8531 |
| 3 | Lys-W-TA | 0.6291 |
| 4 | AspC | 0.5955 |
| 5 | AptA | 0.5800 |
| 6 | H-188 | 0.4556 |
| 7 | G-188 | 0.4292 |
| 8 | F-188 | 0.4250 |
| 9 | AB-R-ATA | 0.3974 |
| 10 | A0A1B728H4 | 0.3863 |
| 11 | A0A1Z5HPJ6 | 0.3821 |
| 12 | S-omega-TA | 0.3562 |
| 13 | S-188 | 0.3091 |
| 14 | CV-TAm | 0.2248 |
| 15 | W-188 | 0.1651 |

ATA117-Rd11 was therefore prioritized for subsequent experimental evaluation based on its integrated catalytic, structural, conformational, and energetic descriptor profile.

---

## 7. Reproducibility and Methodological Scope

The DMCS implementation separates raw descriptor compilation, descriptor normalization, and final ranking into independent computational stages.

The scripts are provided to facilitate inspection and reproduction of the data-processing and scoring workflow.

For independent reproduction of the complete analysis, the following upstream materials should also be retained and made available where applicable:

- Corresponding production molecular dynamics trajectories and Amber topology files.
- CPPTRAJ input files and distance-analysis outputs.
- Clustering input files and cluster summary outputs.
- Active-site RMSF analysis inputs and results.
- Amber MMPBSA input files and corresponding energy output files.
- The input manifest specifying the analysis directories and descriptor values.

The S1 script compiles existing analysis outputs and previously calculated descriptors; it does not independently regenerate the molecular dynamics trajectories, RMSF calculations, or MM/GBSA calculations.

The DMCS framework described here is a descriptor-based normalization and ranking approach. It does not involve training a predictive machine-learning model.

The separation of extraction, normalization, and ranking is intended to provide a transparent and reproducible computational workflow for comparative transaminase prioritization.
