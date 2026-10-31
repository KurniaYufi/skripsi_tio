"""Eksperimen (permintaan Tio 2026-10-29): fitur yang mirip red flag OCP dibuang dari model, lalu dipakai sebagai red flag.

A = R016 (nilai jauh di atas paket sejenis): fitur log_rasio_pagu_sejenis dibuang (perencanaan dan pelaksanaan).
B = R068 (realisasi melebihi nilai kontrak/pagu): fitur rasio_realisasi, log_selisih_realisasi,
    selisih_rasio_realisasi_sejenis dibuang (pelaksanaan).
Pengaturan lain sama persis dengan model v4. Model dan dashboard v4 tidak diubah.
Pemakaian: python3 e1_latih.py A perencanaan | A pelaksanaan | B pelaksanaan
"""
import copy
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v4')
from ens3 import Ensemble3  # noqa: E402
import s2_model  # noqa: E402

OUT = '/mnt/project-files/eksperimen-r016-r068/'
BUANG = {'A': ['log_rasio_pagu_sejenis'],
         'B': ['rasio_realisasi', 'log_selisih_realisasi', 'selisih_rasio_realisasi_sejenis']}

eks, jalur = sys.argv[1], sys.argv[2]
d = pd.read_pickle(s2_model.V1 + 'tahap1.pkl')
F = s2_model.fitur(d, jalur).drop(columns=BUANG[eks])
kw = copy.deepcopy(s2_model.KONF[jalur]['model'])
if 'satu_arah' in kw:
    kw['satu_arah'] = {c: v for c, v in kw['satu_arah'].items() if c in F.columns}
print(eks, jalur, F.shape, list(F.columns), kw, flush=True)
m = Ensemble3(**kw).fit(F)
Ps = [mm.pct(m._potong(F.values.astype(float))) for mm in m.m]
sk = pd.DataFrame({k: np.mean([p[k] for p in Ps], axis=0) for k in ['IF', 'LOF', 'AE']}, index=F.index)
sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
sk.to_pickle(OUT + f'skor_{eks}_{jalur}.pkl')
print('selesai', flush=True)
