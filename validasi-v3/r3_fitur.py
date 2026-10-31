"""Validasi v3, bagian 3: eksplorasi fitur konteks provinsi (dan versi ketat tanpa profil metode satker).

Masalah yang dicek: provinsi Papua mendapat porsi anomali jauh di atas porsi paketnya. Bisa karena
harga dan cara belanja di sana memang berbeda (bukan karena lebih berisiko). Fitur pembanding
provinsi membandingkan paket dengan kebiasaan di provinsinya sendiri.

Aturan pemilihan (ditetapkan sebelum melihat hasil, sama dengan eksplorasi v2 + satu tambahan):
1. Tiap konfigurasi 3 seed; yang dibandingkan rata-ratanya.
2. Syarat: satu satker paling banyak 20 paket di 200 teratas.
3. Dipilih rata-rata P@50/100/200 tertinggi di provinsi "pilih"; konfigurasi baru hanya menggantikan v2
   bila unggul paling sedikit 1 poin persen. Bila selisih < 1 poin, dipilih yang rasio Papua-nya lebih kecil.
4. Angka provinsi "uji" hanya dilaporkan.
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


def log(*a):
    print(f'[{time.time() - T0:6.0f}s]', *a, flush=True)


def median_prov(nilai, kunci_prov, kunci_nas, nmin=20):
    """Median per kelompok provinsi; kelompok kecil (< nmin) memakai median nasional."""
    g = nilai.groupby(kunci_prov)
    med, n = g.transform('median'), g.transform('size')
    return med.where(n >= nmin, nilai.groupby(kunci_nas).transform('median'))


def fitur_v3(jalur, varian):
    F = fitur(d, jalur, KONF[jalur]['pdn_umk'])
    inf = info.loc[F.index]
    if 'A' in varian:  # pagu dibanding paket sejenis (jenis + metode) di provinsi yang sama
        nas = inf.jenis + '|' + inf.metode_pengadaan
        med = median_prov(info.pagu, info.provinsi + '|' + info.jenis + '|' + info.metode_pengadaan,
                          info.jenis + '|' + info.metode_pengadaan).loc[F.index]
        F['log_rasio_pagu_sejenis'] = np.log10(inf.pagu / med)
        del nas
    if 'B' in varian:  # besar pagu dibanding median provinsi untuk jenis yang sama (menghapus beda tingkat harga)
        lp = np.log10(info.pagu)
        F['log_pagu'] = (lp - lp.groupby(info.provinsi + '|' + info.jenis).transform('median')).loc[F.index]
    if 'C' in varian:  # profil satker dibanding median satker di provinsinya
        sat_prov = info.provinsi.loc[F.index]
        for c in ['proporsi_pl_satker', 'porsi_epurchasing_satker', 'log_jumlah_paket_satker']:
            if c in F:
                per_satker = F[c].groupby(satker.loc[F.index]).first()
                prov_satker = sat_prov.groupby(satker.loc[F.index]).first()
                med = per_satker.groupby(prov_satker).median()
                F[c] = F[c] - sat_prov.map(med).values
    if 'E' in varian:  # versi ketat: tanpa profil metode satker
        F = F.drop(columns=['proporsi_pl_satker', 'porsi_epurchasing_satker'])
    return F


def metrik(s, ada, ada_t4, R):
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
    o['spearman_prov_redflag_tanpaRF4'] = spearmanr(prop, ada_t4.groupby(info.provinsi.loc[ada.index]).mean().loc[prop.index])[0]
    return o


VARIAN = {'perencanaan': ['v2', 'A', 'B', 'AB', 'ABC', 'E', 'ABE'],
          'pelaksanaan': ['v2', 'A', 'AB', 'ABC', 'E', 'ABE']}
rows = []
for jalur in ['pelaksanaan', 'perencanaan']:
    R = rf.loc[d['f_pel'].index if jalur == 'pelaksanaan' else info.index, FL[jalur]]
    ada, ada_t4 = R.any(axis=1), R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    for varian in VARIAN[jalur]:
        F = fitur_v3(jalur, varian)
        X = F.values.astype(float)
        per = []
        for sd in SEEDS:
            ens2.SEED = sd
            m = ens2.Ensemble2(**KONF[jalur]['model']).fit(F)
            raw = m.raw(X)
            P = {k: pd.Series(np.searchsorted(m.ref[k], raw[k], side='right') / len(raw[k]), index=F.index).rank(pct=True)
                 for k in ['IF', 'LOF', 'AE']}
            e = (P['IF'] + P['LOF'] + P['AE']) / 3
            o = metrik(e, ada, ada_t4, R)
            for k in ['IF', 'LOF', 'AE']:
                o[f'{k}_semua_rata'] = metrik(P[k], ada, ada_t4, R)['semua_rata']
            per.append(o)
        df = pd.DataFrame(per)
        row = {'jalur': jalur, 'varian': varian, 'kolom': '|'.join(F.columns), **df.mean().to_dict(),
               'pilih_rata_sd': df.pilih_rata.std(), 'uji_rata_sd': df.uji_rata.std()}
        row['lolos'] = row['satker_maks_top200'] <= 20
        rows.append(row)
        pd.DataFrame(rows).to_csv(OUT + 'r3_fitur.csv', index=False)
        log(jalur, varian, f"pilih={row['pilih_rata']:.3f} uji={row['uji_rata']:.3f} semua={row['semua_rata']:.3f} "
            f"tanpaRF4={row['tanpaRF4_rata']:.3f} maksSatker={row['satker_maks_top200']:.0f} papua={row['rasio_papua']:.2f} "
            f"rhoProv={row['spearman_prov_redflag']:.2f}")
log('SELESAI')
