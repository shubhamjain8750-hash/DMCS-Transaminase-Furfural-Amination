#!/usr/bin/env python3
"""S2: Normalize S1 descriptors using the locked DMCS component weights."""
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
INPUT=HERE/"DMCS_RESULTS.csv"
OUTPUT=HERE/"DMCS_STANDARDIZED.csv"
EXPECTED={
 "ATA117-Rd11","A0A2G0CFH8","Lys-W-TA","AspC","AptA",
 "H-188","G-188","F-188","AB-R-ATA","A0A1B728H4",
 "A0A1Z5HPJ6","S-omega-TA","S-188","CV-TAm","W-188"
}
REQUIRED=["Enzyme","Lys_PLP","PLP_UNL","PLP_UNI","RMSF","ClusterFraction","MMGBSA"]

def minmax(s,name):
 lo,hi=float(s.min()),float(s.max())
 if np.isclose(lo,hi):
  raise ValueError(f"{name}: min-max normalization is undefined for a constant descriptor")
 return (s-lo)/(hi-lo)

def main():
 df=pd.read_csv(INPUT)
 missing=set(REQUIRED)-set(df.columns)
 if missing: raise ValueError(f"DMCS_RESULTS.csv missing columns: {sorted(missing)}")
 df["Enzyme"]=df["Enzyme"].astype(str).str.strip()
 if len(df)!=15 or df["Enzyme"].duplicated().any() or set(df["Enzyme"])!=EXPECTED:
  raise ValueError("DMCS_RESULTS.csv must contain exactly the 15 defined enzyme systems")
 for c in REQUIRED[1:]: df[c]=pd.to_numeric(df[c],errors="raise")
 if not np.isfinite(df[REQUIRED[1:]].to_numpy(float)).all():
  raise ValueError("Non-finite descriptor value found")
 if (df["RMSF"]<0).any() or (df["ClusterFraction"]<=0).any() or (df["ClusterFraction"]>1).any():
  raise ValueError("Invalid RMSF or dominant-cluster fraction")
 x=df.copy()
 x["Dcat_CatalyticResidue_PLP"]=1-minmax(x["Lys_PLP"],"catalytic residue–PLP")
 x["Dcat_PLP_UNL"]=1-minmax(x["PLP_UNL"],"PLP–furfural")
 x["Dcat_PLP_UNI"]=1-minmax(x["PLP_UNI"],"PLP–IPA")
 x["Dcat"]=.50*x["Dcat_CatalyticResidue_PLP"]+.25*x["Dcat_PLP_UNL"]+.25*x["Dcat_PLP_UNI"]
 x["Drig"]=1-minmax(x["RMSF"],"5 Å catalytic-pocket Cα RMSF")
 x["Dconf"]=minmax(np.log(x["ClusterFraction"]),"log dominant-cluster fraction")
 x["Dene"]=minmax(x["MMGBSA"].abs(),"absolute GB ΔG")
 x["DMCS"]=.40*x["Dcat"]+.25*x["Drig"]+.15*x["Dconf"]+.20*x["Dene"]
 x=x.sort_values("DMCS",ascending=False).reset_index(drop=True)
 x.insert(0,"Rank",np.arange(1,len(x)+1))
 cols=["Rank","Enzyme","Lys_PLP","PLP_UNL","PLP_UNI","RMSF","ClusterFraction","MMGBSA",
       "Dcat_CatalyticResidue_PLP","Dcat_PLP_UNL","Dcat_PLP_UNI","Dcat","Drig","Dconf","Dene","DMCS"]
 x[cols].to_csv(OUTPUT,index=False,float_format="%.9f")
 print(x[["Rank","Enzyme","RMSF","Dcat","Drig","Dconf","Dene","DMCS"]].to_string(index=False))

if __name__=="__main__": main()
