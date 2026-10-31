"""Alat bersama eksperimen lanjutan (permintaan Tio 2026-10-30): data per tahun, evaluasi yang adil, dan pembanding.

Aturan uji (ditetapkan SEBELUM melihat hasil eksperimen):
- Tahun 2024 = tahun pengembangan (memilih varian). Tahun 2025 = tahun uji (hanya untuk mengecek pilihan dari 2024).
- Di 2025 dipakai juga provinsi uji (provinsi di luar provinsi_pilih.json).
- Ukuran utama: lipat red flag di 5% teratas dibanding acuan, dihitung HANYA pada paket yang red flag-nya bisa berlaku
  (perencanaan: Pengadaan Langsung + Penunjukan Langsung; pelaksanaan: per red flag), dengan dan tanpa RF2.
- Signifikansi: uji hipergeometrik (5% teratas dibanding undian acak dari kelompok yang sama).
"""
import json
import warnings
import sys

import numpy as np
import pandas as pd
from scipy.stats import hypergeom
from sklearn.metrics import average_precision_score, roc_auc_score

warnings.filterwarnings('ignore')

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401  (untuk membuka pickle)

DIR = {'2025': '/mnt/project-files/model-v5/', '2024': '/mnt/project-files/model-v5-2024/'}
OUT = '/mnt/project-files/eksperimen-lanjutan/'
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
RF2 = 'rf2_pl_lewat_ambang'
PL, PENL = 'Pengadaan Langsung', 'Penunjukan Langsung'
_cache = {}


def muat(th):
    if th not in _cache:
        t1 = pd.read_pickle(DIR[th] + 'tahap1.pkl')
        H = pd.read_pickle(DIR[th] + 'tahap2.pkl')
        _cache[th] = dict(info=t1['info'], rf=t1['rf'], H=H)
    return _cache[th]


def berlaku(info, flag):
    """Paket yang secara definisi BISA terkena red flag ini."""
    m = info.metode_pengadaan
    if flag in ('rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket'):
        return m == PL
    if flag == 'rf4_penunjukan_langsung':
        return m == PENL
    return info.penyedia.fillna('-') != '-'  # RF5, RF6: butuh penyedia


def urut(skor):
    """Indeks dari skor tertinggi. Skor kembar diurutkan ACAK (bukan menurut urutan kode RUP), agar kelompok paket
    berskor sama tidak menguntungkan/merugikan secara kebetulan."""
    r = np.random.default_rng(0).random(len(skor))
    return skor.index[np.lexsort((r, -skor.values))]


def _p5(skor, y):
    """Proporsi ber-red flag di 5% teratas, acuan, lipat, p hipergeometrik."""
    o = urut(skor)
    n = max(int(len(o) * 0.05), 1)
    x = int(y.loc[o[:n]].sum())
    N, Kp = len(y), int(y.sum())
    a = Kp / N if N else np.nan
    return dict(n=N, p5=x / n, acuan=a, lipat=(x / n) / a if a else np.nan, p=float(hypergeom.sf(x - 1, N, Kp, n)))


def ukur(skor, th, jalur, provinsi='semua', buang_rf2=False):
    """Semua ukuran untuk satu skor (pd.Series, makin besar makin tidak lazim).
    buang_rf2: paket ber-RF2 dikeluarkan dari daftar (bukan hanya dari label), karena RF2 = pagu > ambang PL sudah
    terbaca langsung dari fitur pagu. Pertanyaannya jadi: di antara paket yang TIDAK kena RF2, apakah model menemukan
    red flag lain lebih sering daripada acak?"""
    D = muat(th)
    if buang_rf2:
        skor = skor[~D['rf'].loc[skor.index, RF2]]
    info, rf = D['info'].loc[skor.index], D['rf'].loc[skor.index]
    flags = D['H'][jalur]['flags']
    if provinsi == 'uji':
        k = ~info.provinsi.isin(DEV)
        skor, info, rf = skor[k], info[k], rf[k]
    R = rf[flags]
    o = {}
    semua = R.any(axis=1)
    tanpa2 = R.drop(columns=[RF2]).any(axis=1)
    order = urut(skor)
    for K in [100, 200]:
        o[f'P@{K}'] = semua.loc[order[:K]].mean()
        o[f'P@{K} tanpa RF2'] = tanpa2.loc[order[:K]].mean()
    for nama, y in [('semua', semua), ('tanpa RF2', tanpa2)]:
        r = _p5(skor, y)
        o[f'5%: {nama}'] = r['p5']
        o[f'acuan: {nama}'] = r['acuan']
        o[f'lipat: {nama}'] = r['lipat']
    # Paket yang red flag-nya berlaku
    E = pd.concat([berlaku(info, f) for f in flags], axis=1).any(axis=1)
    for nama, y in [('semua', semua), ('tanpa RF2', tanpa2)]:
        r = _p5(skor[E], y[E])
        o[f'berlaku 5%: {nama}'] = r['p5']
        o[f'berlaku acuan: {nama}'] = r['acuan']
        o[f'berlaku lipat: {nama}'] = r['lipat']
        o[f'berlaku p: {nama}'] = r['p']
        o[f'berlaku AUC: {nama}'] = roc_auc_score(y[E], skor[E]) if 0 < y[E].mean() < 1 else np.nan
    # Per red flag, di paket yang red flag itu berlaku
    for f in flags:
        e = berlaku(info, f)
        if e.sum() < 50 or R.loc[e, f].sum() == 0:
            continue
        r = _p5(skor[e], R.loc[e, f])
        o[f'{f}: lipat'] = r['lipat']
        o[f'{f}: AUC'] = roc_auc_score(R.loc[e, f], skor[e])
    o['AP semua'] = average_precision_score(semua, skor)
    o['porsi 200 teratas yang red flag-nya berlaku'] = E.loc[order[:200]].mean()
    return o


def pembanding(th, jalur):
    """Skor sederhana TANPA model, untuk menjawab 'apa bedanya dengan tanpa model'."""
    D = muat(th)
    F = D['H'][jalur]['F']
    rng = np.random.default_rng(0)
    b = {'acak': pd.Series(rng.random(len(F)), index=F.index),
         'urut pagu': F.log_pagu,
         'urut pagu dibanding sejenis': F.log_rasio_pagu_sejenis,
         'urut pagu dibanding satker': F.log_rasio_pagu_satker}
    if 'rasio_realisasi' in F:
        b['urut selisih realisasi'] = (F.rasio_realisasi - 1).abs()
    Z = (F - F.mean()) / F.std()
    b['rata-rata skor-z fitur (aturan sederhana)'] = Z.clip(lower=0).mean(axis=1)
    return b


def skor_model(th, jalur):
    sk = muat(th)['H'][jalur]['skor']
    return {'Ensemble (model sekarang)': sk.Ensemble, 'IF saja': sk.IF, 'LOF saja': sk.LOF, 'AE saja': sk.AE}


def tabel(hasil, kolom=None):
    t = pd.DataFrame(hasil).T
    return t[kolom] if kolom else t
