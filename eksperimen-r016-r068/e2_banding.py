"""Membandingkan model v4 dengan model eksperimen (e1_latih.py) memakai tiga set red flag:
lama (red flag v4), lama + baru, dan red flag baru saja. Keluaran: hasil_banding.csv.

Red flag baru:
- RF7 (OCP R016): pagu >= T kali median pagu paket sejenis (jenis x metode, sama dengan fitur log_rasio_pagu_sejenis).
  OCP tidak memberi angka, jadi diuji T = 3, 5, 10.
- RF8 (OCP R068): realisasi > pagu. Varian "tanpa 2x": tidak menghitung rasio 1,95-2,05 (sebagian besar dua catatan
  realisasi bernilai sama untuk satu RUP, diduga tercatat ganda).
"""
import json
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v4')
import s2_model  # noqa: E402

OUT = '/mnt/project-files/eksperimen-r016-r068/'
d = pd.read_pickle(s2_model.V1 + 'tahap1.pkl')
info = d['info']
RF = pd.read_pickle(s2_model.V3 + 'red_flag_v3.pkl')
H = pd.read_pickle('/mnt/project-files/model-v4/tahap2.pkl')
DEV = set(json.load(open(s2_model.V1 + 'eksplorasi/provinsi_pilih.json')))

rasio_sejenis = 10 ** d['f_ren'].log_rasio_pagu_sejenis
rr = d['f_pel'].rasio_realisasi
BARU = {f'RF7 R016 >= {T}x sejenis': rasio_sejenis >= T for T in [3, 5, 10]}
BARU['RF8 R068 realisasi > pagu'] = (rr > 1).reindex(info.index, fill_value=False)
BARU['RF8 R068 tanpa 2x'] = ((rr > 1) & ~rr.between(1.95, 2.05)).reindex(info.index, fill_value=False)
EKS = {('A', 'perencanaan'): [k for k in BARU if 'RF7' in k],
       ('A', 'pelaksanaan'): [k for k in BARU if 'RF7' in k],
       ('B', 'pelaksanaan'): [k for k in BARU if 'RF8' in k]}


def ukur(s, ada):
    s = s.sort_values(ascending=False)
    a = ada.loc[s.index].values.astype(bool)
    dev = info.provinsi.loc[s.index].isin(DEV).values
    n5 = int(len(a) * 0.05)
    return {'acuan': a.mean(), 'P@200': a[:200].mean(), '5% teratas': a[:n5].mean(),
            'lift 5%': a[:n5].mean() / a.mean(), 'uji 5%': a[~dev][:int((~dev).sum() * 0.05)].mean(),
            'acuan uji': a[~dev].mean()}


rows = []
for (eks, jalur), baru in EKS.items():
    try:
        se = pd.read_pickle(OUT + f'skor_{eks}_{jalur}.pkl').Ensemble
    except FileNotFoundError:
        print('belum ada', eks, jalur)
        continue
    sv = H[jalur]['skor'].Ensemble
    idx = sv.index
    lama = RF.loc[idx, s2_model.FLAGS[jalur]].any(axis=1)
    sets = {'lama': lama}
    if jalur == 'perencanaan':
        sets['lama tanpa RF4'] = RF.loc[idx, ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket']].any(axis=1)
    for b in baru:
        sets[f'lama + {b}'] = lama | BARU[b].loc[idx]
        sets[f'{b} saja'] = BARU[b].loc[idx]
    top_v, top_e = set(sv.nlargest(200).index), set(se.nlargest(200).index)
    jac = len(top_v & top_e) / len(top_v | top_e)
    for nama, ada in sets.items():
        for model, s in [('v4', sv), (f'eksperimen {eks}', se)]:
            rows.append({'eksperimen': eks, 'jalur': jalur, 'red flag': nama, 'model': model, **ukur(s, ada),
                         'jaccard top200 v4-eks': jac})
R = pd.DataFrame(rows)
R.to_csv(OUT + 'hasil_banding.csv', index=False)
pd.set_option('display.width', 250)
pd.set_option('display.max_rows', 200)
print(R.drop(columns=['jaccard top200 v4-eks']).round(3).to_string(index=False))
print(R.groupby(['eksperimen', 'jalur'])['jaccard top200 v4-eks'].first().round(3))
