"""Eksperimen satker kecil (permintaan Tio 2026-10-29): satker yang hanya punya 1-4 paket menguasai puncak perencanaan
(0,4% paket, tetapi 58% dari 50 teratas), karena porsi pagu satker = 100% dan jumlah paket = 1 terlihat ekstrem.

Varian (dilatih di data v5, pengaturan lain sama dengan v4/v5):
  N<n> : untuk satker dengan paket < n, porsi_pagu_satker diganti median seluruh paket (netral) dan
         log_rasio_pagu_satker = 0, karena "median satker" dari 1-4 paket tidak bermakna;
         log_jumlah_paket_satker satu arah (dipotong di median): satker kecil tidak dianggap aneh.
  N<n>-tanpaJ : sama, tetapi jumlah paket satker tidak dipotong.
  D   : porsi_pagu_satker dan log_jumlah_paket_satker dibuang; konteks satker cukup dari log_rasio_pagu_satker
        (satu arah), yang bernilai 0 (wajar) untuk satker 1 paket.
  R   : porsi_pagu_satker diganti log10(pagu / rata-rata pagu satker) satu arah (porsi dibanding bagian rata-rata,
        untuk satker 1 paket = 0), log_jumlah_paket_satker dibuang.
  X<n>: paket di satker dengan paket < n tidak ikut model (konteks satker tidak cukup).
Pemakaian: python3 x1_satker_kecil.py <jalur> <varian>   (varian: N3, N5, N10, N5-tanpaJ)
"""
import copy
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
from ens3 import Ensemble3  # noqa: E402
import s2_model  # noqa: E402

O = '/mnt/project-files/model-v5/eksperimen-satker-kecil/'
jalur, varian = sys.argv[1], sys.argv[2]
n_min = int(varian.split('-')[0][1:]) if varian[0] in 'NX' else 0
d = pd.read_pickle(s2_model.DATA + 'tahap1.pkl')
info = d['info']
sat = info.provinsi + '|' + info.nama_satuan_kerja
n_paket = sat.map(sat.value_counts())
F = s2_model.fitur(d, jalur)
kecil = (n_paket.loc[F.index] < n_min).values
kw = copy.deepcopy(s2_model.KONF[jalur]['model'])
if varian[0] == 'N':
    F.loc[kecil, 'porsi_pagu_satker'] = F.porsi_pagu_satker.median()
    F.loc[kecil, 'log_rasio_pagu_satker'] = 0.0
    if 'tanpaJ' not in varian:
        kw['satu_arah'] = {**kw.get('satu_arah', {}), 'log_jumlah_paket_satker': 'median'}
elif varian == 'D':
    F = F.drop(columns=['porsi_pagu_satker', 'log_jumlah_paket_satker'])
elif varian == 'R':
    rata = info.pagu.groupby(sat).transform('mean').loc[F.index]
    F['porsi_pagu_satker'] = np.log10(info.pagu.loc[F.index] / rata)
    F = F.drop(columns=['log_jumlah_paket_satker'])
    kw['satu_arah'] = {**kw.get('satu_arah', {}), 'porsi_pagu_satker': 'nol'}
elif varian[0] == 'X':
    F = F[~kecil]
print(jalur, varian, F.shape, 'paket satker kecil:', int(kecil.sum()), kw, flush=True)
m = Ensemble3(**kw).fit(F)
Ps = [mm.pct(m._potong(F.values.astype(float))) for mm in m.m]
sk = pd.DataFrame({k: np.mean([p[k] for p in Ps], axis=0) for k in ['IF', 'LOF', 'AE']}, index=F.index)
sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
sk.to_pickle(O + f'skor_{jalur}_{varian}.pkl')
print('selesai', flush=True)
