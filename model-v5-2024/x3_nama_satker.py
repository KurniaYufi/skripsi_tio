"""Eksperimen fitur nama di satker (permintaan Tio 2026-10-29, kasus "paket A 20 jt, B 20 jt, C 1 M bernama sama di satker
yang sama"). Model v5 belum menangkap pola ini: dari 2.614 paket yang pagunya >= 10 kali paket lain bernama sama di
satkernya, hanya 2,1% masuk 5% teratas (acak = 5%).

Fitur baru log_rasio_pagu_nama_satker = log10(pagu / median pagu paket LAIN dengan nama sama di satker yang sama), satu arah.
Nama disamakan dulu: huruf kecil, angka dan tanda baca dibuang. Paket yang tidak punya kembaran nama cukup -> 0 (wajar).
Beda dengan fitur N di validasi-v3 (dibanding 30 nama paling mirip secara NASIONAL, hasilnya lebih buruk).

Varian: M2 = cukup 1 paket lain bernama sama; M3 = minimal 2 paket lain.
Pemakaian: python3 x3_nama_satker.py <jalur> <M2|M3>. Keluaran: eksperimen-nama-satker/skor_<jalur>_<varian>.pkl
"""
import copy
import os
import re
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5-2024')
from ens3 import Ensemble3  # noqa: E402
import s2_model  # noqa: E402

O = '/mnt/project-files/model-v5-2024/eksperimen-nama-satker/'
FITUR = O + 'fitur_nama_satker.pkl'


def nama_dasar(t):
    t = re.sub(r'[^a-z ]', ' ', str(t).lower())
    return re.sub(r'\s+', ' ', t).strip()


def hitung_fitur(info):
    """Rasio pagu terhadap median paket lain bernama sama di satker, dan jumlah paket lain itu."""
    kunci = info.provinsi + '|' + info.nama_satuan_kerja + '|' + info.nama_paket.map(nama_dasar)
    rasio = pd.Series(np.nan, index=info.index)
    n_lain = kunci.map(kunci.value_counts()) - 1
    for _, idx in kunci[n_lain > 0].groupby(kunci[n_lain > 0]).groups.items():
        p = info.pagu.loc[idx].values
        med = np.array([np.median(np.delete(p, k)) for k in range(len(p))])
        rasio.loc[idx] = np.log10(p / med)
    return pd.DataFrame({'log_rasio_pagu_nama_satker': rasio, 'n_nama_lain': n_lain})


if __name__ == '__main__':
    jalur, varian = sys.argv[1], sys.argv[2]
    d = pd.read_pickle(s2_model.DATA + 'tahap1.pkl')
    if not os.path.exists(FITUR):
        hitung_fitur(d['info']).to_pickle(FITUR)
    X = pd.read_pickle(FITUR)
    F = s2_model.fitur(d, jalur)
    minimal = int(varian[1:]) - 1
    ok = X.n_nama_lain.loc[F.index] >= minimal
    F['log_rasio_pagu_nama_satker'] = X.log_rasio_pagu_nama_satker.loc[F.index].where(ok, 0.0).fillna(0.0)
    kw = copy.deepcopy(s2_model.KONF[jalur]['model'])
    kw['satu_arah'] = {**kw.get('satu_arah', {}), 'log_rasio_pagu_nama_satker': 'nol'}
    print(jalur, varian, F.shape, 'paket dengan pembanding nama:', int(ok.sum()), kw, flush=True)
    m = Ensemble3(**kw).fit(F)
    Ps = [mm.pct(m._potong(F.values.astype(float))) for mm in m.m]
    sk = pd.DataFrame({k: np.mean([p[k] for p in Ps], axis=0) for k in ['IF', 'LOF', 'AE']}, index=F.index)
    sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
    sk.to_pickle(O + f'skor_{jalur}_{varian}.pkl')
    print('selesai', flush=True)
