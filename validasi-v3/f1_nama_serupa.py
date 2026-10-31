"""Fitur baru: pagu dibanding paket dengan NAMA serupa (pendekatan "kategori barang" OCP R016).

Data RUP tidak punya kode kategori barang, tetapi nama paket umumnya memakai nomenklatur belanja
(mis. "Belanja Makanan dan Minuman Rapat"). Untuk tiap paket dicari 30 paket lain dengan nama paling
mirip (TF-IDF + SVD, kemiripan kosinus) pada jenis pengadaan yang sama, lalu dihitung
log10(pagu / median pagu 30 paket itu). Nilai besar = jauh lebih mahal dari paket sejenis namanya.
Keluaran: fitur_nama_serupa.pkl (Series per kode_rup).
"""
import re
import time
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

OUT = '/mnt/project-files/validasi-v3/'
T0 = time.time()
info = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')['info']


def bersih(t):
    t = re.sub(r'[\d\.\-/,()]+', ' ', str(t).lower())
    return re.sub(r'\s+', ' ', t).strip()


nm = info.nama_paket.map(bersih)
K = 30
hasil = pd.Series(np.nan, index=info.index)
mirip = pd.Series(np.nan, index=info.index)
for jenis, idx in info.groupby('jenis').groups.items():
    X = TfidfVectorizer(ngram_range=(1, 2), min_df=3, sublinear_tf=True).fit_transform(nm.loc[idx])
    Z = TruncatedSVD(n_components=128, random_state=42).fit_transform(X).astype(np.float32)
    Z /= np.linalg.norm(Z, axis=1, keepdims=True) + 1e-9
    pagu = info.pagu.loc[idx].values
    med, sim = np.empty(len(idx)), np.empty(len(idx))
    for a in range(0, len(idx), 512):
        S = Z[a:a + 512] @ Z.T
        S[np.arange(S.shape[0]), np.arange(a, a + S.shape[0])] = -1  # buang diri sendiri
        nb = np.argpartition(-S, K, axis=1)[:, :K]
        med[a:a + 512] = np.median(pagu[nb], axis=1)
        sim[a:a + 512] = np.take_along_axis(S, nb, axis=1).mean(axis=1)
    hasil.loc[idx] = np.log10(pagu / med)
    mirip.loc[idx] = sim
    print(f'[{time.time() - T0:5.0f}s] {jenis}: {len(idx)} paket, kemiripan rata-rata 30 tetangga {sim.mean():.3f}', flush=True)
pd.to_pickle({'log_rasio_pagu_nama_serupa': hasil, 'kemiripan_tetangga': mirip}, OUT + 'fitur_nama_serupa.pkl')
print(hasil.describe().round(3).to_string())
print('korelasi dengan log_rasio_pagu_sejenis:',
      round(np.corrcoef(hasil, pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')['f_ren'].log_rasio_pagu_sejenis)[0, 1], 3))
