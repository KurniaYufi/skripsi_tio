"""K3: latih varian model sekarang + ide project sebelah. Pemakaian: python3 k3_latih_sebelah.py <varian> <tahun>
Pengaturan model sama dengan model sekarang (Ensemble3, 5 seed, s2_model.KONF), kecuali yang diubah varian.
Keluaran: sebelah/skor_<varian>_<tahun>.pkl (persentil IF/LOF/AE rata-rata seed + Ensemble).

Varian perencanaan (dasar: log_pagu, sejenis, satker, nama):
  ren_pangsa / ren_kembar / ren_nonkomp   dasar + satu fitur sebelah
  ren_zrank     sejenis & satker diganti posisi peringkat dua arah (cara project sebelah)
  ren_robust    fitur dasar, penskalaan RobustScaler dipotong +-10 (cara project sebelah)
  ren_sebelah   6 fitur project sebelah apa adanya
Varian pelaksanaan (dasar: log_pagu, sejenis, satker, rasio_realisasi, selisih):
  pel_zrasio    rasio_realisasi diganti posisi rasio di jenis x metode x kuintil pagu
  pel_jangkauan / pel_kebiasaan / pel_pangsa / pel_nonkomp / pel_kembar   dasar + satu fitur sebelah
  pel_kebzr     gabungan pel_kebiasaan + pel_zrasio (dua fitur yang tidak bocor)
  pel_robust    RobustScaler dipotong +-10
  pel_sebelah   9 fitur project sebelah apa adanya
"""
import copy
import sys
import time
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
sys.path.insert(0, '/mnt/project-files/model-v5')
import s2_model  # noqa: E402
from ens3 import Ensemble3  # noqa: E402
from lib import muat  # noqa: E402
from k1_fitur_sebelah import R  # noqa: E402

SEB6 = ['k_z_sejenis', 'k_z_satker', 'k_pangsa_satker', 'k_bulat', 'k_kembar_satker', 'k_nonkomp_satker']
TAMBAH = {'pangsa': 'k_pangsa_satker', 'kembar': 'k_kembar_satker', 'nonkomp': 'k_nonkomp_satker',
          'jangkauan': 'k_jangkauan', 'kebiasaan': 'k_kebiasaan'}


def siapkan(v, th):
    jalur = 'perencanaan' if v.startswith('ren') else 'pelaksanaan'
    F = muat(th)['H'][jalur]['F'].copy()
    X = pd.read_pickle(R + f'fitur_{th}.pkl').loc[F.index]
    kw = copy.deepcopy(s2_model.KONF[jalur]['model'])
    isi = v.split('_', 1)[1]
    if isi in TAMBAH:
        F[TAMBAH[isi]] = X[TAMBAH[isi]]
    elif isi == 'zrank':
        F['log_rasio_pagu_sejenis'] = X.k_z_sejenis
        F['log_rasio_pagu_satker'] = X.k_z_satker
        for c in ['log_rasio_pagu_sejenis', 'log_rasio_pagu_satker']:
            kw['satu_arah'].pop(c, None)  # dua arah, seperti project sebelah
    elif isi == 'kebzr':  # gabungan dua fitur yang tidak bocor: kebiasaan penyedia + posisi rasio realisasi
        F['rasio_realisasi'] = X.k_z_rasio
        F['k_kebiasaan'] = X.k_kebiasaan
    elif isi == 'zrasio':
        F['rasio_realisasi'] = X.k_z_rasio
    elif isi == 'sebelah':
        F = X[SEB6 + (['k_z_rasio', 'k_jangkauan', 'k_kebiasaan'] if jalur == 'pelaksanaan' else [])].copy()
        kw['satu_arah'], kw['skala_sama'] = {}, {}
    elif isi == 'robust':
        for c in kw['satu_arah']:
            F[c] = F[c].clip(lower=0)
        F = pd.DataFrame(np.clip(RobustScaler().fit_transform(F), -10, 10), index=F.index, columns=F.columns)
        kw['satu_arah'], kw['skala_sama'] = {}, {}
    else:
        raise SystemExit('varian tidak dikenal: ' + v)
    return F, kw


if __name__ == '__main__':
    v, th = sys.argv[1], sys.argv[2]
    F, kw = siapkan(v, th)
    t = time.time()
    print(v, th, F.shape, list(F.columns), kw, flush=True)
    m = Ensemble3(**kw).fit(F)
    sk = pd.DataFrame(m.pct(F.values.astype(float)), index=F.index)
    sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
    sk.to_pickle(R + f'skor_{v}_{th}.pkl')
    pd.to_pickle(dict(model=m, cols=list(F.columns)), R + f'model_{v}_{th}.pkl')
    print('selesai', v, th, round(time.time() - t), 'detik', flush=True)
