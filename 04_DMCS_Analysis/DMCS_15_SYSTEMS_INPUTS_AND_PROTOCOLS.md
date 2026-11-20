# DMCS 15-System Computational Input Archive

## Scope and provenance

This file consolidates the system-specific computational input files collected from the selected 500 ns analysis folders. It preserves the inputs required to inspect production settings, solvent stripping, catalytic distance definitions, conformational clustering, RMSF selections and MM/GBSA settings.

The associated machine-readable tables are `DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv` and `DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv`.

**Important:** Distance series, cluster summaries and MM/GBSA GB energy values were parsed from the uploaded analysis outputs. RMSF selections are not equally complete across all systems. Where a system has only a whole-protein per-residue RMSF series, a structurally aligned active-site residue mapping must be specified before calculating a comparable active-site rigidity descriptor. The per-residue file is retained so that mapping can be audited.

## Analysis and scoring definitions

- Production MD settings were read from each system's own `md1.in` file.
- Distance descriptors are arithmetic means of the second numeric column in the system-specific CPPTRAJ time series; all three series contain 50,000 frames.
- The largest-cluster fraction is taken from the cluster-summary row with the maximum frame count.
- MM/GBSA uses the first `DELTA TOTAL` in the GB section of `FINAL_RESULTS_UNL_MMPBSA.dat`; the PB result is retained separately for traceability and is not used as the DMCS energy descriptor.
- The DMCS component weights are Dcat 0.40, Drig 0.25, Dconf 0.15 and Dene 0.20. Dcat subweights are catalytic-residue–PLP 0.50, PLP–furfural 0.25 and PLP–IPA 0.25.

## System-specific input files

### ATA117-Rd11

Source folder: `ATA-117-rd11_rerun_500ns`

#### Production MD

**md1.in**

```text
# production: lipase, explicit solvent, fixed protonation
&cntrl
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntb=2, ntp=1, pres0=1.0, taup=1.0,
  cut=8.0,
  dt=0.002,
  nstlim=250000000,
  ig=-1,
  ntpr=5000, ntwx=5000, ntwr=5000,
  ioutfm=1,
  iwrap=1,
  igb=0,
  irest=1, ntx=5,
/
```

#### Trajectory preparation

**make_ATA117_nowat.in**

```text
parm solv_complexN.prmtop
trajin md1.nc

autoimage
strip :WAT,Na+,Cl-

trajout ATA117_nowat.nc netcdf

run
```

#### DMCS distance definitions

**dmcs_distances.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin ATA117_nowat.nc

distance lys_plp :188@NZ :333@P  out lys_plp.dat

distance plp_unl :333@C5 :332@C  out plp_unl.dat
distance plp_uni :333@C5 :331@N1 out plp_uni.dat

run
```

#### DMCS clustering definitions

**cluster_dmcs_ATA117.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin ATA117_nowat.nc

rms first :UNP,UNL

cluster hieragglo epsilon 1.2     rms :UNP,UNL     sieve 10 random     out dmcs_clusters.dat     summary dmcs_cluster_summary.dat     repout dmcs_cluster_rep.pdb

run
```

#### Active-site or residue-wise RMSF definitions

**active_site_rmsf.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin ATA117_nowat.nc

rms first :1-330@CA,C,N

atomicfluct out active_site_rmsf.dat :106,115,142,188,231,249@CA byres

run
```

#### MM/GBSA controls

**mmpbsa.in**

```text
&general
  startframe=1,
  endframe=50000,
  interval=200,     
  verbose=1,
  keep_files=0,
  entropy=0,
  netcdf=1,
  use_sander=0,      
/

&gb
  igb=5,
  saltcon=0.150,
/

&pb
  istrng=0.150,
/

&decomp
  idecomp=2,
  dec_verbose=1,
  print_res="1-331",
/
```

**run_mmpbsa_all.sh**

```text
#!/bin/bash

export AMBERHOME=/workspace/amber24
export PYTHONNOUSERSITE=1

echo "===== UNI ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_uni.prmtop -rp solv_receptor.prmtop -lp solv_uni.prmtop -y complex_UNI_nowat.nc -o FINAL_RESULTS_UNI_MMPBSA.dat -do FINAL_DECOMP_UNI_MMPBSA.dat > mmpbsa_uni.log 2>&1

