"""Validasi v3, bagian 6b: tambahan varian E (profil metode satker dibuang) untuk jalur perencanaan.

Ditambahkan setelah r6 karena tidak ada varian perencanaan yang lolos syarat; E adalah opsi "versi ketat"
yang sudah diusulkan di ringkasan eksplorasi v2, tetapi di r6 hanya diuji dalam gabungan NE.
Protokol dan aturan sama persis dengan r6 di bawah ini.

Asal: bagian 6, pemilihan konfigurasi v3 dengan red flag yang diperbaiki.

Red flag v3 (hasil r1): RF1 untuk pekerjaan konstruksi memakai dua jendela (180-200 jt aturan lama dan
360-400 jt aturan baru, karena 2025 tahun peralihan Perpres 46/2025); RF5 memakai definisi OCP R040
(porsi nilai satu penyedia > 40% dari realisasi satker, satker >= 5 paket). RF2, RF3, RF4, RF6 tetap.

Kandidat fitur:
  N = tambah "pagu dibanding paket bernama serupa" (f1_nama_serupa.py)
  L = profil metode satker dihitung tanpa paket itu sendiri (leave-one-out), agar metode paket
      itu sendiri tidak ikut masuk ke fiturnya
  E = profil metode satker dibuang
  U = PDN/UMK dibuang (pelaksanaan), Q = penskalaan quantile (pelaksanaan)

Aturan pemilihan (ditetapkan sebelum melihat hasil):
1. Skor tiap konfigurasi = rata-rata skor ensemble dari 3 seed (v3 akan memakai rata-rata seed).
2. Syarat: satu satker paling banyak 20 paket di 200 teratas, DAN rata-rata P@K tanpa red flag 4 di
   provinsi pilih harus di atas acuannya (model harus lebih baik dari acak untuk red flag selain
   penunjukan langsung, yang bisa terbawa lewat profil satker).
3. Dari yang lolos, dipilih rata-rata P@50/100/200 tertinggi di provinsi pilih. Konfigurasi baru
   menggantikan v2 hanya bila unggul >= 1 poin persen.
4. Provinsi uji hanya dilaporkan.
"""
import json
import sys
import time
import numpy as np
import pandas as pd
from scipy.stats import hypergeom

sys.path.insert(0, '/mnt/project-files/model-v2')
import ens2  # noqa: E402
from s2_model import KONF, fitur  # noqa: E402

V1 = '/mnt/project-files/model-v1/'
OUT = '/mnt/project-files/validasi-v3/'
T0 = time.time()
d = pd.read_pickle(V1 + 'tahap1.pkl')
info, rf = d['info'], d['rf']
satker = info.provinsi + '|' + info.nama_satuan_kerja
DEV = set(json.load(open(V1 + 'eksplorasi/provinsi_pilih.json')))
SEEDS = [42, 1, 2]
KS = [50, 100, 200]
V = pd.read_pickle(OUT + 'r1_variasi_red_flag.pkl')
NAMA = pd.read_pickle(OUT + 'fitur_nama_serupa.pkl')['log_rasio_pagu_nama_serupa']

# ---- red flag v3
pl = info.metode_pengadaan == 'Pengadaan Langsung'
rf3 = rf.copy()
rf3['rf1_pl_dekat_ambang'] = rf['rf1_pl_dekat_ambang'] | (pl & (info.jenis == 'Pekerjaan Konstruksi')
                                                         & (info.pagu >= 180e6) & (info.pagu <= 200e6))
rf3['rf5_penyedia_dominan'] = V['rf5_porsi40_n5']
FL = {'perencanaan': list(rf.columns[:4]), 'pelaksanaan': list(rf.columns)}


def log(*a):
    print(f'[{time.time() - T0:6.0f}s]', *a, flush=True)


def fitur_v3(jalur, varian):
    pdn_umk = KONF[jalur]['pdn_umk'] and 'U' not in varian
    F = fitur(d, jalur, pdn_umk)
    if 'N' in varian:
        F['log_rasio_pagu_nama_serupa'] = NAMA.loc[F.index]
    if 'L' in varian:  # profil metode satker tanpa paket itu sendiri
        n = info.groupby(satker).pagu.transform('size')
        for c, metode in [('proporsi_pl_satker', 'Pengadaan Langsung'), ('porsi_epurchasing_satker', 'E-Purchasing')]:
            sendiri = (info.metode_pengadaan == metode).astype(float)
            jumlah = sendiri.groupby(satker).transform('sum')
            F[c] = ((jumlah - sendiri) / (n - 1).clip(lower=1)).loc[F.index]
    if 'E' in varian:
        F = F.drop(columns=['proporsi_pl_satker', 'porsi_epurchasing_satker'])
    return F


def model_kwargs(jalur, varian):
    kw = dict(KONF[jalur]['model'])
    if 'Q' in varian:
        kw['skala'] = 'quantile'
    return kw


