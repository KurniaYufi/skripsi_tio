"""J2: latih model RANCANGAN (5 seed, Ensemble3 seperti model sekarang). Pemakaian: python3 j2_latih_rancangan.py <varian>
Varian (nama = jalur_isi_tahun):
  ren_penuh_2025       semua fitur perencanaan rancangan (8)
  ren_lintas_2025      4 fitur dasar (sejenis = jenis saja) + 2 fitur tahun lalu
  ren_tanpalintas_TH   6 fitur tanpa tahun lalu (2024 dan 2025)
  pel_penuh_TH         7 fitur pelaksanaan rancangan (2024 dan 2025)
  pel_tanpapdnumk_2025 5 fitur (sejenis = jenis saja, tanpa selisih PDN/UMK)
Fitur rasio satu arah; fitur jarang (nama, tahun lalu, UMK, PDN) memakai skala fitur sejenis (skala_sama), pelajaran audit v5.
"""
import sys
import time
import numpy as np
import pandas as pd
sys.path.insert(0, '/mnt/project-files/model-v5')
import s2_model  # noqa: E402
from ens3 import Ensemble3  # noqa: E402
from lib import OUT  # noqa: E402

R = OUT + 'rancangan/'
PILIH = {
    'ren_penuh': None,
    'ren_lintas': ['log_pagu', 'log_rasio_pagu_jenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_satker',
                   'log_rasio_pagu_tahun_lalu', 'log_lonjakan_satker'],
    'ren_tanpalintas': ['log_pagu', 'log_rasio_pagu_jenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_satker',
                        'log_kekaburan_nama', 'umk_tidak_dicadangkan'],
    'pel_penuh': None,
    'pel_tanpapdnumk': ['log_pagu', 'log_rasio_pagu_jenis', 'log_rasio_pagu_satker', 'rasio_realisasi', 'log_selisih_realisasi'],
}
SATU_ARAH = ['log_rasio_pagu_jenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_satker', 'log_rasio_pagu_tahun_lalu',
             'log_lonjakan_satker']
JARANG = ['log_rasio_pagu_nama_satker', 'log_rasio_pagu_tahun_lalu', 'umk_tidak_dicadangkan', 'selisih_pdn', 'selisih_umk']


def konf(F, jalur):
    kw = dict(s2_model.KONF[jalur]['model'])
    kw['satu_arah'] = {c: 'nol' for c in SATU_ARAH if c in F}
    kw['skala_sama'] = {c: 'log_rasio_pagu_jenis' for c in JARANG if c in F}
    return kw


if __name__ == '__main__':
    v = sys.argv[1]
    nama, th = v.rsplit('_', 1)
    jalur = 'perencanaan' if nama.startswith('ren') else 'pelaksanaan'
    F = pd.read_pickle(R + f'fitur_{th}_{jalur}.pkl')
    if PILIH[nama]:
        F = F[PILIH[nama]]
    kw = konf(F, jalur)
    t = time.time()
    print(v, F.shape, list(F.columns), kw, flush=True)
    m = Ensemble3(**kw).fit(F)
    P = m.pct(F.values.astype(float))
    sk = pd.DataFrame(P, index=F.index)
    sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
    sk.to_pickle(R + f'skor_{v}.pkl')
    pd.to_pickle(dict(model=m, cols=list(F.columns)), R + f'model_{v}.pkl')
    print('selesai', v, round(time.time() - t), 'detik', flush=True)
