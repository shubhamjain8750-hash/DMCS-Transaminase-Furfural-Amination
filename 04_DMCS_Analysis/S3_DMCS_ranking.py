#!/usr/bin/env python3
"""S3: Validate and export the complete 15-system DMCS ranking."""
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
INPUT=HERE/"DMCS_STANDARDIZED.csv"
OUTPUT=HERE/"DMCS_Final_Ranking.csv"
EXPECTED={
 "ATA117-Rd11","A0A2G0CFH8","Lys-W-TA","AspC","AptA",
 "H-188","G-188","F-188","AB-R-ATA","A0A1B728H4",
 "A0A1Z5HPJ6","S-omega-TA","S-188","CV-TAm","W-188"
}
REQUIRED=["Enzyme","Dcat","Drig","Dconf","Dene","DMCS"]

def main():
 d=pd.read_csv(INPUT)
 missing=set(REQUIRED)-set(d.columns)
 if missing: raise ValueError(f"DMCS_STANDARDIZED.csv missing columns: {sorted(missing)}")
 d["Enzyme"]=d["Enzyme"].astype(str).str.strip()
 if len(d)!=15 or d["Enzyme"].duplicated().any() or set(d["Enzyme"])!=EXPECTED:
  raise ValueError("Standardized table must contain exactly the 15 defined systems")
 for c in REQUIRED[1:]: d[c]=pd.to_numeric(d[c],errors="raise")
 if not np.isfinite(d[REQUIRED[1:]].to_numpy(float)).all():
  raise ValueError("Non-finite score found")
 for c in REQUIRED[1:]:
  if ((d[c]<0)|(d[c]>1)).any(): raise ValueError(f"{c} must be in [0,1]")
 d=d.sort_values("DMCS",ascending=False).reset_index(drop=True)
 d.insert(0,"Rank",np.arange(1,len(d)+1))
 d[["Rank","Enzyme","Dcat","Drig","Dconf","Dene","DMCS"]].to_csv(OUTPUT,index=False,float_format="%.6f")
 print(d[["Rank","Enzyme","Dcat","Drig","Dconf","Dene","DMCS"]].to_string(index=False))

if __name__=="__main__": main()
