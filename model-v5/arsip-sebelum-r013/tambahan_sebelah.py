"""Tambahan dari project "TRAIN ANOMALY DETECTION" yang lolos uji (eksperimen-lanjutan/hasil-ide-project-sebelah.md),
diterapkan atas permintaan Tio 2026-10-31. Definisi sama persis dengan eksperimen-lanjutan/k1_fitur_sebelah.py.

Fitur jalur pelaksanaan:
  log_rasio_kebiasaan_penyedia = log10(realisasi) - median log10 realisasi semua paket penyedia itu (jalur pelaksanaan).
  Bernilai 0 bila penyedia kosong/"-" atau punya < 3 paket. Tidak bocor ke red flag mana pun (AUC <= 0,60).
Red flag jalur pelaksanaan (hanya untuk menilai, tidak masuk model):
  e3_metode_berubah      metode realisasi berbeda dari metode RUP (Perpres Ps. 18-19, 22; OCP R012)
  e4_pdn_kurang          RUP menyatakan PDN, tetapi porsi nilai PDN realisasi < 50% (Ps. 66)
  e5_umk_kurang          RUP dicadangkan untuk UMK, tetapi porsi nilai UMK realisasi < 50% (Ps. 65)
  e6_penyedia_kuasai     penyedia utama menguasai >= 50% paket non-katalog satker (satker >= 5 paket; Ps. 7(1), OCP R040)
"""
import numpy as np
import pandas as pd


def satker_dasar(info):
    return info.provinsi + '|' + info.nama_satuan_kerja.str.replace(r'\s*-\s*[\d\.]+$', '', regex=True).str.upper().str.strip()


def pny(s):
    s = s.fillna('-').str.upper().str.replace(r'[^A-Z0-9 ]', ' ', regex=True)
    s = s.str.replace(r'\b(PT|CV|UD|TB|TOKO|KOPERASI|PERSERO|TBK)\b', ' ', regex=True)
    return s.str.split().str.join(' ').fillna('')


def kebiasaan_penyedia(info, idx):
    """(nilai fitur, aktif, median realisasi penyedia, jumlah paket penyedia) untuk paket idx."""
    ip = info.loc[idx]
    p = pny(ip.penyedia)
    ada = ~p.isin(['', '-'])
    lr = np.log10(ip.realisasi)
    med = lr[ada].groupby(p[ada]).median()
    cnt = p[ada].value_counts()
    aktif = ada & (p.map(cnt).fillna(0) >= 3)
    nilai = (lr - p.map(med)).where(aktif, 0.0).fillna(0.0)
    return nilai, aktif, (10 ** p.map(med)).where(aktif), p.map(cnt).fillna(0).astype(int)


def rf_sebelah(d, idx):
    i = d['info']
    ip = i.loc[idx]
    fp = d['f_pel'].reindex(idx)
    mr = ip.metode_realisasi.fillna('-')
    Y = pd.DataFrame(index=i.index)
    v = {'e3_metode_berubah': (~mr.isin(['-', 'Dikecualikan'])) & (mr != ip.metode_pengadaan),
         'e4_pdn_kurang': (ip.produk_dalam_negeri == 'Ya') & (fp.porsi_pdn.fillna(1) < 0.5),
         'e5_umk_kurang': (ip.status_umk == 'Ya') & (fp.porsi_umk.fillna(1) < 0.5)}
    sk, p = satker_dasar(ip), pny(ip.penyedia)
    nonkat = ~ip.sumber_transaksi.fillna('').str.startswith('E-Katalog') & ~p.isin(['', '-'])
    n_sk = sk[nonkat].value_counts()
    top = p[nonkat].groupby(sk[nonkat]).agg(lambda s: s.value_counts().iloc[0] / len(s))
    utama = p[nonkat].groupby(sk[nonkat]).agg(lambda s: s.value_counts().index[0])
    v['e6_penyedia_kuasai'] = nonkat & sk.map(n_sk).ge(5) & sk.map(top).ge(0.5) & (p == sk.map(utama))
    for c, s in v.items():
        Y[c] = False
        Y.loc[idx, c] = s.fillna(False).values
    return Y.astype(bool)
