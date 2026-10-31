"""Membandingkan varian pelaksanaan (x5_pelaksanaan.py) dan bobot ensemble dengan v5.
Keluaran: eksperimen-pelaksanaan/banding.csv.

Aturan pilih (ditulis SEBELUM melihat hasil):
1. Ukuran utama = presisi 5% teratas terhadap red flag di 19 provinsi pilih. Varian P (fitur penyedia, dekat dengan
   RF5/RF6) dinilai dengan RF1-RF4 saja, dibanding v5 yang juga dinilai dengan RF1-RF4.
2. Syarat lolos: porsi pagu < Rp10 jt di 200 teratas tidak naik lebih dari 10 poin dari v5, dan satu satker paling
   banyak 20 paket di 200 teratas.
3. Dipilih varian lolos dengan kenaikan terbesar; bila kenaikannya < 1 poin, v5 dipertahankan.
4. Provinsi uji hanya dilaporkan, tidak dipakai memilih.
Bobot ensemble (W, bobot IF-LOF-AE) dihitung dari persentil v5 tanpa melatih ulang.
"""
import glob
import json
import os
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5/'
E = O + 'eksperimen-pelaksanaan/'
info = pd.read_pickle(O + 'tahap1.pkl')['info']
RF = pd.read_pickle(O + 'red_flag_v5.pkl')
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
sat = info.provinsi + '|' + info.nama_satuan_kerja
H = pd.read_pickle(O + 'tahap2.pkl')['pelaksanaan']
ALL, RF14 = list(RF.columns), list(RF.columns[:4])


def ukur(s):
    idx = s.sort_values(ascending=False).index
    a = RF.loc[idx, ALL].any(axis=1).values
    a4 = RF.loc[idx, RF14].any(axis=1).values
    dev = info.provinsi.loc[idx].isin(DEV).values
    n5, np_, nu = int(len(a) * 0.05), int(dev.sum() * 0.05), int((~dev).sum() * 0.05)
    return {'P@50': a[:50].mean(), 'P@200': a[:200].mean(), '5% teratas': a[:n5].mean(),
            'pilih 5%': a[dev][:np_].mean(), 'uji 5%': a[~dev][:nu].mean(),
            'acuan pilih': a[dev].mean(), 'acuan uji': a[~dev].mean(),
            'RF1-4 pilih 5%': a4[dev][:np_].mean(), 'RF1-4 uji 5%': a4[~dev][:nu].mean(),
            'RF1-4 acuan uji': a4[~dev].mean(),
            'pagu < Rp10 jt di 200 teratas': (info.pagu.loc[idx[:200]] < 1e7).mean(),
            'satker maks 200 teratas': int(sat.loc[idx[:200]].value_counts().iloc[0])}


base = H['skor'].Ensemble
rows = [{'varian': 'v5', **ukur(base)}]
for f in sorted(glob.glob(E + 'skor_*.pkl')):
    rows.append({'varian': os.path.basename(f)[5:-4], **ukur(pd.read_pickle(f).Ensemble)})
pr = H['pct_rata']
for w in [(1, 2, 1), (1, 2, 2), (1, 1, 2), (0, 1, 1)]:
    s = (w[0] * pr.IF + w[1] * pr.LOF + w[2] * pr.AE) / sum(w)
    rows.append({'varian': 'W' + ''.join(map(str, w)), **ukur(s)})
R = pd.DataFrame(rows)
for i, r in R.iterrows():
    v = R.iloc[0]
    kol = 'RF1-4 pilih 5%' if r.varian == 'P' else 'pilih 5%'
    R.loc[i, 'naik pilih'] = r[kol] - v[kol]
    R.loc[i, 'lolos'] = (r['pagu < Rp10 jt di 200 teratas'] <= v['pagu < Rp10 jt di 200 teratas'] + 0.10) \
        and (r['satker maks 200 teratas'] <= 20)
cand = R[(R.varian != 'v5') & R.lolos & (R['naik pilih'] >= 0.01)]
R['terpilih'] = R.varian == (cand.sort_values('naik pilih').varian.iat[-1] if len(cand) else 'v5')
R.to_csv(E + 'banding.csv', index=False)
pd.set_option('display.width', 250)
print(R.round(3).T.to_string())
