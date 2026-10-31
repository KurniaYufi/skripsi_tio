"""Validasi v3, bagian 6c: analisis tambahan setelah r6 (tidak ada varian perencanaan yang lolos syarat).

Aturan utama r6 menilai puncak daftar (P@50/100/200). Dashboard memakai titik kerja lain: "paket tidak
lazim" = 5% skor tertinggi, yang juga menjadi dasar warna peta. Karena aturan utama tidak menghasilkan
calon yang sah di jalur perencanaan, dipakai aturan kedua: presisi red flag pada 5% teratas, dipilih di
19 provinsi pilih, lalu dicek di 19 provinsi uji. Skor diambil dari r6_skor.pkl dan r6b_skor.pkl.
Keluaran: r6c_lima_persen.csv
"""
import json
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v3')
from s2_model import FLAGS  # noqa: E402

V1 = '/mnt/project-files/model-v1/'
OUT = '/mnt/project-files/validasi-v3/'
d = pd.read_pickle(V1 + 'tahap1.pkl')
info = d['info']
DEV = set(json.load(open(V1 + 'eksplorasi/provinsi_pilih.json')))
rf3 = pd.read_pickle(OUT + 'red_flag_v3.pkl')
skor = {**pd.read_pickle(OUT + 'r6_skor.pkl'), **pd.read_pickle(OUT + 'r6b_skor.pkl')}
rows = []
for (jalur, varian), s in skor.items():
    R = rf3.loc[s.index, FLAGS[jalur]]
    ada, t4 = R.any(axis=1), R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    dev = info.provinsi.loc[s.index].isin(DEV)
    for grp, m in [('pilih', dev), ('uji', ~dev)]:
        ss = s[m].sort_values(ascending=False)
        for q in (0.01, 0.05, 0.10):
            top = ss.index[:int(len(ss) * q)]
            rows.append({'jalur': jalur, 'varian': varian, 'provinsi': grp, 'ambang': f'{int(q * 100)}%',
                         'presisi': ada.loc[top].mean(), 'acuan': ada[m].mean(), 'lift': ada.loc[top].mean() / ada[m].mean(),
                         'presisi_tanpaRF4': t4.loc[top].mean(), 'lift_tanpaRF4': t4.loc[top].mean() / t4[m].mean(),
                         **{f'lift_{c[:3]}': R.loc[top, c].mean() / R.loc[m.values, c].mean() for c in R}})
df = pd.DataFrame(rows)
df.to_csv(OUT + 'r6c_lima_persen.csv', index=False)
pd.set_option('display.width', 250)
print(df[df.ambang == '5%'].round(3).to_string(index=False))
