"""Eksplorasi putaran 2.

Pelajaran putaran 1 (exp.py):
- One-hot metode memuat "penunjukan langsung" yang sama persis dengan red flag 4, sehingga Precision@K berputar.
  Mengikuti prinsip review-fitur-v1 (fitur yang sama dengan red flag dikeluarkan), one-hot metode tidak dipakai.
- Precision@K bisa melonjak karena 200 paket teratas hanya berasal dari segelintir satker (fitur tingkat satker
  sama untuk semua paket di satker itu). Daftar seperti itu tidak berguna untuk prioritas dan tidak stabil.

Aturan pemilihan putaran 2 (ditetapkan sebelum melihat hasil):
1. Setiap konfigurasi dijalankan dengan 3 seed; yang dibandingkan rata-ratanya.
2. Syarat: di 200 paket teratas nasional, satu satker paling banyak 10% (20 paket).
3. Dari yang memenuhi syarat, dipilih rata-rata P@50/100/200 tertinggi di provinsi "pilih".
4. Angka di provinsi "uji" hanya dilaporkan, tidak dipakai memilih.
"""
import itertools
import json
import sys
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import QuantileTransformer, StandardScaler

D = '/mnt/project-files/model-v1/'
OUT = D + 'eksplorasi/'
d = pd.read_pickle(D + 'tahap1.pkl')
info, rf = d['info'], d['rf']
FL = {'perencanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung'],
      'pelaksanaan': list(rf.columns)}
dev_prov = set(json.load(open(OUT + 'provinsi_pilih.json')))
satker = info.provinsi + '|' + info.nama_satuan_kerja
SEEDS = [42, 1, 2]
SATKER_LEVEL = ['log_jumlah_paket_satker', 'proporsi_pl_satker', 'porsi_epurchasing_satker']


def fitur(jalur, extra=False, satker_level=True, pdn_umk=True):
    F = (d['f_ren'] if jalur == 'perencanaan' else d['f_pel']).copy()
    F = F.drop(columns=[c for c in F if c.startswith('metode_')])
    if extra:
        F['log_rasio_pagu_satker'] = np.log10(info.pagu / info.pagu.groupby(satker).transform('median')).loc[F.index]
        F['porsi_epurchasing_satker'] = (info.metode_pengadaan == 'E-Purchasing').groupby(satker).transform('mean').loc[F.index]
        if jalur == 'pelaksanaan':
            r = F['rasio_realisasi']
            grp = (info.jenis + '|' + info.metode_pengadaan).loc[F.index]
            F['selisih_rasio_realisasi_sejenis'] = (r - r.groupby(grp).transform('median')).abs()
    if not satker_level:
        F = F.drop(columns=[c for c in SATKER_LEVEL if c in F])
    if not pdn_umk:
        F = F.drop(columns=['pdn', 'umk'])
    return F


def olah(F, skala, seed):
    X = F.values.astype(float)
    if skala == 'std':
        return StandardScaler().fit_transform(X)
    biner = np.array([set(np.unique(F[c])) <= {0.0, 1.0} for c in F])
    Z = X.copy()
    qt = QuantileTransformer(n_quantiles=1000, output_distribution='normal', subsample=200000, random_state=seed)
    Z[:, ~biner] = qt.fit_transform(X[:, ~biner])
    return Z


CACHE = {}


