"""Eksplorasi jalur pelaksanaan (permintaan Tio 2026-10-29: "explore supaya hasilnya lebih bagus").
Model v5 di pelaksanaan hanya sedikit di atas acak (provinsi uji 5% teratas 27,7% vs acuan 25,6%).

Varian (hanya jalur pelaksanaan, pengaturan lain sama dengan v5):
  Q   : penskalaan quantile (seperti perencanaan), bukan standar.
  S   : rasio pagu sejenis dan rasio pagu satker satu arah (seperti perencanaan).
  QS  : Q + S.
  K   : fitur ringkas, pdn/umk biner dari RUP dan one-hot sumber transaksi dibuang.
  QSK : Q + S + K.
  L50 : LOF dengan 50 tetangga (bukan 20).
  P   : tambah dua fitur penyedia: jumlah paket dan jumlah satker yang dilayani penyedia (nasional, log).
        Dekat dengan RF5/RF6, jadi varian ini dinilai dengan RF1-RF4 saja (lihat x6).
Pemakaian: python3 x5_pelaksanaan.py <varian>. Keluaran: eksperimen-pelaksanaan/skor_<varian>.pkl
"""
import copy
import re
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
from ens3 import Ensemble3  # noqa: E402
import s2_model  # noqa: E402

O = '/mnt/project-files/model-v5/eksperimen-pelaksanaan/'
BENTUK = r'\b(PT|CV|UD|TB|TK|PD|FA|FIRMA|PERSERO|TBK|KOPERASI|KPRI|PO)\b'


def kunci(nama):
    s = re.sub(r'[^A-Z0-9 ]', ' ', str(nama).upper())
    return re.sub(r'\s+', ' ', re.sub(BENTUK, ' ', s)).strip()


varian = sys.argv[1]
d = pd.read_pickle(s2_model.DATA + 'tahap1.pkl')
info = d['info']
F = s2_model.fitur(d, 'pelaksanaan')
kw = copy.deepcopy(s2_model.KONF['pelaksanaan']['model'])
if 'Q' in varian:
    kw['skala'] = 'quantile'
if 'S' in varian:
    kw['satu_arah'] = {**kw['satu_arah'], 'log_rasio_pagu_sejenis': 'nol', 'log_rasio_pagu_satker': 'nol'}
if 'K' in varian:
    F = F.drop(columns=['pdn', 'umk'] + [c for c in F if c.startswith('sumber_')])
if varian == 'L50':
    kw['lof_k'] = 50
if varian == 'P':
    pny = info.penyedia.loc[F.index].map(kunci)
    ada = (info.penyedia.loc[F.index] != '-') & (pny != '')
    satker = (info.provinsi + '|' + info.nama_satuan_kerja).loc[F.index]
    F['log_paket_penyedia'] = np.where(ada, np.log10(pny.map(pny[ada].value_counts()).fillna(1)), 0.0)
    F['log_satker_penyedia'] = np.where(ada, np.log10(pny.map(satker[ada].groupby(pny[ada]).nunique()).fillna(1)), 0.0)
print(varian, F.shape, kw, flush=True)
m = Ensemble3(**kw).fit(F)
Ps = [mm.pct(m._potong(F.values.astype(float))) for mm in m.m]
sk = pd.DataFrame({k: np.mean([p[k] for p in Ps], axis=0) for k in ['IF', 'LOF', 'AE']}, index=F.index)
sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
sk.to_pickle(O + f'skor_{varian}.pkl')
print('selesai', flush=True)