echo "===== UNL ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unl.prmtop -rp solv_receptor.prmtop -lp solv_unl.prmtop -y complex_UNL_nowat.nc -o FINAL_RESULTS_UNL_MMPBSA.dat -do FINAL_DECOMP_UNL_MMPBSA.dat > mmpbsa_unl.log 2>&1

echo "===== UNP ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unp.prmtop -rp solv_receptor.prmtop -lp solv_unp.prmtop -y complex_UNP_nowat.nc -o FINAL_RESULTS_UNP_MMPBSA.dat -do FINAL_DECOMP_UNP_MMPBSA.dat > mmpbsa_unp.log 2>&1

echo "DONE"
```

#### Associated compact outputs

- `lys_plp.dat`
- `lys_plp_rep.dat`
- `plp_uni.dat`
- `plp_uni_rep.dat`
- `plp_unl.dat`
- `plp_unl_rep.dat`
- `dmcs_cluster_summary.dat`
- `dmcs_clusters.dat`
- `active_site_rmsf.dat`
- `rmsf_complex_all_byres.dat`
- `rmsf_ligands_all_byatom.dat`
- `rmsf_protein_calpha.dat`
- `rmsf_uni_byatom.dat`
- `rmsf_unl_byatom.dat`
- `rmsf_unp_byatom.dat`
- `FINAL_RESULTS_UNL_MMPBSA.dat`

### A0A2G0CFH8

Source folder: `A0A2G0CFH8-500ns`

#### Production MD

**md1.in**

```text
# production: lipase, explicit solvent, fixed protonation
&cntrl
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntb=2, ntp=1, pres0=1.0, taup=1.0,
  cut=8.0,
  dt=0.002,
  nstlim=250000000,
  ig=-1,
  ntpr=5000, ntwx=5000, ntwr=5000,
  ioutfm=1,
  iwrap=1,
  igb=0,
  irest=1, ntx=5,
/
```

#### Trajectory preparation

**make_A0A2G0CFH8_nowat.in**

```text
parm solv_complexN.prmtop
trajin md1.nc

autoimage
strip :WAT,Na+,Cl-

trajout A0A2G0CFH8_nowat.nc netcdf

run
```

#### DMCS distance definitions

**dmcs_distances_A0A2G0CFH8.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin A0A2G0CFH8_nowat.nc

distance lys_plp :240@NZ :276@C14 out lys_plp.dat

distance plp_unl :276@C14 :275@C7 out plp_unl.dat

distance plp_uni :276@C14 :274@N1 out plp_uni.dat

run
```

#### DMCS clustering definitions

**cluster_dmcs_A0A2G0CFH8.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin A0A2G0CFH8_nowat.nc

rms first :UNP,UNL

cluster hieragglo epsilon 1.2     rms :UNP,UNL     sieve 10 random     out dmcs_clusters.dat     summary dmcs_cluster_summary.dat     repout dmcs_cluster_rep.pdb

run
```

#### Active-site or residue-wise RMSF definitions

**active_site_rmsf.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin A0A2G0CFH8_nowat.nc

rms first :1-273@CA,C,N

atomicfluct out active_site_rmsf.dat :34,90,114,117,143,147,164,179,180,181,200,201,202,203,236,237,238,240@CA byres

run
```

#### MM/GBSA controls

**mmpbsa.in**

```text
&general
  startframe=1,
  endframe=50000,
  interval=200,     
  verbose=1,
  keep_files=0,
  entropy=0,
  netcdf=1,
  use_sander=0,      
/

&gb
  igb=5,
  saltcon=0.150,
/

&pb
  istrng=0.150,
/

&decomp
  idecomp=2,
  dec_verbose=1,
  print_res="1-274",
/
```

**run_mmpbsa_all.sh**

```text
#!/bin/bash

export AMBERHOME=/workspace/amber24
export PYTHONNOUSERSITE=1

echo "===== UNI ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_uni.prmtop -rp solv_receptor.prmtop -lp solv_uni.prmtop -y complex_UNI_nowat.nc -o FINAL_RESULTS_UNI_MMPBSA.dat -do FINAL_DECOMP_UNI_MMPBSA.dat > mmpbsa_uni.log 2>&1

echo "===== UNL ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unl.prmtop -rp solv_receptor.prmtop -lp solv_unl.prmtop -y complex_UNL_nowat.nc -o FINAL_RESULTS_UNL_MMPBSA.dat -do FINAL_DECOMP_UNL_MMPBSA.dat > mmpbsa_unl.log 2>&1

echo "===== UNP ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unp.prmtop -rp solv_receptor.prmtop -lp solv_unp.prmtop -y complex_UNP_nowat.nc -o FINAL_RESULTS_UNP_MMPBSA.dat -do FINAL_DECOMP_UNP_MMPBSA.dat > mmpbsa_unp.log 2>&1

echo "DONE"
```

