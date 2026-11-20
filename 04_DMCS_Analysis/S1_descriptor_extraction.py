#!/usr/bin/env python3
"""S1: Extract DMCS descriptors using one harmonized 5.0 Å pocket-RMSF protocol.

For every system, the protein C-alpha RMSF profile is read from the common
CPPTRAJ output (rmsf_protein_calpha.dat). The catalytic pocket is defined
independently from that system's assembled ternary complexN.pdb as protein
residues with >=1 heavy atom within the selected cutoff of any heavy atom in
UNP (PLP), UNL (furfural) or UNI (isopropylamine).
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "S1_INPUTS.csv"
PROTEIN_RESNAMES = {
    "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HID","HIE","HIP",
    "ILE","LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL","CYX"
}
LIGANDS = {"UNP":"PLP","UNL":"Furfural","UNI":"Isopropylamine"}
EXPECTED_LIGAND_HEAVY = {"UNP":16,"UNL":7,"UNI":4}


def read_pdb(path: Path):
    protein, ligands = {}, []
    with path.open(errors="replace") as fh:
        for line in fh:
            if not line.startswith(("ATOM  ","HETATM")):
                continue
            atom_name = line[12:16].strip()
            resname = line[17:20].strip()
            chain = line[21:22].strip()
            try:
                resid = int(line[22:26])
                icode = line[26:27].strip()
                xyz = np.array([float(line[30:38]),float(line[38:46]),float(line[46:54])])
            except ValueError:
                continue
            element = line[76:78].strip().upper() or re.sub(r"[^A-Za-z]","",atom_name)[:1].upper()
            if element in {"H","D"}:
                continue
            atom = {"xyz":xyz,"resid":resid,"resname":resname,"chain":chain,"icode":icode}
            if resname in LIGANDS:
                ligands.append(atom)
            elif line.startswith("ATOM  ") and resname in PROTEIN_RESNAMES:
                protein.setdefault(resid,[]).append(atom)
    counts = {name:sum(a["resname"]==name for a in ligands) for name in LIGANDS}
    if counts != EXPECTED_LIGAND_HEAVY:
        raise ValueError(f"{path}: unexpected UNP/UNL/UNI heavy-atom inventory {counts}")
    if not protein:
        raise ValueError(f"{path}: no protein atoms parsed")
    residue_meta = {}
    ligand_xyz = np.array([a["xyz"] for a in ligands])
    ligand_names = np.array([a["resname"] for a in ligands])
    for resid, atoms in protein.items():
        chain_keys = {(a["chain"],a["icode"]) for a in atoms}
        if len(chain_keys) != 1:
            raise ValueError(f"{path}: residue {resid} maps to multiple chains/insertion codes")
        coords = np.array([a["xyz"] for a in atoms])
        d = np.linalg.norm(coords[:,None,:]-ligand_xyz[None,:,:],axis=2)
        ix = np.unravel_index(np.argmin(d),d.shape)
        residue_meta[resid] = {
            "Residue_Name":atoms[0]["resname"],
            "Minimum_Distance_to_UNP_UNL_UNI_A":float(d[ix]),
            "Closest_Ligand":LIGANDS[str(ligand_names[ix[1]])],
        }
    return residue_meta


def read_rmsf(path: Path):
    out={}
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f=line.split()
        if len(f)<2:
            continue
        resid=int(float(f[0])); value=float(f[1])
        if resid in out or not np.isfinite(value) or value<0:
            raise ValueError(f"{path}: duplicate or invalid RMSF row {line.strip()}")
        out[resid]=value
    if not out:
        raise ValueError(f"{path}: no RMSF rows")
    return out


def mean_distance(path: Path):
    a=np.loadtxt(path,comments="#",ndmin=2)
    if a.shape[1]<2 or not np.isfinite(a[:,1]).all():
        raise ValueError(f"{path}: expected finite frame/distance columns")
    return float(a[:,1].mean()),int(a.shape[0])


def clusters(path: Path):
    rows=[]
    for line in path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f=line.split()
        if len(f)<3:
            continue
        rows.append((int(float(f[0])),int(float(f[1])),float(f[2])))
    if not rows:
        raise ValueError(f"{path}: no cluster records")
    if sum(x[1] for x in rows)!=50000:
        raise ValueError(f"{path}: cluster frame counts do not sum to 50,000")
    cid,n,frac=max(rows,key=lambda x:x[1])
    if n<=0 or not 0<frac<=1:
        raise ValueError(f"{path}: invalid dominant-cluster result")
    return cid,n,frac,len(rows)


def gb_pb(path: Path):
    values=[]
    for line in path.read_text(errors="replace").splitlines():
        if re.match(r"\s*DELTA TOTAL\s+[-+0-9.]",line):
            values.append(float(line.split()[2]))
    if len(values)<2:
        raise ValueError(f"{path}: expected GB and PB DELTA TOTAL rows")
    return values[0],values[1]


def validate_cpptraj(path: Path,nres: int):
    t=path.read_text(errors="replace")
    must=["trajin md1.nc 1 last 10","autoimage","reference md1.rst7",
          "rms reference","rmsf_protein_calpha.dat","@CA byres"]
    for token in must:
        if token not in t:
            raise ValueError(f"{path}: missing common RMSF setting {token}")
    if t.lower().find("rms reference")>t.lower().find("atomicfluct"):
        raise ValueError(f"{path}: align protein before atomic fluctuation")
    m=re.search(r"rmsf_protein_calpha\.dat[\s\\]*:1-(\d+)@CA",t,re.I)
    if not m or int(m.group(1))!=nres:
        raise ValueError(f"{path}: protein C-alpha RMSF mask does not match {nres} protein residues")


def validate_md(path: Path):
    t=path.read_text(errors="replace").lower().replace(" ","")
    for key in ("dt=0.002","nstlim=250000000","ntwx=5000"):
        if key not in t:
            raise ValueError(f"{path}: expected 500 ns production setting {key} not found")


def normalize(x):
    lo=float(np.min(x)); hi=float(np.max(x))
    if np.isclose(lo,hi):
        raise ValueError("Cannot min-max normalize a constant descriptor")
    return (np.asarray(x,dtype=float)-lo)/(hi-lo)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--analysis-root",required=True,help="Parent directory containing the 15 analysis folders")
    ap.add_argument("--output-dir",default=str(HERE),help="Output directory")
    ap.add_argument("--pocket-cutoff",type=float,default=5.0)
    ap.add_argument("--sensitivity-cutoffs",default="4,5,6")
    args=ap.parse_args()
    root=Path(args.analysis_root).expanduser().resolve()
    out=Path(args.output_dir).expanduser().resolve(); out.mkdir(parents=True,exist_ok=True)
    cutoffs=sorted(set(float(x.strip()) for x in args.sensitivity_cutoffs.split(",") if x.strip()))
    if args.pocket_cutoff not in cutoffs: cutoffs.append(args.pocket_cutoff); cutoffs.sort()
    if any(x<=0 for x in cutoffs): ap.error("Cutoffs must be positive")
    manifest=pd.read_csv(MANIFEST)
    required={"Enzyme","Directory","Catalytic_Residue","CatalyticDistanceFile"}
    if not required.issubset(manifest.columns): raise ValueError(f"Manifest must contain {sorted(required)}")
    if len(manifest)!=15 or manifest["Enzyme"].duplicated().any(): raise ValueError("Manifest must contain 15 unique systems")
    raw=[]; all_pocket=[]; all_rmsf=[]; per_system={}
    for rec in manifest.to_dict("records"):
        name=str(rec["Enzyme"]); folder=root/str(rec["Directory"])
        needed=["complexN.pdb","rmsf_protein_calpha.dat","cpptraj.in","md1.in",
                str(rec["CatalyticDistanceFile"]),"plp_unl.dat","plp_uni.dat",
                "dmcs_cluster_summary.dat","FINAL_RESULTS_UNL_MMPBSA.dat","mmpbsa.in"]
        missing=[x for x in needed if not (folder/x).is_file()]
        if missing: raise FileNotFoundError(f"{name}: missing {missing}")
        pocket=read_pdb(folder/"complexN.pdb")
        rmsf=read_rmsf(folder/"rmsf_protein_calpha.dat")
        if set(pocket)!=set(rmsf):
            raise ValueError(f"{name}: PDB/RMSF residue mapping mismatch")
        validate_cpptraj(folder/"cpptraj.in",len(pocket))
        validate_md(folder/"md1.in")
        cat,ncat=mean_distance(folder/str(rec["CatalyticDistanceFile"]))
        unl,nunl=mean_distance(folder/"plp_unl.dat")
        uni,nuni=mean_distance(folder/"plp_uni.dat")
        if (ncat,nunl,nuni)!=(50000,50000,50000):
            raise ValueError(f"{name}: distance series must each contain 50,000 frames")
        cid,cframes,cfrac,ncl=clusters(folder/"dmcs_cluster_summary.dat")
        gb,pb=gb_pb(folder/"FINAL_RESULTS_UNL_MMPBSA.dat")
        summary={
          "Enzyme":name,"Analysis_Directory":str(rec["Directory"]),
          "Catalytic_Residue":str(rec["Catalytic_Residue"]),
          "Catalytic_Distance_File":str(rec["CatalyticDistanceFile"]),
          "CatalyticResidue_PLP_mean_A":cat,"CatalyticResidue_PLP_n_frames":ncat,
          "PLP_UNL_mean_A":unl,"PLP_UNL_n_frames":nunl,"PLP_UNI_mean_A":uni,"PLP_UNI_n_frames":nuni,
          "Largest_Cluster_ID":cid,"Largest_Cluster_Frames":cframes,
          "Largest_Cluster_Fraction":cfrac,"Total_Clusters":ncl,
          "GB_Delta_Total_kcal_mol":gb,"PB_Delta_Total_kcal_mol":pb,
          "Protein_Residue_Count":len(pocket)
        }
        all_rmsf.extend([{"Enzyme":name,"Residue":r,"RMSF_A":v,"Source_File":"rmsf_protein_calpha.dat"} for r,v in sorted(rmsf.items())])
        site=[]
        for cutoff in cutoffs:
            ids=sorted(r for r,x in pocket.items() if x["Minimum_Distance_to_UNP_UNL_UNI_A"]<=cutoff)
            if not ids: raise ValueError(f"{name}: no residues within {cutoff} Å")
            mean=float(np.mean([rmsf[r] for r in ids]))
            summary[f"Pocket_Cutoff_{cutoff:g}A_N"]=len(ids)
            summary[f"Pocket_Cutoff_{cutoff:g}A_RMSF_Mean_A"]=mean
            summary[f"Pocket_Cutoff_{cutoff:g}A_Residues"]=";".join(map(str,ids))
            if np.isclose(cutoff,args.pocket_cutoff):
                summary["Active_Site_RMSF_Cutoff_A"]=cutoff
                summary["Active_Site_RMSF_Mean_A"]=mean
                summary["Active_Site_RMSF_SD_A"]=float(np.std([rmsf[r] for r in ids],ddof=1)) if len(ids)>1 else 0.0
                summary["Active_Site_RMSF_N"]=len(ids)
                summary["Active_Site_RMSF_Residues"]=";".join(map(str,ids))
            if np.isclose(cutoff,5.0):
                for r in ids:
                    site.append({"Enzyme":name,"Residue":r,"Residue_Name":pocket[r]["Residue_Name"],
                      "Minimum_Distance_to_UNP_UNL_UNI_A":pocket[r]["Minimum_Distance_to_UNP_UNL_UNI_A"],
                      "Closest_Ligand":pocket[r]["Closest_Ligand"],"CAlpha_RMSF_A":rmsf[r],"Pocket_Cutoff_A":5.0})
        summary.update({"Catalytic_Distance_Frames":ncat,"Pocket_Residue_Count_5A":summary.get("Pocket_Cutoff_5A_N")})
        raw.append(summary); all_pocket.extend(site); per_system[name]=(folder,summary,site,rmsf)
        print(f"{name}: pocket residues={summary[f'Pocket_Cutoff_{args.pocket_cutoff:g}A_N']}; RMSF={summary[f'Pocket_Cutoff_{args.pocket_cutoff:g}A_RMSF_Mean_A']:.4f} Å; frames=50,000")
    rawdf=pd.DataFrame(raw)
    rawdf.to_csv(out/"DMCS_15_SYSTEM_RAW_DESCRIPTORS.csv",index=False,float_format="%.9f")
    pd.DataFrame(all_pocket).to_csv(out/"DMCS_ACTIVE_SITE_RESIDUES.csv",index=False,float_format="%.6f")
    pd.DataFrame(all_rmsf).to_csv(out/"DMCS_15_SYSTEM_RMSF_PER_RESIDUE.csv",index=False,float_format="%.6f")
    result=rawdf[["Enzyme","CatalyticResidue_PLP_mean_A","PLP_UNL_mean_A","PLP_UNI_mean_A","Active_Site_RMSF_Mean_A","Largest_Cluster_Fraction","GB_Delta_Total_kcal_mol"]].copy()
    result.columns=["Enzyme","Lys_PLP","PLP_UNL","PLP_UNI","RMSF","ClusterFraction","MMGBSA"]
    result.to_csv(out/"DMCS_RESULTS.csv",index=False,float_format="%.9f")
    # 4/5/6 A sensitivity table.
    sensitivity=[]
    for cutoff in cutoffs:
        x=rawdf[["Enzyme","CatalyticResidue_PLP_mean_A","PLP_UNL_mean_A","PLP_UNI_mean_A",f"Pocket_Cutoff_{cutoff:g}A_RMSF_Mean_A","Largest_Cluster_Fraction","GB_Delta_Total_kcal_mol"]].copy()
        x["Dcat"]=.5*(1-normalize(x["CatalyticResidue_PLP_mean_A"]))+.25*(1-normalize(x["PLP_UNL_mean_A"]))+.25*(1-normalize(x["PLP_UNI_mean_A"]))
        x["Drig"]=1-normalize(x[f"Pocket_Cutoff_{cutoff:g}A_RMSF_Mean_A"])
        x["Dconf"]=normalize(np.log(x["Largest_Cluster_Fraction"]))
        x["Dene"]=normalize(x["GB_Delta_Total_kcal_mol"].abs())
        x["DMCS"]=.4*x["Dcat"]+.25*x["Drig"]+.15*x["Dconf"]+.2*x["Dene"]
        x=x.sort_values("DMCS",ascending=False).reset_index(drop=True); x["Rank"]=np.arange(1,len(x)+1); x["Pocket_Cutoff_A"]=cutoff
        x=x.rename(columns={f"Pocket_Cutoff_{cutoff:g}A_RMSF_Mean_A":"RMSF"})
        sensitivity.append(x[["Pocket_Cutoff_A","Rank","Enzyme","RMSF","Dcat","Drig","Dconf","Dene","DMCS"]])
    sens=pd.concat(sensitivity,ignore_index=True)
    sens.to_csv(out/"DMCS_RMSF_CUTOFF_SENSITIVITY.csv",index=False,float_format="%.6f")
    # Create per-enzyme researcher-facing result folders.
    data_root=out/"15_Enzyme_Analysis_Data"
    for name,(folder,summary,site,rmsf) in per_system.items():
        d=data_root/name; d.mkdir(parents=True,exist_ok=True)
        pd.DataFrame([summary]).to_csv(d/"descriptor_summary.csv",index=False,float_format="%.9f")
        pd.DataFrame(site).to_csv(d/"active_site_rmsf.csv",index=False,float_format="%.6f")
        pd.DataFrame([{"Enzyme":name,"Residue":r,"RMSF_A":v} for r,v in sorted(rmsf.items())]).to_csv(d/"protein_ca_rmsf.csv",index=False,float_format="%.6f")
        with (d/"rmsf_protein_calpha.dat").open("w") as fh:
            fh.write("#Res        AtomicFlx\n")
            for r,v in sorted(rmsf.items()): fh.write(f"{r:8d} {v:12.4f}\n")
        sens[sens["Enzyme"]==name].to_csv(d/"cutoff_sensitivity.csv",index=False,float_format="%.6f")
    # Standardized score outputs, exactly matching S2/S3 data contract.
    def score(df):
        x=df.copy()
        x["Dcat"]=.5*(1-normalize(x["Lys_PLP"]))+.25*(1-normalize(x["PLP_UNL"]))+.25*(1-normalize(x["PLP_UNI"]))
        x["Drig"]=1-normalize(x["RMSF"])
        x["Dconf"]=normalize(np.log(x["ClusterFraction"]))
        x["Dene"]=normalize(x["MMGBSA"].abs())
        x["DMCS"]=.4*x["Dcat"]+.25*x["Drig"]+.15*x["Dconf"]+.2*x["Dene"]
        return x.sort_values("DMCS",ascending=False).reset_index(drop=True)
    scored=score(result); scored.insert(0,"Rank",np.arange(1,len(scored)+1))
    scored.to_csv(out/"DMCS_STANDARDIZED.csv",index=False,float_format="%.9f")
    scored[["Rank","Enzyme","Dcat","Drig","Dconf","Dene","DMCS"]].to_csv(out/"DMCS_Final_Ranking.csv",index=False,float_format="%.6f")
    summary=scored[["Enzyme","Lys_PLP","PLP_UNL","PLP_UNI","RMSF","ClusterFraction","MMGBSA"]].copy()
    summary.columns=["Enzyme","CatalyticDistance","FurfuralDistance","IPADistance","RMSF","ClusterFraction","EnergyDescriptor"]
    summary["EnergyDescriptor"]=summary["EnergyDescriptor"].abs()
    summary.to_csv(out/"DMCS_Descriptor_Summary.csv",index=False,float_format="%.9f")
    print("\\nS1 finished. Score table written with 5 Å structure-derived catalytic pockets.")
    print(scored[["Rank","Enzyme","RMSF","Dcat","Drig","Dconf","Dene","DMCS"]].to_string(index=False))


if __name__=="__main__":
    main()
