"""Validasi v3, bagian 3b: uji fitur "pagu dibanding paket bernama serupa" (lihat f1_nama_serupa.py).

Protokol sama dengan r3_fitur.py (3 seed, provinsi pilih/uji, syarat keberagaman satker), ditambah
uji paket buatan: pagu paket biasa dinaikkan 5-20 kali. Fitur nama serupa diharapkan membuat
paket seperti ini lebih mudah tertangkap karena pembandingnya paket dengan barang/jasa yang mirip.
"""
import json
import sys
import time
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

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
FL = {'perencanaan': list(rf.columns[:4]), 'pelaksanaan': list(rf.columns)}
SEEDS = [42, 1, 2]
KS = [50, 100, 200]
PAPUA = info.provinsi.str.contains('Papua')
NAMA = pd.read_pickle(OUT + 'fitur_nama_serupa.pkl')['log_rasio_pagu_nama_serupa']


def log(*a):
    print(f'[{time.time() - T0:6.0f}s]', *a, flush=True)


def fitur_n(jalur, varian):
    F = fitur(d, jalur, KONF[jalur]['pdn_umk'])
    if 'N' in varian:
        F['log_rasio_pagu_nama_serupa'] = NAMA.loc[F.index]
    if 'G' in varian:  # ganti: pembanding jenis+metode diganti pembanding nama serupa
        F = F.drop(columns=['log_rasio_pagu_sejenis'])
    if 'E' in varian:
        F = F.drop(columns=['proporsi_pl_satker', 'porsi_epurchasing_satker'])
    return F


def metrik(s, ada, ada_t4):
    s = s.sort_values(ascending=False)
    a = ada.loc[s.index].values
    o = {f'P@{K}': a[:K].mean() for K in KS}
    o['semua_rata'] = np.mean([o[f'P@{K}'] for K in KS])
    dev = info.provinsi.loc[s.index].isin(DEV).values
    o['pilih_rata'] = np.mean([a[dev][:K].mean() for K in KS])
    o['uji_rata'] = np.mean([a[~dev][:K].mean() for K in KS])
    b = ada_t4.loc[s.index].values
    o['tanpaRF4_rata'] = np.mean([b[:K].mean() for K in KS])
    sat = satker.loc[s.index].values
    o['satker_maks_top200'] = pd.Series(sat[:200]).value_counts().iloc[0]
    an = s.index[:int(len(s) * 0.05)]
    pap = PAPUA.loc[s.index]
    o['rasio_papua'] = pap.loc[an].mean() / pap.mean()
    o['presisi_5persen'] = ada.loc[an].mean()
    prov = info.provinsi.loc[s.index]
    prop = pd.Series(s.index.isin(an), index=s.index).groupby(prov).mean()
    o['spearman_prov_redflag'] = spearmanr(prop, ada.groupby(info.provinsi.loc[ada.index]).mean().loc[prop.index])[0]
    return o


def skor_model(m, X):
    raw = m.raw(X)
    return {k: np.searchsorted(m.ref[k], raw[k], side='right') / len(m.ref[k]) for k in ['IF', 'LOF', 'AE']}


VARIAN = {'perencanaan': ['v2', 'N', 'NG', 'NE', 'NGE'], 'pelaksanaan': ['v2', 'N', 'NG']}
rows = []
for jalur in ['perencanaan', 'pelaksanaan']:
    R = rf.loc[d['f_pel'].index if jalur == 'pelaksanaan' else info.index, FL[jalur]]
    ada, ada_t4 = R.any(axis=1), R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    # paket buatan: paket biasa (tanpa red flag) yang pagunya dinaikkan 5-20x (realisasi ikut naik di pelaksanaan)
    rng = np.random.default_rng(11)
    biasa = R.index[~R.any(axis=1).values]
    pilih = rng.choice(biasa, 1000, replace=False)
    f = 10 ** rng.uniform(np.log10(5), np.log10(20), 1000)
    S = info.pagu.groupby(satker).transform('sum').loc[pilih].values
    p = info.pagu.loc[pilih].values
    for varian in VARIAN[jalur]:
        F = fitur_n(jalur, varian)
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
        per = []
        for sd in SEEDS:
            ens2.SEED = sd
            m = ens2.Ensemble2(**KONF[jalur]['model']).fit(F)
            P0 = skor_model(m, X)
            P = {k: pd.Series(v, index=F.index).rank(pct=True) for k, v in P0.items()}
            e = (P['IF'] + P['LOF'] + P['AE']) / 3
            o = metrik(e, ada, ada_t4)
            ens_real = np.mean([P0[k] for k in P0], axis=0)
            thr = np.quantile(ens_real, 0.95)
            sb = skor_model(m, Fb[F.columns].values.astype(float))
            sa = skor_model(m, F.loc[pilih].values.astype(float))
            eb, ea = np.mean([sb[k] for k in sb], axis=0), np.mean([sa[k] for k in sa], axis=0)
            o['buatan_terdeteksi_5persen'] = (eb >= thr).mean()
            o['buatan_persentil_sebelum'] = np.mean(np.searchsorted(np.sort(ens_real), ea) / len(ens_real))
            o['buatan_persentil_sesudah'] = np.mean(np.searchsorted(np.sort(ens_real), eb) / len(ens_real))
            per.append(o)
        df = pd.DataFrame(per)
        row = {'jalur': jalur, 'varian': varian, 'kolom': '|'.join(F.columns), **df.mean().to_dict(),
               'pilih_rata_sd': df.pilih_rata.std()}
        row['lolos'] = row['satker_maks_top200'] <= 20
        rows.append(row)
        pd.DataFrame(rows).to_csv(OUT + 'r3b_fitur_nama.csv', index=False)
        log(jalur, varian, f"pilih={row['pilih_rata']:.3f} uji={row['uji_rata']:.3f} semua={row['semua_rata']:.3f} "
            f"tanpaRF4={row['tanpaRF4_rata']:.3f} maksSatker={row['satker_maks_top200']:.0f} papua={row['rasio_papua']:.2f} "
            f"buatan={row['buatan_terdeteksi_5persen']:.2f} ({row['buatan_persentil_sebelum']:.2f}->{row['buatan_persentil_sesudah']:.2f})")
log('SELESAI')
