"""Tahap 5: uji validitas model v3. Hasil di folder validasi/, dirangkum di dashboard dan ringkasan-validasi-v3.md.

1. Kesesuaian dengan red flag: Precision@K, uji hipergeometrik, interval Wilson, provinsi pilih/uji, dibanding
   model tunggal, pembanding sederhana, dan metode lain (ECOD, HBOS, KNN, PCA).
2. Lift per red flag, dan tumpang tindih tiap red flag dengan fitur (agar terlihat red flag mana yang
   "mudah" ditemukan karena dihitung dari besaran yang juga menjadi fitur).
3. Bootstrap per satker: selang kepercayaan P@200 dan selisihnya dengan pembanding.
4. Kestabilan: ensemble kedua dengan 5 seed lain; dibanding kestabilan satu seed.
5. Kepekaan ambang 1/5/10% dan kesesuaian peta provinsi dengan red flag.
6. Anomali buatan per tipe (gaya ADBench dan skenario pengadaan).
7. Validitas prediktif lintas tahap: skor perencanaan terhadap red flag yang baru muncul di pelaksanaan,
   mentah dan setelah dikontrol ukuran paket (pagu dan porsi pagu di satker).
8. Konsistensi antar-red flag v3 di tingkat satker.
Uji kesetiaan SHAP ada di s6_shap_hapus.py (butuh hasil tahap 3).
"""
import json
import os
import sys
import time
import numpy as np
import pandas as pd
from scipy.stats import hypergeom, norm, skew, spearmanr
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors

sys.path.insert(0, '/mnt/project-files/model-v3')
from ens3 import Ensemble3  # noqa: E402
from s2_model import KONF, V1, V3  # noqa: E402

OUT = os.environ.get('V3_OUT', '/mnt/project-files/model-v3/')  # bisa diganti untuk uji kode

T0 = time.time()
VAL = OUT + 'validasi/'
os.makedirs(VAL, exist_ok=True)
d = pd.read_pickle(V1 + 'tahap1.pkl')
info = d['info']
satker = info.provinsi + '|' + info.nama_satuan_kerja
DEV = set(json.load(open(V1 + 'eksplorasi/provinsi_pilih.json')))
H = pd.read_pickle(OUT + 'tahap2.pkl')
RF3 = pd.read_pickle(V3 + 'red_flag_v3.pkl')
V = pd.read_pickle(V3 + 'r1_variasi_red_flag.pkl')
KS = [50, 100, 200]
NB = 500
SEEDS_B = [5, 6, 7, 8, 9]
AMBANG = {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 400e6, 'Jasa Konsultansi': 100e6}
PAPUA = info.provinsi.str.contains('Papua')


def log(*a):
    print(f'[{time.time() - T0:6.0f}s]', *a, flush=True)


def wilson(k, n, z=1.96):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def topk_beragam(order, sat, K, maks=5):
    """K paket teratas dengan syarat satu satker paling banyak `maks` paket."""
    pilih, hit = [], {}
    for i in order:
        if hit.get(sat[i], 0) < maks:
            pilih.append(i)
            hit[sat[i]] = hit.get(sat[i], 0) + 1
            if len(pilih) == K:
                break
    return pilih


def ukur(s, ada, ada_t4, jumlah):
    s = s.sort_values(ascending=False)
    a = ada.loc[s.index].values
    N, M = len(a), int(a.sum())
    o = {'N': N, 'acuan': M / N}
    for K in KS:
        k = int(a[:K].sum())
        o[f'P@{K}'] = k / K
        o[f'pval@{K}'] = hypergeom.sf(k - 1, N, M, K)
        o[f'rata_rf@{K}'] = jumlah.loc[s.index[:K]].mean()
    o['P@200_ci_lo'], o['P@200_ci_hi'] = wilson(int(a[:200].sum()), 200)
    dev = info.provinsi.loc[s.index].isin(DEV).values
    o['pilih_rata'] = np.mean([a[dev][:K].mean() for K in KS])
    o['uji_rata'] = np.mean([a[~dev][:K].mean() for K in KS])
    o['acuan_pilih'], o['acuan_uji'] = a[dev].mean(), a[~dev].mean()
    b = ada_t4.loc[s.index].values
    o['tanpaRF4_rata'] = np.mean([b[:K].mean() for K in KS])
    o['acuan_tanpaRF4'] = b.mean()
    sat = satker.loc[s.index].values
    o['satker_unik_top200'] = len(set(sat[:200]))
    o['satker_maks_top200'] = pd.Series(sat[:200]).value_counts().iloc[0]
    o['P@200_beragam'] = a[topk_beragam(range(N), sat, 200)].mean()
    n5 = int(N * 0.05)
    o['presisi_5persen'] = a[:n5].mean()
    o['lift_5persen'] = o['presisi_5persen'] / o['acuan']
    o['tanpaRF4_5persen'] = b[:n5].mean()
    o['pilih_5persen'] = a[dev][:int(dev.sum() * 0.05)].mean()
    o['uji_5persen'] = a[~dev][:int((~dev).sum() * 0.05)].mean()
    o['auc_redflag'] = roc_auc_score(a, -np.arange(N))
    return o


