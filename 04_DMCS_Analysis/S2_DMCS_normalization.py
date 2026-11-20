#!/usr/bin/env python3
"""S2: Normalize the S1 raw descriptor table and calculate the composite DMCS."""
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
INPUT=HERE/"DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv"
OUTPUT=HERE/"DMCS_STANDARDIZED.csv"
EXPECTED={
 "ATA117-Rd11","A0A2G0CFH8","Lys-W-TA","AspC","AptA",
 "H-188","G-188","F-188","AB-R-ATA","A0A1B728H4",
 "A0A1Z5HPJ6","S-omega-TA","S-188","CV-TAm","W-188"
}
REQUIRED=[
 "Enzyme","CatalyticResidue_PLP_mean_A","PLP_UNL_mean_A","PLP_UNI_mean_A",
 "Active_Site_RMSF_Mean_A","Active_Site_RMSF_N","Largest_Cluster_Fraction",
 "GB_Delta_Total_kcal_mol"
]

def minmax(s,name):
 lo,hi=float(s.min()),float(s.max())
 if np.isclose(lo,hi):
  raise ValueError(f"{name}: min-max normalization is undefined for constant values")
 return (s-lo)/(hi-lo)

def main():
 d=pd.read_csv(INPUT)
 missing=set(REQUIRED)-set(d.columns)
 if missing: raise ValueError(f"Raw descriptor table missing columns: {sorted(missing)}")
 d["Enzyme"]=d["Enzyme"].astype(str).str.strip()
 if len(d)!=15 or d["Enzyme"].duplicated().any() or set(d["Enzyme"])!=EXPECTED:
  raise ValueError("Raw descriptor table must contain exactly the 15 defined systems")
 for c in REQUIRED[1:]: d[c]=pd.to_numeric(d[c],errors="raise")
 if not np.isfinite(d[REQUIRED[1:]].to_numpy(float)).all():
  raise ValueError("Non-finite descriptor detected")
 if (d["Active_Site_RMSF_Mean_A"]<0).any() or (d["Active_Site_RMSF_N"]<1).any():
  raise ValueError("Invalid pocket RMSF descriptor or pocket residue count")
 if (d["Largest_Cluster_Fraction"]<=0).any() or (d["Largest_Cluster_Fraction"]>1).any():
  raise ValueError("Dominant-cluster fractions must be in (0,1]")

 x=d.copy()
 x["Dcat_CatalyticResidue_PLP"]=1-minmax(x["CatalyticResidue_PLP_mean_A"],"catalytic residue–PLP")
 x["Dcat_PLP_UNL"]=1-minmax(x["PLP_UNL_mean_A"],"PLP–furfural")
 x["Dcat_PLP_UNI"]=1-minmax(x["PLP_UNI_mean_A"],"PLP–IPA")
 x["Dcat"]=.50*x["Dcat_CatalyticResidue_PLP"]+.25*x["Dcat_PLP_UNL"]+.25*x["Dcat_PLP_UNI"]
 x["Drig"]=1-minmax(x["Active_Site_RMSF_Mean_A"],"5 Å catalytic-pocket Cα RMSF")
 x["Dconf"]=minmax(np.log(x["Largest_Cluster_Fraction"]),"log dominant-cluster fraction")
 x["Dene"]=minmax(x["GB_Delta_Total_kcal_mol"].abs(),"absolute GB ΔG")
 x["DMCS"]=.40*x["Dcat"]+.25*x["Drig"]+.15*x["Dconf"]+.20*x["Dene"]
 x=x.sort_values("DMCS",ascending=False).reset_index(drop=True)
 x.insert(0,"Rank",np.arange(1,len(x)+1))
 cols=["Rank","Enzyme","CatalyticResidue_PLP_mean_A","PLP_UNL_mean_A","PLP_UNI_mean_A",
       "Active_Site_RMSF_Mean_A","Active_Site_RMSF_N","Largest_Cluster_Fraction",
       "GB_Delta_Total_kcal_mol","Dcat","Drig","Dconf","Dene","DMCS"]
 x[cols].to_csv(OUTPUT,index=False,float_format="%.9f")
 print(x[["Rank","Enzyme","Active_Site_RMSF_Mean_A","Dcat","Drig","Dconf","Dene","DMCS"]].to_string(index=False))

if __name__=="__main__": main()
