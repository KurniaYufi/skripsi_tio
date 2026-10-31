"""C: varian yang perlu latih ulang. Pemakaian: python3 c_latih.py <varian> [jalur ...]
Keluaran: skor/<varian>__<tahun>__<jalur>.pkl = DataFrame persentil IF/LOF/AE (rata-rata seed) untuk setiap paket.

Varian:
  lofk5 / lofk10 / lofk50 / lofk100   LOF saja dengan k berbeda (sekarang k = 20)
  lof100rb                            LOF k = 20, sampel latih 100 rb baris unik (sekarang 30 rb)
  gabung_tahun                        dilatih dengan data 2024 + 2025 sekaligus, lalu menilai tiap tahun
  silang_tahun                        model 2024 menilai 2025 dan model 2025 menilai 2024 (tanpa latih ulang)
  per_metode                          model terpisah untuk PL, E-Purchasing, dan metode lain; peringkat dalam kelompok
  plus_bulat                          + fitur kebulatan pagu (jumlah nol di belakang, tidak berkaitan dengan red flag)
  plus_ambang                         + jarak pagu ke ambang PL (SENGAJA bocor ke RF1/RF2, hanya sebagai pembanding)
  plus_kembar                         + jumlah paket lain bernama sama di satker (sebagian bocor ke RF3)
  tanpa_logpagu                       tanpa besar pagu mutlak (hanya pagu dibanding pembanding), agar proyek besar yang wajar
                                      tidak naik hanya karena besar
  per_metode_tanpa_logpagu            gabungan dua varian di atas
  seed10                              10 seed, bukan 5
"""
import copy
import os
import sys
import time

import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, '/mnt/project-files/model-v5')
import s2_model  # noqa: E402
from ens3 import Ensemble3  # noqa: E402
from x3_nama_satker import nama_dasar  # noqa: E402
from lib import muat, OUT  # noqa: E402

S = OUT + 'skor/'
os.makedirs(S, exist_ok=True)
AMBANG = {'2025': {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 400e6, 'Jasa Konsultansi': 100e6},
          '2024': {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 200e6, 'Jasa Konsultansi': 100e6}}
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:6.0f}s]', *a, flush=True)


def F_dasar(th, jalur):
    return muat(th)['H'][jalur]['F'].copy()


def konf(jalur):
    return copy.deepcopy(s2_model.KONF[jalur]['model'])


def pct(m, F):
    Ps = [mm.pct(m._potong(F.values.astype(float))) for mm in m.m]
    return pd.DataFrame({k: np.mean([p[k] for p in Ps], axis=0) for k in ['IF', 'LOF', 'AE']}, index=F.index)


def latih(F, kw, **ubah):
    kw = {**kw, **ubah}
    return Ensemble3(**kw).fit(F)


def lof_saja(F, kw, k, n_sampel=30000, seeds=(42, 1, 2, 3, 4)):
    """Sama dengan bagian LOF di ens2 (skala std, satu arah, skala_sama, sampel baris unik), dengan k / sampel lain."""
    X = F.values.astype(float).copy()
    cols = list(F.columns)
    for c, cara in kw.get('satu_arah', {}).items():
        X[:, cols.index(c)] = np.maximum(X[:, cols.index(c)], 0.0)
    sc = StandardScaler().fit(X)
    for c, acuan in kw.get('skala_sama', {}).items():
        sc.scale_[cols.index(c)] = sc.scale_[cols.index(acuan)]
    Z = sc.transform(X)
    uniq = np.unique(Z.round(6), axis=0)
    out = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        idx = rng.choice(len(uniq), size=min(n_sampel, len(uniq)), replace=False)
        lof = LocalOutlierFactor(n_neighbors=k, novelty=True, n_jobs=-1).fit(uniq[idx])
        ref = np.sort(-lof.score_samples(Z))
        out.append(np.searchsorted(ref, -lof.score_samples(Z), side='right') / len(ref))
    return pd.DataFrame({'LOF': np.mean(out, axis=0)}, index=F.index)


