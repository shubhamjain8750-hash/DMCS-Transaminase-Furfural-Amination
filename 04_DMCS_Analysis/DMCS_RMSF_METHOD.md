# Harmonized catalytic-pocket RMSF method

## Purpose

This document defines the RMSF-based rigidity descriptor (Drig) used in the canonical 15-system DMCS comparison. The method avoids mixing RMSF outputs generated from different selections and defines the catalytic pocket separately for every enzyme from its own prepared complex.

## Common RMSF source

The common source is `rmsf_protein_calpha.dat` in each of the 15 system folders. It is a protein-only, per-residue Cα RMSF profile. The corresponding CPPTRAJ workflow images the trajectory, centers the protein, fits the protein backbone to a reference structure and then calculates residue-wise Cα fluctuations.

Representative command sequence (N is the system-specific protein residue endpoint):

    trajin md1.nc 1 last 10
    autoimage
    center :1-N mass origin
    reference md1.rst7 parm solv_complexN.prmtop
    rms reference :1-N@CA,C,N
    atomicfluct out rmsf_protein_calpha.dat :1-N@CA byres

The public example input uses a 330-residue mask and must be adapted for systems with different residue counts. The explicit backbone RMS fit precedes `atomicfluct`; `atomicfluct` itself does not perform this fit.

The production settings `dt=0.002 ps`, `nstlim=250000000` and `ntwx=5000` correspond to 500 ns and 50,000 saved frames when the completed trajectory is written. The RMSF input samples every tenth saved frame.

## Structure-derived catalytic pocket

The prepared structures contain PLP (`UNP`), furfural (`UNL`) and IPA (`UNI`). For each system independently:

1. Retain protein atoms and heavy atoms of UNP, UNL and UNI; exclude H and D.
2. For every protein residue R, calculate the minimum distance between any protein heavy atom in R and any heavy atom in the combined UNP/UNL/UNI set: `d(R) = min ||x_i - x_j||`.
3. Select residues satisfying `d(R) <= 5.0 Å`.
4. Map each selected residue's Cα RMSF from `rmsf_protein_calpha.dat` using its original residue number.
5. Calculate the arithmetic mean: `RMSF_pocket = (1/N) * sum(RMSF_CA,R)`.

The 5.0 Å cutoff is the canonical definition. No fixed residue-number mask is transferred between enzymes. The full residue-level map is `DMCS_ACTIVE_SITE_RESIDUES.csv`.

## Cutoff sensitivity

The pocket is also recalculated at 4.0 and 6.0 Å. System-specific residue counts, pocket means, component scores, composite scores and ranks are provided in `DMCS_RMSF_CUTOFF_SENSITIVITY.csv`. The 5.0 Å value remains the canonical analysis.

## Other descriptors and score

The three distance descriptors are means of their CPPTRAJ distance time series. Each series contains 50,000 frames in the inspected source data. Conformational persistence is the fraction of frames in the largest cluster (selected by maximum frame count). The first `DELTA TOTAL` value in the UNL-containing MMPBSA report is used as the GB result; the second is PB. Signed GB ΔG is retained in the raw data, while its absolute magnitude is used for Dene.

    DMCS = 0.40*Dcat + 0.25*Drig + 0.15*Dconf + 0.20*Dene
    Dcat = 0.50*Dcat(catalytic residue–PLP)
         + 0.25*Dcat(PLP–furfural)
         + 0.25*Dcat(PLP–IPA)

Distances and RMSF are inverse min–max normalized; log cluster fraction and absolute GB ΔG are positive min–max normalized over the 15-system panel.

## Interpretation

Lower pocket RMSF contributes a higher Drig component after inverse scaling. The mean summarizes positional fluctuation for the defined residues; it does not by itself prove catalytic competence or a specific chemical mechanism. Drig is interpreted as one component of the composite score.