def metrik(s, R):
    s = s.sort_values(ascending=False)
    ada = R.any(axis=1).loc[s.index].values
    ada4 = R.drop(columns='rf4_penunjukan_langsung').any(axis=1).loc[s.index].values
    dev = info.provinsi.loc[s.index].isin(DEV).values
    N, M = len(ada), int(ada.sum())
    o = {f'P@{K}': ada[:K].mean() for K in KS}
    o['pval@200'] = hypergeom.sf(int(ada[:200].sum()) - 1, N, M, 200)
    o['semua_rata'] = np.mean([o[f'P@{K}'] for K in KS])
    o['pilih_rata'] = np.mean([ada[dev][:K].mean() for K in KS])
    o['uji_rata'] = np.mean([ada[~dev][:K].mean() for K in KS])
    o['pilih_tanpaRF4'] = np.mean([ada4[dev][:K].mean() for K in KS])
    o['uji_tanpaRF4'] = np.mean([ada4[~dev][:K].mean() for K in KS])
    o['acuan'], o['acuan_pilih'], o['acuan_uji'] = ada.mean(), ada[dev].mean(), ada[~dev].mean()
    o['acuan_pilih_tanpaRF4'], o['acuan_uji_tanpaRF4'] = ada4[dev].mean(), ada4[~dev].mean()
    sat = satker.loc[s.index].values
    o['satker_maks_top200'] = pd.Series(sat[:200]).value_counts().iloc[0]
    o['satker_unik_top200'] = len(set(sat[:200]))
    n5 = int(N * 0.05)
    o['lift_5persen'] = ada[:n5].mean() / ada.mean()
    for c in R:
        o[f'top200_{c}'] = R[c].loc[s.index[:200]].mean()
    return o


def skor_model(m, X):
    raw = m.raw(X)
    return {k: np.searchsorted(m.ref[k], raw[k], side='right') / len(m.ref[k]) for k in ['IF', 'LOF', 'AE']}


VARIAN = {'perencanaan': ['E']}
rows, simpan = [], {}
for jalur in ['perencanaan']:
    idx = d['f_pel'].index if jalur == 'pelaksanaan' else info.index
    R = rf3.loc[idx, FL[jalur]]
    rng = np.random.default_rng(11)
    biasa = R.index[~R.any(axis=1).values]
    pilih = rng.choice(biasa, 1000, replace=False)
    f = 10 ** rng.uniform(np.log10(5), np.log10(20), 1000)
    S = info.pagu.groupby(satker).transform('sum').loc[pilih].values
    p = info.pagu.loc[pilih].values
    for varian in VARIAN[jalur]:
        F = fitur_v3(jalur, varian)
        X = F.values.astype(float)
        Fb = F.loc[pilih].copy()
        r = np.log10(f)
        Fb['log_pagu'] += r
        for c in ['log_rasio_pagu_sejenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_serupa']:
            if c in Fb:
                Fb[c] += r
        Fb['porsi_pagu_satker'] = p * f / (S - p + p * f)
        if jalur == 'pelaksanaan':
            a = info.realisasi.loc[pilih].values
            Fb['log_selisih_realisasi'] = np.log10(1 + np.abs(a * f - p * f))
        ens_seeds, buatan = [], []
        for sd in SEEDS:
            ens2.SEED = sd
            m = ens2.Ensemble2(**model_kwargs(jalur, varian)).fit(F)
            P0 = skor_model(m, X)
            ens_seeds.append(pd.Series(np.mean([P0[k] for k in P0], axis=0), index=F.index))
            e_real = np.sort(ens_seeds[-1].values)
            thr = np.quantile(e_real, 0.95)
            sb = skor_model(m, Fb[F.columns].values.astype(float))
            sa = skor_model(m, F.loc[pilih].values.astype(float))
            eb, ea = np.mean([sb[k] for k in sb], axis=0), np.mean([sa[k] for k in sa], axis=0)
            buatan.append({'buatan_terdeteksi_5persen': (eb >= thr).mean(),
                           'buatan_persentil_sebelum': np.mean(np.searchsorted(e_real, ea) / len(e_real)),
                           'buatan_persentil_sesudah': np.mean(np.searchsorted(e_real, eb) / len(e_real))})
        e = pd.concat(ens_seeds, axis=1).mean(axis=1)
        o = metrik(e, R)
        jac = []
        for i in range(len(SEEDS)):
            for j in range(i + 1, len(SEEDS)):
                A1, A2 = set(ens_seeds[i].nlargest(200).index), set(ens_seeds[j].nlargest(200).index)
                jac.append(len(A1 & A2) / len(A1 | A2))
        row = {'jalur': jalur, 'varian': varian, 'kolom': '|'.join(F.columns), **o,
               **pd.DataFrame(buatan).mean().to_dict(), 'jaccard_top200_antarseed': np.mean(jac)}
        row['lolos'] = (row['satker_maks_top200'] <= 20) and (row['pilih_tanpaRF4'] > row['acuan_pilih_tanpaRF4'])
        rows.append(row)
        simpan[(jalur, varian)] = e
        pd.DataFrame(rows).to_csv(OUT + 'r6b_pilih_E.csv', index=False)
        pd.to_pickle(simpan, OUT + 'r6b_skor.pkl')
        log(jalur, varian, f"pilih={row['pilih_rata']:.3f} (acuan {row['acuan_pilih']:.3f}) uji={row['uji_rata']:.3f} "
            f"(acuan {row['acuan_uji']:.3f}) tanpaRF4 pilih={row['pilih_tanpaRF4']:.3f} (acuan {row['acuan_pilih_tanpaRF4']:.3f}) "
            f"maksSatker={row['satker_maks_top200']:.0f} buatan={row['buatan_terdeteksi_5persen']:.2f} "
            f"jac={row['jaccard_top200_antarseed']:.2f} lolos={row['lolos']}")
log('SELESAI')