class ECOD:
    """Empirical-CDF outlier detection (Li et al., 2022): ekor kiri/kanan per fitur dijumlahkan."""

    def fit(self, X):
        self.S, self.n, self.sk = np.sort(X, axis=0), len(X), np.sign(skew(X, axis=0))
        return self

    def raw(self, X):
        L, R = np.empty_like(X), np.empty_like(X)
        for j in range(X.shape[1]):
            L[:, j] = np.searchsorted(self.S[:, j], X[:, j], side='right') / self.n
            R[:, j] = (self.n - np.searchsorted(self.S[:, j], X[:, j], side='left')) / self.n
        L, R = np.clip(L, 1 / self.n, 1), np.clip(R, 1 / self.n, 1)
        ol, orr = -np.log(L).sum(1), -np.log(R).sum(1)
        oa = -np.log(np.where(self.sk < 0, L, R)).sum(1)
        return np.maximum(np.maximum(ol, orr), oa)


class HBOS:
    """Histogram-based outlier score: jumlah -log kepadatan histogram tiap fitur."""

    def fit(self, X, bins=50):
        self.e, self.h = [], []
        for j in range(X.shape[1]):
            c = X[:, j]
            e = np.array([-0.5, 0.5, 1.5]) if set(np.unique(c)) <= {0.0, 1.0} else np.linspace(c.min(), c.max(), bins + 1)
            h, _ = np.histogram(c, bins=e)
            self.e.append(e)
            self.h.append(np.maximum(h / h.max(), 1e-6))
        return self

    def raw(self, X):
        s = np.zeros(len(X))
        for j, (e, h) in enumerate(zip(self.e, self.h)):
            k = np.searchsorted(e, X[:, j], side='right') - 1
            luar = ((k < 0) | (k >= len(h))) & (X[:, j] != e[-1])
            k[X[:, j] == e[-1]] = len(h) - 1
            s += -np.log(np.where(luar, 1e-6, h[np.clip(k, 0, len(h) - 1)]))
        return s


class KNN:
    def fit(self, ref, k=20):
        self.nn = NearestNeighbors(n_neighbors=k, n_jobs=-1).fit(ref)
        return self

    def raw(self, Z):
        return self.nn.kneighbors(Z)[0].mean(axis=1)


class PCAre:
    def fit(self, Z):
        idx = np.random.default_rng(42).choice(len(Z), size=min(100000, len(Z)), replace=False)
        self.p = PCA(n_components=0.9, random_state=42).fit(Z[idx])
        return self

    def raw(self, Z):
        return ((self.p.inverse_transform(self.p.transform(Z)) - Z) ** 2).mean(axis=1)


class SkorZ:
    """Pembanding paling sederhana: jumlah nilai mutlak skor-z fitur kontinu."""

    def fit(self, Z, cont):
        self.cont, self.mu, self.sd = cont, Z[:, cont].mean(0), Z[:, cont].std(0) + 1e-12
        return self

    def raw(self, Z):
        return np.abs((Z[:, self.cont] - self.mu) / self.sd).sum(1)


def pct_ref(ref_sorted, s):
    return np.searchsorted(ref_sorted, s, side='right') / len(ref_sorted)


def ubah_pagu(F, p_lama, p_baru, S_satker, jalur, a_lama=None, a_baru=None):
    """Perbarui fitur yang bergantung pada pagu (dan realisasi) untuk paket buatan."""
    F = F.copy()
    r = np.log10(p_baru / p_lama)
    F['log_pagu'] = np.log10(p_baru)
    for c in ['log_rasio_pagu_sejenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_serupa']:
        if c in F:
            F[c] += r
    F['porsi_pagu_satker'] = p_baru / (S_satker - p_lama + p_baru)
    if jalur == 'pelaksanaan':
        F['rasio_realisasi'] = np.clip(a_baru / p_baru, None, 5)
        F['log_selisih_realisasi'] = np.log10(1 + np.abs(a_baru - p_baru))
    return F