def tambah(th, jalur, F, jenis):
    info = muat(th)['info'].loc[F.index]
    if jenis == 'bulat':
        p = info.pagu.round().astype('int64').astype(str)
        nol = p.str.len() - p.str.rstrip('0').str.len()
        F['kebulatan_pagu'] = nol / p.str.len()
    elif jenis == 'ambang':
        amb = info.jenis.map(AMBANG[th]).fillna(200e6)
        F['jarak_ambang_pl'] = np.where(info.metode_pengadaan == 'Pengadaan Langsung',
                                        np.log10(info.pagu / amb).clip(-2, 1), -2.0)
    elif jenis == 'kembar':
        semua = muat(th)['info']
        kunci = semua.provinsi + '|' + semua.nama_satuan_kerja + '|' + semua.jenis + '|' + semua.nama_paket.map(nama_dasar)
        F['log_jumlah_kembar_satker'] = np.log10(kunci.map(kunci.value_counts())).loc[F.index]
    return F


def simpan(df, varian, th, jalur):
    df.to_pickle(S + f'{varian}__{th}__{jalur}.pkl')
    log('simpan', varian, th, jalur, df.shape)


def jalankan(varian, jalur):
    kw = konf(jalur)
    if varian.startswith('lofk') or varian == 'lof100rb':
        k = 20 if varian == 'lof100rb' else int(varian[4:])
        n = 100000 if varian == 'lof100rb' else 30000
        for th in ['2024', '2025']:
            simpan(lof_saja(F_dasar(th, jalur), kw, k, n), varian, th, jalur)
    elif varian == 'gabung_tahun':
        F = {th: F_dasar(th, jalur) for th in ['2024', '2025']}
        Fg = pd.concat([F['2024'].set_axis('24_' + F['2024'].index.astype(str)),
                        F['2025'].set_axis('25_' + F['2025'].index.astype(str))])
        m = latih(Fg, kw)
        for th in ['2024', '2025']:
            simpan(pct(m, F[th]), varian, th, jalur)
    elif varian == 'silang_tahun':
        for latih_th, nilai_th in [('2024', '2025'), ('2025', '2024')]:
            m = muat(latih_th)['H'][jalur]['model']
            simpan(pct(m, F_dasar(nilai_th, jalur)), varian, nilai_th, jalur)
    elif varian == 'per_metode':
        for th in ['2024', '2025']:
            F = F_dasar(th, jalur)
            met = muat(th)['info'].metode_pengadaan.loc[F.index]
            grp = np.where(met == 'Pengadaan Langsung', 'PL', np.where(met == 'E-Purchasing', 'EP', 'lain'))
            hasil = []
            for g in ['PL', 'EP', 'lain']:
                Fg = F[grp == g]
                hasil.append(pct(latih(Fg, kw), Fg))
                log(th, jalur, g, len(Fg))
            simpan(pd.concat(hasil).loc[F.index], varian, th, jalur)
    elif varian.startswith('plus_'):
        jenis = varian[5:]
        for th in ['2024', '2025']:
            F = tambah(th, jalur, F_dasar(th, jalur), jenis)
            simpan(pct(latih(F, kw), F), varian, th, jalur)
    elif varian == 'tanpa_logpagu':
        for th in ['2024', '2025']:
            F = F_dasar(th, jalur).drop(columns=['log_pagu'])
            simpan(pct(latih(F, kw), F), varian, th, jalur)
    elif varian == 'per_metode_tanpa_logpagu':
        for th in ['2024', '2025']:
            F = F_dasar(th, jalur).drop(columns=['log_pagu'])
            met = muat(th)['info'].metode_pengadaan.loc[F.index]
            grp = np.where(met == 'Pengadaan Langsung', 'PL', np.where(met == 'E-Purchasing', 'EP', 'lain'))
            simpan(pd.concat([pct(latih(F[grp == g], kw), F[grp == g]) for g in ['PL', 'EP', 'lain']]).loc[F.index],
                   varian, th, jalur)
    elif varian == 'seed10':
        for th in ['2024', '2025']:
            F = F_dasar(th, jalur)
            simpan(pct(latih(F, kw, seeds=[42, 1, 2, 3, 4, 5, 6, 7, 8, 9]), F), varian, th, jalur)
    else:
        sys.exit('varian tidak dikenal: ' + varian)


if __name__ == '__main__':
    v = sys.argv[1]
    for j in (sys.argv[2:] or ['perencanaan', 'pelaksanaan']):
        log('mulai', v, j)
        jalankan(v, j)
