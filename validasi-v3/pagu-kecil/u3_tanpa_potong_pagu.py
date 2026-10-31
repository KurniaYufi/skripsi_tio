"""Uji lanjutan (2026-10-29) setelah model v4: LOF di jalur perencanaan v4 lemah di puncak daftar (P@50 2%) dan
200 teratas kurang stabil (Jaccard 0,41). Dugaan: pemotongan log_pagu di median membuat separuh paket punya nilai
log_pagu persis sama, sehingga kepadatan lokal (LOF) dan pemisahan acak (IF) terganggu.
Varian BS2 = batas Rp1 jt + hanya rasio pagu yang dipotong di 0 (log_pagu tidak dipotong; paket < Rp1 jt
sudah dibuang, jadi pagu kecil tidak lagi ekstrem). Dilatih dengan dua set seed untuk mengukur kestabilan.
Keluaran: skor_BS2.pkl, skor_BS2_seedB.pkl, pct_BS2.pkl (persentil IF/LOF/AE)
"""
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v4')
from s2_model import KONF, fitur  # noqa: E402
from ens3 import Ensemble3  # noqa: E402
SEEDS_B = [5, 6, 7, 8, 9]  # sama dengan s5_validasi.py

OUT = '/mnt/project-files/validasi-v3/pagu-kecil/'
d = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')
F = fitur(d, 'perencanaan')  # sudah memakai batas Rp1 jt
kw = dict(KONF['perencanaan']['model'])
kw['satu_arah'] = {'log_rasio_pagu_sejenis': 'nol', 'log_rasio_pagu_satker': 'nol'}
X = F.values.astype(float)
m = Ensemble3(**kw).fit(F)
P = m.pct(X)
pd.DataFrame(P, index=F.index).to_pickle(OUT + 'pct_BS2.pkl')
pd.Series(m.score(X), index=F.index).to_pickle(OUT + 'skor_BS2.pkl')
m2 = Ensemble3(seeds=SEEDS_B, **kw).fit(F)
pd.Series(m2.score(X), index=F.index).to_pickle(OUT + 'skor_BS2_seedB.pkl')
print('selesai', F.shape, flush=True)
