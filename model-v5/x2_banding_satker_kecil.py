"""Membandingkan varian satker kecil (x1_satker_kecil.py) dengan v5. Keluaran: eksperimen-satker-kecil/banding.csv.

Aturan pilih (ditetapkan sebelum melihat hasil, sama gaya dengan validasi-v3/r6c): di provinsi pilih, presisi 5% teratas
terhadap red flag tidak boleh turun lebih dari 1 poin dari v5; dari yang lolos, dipilih yang porsi satker kecil
(< 10 paket) di 200 teratas paling rendah. Provinsi uji hanya dilaporkan.
"""
import glob
import json
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5/'
E = O + 'eksperimen-satker-kecil/'
d = pd.read_pickle(O + 'tahap1.pkl')
info = d['info']
RF = pd.read_pickle(O + 'red_flag_v5.pkl')
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
sat = info.provinsi + '|' + info.nama_satuan_kerja
n_paket = sat.map(sat.value_counts())
FLAGS = {'perencanaan': list(RF.columns[:4]), 'pelaksanaan': list(RF.columns)}
H = pd.read_pickle(O + 'tahap2.pkl')


def ukur(s, jalur):
    s = s.sort_values(ascending=False)
    idx = s.index
    a = RF.loc[idx, FLAGS[jalur]].any(axis=1).values
    b = RF.loc[idx, FLAGS[jalur][:3]].any(axis=1).values
    dev = info.provinsi.loc[idx].isin(DEV).values
    n5 = int(len(a) * 0.05)
    kecil = (n_paket.loc[idx] < 10).values
    return {'P@50': a[:50].mean(), 'P@200': a[:200].mean(), '5% teratas': a[:n5].mean(),
            'tanpa RF4 P@200': b[:200].mean(), 'tanpa RF4 5%': b[:n5].mean(),
            'pilih 5%': a[dev][:int(dev.sum() * 0.05)].mean(), 'uji 5%': a[~dev][:int((~dev).sum() * 0.05)].mean(),
            'acuan pilih': a[dev].mean(), 'acuan uji': a[~dev].mean(),
            'satker<10 di 50 teratas': kecil[:50].mean(), 'satker<10 di 200 teratas': kecil[:200].mean(),
            'satker unik 200 teratas': len(set(sat.loc[idx[:200]])),
            'pagu < Rp10 jt di 200 teratas': (info.pagu.loc[idx[:200]] < 1e7).mean()}


rows = []
for jalur in ['perencanaan', 'pelaksanaan']:
    base = H[jalur]['skor'].Ensemble
    rows.append({'jalur': jalur, 'varian': 'v5 (sekarang)', 'jaccard200 vs v5': 1.0, **ukur(base, jalur)})
    for f in sorted(glob.glob(E + f'skor_{jalur}_*.pkl')):
        v = os.path.basename(f)[len(f'skor_{jalur}_'):-4]
        s = pd.read_pickle(f).Ensemble
        A, B = set(base.nlargest(200).index), set(s.nlargest(200).index)
        rows.append({'jalur': jalur, 'varian': v, 'jaccard200 vs v5': len(A & B) / len(A | B), **ukur(s, jalur)})
R = pd.DataFrame(rows)
for jalur, g in R.groupby('jalur'):
    b = g[g.varian == 'v5 (sekarang)']['pilih 5%'].iat[0]
    lolos = g[(g.varian != 'v5 (sekarang)') & (g['pilih 5%'] >= b - 0.01)]
    pilih = lolos.sort_values('satker<10 di 200 teratas').varian.iat[0] if len(lolos) else 'v5 (sekarang)'
    R.loc[g.index, 'terpilih'] = R.loc[g.index, 'varian'] == pilih
R.to_csv(E + 'banding.csv', index=False)
pd.set_option('display.width', 250)
print(R.round(3).T.to_string())
