"""K1: fitur, red flag, dan metode dari project "TRAIN ANOMALY DETECTION" yang dihitung ulang di data project ini
(permintaan Tio 2026-10-31: "coba semua yang sekira bisa improve project ini").
Keluaran: sebelah/fitur_{th}.pkl (semua paket) dan sebelah/rf_{th}.pkl.

Fitur kandidat (definisi mengikuti laporan project sebelah):
  k_pangsa_satker   log10(pagu / total pagu satker)
  k_kembar_satker   log10(banyak paket di satker dengan pagu persis sama)
  k_bulat           jumlah angka nol di belakang / (jumlah digit - 1)
  k_nonkomp_satker  porsi nilai pagu satker yang memakai Pengadaan/Penunjukan Langsung
  k_z_sejenis       posisi peringkat log pagu di jenis x metode, Phi^-1((r - 0,5)/n); cadangan jenis bila < 30 paket (dua arah)
  k_z_satker        posisi peringkat log pagu di satker; 0 bila satker < 5 paket (dua arah)
  k_z_rasio         (pelaksanaan) posisi log(realisasi/pagu) di jenis x metode x kuintil pagu
  k_jangkauan       (pelaksanaan) log10(banyak satker yang dilayani penyedia), dipotong di persentil 95; 0 bila tanpa penyedia
  k_kebiasaan       (pelaksanaan) log10(realisasi) - median log10 realisasi paket penyedia itu; 0 bila penyedia < 3 paket
Red flag kandidat:
  P4 Penunjukan Langsung dengan pagu > ambang PL;  P5 paket <= Rp15 M (Barang/Konstruksi/Jasa Lainnya) tidak dicadangkan UMK;
  P6 RUP bukan PDN;  E3 metode realisasi != metode RUP;  E4 RUP PDN tetapi PDN realisasi < 50%;
  E5 RUP UMK tetapi UMK realisasi < 50%;  E6 penyedia menguasai >= 50% paket non-katalog satker (satker >= 5 paket);
  C4 R050 (sudah ada): penyedia > 40% nilai realisasi satker x jenis.
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import norm
from lib import muat, OUT
from i_kandidat_rf import satker_dasar, pny, T1, AMB

R = OUT + 'sebelah/'
os.makedirs(R, exist_ok=True)


def zrank(v, grup):
    r = v.groupby(grup).rank(method='average')
    n = v.groupby(grup).transform('size')
    return pd.Series(norm.ppf((r - 0.5) / n), index=v.index)


def bulat(p):
    s = p.round().astype('int64').astype(str)
    nol = s.str.len() - s.str.rstrip('0').str.len()
    return (nol / (s.str.len() - 1).clip(lower=1)).astype(float)


def fitur(th):
    D = muat(th); i = D['info']; d1 = pd.read_pickle(T1[th]); fp = d1['f_pel']
    sk = satker_dasar(i)
    X = pd.DataFrame(index=i.index)
    X['k_pangsa_satker'] = np.log10(i.pagu / i.pagu.groupby(sk).transform('sum'))
    X['k_kembar_satker'] = np.log10(i.pagu.groupby([sk, i.pagu]).transform('size').astype(float))
    X['k_bulat'] = bulat(i.pagu)
    nk = i.metode_pengadaan.isin(['Pengadaan Langsung', 'Penunjukan Langsung'])
    X['k_nonkomp_satker'] = (i.pagu * nk).groupby(sk).transform('sum') / i.pagu.groupby(sk).transform('sum')
    lp = np.log10(i.pagu)
    jm = i.jenis + '|' + i.metode_pengadaan
    n_jm = jm.map(jm.value_counts())
    g = jm.where(n_jm >= 30, i.jenis)
    X['k_z_sejenis'] = zrank(lp, g)
    n_sk = sk.map(sk.value_counts())
    X['k_z_satker'] = zrank(lp, sk).where(n_sk >= 5, 0.0)
    # Pelaksanaan: hanya paket di jalur pelaksanaan
    idx = D['H']['pelaksanaan']['F'].index
    ip = i.loc[idx]
    q = pd.qcut(np.log10(ip.pagu), 5, labels=False, duplicates='drop').astype(str)
    X['k_z_rasio'] = np.nan
    X.loc[idx, 'k_z_rasio'] = zrank(np.log10(ip.realisasi / ip.pagu), ip.jenis + '|' + ip.metode_pengadaan + '|' + q)
    p = pny(ip.penyedia); ada = ~p.isin(['', '-'])
    jang = sk.loc[idx][ada].groupby(p[ada]).nunique()
    jl = np.log10(p.map(jang).fillna(1).astype(float)).where(ada, 0.0)
    X['k_jangkauan'] = np.nan
    X.loc[idx, 'k_jangkauan'] = jl.clip(upper=jl[ada].quantile(0.95))
    lr = np.log10(ip.realisasi)
    med = lr[ada].groupby(p[ada]).median(); cnt = p[ada].value_counts()
    keb = (lr - p.map(med)).where(ada & (p.map(cnt) >= 3), 0.0).fillna(0.0)
    X['k_kebiasaan'] = np.nan
    X.loc[idx, 'k_kebiasaan'] = keb
    return X


def red_flag(th):
    D = muat(th); i = D['info']; fp = pd.read_pickle(T1[th])['f_pel']
    amb = i.jenis.map(AMB[th])
    Y = pd.DataFrame(index=i.index)
    Y['P4_penl_lewat_ambang'] = (i.metode_pengadaan == 'Penunjukan Langsung') & (i.pagu > amb.fillna(np.inf))
    Y['P5_tidak_dicadangkan_umk'] = i.jenis.isin(['Barang', 'Pekerjaan Konstruksi', 'Jasa Lainnya']) & (i.pagu <= 15e9) & (i.status_umk != 'Ya')
    Y['P6_bukan_pdn'] = i.produk_dalam_negeri != 'Ya'
    idx = D['H']['pelaksanaan']['F'].index
    ip = i.loc[idx]
    mr = ip.metode_realisasi.fillna('-')
    e3 = (~mr.isin(['-', 'Dikecualikan'])) & (mr != ip.metode_pengadaan)
    pf = fp.reindex(idx)
    e4 = (ip.produk_dalam_negeri == 'Ya') & (pf.porsi_pdn.fillna(1) < 0.5)
    e5 = (ip.status_umk == 'Ya') & (pf.porsi_umk.fillna(1) < 0.5)
    sk = satker_dasar(ip); p = pny(ip.penyedia)
    nonkat = ~ip.sumber_transaksi.fillna('').str.startswith('E-Katalog') & ~p.isin(['', '-'])
    n_sk = sk[nonkat].value_counts()
    top = p[nonkat].groupby(sk[nonkat]).agg(lambda s: s.value_counts().iloc[0] / len(s))
    utama = p[nonkat].groupby(sk[nonkat]).agg(lambda s: s.value_counts().index[0])
    e6 = nonkat & sk.map(n_sk).ge(5) & sk.map(top).ge(0.5) & (p == sk.map(utama))
    for c, v in [('E3_metode_berubah', e3), ('E4_pdn_kurang', e4), ('E5_umk_kurang', e5), ('E6_penyedia_kuasai_satker', e6)]:
        Y[c] = False
        Y.loc[idx, c] = v.fillna(False).values
    K = pd.read_pickle(OUT + f'kandidat_rf_{th}.pkl')
    Y['C4_R050_satker_jenis'] = K.C4_R050_pangsa_satker_jenis.reindex(i.index).fillna(False)
    return Y.astype(bool)


if __name__ == '__main__':
    pd.set_option('display.width', 250)
    for th in ['2024', '2025']:
        X = fitur(th); Y = red_flag(th)
        X.to_pickle(R + f'fitur_{th}.pkl'); Y.to_pickle(R + f'rf_{th}.pkl')
        print('=====', th)
        print(X.describe(percentiles=[.05, .5, .95]).T.round(3).to_string())
        print('porsi nol:', (X == 0).mean().round(3).to_dict())
        print('red flag (jumlah):', Y.sum().to_dict())