#### Associated compact outputs

- `lys_plp.dat`
- `plp_uni.dat`
- `plp_unl.dat`
- `dmcs_cluster_summary.dat`
- `dmcs_clusters.dat`
- `active_site_rmsf.dat`
- `rmsf_complex_all_byres.dat`
- `rmsf_ligands_all_byatom.dat`
- `rmsf_protein_calpha.dat`
- `rmsf_uni_byatom.dat`
- `rmsf_unl_byatom.dat`
- `rmsf_unp_byatom.dat`
- `FINAL_RESULTS_UNL_MMPBSA.dat`

### Lys-W-TA

Source folder: `Lys-W-TA-500ns`

#### Production MD

**md1.in**

```text
# production: lipase, explicit solvent, fixed protonation
&cntrl
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntb=2, ntp=1, pres0=1.0, taup=1.0,
  cut=8.0,
  dt=0.002,
  nstlim=250000000,
  ig=-1,
  ntpr=5000, ntwx=5000, ntwr=5000,
  ioutfm=1,
  iwrap=1,
  igb=0,
  irest=1, ntx=5,
/
```

#### Trajectory preparation

**make_LysWTA_nowat.in**

```text
parm solv_complexN.prmtop
trajin md1.nc

autoimage
strip :WAT,Na+,Cl-

trajout LysWTA_nowat.nc netcdf

run
```

#### DMCS distance definitions

**dmcs_distances.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin LysWTA_nowat.nc

distance lys_plp :136@NZ :418@P out lys_plp.dat
distance plp_unl :418@P  :417@C  out plp_unl.dat
distance plp_uni :418@P  :416@N1 out plp_uni.dat

run
```

#### DMCS clustering definitions

**cluster_dmcs_LysWTA.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin LysWTA_nowat.nc

rms first :UNP,UNL

cluster hieragglo epsilon 1.2     rms :UNP,UNL     sieve 10 random     out dmcs_clusters.dat     summary dmcs_cluster_summary.dat     repout dmcs_cluster_rep.pdb

run
```

#### Active-site or residue-wise RMSF definitions

**active_site_rmsf.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin LysWTA_nowat.nc

rms first :1-415@CA,C,N

atomicfluct out active_site_rmsf.dat :136@CA byres

run
```

#### MM/GBSA controls

**mmpbsa.in**

```text
&general
  startframe=1,
  endframe=50000,
  interval=200,     
  verbose=1,
  keep_files=0,
  entropy=0,
  netcdf=1,
  use_sander=0,      
/

&gb
  igb=5,
  saltcon=0.150,
/

&pb
  istrng=0.150,
/

&decomp
  idecomp=2,
  dec_verbose=1,
  print_res="1-416",
/
```

**run_mmpbsa_all.sh**

```text
#!/bin/bash

export AMBERHOME=/workspace/amber24
export PYTHONNOUSERSITE=1

echo "===== UNI ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_uni.prmtop -rp solv_receptor.prmtop -lp solv_uni.prmtop -y complex_UNI_nowat.nc -o FINAL_RESULTS_UNI_MMPBSA.dat -do FINAL_DECOMP_UNI_MMPBSA.dat > mmpbsa_uni.log 2>&1

echo "===== UNL ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unl.prmtop -rp solv_receptor.prmtop -lp solv_unl.prmtop -y complex_UNL_nowat.nc -o FINAL_RESULTS_UNL_MMPBSA.dat -do FINAL_DECOMP_UNL_MMPBSA.dat > mmpbsa_unl.log 2>&1

echo "===== UNP ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unp.prmtop -rp solv_receptor.prmtop -lp solv_unp.prmtop -y complex_UNP_nowat.nc -o FINAL_RESULTS_UNP_MMPBSA.dat -do FINAL_DECOMP_UNP_MMPBSA.dat > mmpbsa_unp.log 2>&1