def skor(jalur, fk, skala, model, hp, seed):
    key = (jalur, fk, None if model == 'IF' else skala, model, hp, seed)
    if key in CACHE:
        return CACHE[key]
    F = fitur(jalur, **dict(fk))
    rng = np.random.default_rng(seed)
    h = dict(hp)
    if model == 'IF':
        m = IsolationForest(n_estimators=200, max_samples=h.get('max_samples', 'auto'), random_state=seed, n_jobs=-1).fit(F.values)
        s = -m.score_samples(F.values)
    else:
        Z = olah(F, skala, seed)
        if model == 'LOF':
            uniq = np.unique(Z.round(6), axis=0)
            idx = rng.choice(len(uniq), size=min(30000, len(uniq)), replace=False)
            s = -LocalOutlierFactor(n_neighbors=h.get('k', 20), novelty=True, n_jobs=-1).fit(uniq[idx]).score_samples(Z)
        else:
            idx = rng.choice(len(Z), size=min(100000, len(Z)), replace=False)
            b = h.get('b', max(4, Z.shape[1] // 4))
            m = MLPRegressor(hidden_layer_sizes=(16, b, 16), max_iter=h.get('it', 60), early_stopping=True,
                             random_state=seed).fit(Z[idx], Z[idx])
            s = ((m.predict(Z) - Z) ** 2).mean(axis=1)
    r = pd.Series(s, index=F.index).rank(pct=True)
    CACHE[key] = r
    return r


def gabung(P, cara):
    M = pd.concat(P, axis=1)
    return {'rata': M.mean(axis=1), 'median': M.median(axis=1), 'maks': M.max(axis=1),
            'bobot_keluarga': 0.25 * M['IF'] + 0.5 * M['LOF'] + 0.25 * M['AE']}[cara]


def metrik(s, jalur):
    R = rf.loc[s.index, FL[jalur]]
    ada = R.any(axis=1)
    ada_t4 = R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    dev = info.provinsi.loc[s.index].isin(dev_prov).values
    o = {}
    for nama, mask in [('semua', np.ones(len(s), bool)), ('pilih', dev), ('uji', ~dev)]:
        ss = s[mask].sort_values(ascending=False)
        o[f'{nama}_rata'] = np.mean([ada[ss.index[:K]].mean() for K in [50, 100, 200]])
        if nama == 'semua':
            for K in [50, 100, 200]:
                o[f'P@{K}'] = ada[ss.index[:K]].mean()
            o['rata_tanpaRF4'] = np.mean([ada_t4[ss.index[:K]].mean() for K in [50, 100, 200]])
            n1 = int(len(ss) * 0.01)
            o['lift_1persen'] = ada[ss.index[:n1]].mean() / ada.mean()
            sat = satker.loc[ss.index[:200]]
            o['satker_top200'] = sat.nunique()
            o['satker_maks_top200'] = sat.value_counts().iloc[0]
    o['acuan'] = ada.mean()
    o['acuan_tanpaRF4'] = ada_t4.mean()
    return o


HASIL = []


def uji(tahap, jalur, fk, skala, hp, cara='rata'):
    t = time.time()
    per_seed = []
    for sd in SEEDS:
        P = {m: skor(jalur, fk, skala, m, hp[m], sd) for m in ['IF', 'LOF', 'AE']}
        row = {f'ens_{k}': v for k, v in metrik(gabung(P, cara), jalur).items()}
        for m in ['IF', 'LOF', 'AE']:
            row.update({f'{m}_{k}': v for k, v in metrik(P[m], jalur).items() if k in ('semua_rata', 'pilih_rata', 'uji_rata', 'satker_maks_top200')})
        per_seed.append(row)
    df = pd.DataFrame(per_seed)
    row = {'tahap': tahap, 'jalur': jalur, 'fitur': json.dumps(dict(fk)), 'skala': skala,
           'hp': json.dumps({m: dict(v) for m, v in hp.items()}), 'gabung': cara}
    row.update(df.mean().to_dict())
    row['ens_pilih_rata_sd'] = df['ens_pilih_rata'].std()
    row['ens_semua_rata_sd'] = df['ens_semua_rata'].std()
    row['lolos'] = row['ens_satker_maks_top200'] <= 20
    HASIL.append(row)
    pd.DataFrame(HASIL).to_csv(OUT + 'hasil_eksplorasi2.csv', index=False)
    print(f"[{tahap}] {jalur[:5]} {json.dumps(dict(fk))} {skala} {row['hp']} {cara}: pilih={row['ens_pilih_rata']:.3f}±{row['ens_pilih_rata_sd']:.3f} "
          f"uji={row['ens_uji_rata']:.3f} semua={row['ens_semua_rata']:.3f} tanpaRF4={row['ens_rata_tanpaRF4']:.3f} "
          f"maksSatker={row['ens_satker_maks_top200']:.0f} lolos={row['lolos']} [{time.time() - t:.0f}s]", flush=True)
    return row


def terbaik(rows):
    ok = [r for r in rows if r['lolos']] or rows
    return max(ok, key=lambda r: r['ens_pilih_rata'])


H0 = {'IF': (), 'LOF': (('k', 20),), 'AE': ()}

if __name__ == '__main__':
    best = {}
    for jalur in ['perencanaan', 'pelaksanaan']:
        # Tahap 1a: cara penskalaan pada fitur dasar
        fk0 = tuple(sorted(dict(extra=False, satker_level=True, pdn_umk=True).items()))
        r1 = [uji(1, jalur, fk0, 'std', H0), uji(1, jalur, fk0, 'quantile', H0)]
        skala1 = max(r1, key=lambda r: r['ens_pilih_rata'])['skala']
        # Tahap 1b: tambah/kurang fitur pada penskalaan terpilih
        rows = list(r1)
        for extra, sl, pu in itertools.product([False, True], [True, False], [True, False]):
            fk = tuple(sorted(dict(extra=extra, satker_level=sl, pdn_umk=pu).items()))
            if fk == fk0:
                continue
            rows.append(uji(1, jalur, fk, skala1, H0))
        b = terbaik(rows)
        fk = tuple(sorted(json.loads(b['fitur']).items()))
        skala = b['skala']
        hp = dict(H0)
        for m, opsi in [('LOF', [(('k', 50),), (('k', 100),)]), ('IF', [(('max_samples', 2048),)]), ('AE', [(('b', 3),), (('b', 8),)])]:
            kand = [b]
            for o in opsi:
                h = dict(hp)
                h[m] = o
                kand.append(uji(2, jalur, fk, skala, h))
            b = terbaik(kand)
            hp = {k: tuple(sorted(v.items())) for k, v in json.loads(b['hp']).items()}
        kand = [b] + [uji(3, jalur, fk, skala, hp, c) for c in ['median', 'maks', 'bobot_keluarga']]
        b = terbaik(kand)
        best[jalur] = b
        print('TERBAIK', jalur, b['fitur'], b['skala'], b['hp'], b['gabung'], flush=True)
    json.dump(best, open(OUT + 'terbaik2.json', 'w'), indent=1, default=float)
