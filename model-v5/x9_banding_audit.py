"""Membandingkan varian audit (x8) dengan model saat ini (tahap2.pkl): kewajaran isi peringkat atas lebih dulu,
baru kesesuaian dengan red flag. Keluaran: eksperimen-audit/banding.csv"""
import glob
import json
import os
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5/'
E = O + 'eksperimen-audit/'
info = pd.read_pickle(O + 'tahap1.pkl')['info']
RF = pd.read_pickle(O + 'red_flag_v5.pkl')
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
sat = info.provinsi + '|' + info.nama_satuan_kerja
n_sat = sat.map(sat.value_counts())
FLAGS = {'perencanaan': list(RF.columns[:4]), 'pelaksanaan': list(RF.columns)}
H = pd.read_pickle(O + 'tahap2.pkl')


def ukur(s, jalur):
    idx = s.sort_values(ascending=False).index
    t = idx[:200]
    a = RF.loc[idx, FLAGS[jalur]].any(axis=1).values
    dev = info.provinsi.loc[idx].isin(DEV).values
    return {'satker maks 200': int(sat.loc[t].value_counts().iloc[0]), 'satker unik 200': sat.loc[t].nunique(),
            'pagu<=1jt 200': (info.pagu.loc[t] <= 1e6).mean(), 'pagu<=1jt semua': (info.pagu.loc[idx] <= 1e6).mean(),
            'satker<10 200': (n_sat.loc[t] < 10).mean(), 'satker<10 semua': (n_sat.loc[idx] < 10).mean(),
            'P@50': a[:50].mean(), 'P@200': a[:200].mean(), '5%': a[:int(len(a) * .05)].mean(),
            'pilih 5%': a[dev][:int(dev.sum() * .05)].mean(), 'uji 5%': a[~dev][:int((~dev).sum() * .05)].mean(),
            'acuan uji': a[~dev].mean()}


rows = []
for jalur in ['perencanaan', 'pelaksanaan']:
    base = H[jalur]['skor'].Ensemble
    rows.append({'jalur': jalur, 'varian': 'dasar', **ukur(base, jalur)})
    for f in sorted(glob.glob(E + f'skor_{jalur}_*.pkl')):
        rows.append({'jalur': jalur, 'varian': os.path.basename(f)[len(f'skor_{jalur}_'):-4],
                     **ukur(pd.read_pickle(f).Ensemble, jalur)})
R = pd.DataFrame(rows)
R.to_csv(E + 'banding.csv', index=False)
pd.set_option('display.width', 250)
print(R.round(3).to_string())