echo "DONE"
```

#### Associated compact outputs

- `lys_plp.dat`
- `plp_uni.dat`
- `plp_unl.dat`
- `dmcs_cluster_summary.dat`
- `dmcs_clusters.dat`
- `active_site_rmsf.dat`
- `rmsf_complex_all_byres.dat`
- `rmsf_ligands_all_byatom.dat`
- `rmsf_protein_calpha.dat`
- `rmsf_uni_byatom.dat`
- `rmsf_unl_byatom.dat`
- `rmsf_unp_byatom.dat`
- `FINAL_RESULTS_UNL_MMPBSA.dat`

### AspC

Source folder: `AspC-500ns`

#### Production MD

**md1.in**

```text
# production: lipase, explicit solvent, fixed protonation
&cntrl
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntb=2, ntp=1, pres0=1.0, taup=1.0,
  cut=8.0,
  dt=0.002,
  nstlim=250000000,
  ig=-1,
  ntpr=5000, ntwx=5000, ntwr=5000,
  ioutfm=1,
  iwrap=1,
  igb=0,
  irest=1, ntx=5,
/
```

#### Trajectory preparation

**make_AspC_nowat.in**

```text
parm solv_complexN.prmtop
trajin md1.nc

autoimage
strip :WAT,Na+,Cl-

trajout AspC_nowat.nc netcdf

run
```

#### DMCS distance definitions

**dmcs_distances.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin AspC_nowat.nc

distance lys_plp :234@NZ :380@P  out lys_plp.dat

distance plp_unl :380@C5 :379@C  out plp_unl.dat
distance plp_uni :380@C5 :378@N1 out plp_uni.dat

run
```

#### DMCS clustering definitions

**cluster_dmcs_AspC.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin AspC_nowat.nc

rms first :UNP,UNL

cluster hieragglo epsilon 1.2     rms :UNP,UNL     sieve 10 random     out dmcs_clusters.dat     summary dmcs_cluster_summary.dat     repout dmcs_cluster_rep.pdb

run
```

#### Active-site or residue-wise RMSF definitions

**active_site_rmsf.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin AspC_nowat.nc

rms first :1-377@CA,C,N

atomicfluct out active_site_rmsf.dat :22,57,61,99,146,162,164,234,251,291,294@CA byres

run
```

#### MM/GBSA controls

**mmpbsa.in**

```text
&general
  startframe=1,
  endframe=50000,
  interval=200,     
  verbose=1,
  keep_files=0,
  entropy=0,
  netcdf=1,
  use_sander=0,      
/

&gb
  igb=5,
  saltcon=0.150,
/

&pb
  istrng=0.150,
/

&decomp
  idecomp=2,
  dec_verbose=1,
  print_res="1-378",
/
```

**run_mmpbsa_all.sh**

```text
#!/bin/bash

export AMBERHOME=/workspace/amber24
export PYTHONNOUSERSITE=1

echo "===== UNI ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_uni.prmtop -rp solv_receptor.prmtop -lp solv_uni.prmtop -y complex_UNI_nowat.nc -o FINAL_RESULTS_UNI_MMPBSA.dat -do FINAL_DECOMP_UNI_MMPBSA.dat > mmpbsa_uni.log 2>&1

echo "===== UNL ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unl.prmtop -rp solv_receptor.prmtop -lp solv_unl.prmtop -y complex_UNL_nowat.nc -o FINAL_RESULTS_UNL_MMPBSA.dat -do FINAL_DECOMP_UNL_MMPBSA.dat > mmpbsa_unl.log 2>&1

echo "===== UNP ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unp.prmtop -rp solv_receptor.prmtop -lp solv_unp.prmtop -y complex_UNP_nowat.nc -o FINAL_RESULTS_UNP_MMPBSA.dat -do FINAL_DECOMP_UNP_MMPBSA.dat > mmpbsa_unp.log 2>&1

echo "DONE"
```

#### Associated compact outputs

- `lys_plp.dat`
- `plp_uni.dat`
- `plp_unl.dat`
- `dmcs_cluster_summary.dat`
- `dmcs_clusters.dat`
- `active_site_rmsf.dat`
- `rmsf_complex_all_byres.dat`
- `rmsf_ligands_all_byatom.dat`
- `rmsf_protein_calpha.dat`
- `rmsf_uni_byatom.dat`
- `rmsf_unl_byatom.dat`
- `rmsf_unp_byatom.dat`
- `FINAL_RESULTS_UNL_MMPBSA.dat`