def buat_sintetis(F, jalur, R, skor_ens, rng, n=1000):
    cols = list(F.columns)
    biner = np.array([set(np.unique(F[c])) <= {0.0, 1.0} for c in cols])
    X = F.values.astype(float)
    C = X[:, ~biner]
    mn, mx = C.min(0), C.max(0)
    mu, sd = C.mean(0), C.std(0) + 1e-12
    out = {}

    def rakit(cont, src_rows):
        Y = X[src_rows].copy()
        Y[:, ~biner] = cont
        return Y

    # 1. global: seragam di [min, max] diperlebar 10%
    lo, hi = mn - 0.1 * (mx - mn), mx + 0.1 * (mx - mn)
    out['global'] = rakit(rng.uniform(lo, hi, size=(n, C.shape[1])), rng.integers(0, len(X), n))
    # 2. lokal (ADBench): GMM pada data asli, kovarians diperbesar 5 kali; kontrol = GMM tanpa diperbesar
    sub = (C[rng.choice(len(C), min(50000, len(C)), replace=False)] - mu) / sd
    g = GaussianMixture(n_components=8, covariance_type='full', random_state=0).fit(sub)

    def sampel_gmm(alpha, m):
        comp = rng.choice(len(g.weights_), size=m, p=g.weights_)
        Z = np.vstack([rng.multivariate_normal(g.means_[k], alpha * g.covariances_[k]) for k in comp])
        return np.clip(Z * sd + mu, mn, mx)

    out['lokal'] = rakit(sampel_gmm(5.0, n), rng.integers(0, len(X), n))
    out['kontrol_normal'] = rakit(sampel_gmm(1.0, n), rng.integers(0, len(X), n))
    # 3. dependensi: tiap fitur diambil acak dari paket berbeda (hubungan antarfitur rusak)
    out['dependensi'] = rakit(np.column_stack([C[rng.integers(0, len(C), n), j] for j in range(C.shape[1])]),
                              rng.integers(0, len(X), n))
    # 4. berkelompok: 20 kelompok x 50 paket hampir kembar, 3 fitur digeser +3 simpangan baku
    rows = []
    for _ in range(20):
        base = C[rng.integers(0, len(C))].copy()
        j = rng.choice(C.shape[1], 3, replace=False)
        base[j] = np.minimum(base[j] + 3 * sd[j], mx[j])
        rows.append(np.clip(base + rng.normal(0, 0.05, (50, C.shape[1])) * sd, mn, mx))
    out['berkelompok'] = rakit(np.vstack(rows), rng.integers(0, len(X), 1000))
    # 5. skenario pengadaan: paket biasa (tanpa red flag, skor di bawah median) yang pagunya digelembungkan 5-20x
    biasa = F.index[(~R.any(axis=1)).values & (skor_ens < skor_ens.median()).values]
    pilih = rng.choice(biasa, n, replace=False)
    inf = info.loc[pilih]
    S = info.pagu.groupby(satker).transform('sum').loc[pilih].values
    p = inf.pagu.values
    f = 10 ** rng.uniform(np.log10(5), np.log10(20), n)
    a = inf.realisasi.values if jalur == 'pelaksanaan' else None
    out['pagu_digelembungkan'] = ubah_pagu(F.loc[pilih], p, p * f, S, jalur, a, None if a is None else a * f)[cols].values
    if jalur == 'pelaksanaan':
        Fx = F.loc[pilih].copy()
        r = rng.uniform(1.3, 3.0, n)
        grp = (inf.jenis + '|' + inf.metode_pengadaan).values
        med = F['rasio_realisasi'].groupby((info.jenis + '|' + info.metode_pengadaan).loc[F.index]).median()
        Fx['rasio_realisasi'] = r
        Fx['log_selisih_realisasi'] = np.log10(1 + (r - 1) * p)
        Fx['selisih_rasio_realisasi_sejenis'] = np.abs(r - med.reindex(grp).values)
        out['realisasi_lewat_pagu'] = Fx[cols].values
    # 6. paket pengadaan langsung kecil dinaikkan ke 90-100% ambang (pola red flag 1)
    pl = F.index[(info.metode_pengadaan.loc[F.index] == 'Pengadaan Langsung').values
                 & (info.pagu.loc[F.index] < 0.5 * info.jenis.loc[F.index].map(AMBANG)).values
                 & ~R.any(axis=1).values]
    pilih = rng.choice(pl, n, replace=False)
    inf = info.loc[pilih]
    T = inf.jenis.map(AMBANG).values
    p, p2 = inf.pagu.values, rng.uniform(0.9, 1.0, n) * T
    S = info.pagu.groupby(satker).transform('sum').loc[pilih].values
    a = inf.realisasi.values if jalur == 'pelaksanaan' else None
    out['dekat_ambang'] = ubah_pagu(F.loc[pilih], p, p2, S, jalur, a, None if a is None else a * p2 / p)[cols].values
    return out


