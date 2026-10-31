"""Eksplorasi model: pengolahan fitur, tambah/kurang fitur, pengaturan model, dan cara penggabungan skor.

Pemilihan konfigurasi memakai provinsi "pilih" (dev); angka akhir dilaporkan di provinsi "uji" (test),
supaya pilihan tidak dipas-paskan dengan red flag. Model tetap dilatih tanpa label pada semua paket.
"""
import json
import sys
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import QuantileTransformer, RobustScaler, StandardScaler

D = '/mnt/project-files/model-v1/'
OUT = D + 'eksplorasi/'
SEED = 42
d = pd.read_pickle(D + 'tahap1.pkl')
info, rf = d['info'], d['rf']
FL = {'perencanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung'],
      'pelaksanaan': list(rf.columns)}

# Pembagian provinsi: separuh untuk memilih konfigurasi, separuh untuk menguji
prov = sorted(info.provinsi.unique())
rng = np.random.default_rng(7)
dev_prov = set(rng.choice(prov, size=len(prov) // 2, replace=False))
json.dump(sorted(dev_prov), open(OUT + 'provinsi_pilih.json', 'w'), ensure_ascii=False)

satker = info.provinsi + '|' + info.nama_satuan_kerja


def fitur(jalur, metode=True, extra=False, pdn_umk=True, jenis=True):
    F = (d['f_ren'] if jalur == 'perencanaan' else d['f_pel']).copy()
    if not metode:
        F = F.drop(columns=[c for c in F if c.startswith('metode_')])
    if not jenis:
        F = F.drop(columns=[c for c in F if c.startswith('jenis_')])
    if not pdn_umk:
        F = F.drop(columns=['pdn', 'umk'])
    if extra:
        # dihitung dari seluruh RUP lingkup penelitian, sama seperti fitur satker lain
        s = satker
        F['log_rasio_pagu_satker'] = np.log10(info.pagu / info.pagu.groupby(s).transform('median')).loc[F.index]
        F['porsi_epurchasing_satker'] = (info.metode_pengadaan == 'E-Purchasing').groupby(s).transform('mean').loc[F.index]
        if jalur == 'pelaksanaan':
            r = F['rasio_realisasi']
            grp = (info.jenis + '|' + info.metode_pengadaan).loc[F.index]
            F['selisih_rasio_realisasi_sejenis'] = (r - r.groupby(grp).transform('median')).abs()
    return F


def olah(F, skala):
    X = F.values.astype(float)
    if skala == 'std':
        return StandardScaler().fit_transform(X)
    biner = np.array([set(np.unique(F[c])) <= {0.0, 1.0} for c in F])
    Z = X.copy()
    if skala == 'quantile':
        qt = QuantileTransformer(n_quantiles=1000, output_distribution='normal', subsample=200000, random_state=SEED)
        Z[:, ~biner] = qt.fit_transform(X[:, ~biner])
    elif skala == 'robust':
        Z[:, ~biner] = RobustScaler(quantile_range=(5, 95)).fit_transform(X[:, ~biner])
    return Z


CACHE = {}


def skor_model(jalur, fk, skala, model, hp):
    key = (jalur, fk, None if model == 'IF' else skala, model, hp)
    if key in CACHE:
        return CACHE[key]
    F = fitur(jalur, **dict(fk))
    rng_ = np.random.default_rng(SEED)
    if model == 'IF':
        ms = dict(hp).get('max_samples', 'auto')
        m = IsolationForest(n_estimators=200, max_samples=ms, random_state=SEED, n_jobs=-1).fit(F.values)
        s = -m.score_samples(F.values)
    else:
        Z = olah(F, skala)
        if model == 'LOF':
            uniq = np.unique(Z.round(6), axis=0)
            idx = rng_.choice(len(uniq), size=min(30000, len(uniq)), replace=False)
            m = LocalOutlierFactor(n_neighbors=dict(hp).get('k', 20), novelty=True, n_jobs=-1).fit(uniq[idx])
            s = -m.score_samples(Z)
        else:
            idx = rng_.choice(len(Z), size=min(100000, len(Z)), replace=False)
            k = Z.shape[1]
            b = dict(hp).get('b', max(4, k // 4))
            m = MLPRegressor(hidden_layer_sizes=(16, b, 16), max_iter=dict(hp).get('it', 60), early_stopping=True,
                             random_state=SEED).fit(Z[idx], Z[idx])
            s = ((m.predict(Z) - Z) ** 2).mean(axis=1)
    r = pd.Series(s, index=F.index).rank(pct=True)
    CACHE[key] = r
    return r


def gabung(P, cara):
    M = pd.concat(P, axis=1)
    if cara == 'rata':
        return M.mean(axis=1)
    if cara == 'median':
        return M.median(axis=1)
    if cara == 'maks':
        return M.max(axis=1)
    if cara == 'bobot_keluarga':  # IF dan AE berkorelasi tinggi, jadi berbagi setengah bobot
        return 0.25 * M['IF'] + 0.5 * M['LOF'] + 0.25 * M['AE']
    raise ValueError(cara)


def evaluasi(s, jalur):
    R = rf.loc[s.index, FL[jalur]]
    ada = R.any(axis=1)
    ada_t4 = R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    out = {}
    for nama, mask in [('pilih', info.provinsi.loc[s.index].isin(dev_prov)), ('uji', ~info.provinsi.loc[s.index].isin(dev_prov)),
                       ('semua', pd.Series(True, index=s.index))]:
        ss = s[mask.values].sort_values(ascending=False)
        for K in [50, 100, 200]:
            top = ss.index[:K]
            out[f'{nama}_P@{K}'] = ada[top].mean()
            out[f'{nama}_P@{K}_tanpaRF4'] = ada_t4[top].mean()
        out[f'{nama}_acuan'] = ada[mask.values].mean()
        out[f'{nama}_acuan_tanpaRF4'] = ada_t4[mask.values].mean()
    for x in ['pilih', 'uji', 'semua']:
        out[f'{x}_rata'] = np.mean([out[f'{x}_P@{K}'] for K in [50, 100, 200]])
        out[f'{x}_rata_tanpaRF4'] = np.mean([out[f'{x}_P@{K}_tanpaRF4'] for K in [50, 100, 200]])
    return out


HASIL = []


def uji(label, tahap, jalur, fk, skala, hp, cara='rata'):
    t = time.time()
    P = {m: skor_model(jalur, fk, skala, m, hp[m]) for m in ['IF', 'LOF', 'AE']}
    row = {'tahap': tahap, 'label': label, 'jalur': jalur, 'fitur': str(dict(fk)), 'skala': skala,
           'hp': str({m: dict(v) for m, v in hp.items()}), 'gabung': cara}
    row.update({f'ens_{k}': v for k, v in evaluasi(gabung(P, cara), jalur).items()})
    for m in ['IF', 'LOF', 'AE']:
        e = evaluasi(P[m], jalur)
        row[f'{m}_pilih_rata'] = e['pilih_rata']
        row[f'{m}_uji_rata'] = e['uji_rata']
        row[f'{m}_semua_rata'] = e['semua_rata']
    HASIL.append(row)
    pd.DataFrame(HASIL).to_csv(OUT + 'hasil_eksplorasi.csv', index=False)
    print(f"[{tahap}] {jalur:12s} {label:40s} pilih={row['ens_pilih_rata']:.3f} (tanpaRF4 {row['ens_pilih_rata_tanpaRF4']:.3f}) "
          f"uji={row['ens_uji_rata']:.3f} | IF {row['IF_pilih_rata']:.3f} LOF {row['LOF_pilih_rata']:.3f} AE {row['AE_pilih_rata']:.3f} "
          f"[{time.time() - t:.0f}s]", flush=True)
    return row


def fz(**kw):
    base = dict(metode=True, extra=False, pdn_umk=True, jenis=True)
    base.update(kw)
    return tuple(sorted(base.items()))


H0 = {'IF': (), 'LOF': (('k', 20),), 'AE': ()}


def pilih_terbaik(rows, kunci='ens_pilih_rata'):
    return max(rows, key=lambda r: r[kunci])


if __name__ == '__main__':
    terbaik = {}
    for jalur in ['perencanaan', 'pelaksanaan']:
        # Tahap 1: pengolahan fitur dan one-hot metode
        r1 = [uji('v1 (std, one-hot metode)', 1, jalur, fz(), 'std', H0),
              uji('quantile, one-hot metode', 1, jalur, fz(), 'quantile', H0),
              uji('std, tanpa one-hot metode', 1, jalur, fz(metode=False), 'std', H0),
              uji('quantile, tanpa one-hot metode', 1, jalur, fz(metode=False), 'quantile', H0),
              uji('robust, tanpa one-hot metode', 1, jalur, fz(metode=False), 'robust', H0)]
        # Metode one-hot memuat penunjukan langsung (= red flag 4), jadi pilihan dibatasi ke varian tanpa one-hot metode
        bersih = [r for r in r1 if 'tanpa one-hot' in r['label']]
        b1 = pilih_terbaik(bersih)
        skala = b1['skala']
        # Tahap 2: tambah/kurang fitur
        r2 = [b1,
              uji('+ fitur tambahan', 2, jalur, fz(metode=False, extra=True), skala, H0),
              uji('- pdn & umk', 2, jalur, fz(metode=False, pdn_umk=False), skala, H0),
              uji('+ fitur tambahan, - pdn & umk', 2, jalur, fz(metode=False, extra=True, pdn_umk=False), skala, H0),
              uji('- one-hot jenis', 2, jalur, fz(metode=False, jenis=False), skala, H0)]
        b2 = pilih_terbaik(r2)
        fk = tuple(sorted(eval(b2['fitur']).items()))
        # Tahap 3: pengaturan model (satu per satu, sisanya tetap)
        hp = dict(H0)
        for m, opsi in [('LOF', [(('k', 50),), (('k', 100),)]),
                        ('IF', [(('max_samples', 2048),)]),
                        ('AE', [(('b', 3),), (('it', 200),), (('b', 3), ('it', 200))])]:
            kand = [b2 if m == 'LOF' else best3]
            for o in opsi:
                h = dict(hp)
                h[m] = o
                kand.append(uji(f'{m} {dict(o)}', 3, jalur, fk, skala, h))
            best3 = pilih_terbaik(kand)
            hp = {k: tuple(sorted(v.items())) for k, v in eval(best3['hp']).items()}
        # Tahap 4: cara penggabungan
        r4 = [best3] + [uji(f'gabung {c}', 4, jalur, fk, skala, hp, c) for c in ['median', 'maks', 'bobot_keluarga']]
        terbaik[jalur] = pilih_terbaik(r4)
        print('TERBAIK', jalur, {k: terbaik[jalur][k] for k in ['label', 'fitur', 'skala', 'hp', 'gabung']}, flush=True)
    json.dump({j: {k: (v if isinstance(v, str) else float(v)) for k, v in r.items() if not isinstance(v, (int,)) or True}
               for j, r in terbaik.items()}, open(OUT + 'terbaik.json', 'w'), default=str, indent=1)