### AptA

Source folder: `AptA500ns`

#### Production MD

**md1.in**

```text
# production: lipase, explicit solvent, fixed protonation
&cntrl
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntb=2, ntp=1, pres0=1.0, taup=1.0,
  cut=8.0,
  dt=0.002,
  nstlim=250000000,
  ig=-1,
  ntpr=5000, ntwx=5000, ntwr=5000,
  ioutfm=1,
  iwrap=1,
  igb=0,
  irest=1, ntx=5,
/
```

#### Trajectory preparation

**make_AptA_nowat.in**

```text
parm solv_complexN.prmtop
trajin md1.nc

autoimage
strip :WAT,Na+,Cl-

trajout AptA_nowat.nc netcdf

run
```

#### DMCS distance definitions

**dmcs_distances.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin AptA_nowat.nc

distance lys_plp :281@NZ :442@P  out lys_plp.dat

distance plp_unl :442@C5 :441@C  out plp_unl.dat
distance plp_uni :442@C5 :440@N1 out plp_uni.dat

run
```

#### DMCS clustering definitions

**cluster_dmcs_AptA.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin AptA_nowat.nc

rms first :UNP,UNL

cluster hieragglo epsilon 1.2     rms :UNP,UNL     sieve 10 random     out dmcs_clusters.dat     summary dmcs_cluster_summary.dat     repout dmcs_cluster_rep.pdb

run
```

#### Active-site or residue-wise RMSF definitions

**active_site_rmsf.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin AptA_nowat.nc

rms first :1-439@CA,C,N

atomicfluct out active_site_rmsf.dat :23,52,53,61,65,160,167,226,227,281,294@CA byres

run
```

#### MM/GBSA controls

**mmpbsa.in**

```text
&general
  startframe=1,
  endframe=50000,
  interval=200,     
  verbose=1,
  keep_files=0,
  entropy=0,
  netcdf=1,
  use_sander=0,      
/

&gb
  igb=5,
  saltcon=0.150,
/

&pb
  istrng=0.150,
/

&decomp
  idecomp=2,
  dec_verbose=1,
  print_res="1-440",
/
```

**run_mmpbsa_all.sh**

```text
#!/bin/bash

export AMBERHOME=/workspace/amber24
export PYTHONNOUSERSITE=1

echo "===== UNI ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_uni.prmtop -rp solv_receptor.prmtop -lp solv_uni.prmtop -y complex_UNI_nowat.nc -o FINAL_RESULTS_UNI_MMPBSA.dat -do FINAL_DECOMP_UNI_MMPBSA.dat > mmpbsa_uni.log 2>&1

echo "===== UNL ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unl.prmtop -rp solv_receptor.prmtop -lp solv_unl.prmtop -y complex_UNL_nowat.nc -o FINAL_RESULTS_UNL_MMPBSA.dat -do FINAL_DECOMP_UNL_MMPBSA.dat > mmpbsa_unl.log 2>&1

echo "===== UNP ====="
python $AMBERHOME/bin/MMPBSA.py -O -i mmpbsa.in -cp solv_complex_unp.prmtop -rp solv_receptor.prmtop -lp solv_unp.prmtop -y complex_UNP_nowat.nc -o FINAL_RESULTS_UNP_MMPBSA.dat -do FINAL_DECOMP_UNP_MMPBSA.dat > mmpbsa_unp.log 2>&1

echo "DONE"
```

#### Associated compact outputs

- `lys_plp.dat`
- `plp_uni.dat`
- `plp_unl.dat`
- `dmcs_cluster_summary.dat`
- `dmcs_clusters.dat`
- `active_site_rmsf.dat`
- `rmsf_complex_all_byres.dat`
- `rmsf_ligands_all_byatom.dat`
- `rmsf_protein_calpha.dat`
- `rmsf_uni_byatom.dat`
- `rmsf_unl_byatom.dat`
- `rmsf_unp_byatom.dat`
- `FINAL_RESULTS_UNL_MMPBSA.dat`

### H-188

Source folder: `H-188-500ns`

#### Production MD

**md1.in**

```text
# production: lipase, explicit solvent, fixed protonation
&cntrl
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntb=2, ntp=1, pres0=1.0, taup=1.0,
  cut=8.0,
  dt=0.002,
  nstlim=250000000,
  ig=-1,
  ntpr=5000, ntwx=5000, ntwr=5000,
  ioutfm=1,
  iwrap=1,
  igb=0,
  irest=1, ntx=5,