def simpan(rows, nama):
    pd.DataFrame(rows).to_csv(VAL + nama, index=False)


K_rows, rf_rows, tt_rows, boot_rows, stab_rows, amb_rows, sin_rows, pred_rows, kv_rows = ([] for _ in range(9))
for jalur in ['pelaksanaan', 'perencanaan']:
    h = H[jalur]
    F, m, sk, R = h['F'], h['model'], h['skor'], h['rf']
    X = F.values.astype(float)
    ada = R.any(axis=1)
    ada_t4 = R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    m0 = m.m[0]  # anggota seed 42, dipakai untuk penskalaan pembanding
    Z = m0._z(X)
    cont = np.array([not set(np.unique(F[c])) <= {0.0, 1.0} for c in F])
    log(jalur, F.shape)

    # ---- 1. pembanding
    skor = {'Ensemble': sk.Ensemble, 'IF': sk.IF, 'LOF': sk.LOF, 'AE': sk.AE}
    skor['Acak'] = pd.Series(np.random.default_rng(0).random(len(F)), index=F.index)
    skor['Pagu terbesar'] = F['log_pagu']
    skor['Rasio pagu sejenis terbesar'] = F['log_rasio_pagu_sejenis']
    det = {'Skor-z sederhana': SkorZ().fit(Z, cont), 'ECOD': ECOD().fit(X), 'HBOS': HBOS().fit(X),
           'KNN': KNN().fit(m0.lof._fit_X), 'PCA': PCAre().fit(Z)}
    pakai_z = {'Skor-z sederhana', 'KNN', 'PCA'}
    det_ref = {}
    for k, dm in det.items():
        s = dm.raw(Z if k in pakai_z else X)
        det_ref[k] = np.sort(s)
        skor[k] = pd.Series(s, index=F.index)
    log(jalur, 'pembanding selesai')
    for nama, s in skor.items():
        K_rows.append({'jalur': jalur, 'metode': nama, **ukur(s, ada, ada_t4, R.sum(axis=1))})
    simpan(K_rows, 'v_konvergen.csv')

    # ---- 2. lift per red flag dan tumpang tindih red flag dengan fitur
    n5 = int(len(F) * 0.05)
    for nama in ['Ensemble', 'IF', 'LOF', 'AE', 'Skor-z sederhana', 'Pagu terbesar', 'Acak']:
        o = skor[nama].sort_values(ascending=False).index
        for c in R:
            base = R[c].mean()
            rf_rows.append({'jalur': jalur, 'metode': nama, 'red_flag': c, 'acuan': base,
                            'top200': R[c].loc[o[:200]].mean(), 'top5persen': R[c].loc[o[:n5]].mean(),
                            'lift_top200': R[c].loc[o[:200]].mean() / base, 'lift_top5persen': R[c].loc[o[:n5]].mean() / base})
    for c in R:
        aucs = sorted(((max(a_, 1 - a_), f) for f in F.columns if F[f].nunique() > 1
                       for a_ in [roc_auc_score(R[c], F[f])]), reverse=True)
        tt_rows.append({'jalur': jalur, 'red_flag': c, 'fitur_terdekat': aucs[0][1], 'auc': aucs[0][0],
                        'fitur_kedua': aucs[1][1], 'auc_kedua': aucs[1][0]})
    simpan(rf_rows, 'v_per_redflag.csv')
    simpan(tt_rows, 'v_tumpang_tindih.csv')

    # ---- 3. bootstrap per satker
    sat = satker.loc[F.index].values
    kode, inv = np.unique(sat, return_inverse=True)
    anggota = [np.flatnonzero(inv == i) for i in range(len(kode))]
    a_np = ada.values
    nm_b = ['Ensemble', 'IF', 'LOF', 'AE', 'Acak', 'Pagu terbesar', 'Rasio pagu sejenis terbesar', 'Skor-z sederhana',
            'ECOD', 'HBOS', 'KNN', 'PCA']
    sb = {k: skor[k].values for k in nm_b}
    hb = {k: [] for k in nm_b}
    rng = np.random.default_rng(123)
    for _ in range(NB):
        ix = np.concatenate([anggota[i] for i in rng.integers(0, len(kode), len(kode))])
        for k, s in sb.items():
            top = ix[np.argpartition(-s[ix], 200)[:200]]
            hb[k].append(a_np[top].mean())
    for k, v in hb.items():
        v, dif = np.array(v), np.array(hb['Ensemble']) - np.array(v)
        boot_rows.append({'jalur': jalur, 'metode': k, 'P@200_boot_rata': v.mean(), 'ci_lo': np.percentile(v, 2.5),
                          'ci_hi': np.percentile(v, 97.5), 'acuan': a_np.mean(), 'selisih_ens_rata': dif.mean(),
                          'selisih_ci_lo': np.percentile(dif, 2.5), 'selisih_ci_hi': np.percentile(dif, 97.5),
                          'peluang_ens_lebih_baik': (dif > 0).mean()})
    simpan(boot_rows, 'v_bootstrap.csv')
    log(jalur, 'bootstrap selesai')

    # ---- 4. kestabilan: ensemble kedua dengan 5 seed lain
    m2 = Ensemble3(seeds=SEEDS_B, **KONF[jalur]['model']).fit(F)
    s2 = pd.Series(m2.score(X), index=F.index)
    ps = h['per_seed']
    samp = np.random.default_rng(0).choice(len(F), min(50000, len(F)), replace=False)

    def banding(a, b):
        A2, B2 = set(a.nlargest(200).index), set(b.nlargest(200).index)
        A5, B5 = set(a.nlargest(n5).index), set(b.nlargest(n5).index)
        return {'jaccard_top200': len(A2 & B2) / len(A2 | B2), 'jaccard_anomali5persen': len(A5 & B5) / len(A5 | B5),
                'spearman_skor': spearmanr(a.values[samp], b.values[samp])[0]}

    satu = [banding(ps[c1], ps[c2]) for i, c1 in enumerate(ps) for c2 in list(ps)[i + 1:]]
    stab_rows.append({'jalur': jalur, 'perbandingan': 'satu seed vs satu seed (rata-rata 10 pasangan)',
                      **pd.DataFrame(satu).mean().to_dict()})
    stab_rows.append({'jalur': jalur, 'perbandingan': 'rata-rata 5 seed vs rata-rata 5 seed lain', **banding(sk.Ensemble, s2),
                      'P@200_ensemble_kedua': ada.loc[s2.nlargest(200).index].mean()})
    simpan(stab_rows, 'v_stabilitas.csv')
    log(jalur, 'kestabilan selesai', stab_rows[-2], stab_rows[-1])

    # ---- 5. kepekaan ambang dan peta provinsi
    e = sk.Ensemble
    prov = info.provinsi.loc[F.index]
    tab = {}
    rf_prov = ada.groupby(prov).mean()
    for q in (0.01, 0.05, 0.10):
        an = e >= e.quantile(1 - q)
        tab[q] = an.groupby(prov).mean()
        rho, p = spearmanr(tab[q], rf_prov.loc[tab[q].index])
        bukan = ~tab[q].index.str.contains('Papua')
        rho2, p2 = spearmanr(tab[q][bukan], rf_prov.loc[tab[q].index][bukan])
        amb_rows.append({'jalur': jalur, 'ambang': f'{int(q * 100)}%', 'paket_anomali': int(an.sum()),
                         'presisi_redflag': ada[an].mean(), 'acuan': ada.mean(), 'lift': ada[an].mean() / ada.mean(),
                         'spearman_provinsi_redflag': rho, 'p': p, 'spearman_tanpa_papua': rho2, 'p_tanpa_papua': p2,
                         'porsi_papua_di_anomali': PAPUA.loc[F.index][an].mean(), 'porsi_papua_semua': PAPUA.loc[F.index].mean()})
    T = pd.DataFrame(tab)
    for q1, q2 in [(0.01, 0.05), (0.05, 0.10), (0.01, 0.10)]:
        amb_rows.append({'jalur': jalur, 'ambang': f'peringkat provinsi {int(q1 * 100)}% vs {int(q2 * 100)}%',
                         'spearman_provinsi_redflag': spearmanr(T[q1], T[q2])[0]})
    simpan(amb_rows, 'v_ambang.csv')

    # ---- 6. anomali buatan
    rng = np.random.default_rng(7)
    sint = buat_sintetis(F, jalur, R, e, rng)
    thr_ens = e.quantile(0.95)
    for tipe, Y in sint.items():
        P = m.pct(Y)
        pk = {'IF': P['IF'], 'LOF': P['LOF'], 'AE': P['AE'], 'Ensemble': (P['IF'] + P['LOF'] + P['AE']) / 3}
        for k, dm in det.items():
            pk[k] = pct_ref(det_ref[k], dm.raw(m0._z(Y) if k in pakai_z else Y))
        for k, v in pk.items():
            # ambang = persentil ke-95 skor metode itu pada data asli (IF/LOF/AE: persentil rata-rata seed)
            thr = thr_ens if k == 'Ensemble' else (h['pct_rata'][k].quantile(0.95) if k in ('IF', 'LOF', 'AE') else 0.95)
            sin_rows.append({'jalur': jalur, 'tipe': tipe, 'metode': k, 'n': len(Y), 'terdeteksi_5persen': (v >= thr).mean(),
                             'median_persentil': np.median(v)})
    simpan(sin_rows, 'v_sintetis.csv')
    log(jalur, 'anomali buatan selesai')

    # ---- 8. konsistensi antar-red flag di tingkat satker (satker >= 30 paket)
    s_ = satker.loc[F.index]
    n_sat = s_.map(s_.value_counts())
    rate = R[n_sat.values >= 30].groupby(s_[n_sat.values >= 30]).mean()
    cols = list(R.columns)
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            rho, p = spearmanr(rate[a], rate[b])
            kv_rows.append({'jalur': jalur, 'satker': len(rate), 'rf_a': a, 'rf_b': b, 'spearman': rho, 'p': p})
    simpan(kv_rows, 'v_redflag_konvergen.csv')

