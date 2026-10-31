"""Uji paket pagu kecil (2026-10-29), jalur perencanaan saja.

Masalah: 22,5% dari 200 teratas model v3 berpagu < Rp1 jt. Fitur pagu berupa rasio log, sehingga pagu ratusan
kali lebih kecil dari biasanya dianggap sama tidak lazimnya dengan ratusan kali lebih besar.
Varian (argumen 1):
  B  = batas bawah: paket berpagu < Rp1 jt tidak ikut model.
  S  = skor satu arah: rasio pagu (sejenis, satker) dipotong di 0 dan log_pagu dipotong di median,
       sehingga hanya pagu yang LEBIH BESAR dari biasanya yang bisa menaikkan skor.
  BS = keduanya.
Pengaturan lain sama dengan model v3 (fitur varian E, quantile, 5 seed). Keluaran: skor_<varian>.pkl
"""
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v3')
from s2_model import KONF, fitur  # noqa: E402
from ens3 import Ensemble3  # noqa: E402

varian = sys.argv[1]
OUT = '/mnt/project-files/validasi-v3/pagu-kecil/'
d = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')
F = fitur(d, 'perencanaan')
if 'B' in varian:
    F = F[d['info'].pagu.loc[F.index] >= 1e6]
if 'S' in varian:
    for c in ['log_rasio_pagu_sejenis', 'log_rasio_pagu_satker']:
        F[c] = F[c].clip(lower=0)
    F['log_pagu'] = F['log_pagu'].clip(lower=F['log_pagu'].median())
m = Ensemble3(**KONF['perencanaan']['model']).fit(F)
s = pd.Series(m.score(F.values.astype(float)), index=F.index, name=varian)
s.to_pickle(OUT + f'skor_{varian}.pkl')
print(varian, F.shape, 'selesai', flush=True)