/
```

#### DMCS distance definitions

**dmcs_distances.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin H188_nowat.nc

distance lys_plp :188@NE2 :333@C4 out lys_plp.dat
distance plp_unl :333@C4 :332@C4 out plp_unl.dat
distance plp_uni :333@C4 :331@N1 out plp_uni.dat

run
```

**dmcs_distances_H188.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin H188_nowat.nc

# H188 ↔ PLP
distance his_plp :188@NE2 :333@C4 out lys_plp.dat

# PLP ↔ furfural
distance plp_unl :333@C4 :332@C4 out plp_unl.dat

# PLP ↔ IPA
distance plp_uni :333@C4 :331@N1 out plp_uni.dat

run
```

**dmcs_distances_v2.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin H188_nowat.nc

# Catalytic Histidine → PLP
distance his_plp :188@NE2 :333@C4 out his_plp.dat

# PLP → Furfural
distance plp_unl :333@C4 :332@C4 out plp_unl.dat

# PLP → Isopropylamine
distance plp_uni :333@C4 :331@N1 out plp_uni.dat

run
```

#### DMCS clustering definitions

**cluster_dmcs_v2.in**

```text
parm solv_complexN_md_no_water.prmtop
trajin H188_nowat.nc

rms first :UNP,UNL

cluster hieragglo epsilon 1.2 \
    rms :UNP,UNL \
    sieve 10 random \
    out dmcs_clusters.dat \
    summary dmcs_cluster_summary.dat \
    repout dmcs_cluster_rep.pdb

run
```

#### Active-site or residue-wise RMSF definitions

**rmsf_byres.in**

```text
trajin md1_nowat.nc
atomicfluct RMSFbyres :1-999@CA byres out rmsf_byres_clean.dat
run
```

#### MM/GBSA controls

**mmpbsa.in**

```text
&general
  startframe=1,
  endframe=50000,
  interval=200,
  verbose=1,
  keep_files=0,
  entropy=0,
  netcdf=1,
  use_sander=0,
/

&gb
  igb=5,
  saltcon=0.150,
/

&pb
  istrng=0.150,
/

&decomp
  idecomp=2,
  dec_verbose=1,
  print_res="1-331",
/
```

**run_mmpbsa_all.sh**

```text
#!/bin/bash

export AMBERHOME=/workspace/amber24

echo "===== UNI ====="

python $AMBERHOME/bin/MMPBSA.py -O \
-i mmpbsa.in \
-cp solv_complex_uni.prmtop \
-rp solv_receptor.prmtop \
-lp solv_uni.prmtop \
-y complex_UNI_nowat.nc \
-o FINAL_RESULTS_UNI_MMPBSA.dat \
-do FINAL_DECOMP_UNI_MMPBSA.dat \
> mmpbsa_uni.log 2>&1

echo "===== UNL ====="

python $AMBERHOME/bin/MMPBSA.py -O \
-i mmpbsa.in \
-cp solv_complex_unl.prmtop \
-rp solv_receptor.prmtop \
-lp solv_unl.prmtop \
-y complex_UNL_nowat.nc \
-o FINAL_RESULTS_UNL_MMPBSA.dat \
-do FINAL_DECOMP_UNL_MMPBSA.dat \
> mmpbsa_unl.log 2>&1

echo "===== UNP ====="

python $AMBERHOME/bin/MMPBSA.py -O \
-i mmpbsa.in \
-cp solv_complex_unp.prmtop \
-rp solv_receptor.prmtop \
-lp solv_unp.prmtop \
-y complex_UNP_nowat.nc \
-o FINAL_RESULTS_UNP_MMPBSA.dat \
-do FINAL_DECOMP_UNP_MMPBSA.dat \
> mmpbsa_unp.log 2>&1

echo "DONE"
```

#### Associated compact outputs

- `his_plp.dat`
- `plp_uni.dat`
- `plp_unl.dat`
- `dmcs_cluster_summary.dat`
- `dmcs_clusters.dat`
- `rmsf_byres_clean.dat`
- `rmsf_complex_all_byres.dat`
- `rmsf_ligands_all_byatom.dat`
- `rmsf_protein_calpha.dat`
- `rmsf_uni_byatom.dat`