# ---- 7. validitas prediktif lintas tahap
idx = d['f_pel'].index.intersection(H['perencanaan']['skor'].index)
s = H['perencanaan']['skor'].Ensemble.loc[idx]
Fp = H['perencanaan']['F'].loc[idx]
target = {
    'RF5 penyedia dominan (OCP R040)': RF3.loc[idx, 'rf5_penyedia_dominan'],
    'RF6 penyedia serba-ada': RF3.loc[idx, 'rf6_penyedia_serba_ada'],
    'R049 PL dekat ambang berulang ke penyedia sama': V.loc[idx, 'baru_R049_pl_dekat_ambang_berulang'],
    'R055 PL berulang ke penyedia sama, jumlah lewat ambang': V.loc[idx, 'baru_R055_pl_berulang_lewat_ambang'],
    'R068 realisasi melebihi pagu': V.loc[idx, 'baru_R068_realisasi_lewat_pagu'],
}
# strata ukuran paket: desil pagu x desil porsi pagu di satker (kontrol: apakah skor memberi informasi di luar ukuran?)
strata = (pd.qcut(Fp.log_pagu.rank(method='first'), 10, labels=False).astype(str) + '|'
          + pd.qcut(Fp.porsi_pagu_satker.rank(method='first'), 10, labels=False).astype(str))
srt = s.sort_values(ascending=False)
N = len(srt)
for nama, t in target.items():
    t = t.astype(bool)
    harap = t.groupby(strata).transform('mean')  # peluang target bila hanya ukuran paket yang diketahui
    a = t.loc[srt.index].values
    M = int(a.sum())
    o = {'target': nama, 'acuan_persen': 100 * M / N}
    for q in (0.01, 0.05, 0.10):
        K = int(N * q)
        k = int(a[:K].sum())
        e_ = harap.loc[srt.index[:K]].values
        z = (k - e_.sum()) / np.sqrt((e_ * (1 - e_)).sum() + 1e-12)
        o.update({f'top{int(q * 100)}_persen': 100 * k / K, f'lift_top{int(q * 100)}': (k / K) / (M / N),
                  f'pval_top{int(q * 100)}': hypergeom.sf(k - 1, N, M, K),
                  f'lift_terkontrol_top{int(q * 100)}': k / e_.sum(), f'pval_terkontrol_top{int(q * 100)}': norm.sf(z)})
    o['auc'] = roc_auc_score(a, -np.arange(N))
    pred_rows.append(o)
simpan(pred_rows, 'v_prediktif.csv')
log('SELESAI')
