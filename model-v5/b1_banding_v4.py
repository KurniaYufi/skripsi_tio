"""Membandingkan model v4 (data lama) dengan model v5 (data dibersihkan, s1_data.py).

1. Kesesuaian dengan red flag v5 (definisi sama dengan v3, penyedia dirapikan) dan red flag v3.
2. Berapa paket "bermasalah data" di peringkat atas: catatan ganda, rasio realisasi ekstrem, UMK tertulis persen,
   penyedia unit pemerintah. Keluaran: banding_v4_v5.csv dan masalah_data_atas.csv.
"""
import json
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401  (dibutuhkan untuk membaca tahap2.pkl)
sys.modules.setdefault('ens3', ens3)

O = '/mnt/project-files/model-v5/'
V1 = '/mnt/project-files/model-v1/'
d4 = pd.read_pickle(V1 + 'tahap1.pkl')
d5 = pd.read_pickle(O + 'tahap1.pkl')
RF3 = pd.read_pickle('/mnt/project-files/validasi-v3/red_flag_v3.pkl')
RF5 = pd.read_pickle(O + 'red_flag_v5.pkl')
DEV = set(json.load(open(V1 + 'eksplorasi/provinsi_pilih.json')))
prov = d5['info'].provinsi
FLAGS = {'perencanaan': list(RF5.columns[:4]), 'pelaksanaan': list(RF5.columns)}
MODEL = {'v4': '/mnt/project-files/model-v4/tahap2.pkl', 'v5': O + 'tahap2.pkl'}
if os.path.exists(O + 'varian-pel1jt/tahap2.pkl'):
    MODEL['v5 + pelaksanaan >= Rp1 jt'] = O + 'varian-pel1jt/tahap2.pkl'
H = {k: pd.read_pickle(v) for k, v in MODEL.items()}

# ---- penanda masalah data (dihitung dari data lama vs data bersih)
i4, i5 = d4['info'], d5['info']
r4 = (i4.realisasi / i4.pagu).dropna()
masalah = pd.DataFrame(index=i4.index)
masalah['catatan ganda'] = i4.index.isin(d5['paket_ganda'])
masalah['rasio realisasi ekstrem'] = i4.index.isin(r4.index[(r4 < 0.01) | (r4 > 10)])
u4 = d4['f_pel'].porsi_umk
u5 = d5['f_pel'].porsi_umk.reindex(u4.index)
masalah['UMK tertulis persen'] = i4.index.isin(u4.index[(u5 - u4) > 0.5])
masalah['penyedia unit pemerintah'] = (i4.penyedia.fillna('-') != '-') & (i5.penyedia.reindex(i4.index).fillna('-') == '-') \
    & i4.index.isin(d5['f_pel'].index)
masalah['salah satu'] = masalah.any(axis=1)


def ukur(s, ada):
    s = s.sort_values(ascending=False)
    a = ada.reindex(s.index).fillna(False).values.astype(bool)
    dev = prov.reindex(s.index).isin(DEV).values
    n5 = int(len(a) * 0.05)
    return {'N': len(a), 'acuan': a.mean(), 'P@200': a[:200].mean(), '5% teratas': a[:n5].mean(),
            'uji 5%': a[~dev][:int((~dev).sum() * 0.05)].mean(), 'acuan uji': a[~dev].mean()}


rows, rows_m = [], []
for jalur in ['perencanaan', 'pelaksanaan']:
    for nama, h in H.items():
        s = h[jalur]['skor'].Ensemble
        for lbl, R in [('red flag v5', RF5), ('red flag v3', RF3)]:
            rows.append({'jalur': jalur, 'model': nama, 'label': lbl,
                         **ukur(s, R.reindex(s.index)[FLAGS[jalur]].fillna(False).any(axis=1))})
            if jalur == 'perencanaan':
                rows.append({'jalur': jalur, 'model': nama, 'label': lbl + ' tanpa RF4',
                             **ukur(s, R.reindex(s.index)[FLAGS[jalur][:3]].fillna(False).any(axis=1))})
        top200, top5 = s.nlargest(200).index, s.nlargest(int(len(s) * 0.05)).index
        rows_m.append({'jalur': jalur, 'model': nama,
                       **{f'{c} (200 teratas)': int(masalah[c].reindex(top200).fillna(False).sum()) for c in masalah},
                       **{f'{c} (5% teratas)': int(masalah[c].reindex(top5).fillna(False).sum()) for c in masalah}})
    a, b = set(H['v4'][jalur]['skor'].Ensemble.nlargest(200).index), set(H['v5'][jalur]['skor'].Ensemble.nlargest(200).index)
    print(jalur, 'jaccard 200 teratas v4-v5:', round(len(a & b) / len(a | b), 3))
B = pd.DataFrame(rows)
M = pd.DataFrame(rows_m)
B.to_csv(O + 'banding_v4_v5.csv', index=False)
M.to_csv(O + 'masalah_data_atas.csv', index=False)
pd.set_option('display.width', 250)
print(B.round(3).to_string(index=False))
print(M.T.to_string())
print('jumlah paket bermasalah di data lama:', masalah.sum().to_dict())
