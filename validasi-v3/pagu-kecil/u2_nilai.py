"""Menilai varian paket pagu kecil dengan aturan yang sama seperti pemilihan fitur v3:
dinilai di 19 provinsi pilih, dicek di 19 provinsi uji. Keluaran: u2_nilai.csv
Populasi 'semua' = paket yang dinilai varian itu; 'pagu>=1jt' = populasi bersama agar varian adil dibandingkan.
"""
import json
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v3')
from s2_model import FLAGS  # noqa: E402

V1 = '/mnt/project-files/model-v1/'
OUT = '/mnt/project-files/validasi-v3/pagu-kecil/'
info = pd.read_pickle(V1 + 'tahap1.pkl')['info']
DEV = set(json.load(open(V1 + 'eksplorasi/provinsi_pilih.json')))
R = pd.read_pickle('/mnt/project-files/validasi-v3/red_flag_v3.pkl')[FLAGS['perencanaan']]
v3 = pd.read_pickle('/mnt/project-files/model-v3/tahap2.pkl')['perencanaan']['skor'].Ensemble
skor = {'v3': v3}
for v in ['B', 'S', 'BS']:
    try:
        skor[v] = pd.read_pickle(OUT + f'skor_{v}.pkl')
    except FileNotFoundError:
        pass
rows = []
for v, s in skor.items():
    for pop in ['semua', 'pagu>=1jt']:
        ss = s if pop == 'semua' else s[info.pagu.loc[s.index] >= 1e6]
        if pop == 'semua' and 'B' in v:
            continue
        nama = v if pop == 'semua' else (v + ' (pagu<1jt disembunyikan)' if 'B' not in v else v)
        rr = R.loc[ss.index]
        ada, t4 = rr.any(axis=1), rr.drop(columns='rf4_penunjukan_langsung').any(axis=1)
        pagu = info.pagu.loc[ss.index]
        dev = info.provinsi.loc[ss.index].isin(DEV)
        o = ss.sort_values(ascending=False).index
        row = {'varian': nama, 'n': len(ss), 'acuan': ada.mean()}
        for K in [50, 100, 200]:
            row[f'P@{K}'] = ada.loc[o[:K]].mean()
        row['P@200_tanpaRF4'] = t4.loc[o[:200]].mean()
        row['top200_pagu<1jt'] = (pagu.loc[o[:200]] < 1e6).mean()
        row['top200_pagu<10jt'] = (pagu.loc[o[:200]] < 1e7).mean()
        for grp, m in [('pilih', dev), ('uji', ~dev)]:
            sg = ss[m].sort_values(ascending=False).index
            top = sg[:int(len(sg) * 0.05)]
            row[f'{grp}_5%'] = ada.loc[top].mean()
            row[f'{grp}_lift5%'] = ada.loc[top].mean() / ada[m].mean()
            row[f'{grp}_lift5%_tanpaRF4'] = t4.loc[top].mean() / t4[m].mean()
            row[f'{grp}_P@100'] = ada.loc[sg[:100]].mean()
        rows.append(row)
df = pd.DataFrame(rows)
df.to_csv(OUT + 'u2_nilai.csv', index=False)
pd.set_option('display.width', 300)
print(df.round(3).T.to_string())
