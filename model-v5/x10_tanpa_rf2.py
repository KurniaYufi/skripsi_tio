"""Precision@K TANPA RF2 (pengadaan langsung melewati ambang). RF2 hampir sama dengan ambang pada fitur "pagu dibanding
paket sejenis" (pembandingnya paket dengan jenis DAN metode sama; PL Rp500 jt = puluhan kali median PL), jadi RF2
ikut "menyontek" fitur. Membandingkan model sebelum audit, dasar audit, dan semua varian x8."""
import glob
import json
import os
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5/'
info = pd.read_pickle(O + 'tahap1.pkl')['info']
RF = pd.read_pickle(O + 'red_flag_v5.pkl')
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
H = pd.read_pickle(O + 'tahap2.pkl')
A = pd.read_pickle(O + 'arsip-v5-sebelum-audit/skor.pkl')
A2 = pd.read_pickle(O + 'arsip-audit-putaran2/tahap2.pkl')
A3 = pd.read_pickle(O + 'arsip-audit-putaran3/tahap2.pkl')
A4 = pd.read_pickle(O + 'arsip-audit-putaran4/tahap2.pkl')
A5 = pd.read_pickle(O + 'arsip-audit-putaran5/tahap2.pkl')
FL = {'perencanaan': ['rf1_pl_dekat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung'],
      'pelaksanaan': ['rf1_pl_dekat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung', 'rf5_penyedia_dominan',
                      'rf6_penyedia_serba_ada']}
rows = []
for j in FL:
    src = {'v5 sebelum audit (dashboard)': A[j].Ensemble, 'audit putaran 2': A2[j]['skor'].Ensemble, 'audit putaran 3': A3[j]['skor'].Ensemble,
           'audit putaran 4': A4[j]['skor'].Ensemble, 'audit putaran 5': A5[j]['skor'].Ensemble,
           'dasar audit': H[j]['skor'].Ensemble}
    for f in sorted(glob.glob(O + f'eksperimen-audit/skor_{j}_*.pkl')):
        src[os.path.basename(f)[len(f'skor_{j}_'):-4]] = pd.read_pickle(f).Ensemble
    for v, s in src.items():
        idx = s.sort_values(ascending=False).index
        a = RF.loc[idx, FL[j]].any(axis=1).values
        dev = info.provinsi.loc[idx].isin(DEV).values
        rows.append(dict(jalur=j, varian=v, P50=a[:50].mean(), P200=a[:200].mean(), p5=a[:int(len(a) * .05)].mean(),
                         pilih5=a[dev][:int(dev.sum() * .05)].mean(), uji5=a[~dev][:int((~dev).sum() * .05)].mean(),
                         acuan=a.mean(), acuan_uji=a[~dev].mean()))
R = pd.DataFrame(rows)
R.to_csv(O + 'eksperimen-audit/banding_tanpa_rf2.csv', index=False)
pd.set_option('display.width', 200)
print(R.round(3).to_string())
