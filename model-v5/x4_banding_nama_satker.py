"""Membandingkan varian fitur nama di satker (x3_nama_satker.py) dengan v5. Keluaran: eksperimen-nama-satker/banding.csv.

Selain kesesuaian dengan red flag (seperti x2), dicek juga pola yang ditanyakan Tio: berapa persen paket yang pagunya
>= 10 kali paket lain bernama sama di satkernya masuk 5% teratas. Ini pengecekan kewajaran, bukan bukti validitas,
karena pola itu sekarang ada di fitur.
"""
import glob
import json
import os
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5/'
E = O + 'eksperimen-nama-satker/'
d = pd.read_pickle(O + 'tahap1.pkl')
info = d['info']
RF = pd.read_pickle(O + 'red_flag_v5.pkl')
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
X = pd.read_pickle(E + 'fitur_nama_satker.pkl')
pola = (X.log_rasio_pagu_nama_satker >= 1) & (X.n_nama_lain >= 2)  # >= 10 kali, minimal 2 paket lain (seperti contoh A,B,C)
FLAGS = {'perencanaan': list(RF.columns[:4]), 'pelaksanaan': list(RF.columns)}
H = pd.read_pickle(O + 'tahap2.pkl')


def ukur(s, jalur):
    s = s.sort_values(ascending=False)
    idx = s.index
    a = RF.loc[idx, FLAGS[jalur]].any(axis=1).values
    b = RF.loc[idx, FLAGS[jalur][:3]].any(axis=1).values
    dev = info.provinsi.loc[idx].isin(DEV).values
    n5 = int(len(a) * 0.05)
    top5 = set(idx[:n5])
    pp = pola.loc[idx]
    return {'P@200': a[:200].mean(), '5% teratas': a[:n5].mean(), 'tanpa RF4 P@200': b[:200].mean(),
            'tanpa RF4 5%': b[:n5].mean(), 'pilih 5%': a[dev][:int(dev.sum() * 0.05)].mean(),
            'uji 5%': a[~dev][:int((~dev).sum() * 0.05)].mean(), 'acuan uji': a[~dev].mean(),
            'pola A-B-C: jumlah paket': int(pp.sum()),
            'pola A-B-C: masuk 5% teratas': pp[pp].index.isin(list(top5)).mean(),
            'pola A-B-C di 200 teratas': int(pp.loc[idx[:200]].sum()),
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
R.to_csv(E + 'banding.csv', index=False)
pd.set_option('display.width', 250)
print(R.round(3).T.to_string())
