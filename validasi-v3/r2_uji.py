"""Validasi v3, bagian 2: uji untuk model v2 (tanpa mengubah model).

1. Uji signifikansi Precision@K (hipergeometrik) + selang kepercayaan bootstrap per satker.
2. Pembanding sederhana (acak, pagu terbesar, rasio pagu sejenis, skor-z) dan metode lain
   (ECOD, HBOS, KNN, PCA) serta ensemble dua model (uji peran tiap model).
3. Kestabilan: 5 seed, ambang 1/5/10%, sebaran provinsi (termasuk Papua).
4. Ketahanan terhadap definisi red flag (varian dari r1).
5. Anomali buatan (gaya ADBench + skenario pengadaan): seberapa banyak yang masuk 5% teratas.
6. Uji kesetiaan SHAP (deletion test): skor turun lebih banyak bila fitur teratas SHAP dihapus?
"""
import json
import sys
import time
import numpy as np
import pandas as pd
from scipy.stats import hypergeom, spearmanr, skew
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors

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
import os
QUICK = os.environ.get('QUICK') == '1'  # uji cepat kode pada sampel kecil
SEEDS = [42, 1] if QUICK else [42, 1, 2, 3, 4]
NB = 20 if QUICK else 500
PRE = 'quick_' if QUICK else ''
KS = [50, 100, 200]
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
        s = sat[i]
        if hit.get(s, 0) < maks:
            pilih.append(i)
            hit[s] = hit.get(s, 0) + 1
            if len(pilih) == K:
                break
    return pilih


def ukur(s, ada, jalur, ada_t4=None):
    """Metrik evaluasi untuk satu skor (Series, makin besar makin janggal)."""
    s = s.sort_values(ascending=False)
    a = ada.loc[s.index].values
    N, M = len(a), int(a.sum())
    o = {'N': N, 'acuan': M / N}
    for K in KS:
        k = int(a[:K].sum())
        o[f'P@{K}'] = k / K
        o[f'pval@{K}'] = hypergeom.sf(k - 1, N, M, K)
    lo, hi = wilson(int(a[:200].sum()), 200)
    o['P@200_ci_lo'], o['P@200_ci_hi'] = lo, hi
    prov = info.provinsi.loc[s.index].isin(DEV).values
    for nama, m in [('pilih', prov), ('uji', ~prov)]:
        aa = a[m]
        o[f'{nama}_rata'] = np.mean([aa[:K].mean() for K in KS])
    if ada_t4 is not None:
        b = ada_t4.loc[s.index].values
        o['tanpaRF4_rata'] = np.mean([b[:K].mean() for K in KS])
    sat = satker.loc[s.index].values
    o['satker_unik_top200'] = len(set(sat[:200]))
    o['satker_maks_top200'] = pd.Series(sat[:200]).value_counts().iloc[0]
    pos = topk_beragam(range(N), sat, 200)
    o['P@200_beragam'] = a[pos].mean()
    n5 = int(N * 0.05)
    o['presisi_5persen'] = a[:n5].mean()
    o['lift_5persen'] = o['presisi_5persen'] / o['acuan']
    o['auc_redflag'] = roc_auc_score(a, -np.arange(N))
    return o


# ------------------------------------------------------------------ metode pembanding
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
            luar = (k < 0) | (k >= len(h))
            k[X[:, j] == e[-1]] = len(h) - 1
            luar &= X[:, j] != e[-1]
            dens = np.where(luar, 1e-6, h[np.clip(k, 0, len(h) - 1)])
            s += -np.log(dens)
        return s


class KNN:
    def fit(self, ref, k=20):
        self.nn = NearestNeighbors(n_neighbors=k, n_jobs=-1).fit(ref)
        return self

    def raw(self, Z):
        return self.nn.kneighbors(Z)[0].mean(axis=1)


class PCAre:
    def fit(self, Z):
        rng = np.random.default_rng(42)
        idx = rng.choice(len(Z), size=min(100000, len(Z)), replace=False)
        self.p = PCA(n_components=0.9, random_state=42).fit(Z[idx])
        return self

    def raw(self, Z):
        return ((self.p.inverse_transform(self.p.transform(Z)) - Z) ** 2).mean(axis=1)


def pct_ref(ref_sorted, s):
    return np.searchsorted(ref_sorted, s, side='right') / len(ref_sorted)


# ------------------------------------------------------------------ anomali buatan
def ubah_pagu(F, p_lama, p_baru, S_satker, jalur, a_lama=None, a_baru=None):
    """Perbarui fitur yang bergantung pada pagu (dan realisasi) untuk paket buatan."""
    F = F.copy()
    r = np.log10(p_baru / p_lama)
    F['log_pagu'] = np.log10(p_baru)
    F['log_rasio_pagu_sejenis'] += r
    F['log_rasio_pagu_satker'] += r
    F['porsi_pagu_satker'] = p_baru / (S_satker - p_lama + p_baru)
    if jalur == 'pelaksanaan':
        F['rasio_realisasi'] = np.clip(a_baru / p_baru, None, 5)
        F['log_selisih_realisasi'] = np.log10(1 + np.abs(a_baru - p_baru))
    return F


def buat_sintetis(F, jalur, flags, skor_ens, rng, n=1000):
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
    # 2. lokal (ADBench): GMM pada data normal, kovarians diperbesar 5 kali; kontrol = GMM tanpa diperbesar
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
    # 5. skenario pengadaan: paket biasa (tanpa red flag, skor di bawah median) yang dimanipulasi
    biasa = F.index[(~rf.loc[F.index, flags].any(axis=1)).values & (skor_ens < skor_ens.median()).values]
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
                 & ~rf.loc[F.index, flags].any(axis=1).values]
    pilih = rng.choice(pl, n, replace=False)
    inf = info.loc[pilih]
    T = inf.jenis.map(AMBANG).values
    p, p2 = inf.pagu.values, rng.uniform(0.9, 1.0, n) * T
    S = info.pagu.groupby(satker).transform('sum').loc[pilih].values
    a = inf.realisasi.values if jalur == 'pelaksanaan' else None
    out['dekat_ambang'] = ubah_pagu(F.loc[pilih], p, p2, S, jalur, a, None if a is None else a * p2 / p)[cols].values
    return out


# ------------------------------------------------------------------ utama
semua_metrik, boot_rows, stab_rows, prov_rows, var_rows, sin_rows, del_rows = [], [], [], [], [], [], []
V = pd.read_pickle(OUT + 'r1_variasi_red_flag.pkl')
SKOR = {}
for jalur in ['perencanaan', 'pelaksanaan']:
    F = fitur(d, jalur, KONF[jalur]['pdn_umk'])
    if QUICK:
        F = F.sample(40000, random_state=0)
    X = F.values.astype(float)
    flags = FL[jalur]
    R = rf.loc[F.index, flags]
    ada, ada_t4 = R.any(axis=1), R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    log(jalur, F.shape)

    # --- model v2 dengan 5 seed
    per_seed, models = {}, {}
    for sd in SEEDS:
        ens2.SEED = sd
        m = ens2.Ensemble2(**KONF[jalur]['model']).fit(F)
        raw = m.raw(X)
        P = {k: pd.Series(pct_ref(m.ref[k], raw[k]), index=F.index).rank(pct=True) for k in ['IF', 'LOF', 'AE']}
        P['Ensemble'] = (P['IF'] + P['LOF'] + P['AE']) / 3
        per_seed[sd], models[sd] = P, m
        log(jalur, 'seed', sd, 'P@200 ens', round(ada.loc[P['Ensemble'].nlargest(200).index].mean(), 3))
    m42, P42 = models[42], per_seed[42]
    Z = m42._z(X)

    # --- metode pembanding (seed 42)
    alt = {}
    alt['Acak'] = pd.Series(np.random.default_rng(0).random(len(F)), index=F.index)
    alt['Pagu terbesar'] = F['log_pagu']
    alt['Rasio pagu sejenis terbesar'] = F['log_rasio_pagu_sejenis']
    cont = np.array([not set(np.unique(F[c])) <= {0.0, 1.0} for c in F])
    alt['Skor-z sederhana'] = pd.Series(np.abs((Z[:, cont] - Z[:, cont].mean(0)) / (Z[:, cont].std(0) + 1e-12)).sum(1), index=F.index)
    if jalur == 'pelaksanaan':
        alt['Selisih rasio realisasi terbesar'] = F['selisih_rasio_realisasi_sejenis']
    det = {'ECOD': ECOD().fit(X), 'HBOS': HBOS().fit(X), 'KNN': KNN().fit(m42.lof._fit_X), 'PCA': PCAre().fit(Z)}
    det_ref = {}
    for k, dm in det.items():
        s = dm.raw(Z if k in ('KNN', 'PCA') else X)
        det_ref[k] = np.sort(s)
        alt[k] = pd.Series(s, index=F.index)
        log(jalur, 'pembanding', k, 'P@200', round(ada.loc[alt[k].nlargest(200).index].mean(), 3))
    for a, b in [('IF', 'LOF'), ('IF', 'AE'), ('LOF', 'AE')]:
        alt[f'Ensemble {a}+{b}'] = (P42[a] + P42[b]) / 2

    # --- metrik
    for nama in ['Ensemble', 'IF', 'LOF', 'AE']:
        rows = [ukur(per_seed[sd][nama], ada, jalur, ada_t4) for sd in SEEDS]
        dfm = pd.DataFrame(rows)
        o = dfm.mean().to_dict()
        o.update({f'{c}_sd': dfm[c].std() for c in ['P@50', 'P@100', 'P@200', 'uji_rata', 'tanpaRF4_rata']})
        o.update({'jalur': jalur, 'metode': nama, 'kelompok': 'model v2 (rata-rata 5 seed)'})
        semua_metrik.append(o)
    for nama, s in alt.items():
        o = ukur(s, ada, jalur, ada_t4)
        o.update({'jalur': jalur, 'metode': nama, 'kelompok': 'pembanding (seed 42)'})
        semua_metrik.append(o)
    pd.DataFrame(semua_metrik).to_csv(OUT + PRE + 'r2_metrik.csv', index=False)
    log(jalur, 'metrik selesai')

    # --- bootstrap per satker (P@200 dan selisih berpasangan dengan Ensemble)
    sat = satker.loc[F.index].values
    kode, inv = np.unique(sat, return_inverse=True)
    anggota = [np.flatnonzero(inv == i) for i in range(len(kode))]
    skor_b = {'Ensemble': P42['Ensemble'].values, 'IF': P42['IF'].values, 'LOF': P42['LOF'].values, 'AE': P42['AE'].values}
    for k in ['Pagu terbesar', 'Rasio pagu sejenis terbesar', 'Skor-z sederhana', 'ECOD', 'HBOS', 'KNN', 'PCA']:
        skor_b[k] = alt[k].values
    a_np = ada.values
    rng = np.random.default_rng(123)
    hasil_b = {k: [] for k in skor_b}
    for _ in range(NB):
        ix = np.concatenate([anggota[i] for i in rng.integers(0, len(kode), len(kode))])
        for k, s in skor_b.items():
            top = ix[np.argpartition(-s[ix], 200)[:200]]
            hasil_b[k].append(a_np[top].mean())
    for k, v in hasil_b.items():
        v = np.array(v)
        dif = np.array(hasil_b['Ensemble']) - v
        boot_rows.append({'jalur': jalur, 'metode': k, 'P@200_boot_rata': v.mean(), 'ci_lo': np.percentile(v, 2.5),
                          'ci_hi': np.percentile(v, 97.5), 'acuan': a_np.mean(),
                          'selisih_ens_rata': dif.mean(), 'selisih_ci_lo': np.percentile(dif, 2.5),
                          'selisih_ci_hi': np.percentile(dif, 97.5), 'peluang_ens_lebih_baik': (dif > 0).mean()})
    pd.DataFrame(boot_rows).to_csv(OUT + PRE + 'r2_bootstrap.csv', index=False)
    log(jalur, 'bootstrap selesai')

    # --- kestabilan antar-seed
    for nama in ['Ensemble', 'IF', 'LOF', 'AE']:
        jac, rho = [], []
        samp = np.random.default_rng(0).choice(len(F), min(50000, len(F)), replace=False)
        for i, s1 in enumerate(SEEDS):
            for s2 in SEEDS[i + 1:]:
                A1 = set(per_seed[s1][nama].nlargest(200).index)
                A2 = set(per_seed[s2][nama].nlargest(200).index)
                jac.append(len(A1 & A2) / len(A1 | A2))
                rho.append(spearmanr(per_seed[s1][nama].values[samp], per_seed[s2][nama].values[samp])[0])
        an = [set(per_seed[sd][nama][per_seed[sd][nama] >= per_seed[sd][nama].quantile(0.95)].index) for sd in SEEDS]
        jac5 = np.mean([len(an[i] & an[j]) / len(an[i] | an[j]) for i in range(len(an)) for j in range(i + 1, len(an))])
        stab_rows.append({'jalur': jalur, 'metode': nama, 'jaccard_top200': np.mean(jac), 'jaccard_top200_min': np.min(jac),
                          'jaccard_anomali5persen': jac5, 'spearman_skor': np.mean(rho)})
    pd.DataFrame(stab_rows).to_csv(OUT + PRE + 'r2_stabilitas.csv', index=False)

    # --- ambang 1/5/10% dan sebaran provinsi
    e = P42['Ensemble']
    prov = info.provinsi.loc[F.index]
    tab = {}
    for q in (0.01, 0.05, 0.10):
        an = e >= e.quantile(1 - q)
        tab[q] = an.groupby(prov).mean()
        prov_rows.append({'jalur': jalur, 'ambang': f'{int(q * 100)}%', 'paket_anomali': int(an.sum()),
                          'presisi_redflag': ada[an].mean(), 'acuan': ada.mean(),
                          'porsi_papua_di_anomali': PAPUA.loc[F.index][an].mean(), 'porsi_papua_semua': PAPUA.loc[F.index].mean(),
                          'presisi_papua': ada[an & PAPUA.loc[F.index]].mean(), 'presisi_non_papua': ada[an & ~PAPUA.loc[F.index]].mean(),
                          'acuan_papua': ada[PAPUA.loc[F.index]].mean(), 'acuan_non_papua': ada[~PAPUA.loc[F.index]].mean()})
    T = pd.DataFrame(tab)
    rf_prov = ada.groupby(prov).mean()
    for q1, q2 in [(0.01, 0.05), (0.05, 0.10), (0.01, 0.10)]:
        prov_rows.append({'jalur': jalur, 'ambang': f'spearman peringkat provinsi {int(q1 * 100)}% vs {int(q2 * 100)}%',
                          'nilai': spearmanr(T[q1], T[q2])[0]})
    rho, p = spearmanr(T[0.05], rf_prov)
    prov_rows.append({'jalur': jalur, 'ambang': 'spearman proporsi anomali 5% vs tingkat red flag provinsi', 'nilai': rho, 'p': p})
    for c in flags:
        rho, p = spearmanr(T[0.05], R[c].groupby(prov).mean())
        prov_rows.append({'jalur': jalur, 'ambang': f'spearman proporsi anomali 5% vs {c}', 'nilai': rho, 'p': p})
    T.to_csv(OUT + PRE + f'r2_provinsi_ambang_{jalur}.csv')
    pd.DataFrame(prov_rows).to_csv(OUT + PRE + 'r2_ambang_provinsi.csv', index=False)

    # --- ketahanan terhadap definisi red flag (Ensemble seed 42)
    amb = info.jenis.map(AMBANG)
    pl = info.metode_pengadaan == 'Pengadaan Langsung'
    rf1_ganda = rf['rf1_pl_dekat_ambang'] | (pl & (info.jenis == 'Pekerjaan Konstruksi') & (info.pagu >= 180e6) & (info.pagu <= 200e6))
    varian = {'asli': R,
              'RF1 konstruksi juga 180-200 jt': R.assign(rf1_pl_dekat_ambang=rf1_ganda.loc[F.index]),
              'RF1 95% ambang': R.assign(rf1_pl_dekat_ambang=V.loc[F.index, 'rf1_dekat_ambang_95persen']),
              'RF3 cosine 0,7': R.assign(rf3_pemecahan_paket=V.loc[F.index, 'rf3_pemecahan_cos70']),
              'RF3 cosine 0,9': R.assign(rf3_pemecahan_paket=V.loc[F.index, 'rf3_pemecahan_cos90']),
              'tanpa RF4': R.drop(columns='rf4_penunjukan_langsung')}
    if jalur == 'pelaksanaan':
        varian['RF5 versi OCP R040 (porsi > 40%)'] = R.assign(rf5_penyedia_dominan=V.loc[F.index, 'rf5_porsi40_n5'])
        varian['RF5 dibuang'] = R.drop(columns='rf5_penyedia_dominan')
        varian['+ R049 PL dekat ambang berulang'] = R.assign(r049=V.loc[F.index, 'baru_R049_pl_dekat_ambang_berulang'])
        varian['+ R055 PL berulang lewat ambang'] = R.assign(r055=V.loc[F.index, 'baru_R055_pl_berulang_lewat_ambang'])
        varian['usulan: RF1 ganda + RF5 OCP + R049'] = R.assign(
            rf1_pl_dekat_ambang=rf1_ganda.loc[F.index], rf5_penyedia_dominan=V.loc[F.index, 'rf5_porsi40_n5'],
            r049=V.loc[F.index, 'baru_R049_pl_dekat_ambang_berulang'])
    else:
        varian['usulan: RF1 ganda'] = R.assign(rf1_pl_dekat_ambang=rf1_ganda.loc[F.index])
    for vn, RV in varian.items():
        av = RV.any(axis=1)
        for nama in ['Ensemble', 'IF', 'LOF', 'AE']:
            o = ukur(P42[nama], av, jalur)
            var_rows.append({'jalur': jalur, 'varian': vn, 'metode': nama, **{k: o[k] for k in
                             ['acuan', 'P@50', 'P@100', 'P@200', 'pval@200', 'uji_rata', 'P@200_beragam', 'lift_5persen', 'auc_redflag']}})
    pd.DataFrame(var_rows).to_csv(OUT + PRE + 'r2_redflag_varian.csv', index=False)
    log(jalur, 'varian red flag selesai')

    # --- anomali buatan
    rng = np.random.default_rng(7)
    sint = buat_sintetis(F, jalur, flags, P42['Ensemble'], rng)
    raw_real = m42.raw(X)
    ens_real = np.mean([pct_ref(m42.ref[k], raw_real[k]) for k in ['IF', 'LOF', 'AE']], axis=0)
    thr_ens = np.quantile(ens_real, 0.95)
    samp = np.random.default_rng(1).choice(len(X), min(50000, len(X)), replace=False)
    for tipe, Y in sint.items():
        rawY = m42.raw(Y)
        pk = {k: pct_ref(m42.ref[k], rawY[k]) for k in ['IF', 'LOF', 'AE']}
        pk['Ensemble'] = np.mean([pk['IF'], pk['LOF'], pk['AE']], axis=0)
        real = {k: pct_ref(m42.ref[k], raw_real[k]) for k in ['IF', 'LOF', 'AE']}
        real['Ensemble'] = ens_real
        for k, dm in det.items():
            rY = dm.raw(m42._z(Y) if k in ('KNN', 'PCA') else Y)
            pk[k] = pct_ref(det_ref[k], rY)
            real[k] = pct_ref(det_ref[k], alt[k].values)
        for k in pk:
            thr = thr_ens if k == 'Ensemble' else 0.95
            y = np.r_[np.ones(len(Y)), np.zeros(len(samp))]
            sc = np.r_[pk[k], real[k][samp]]
            sin_rows.append({'jalur': jalur, 'tipe': tipe, 'metode': k, 'n': len(Y),
                             'terdeteksi_5persen': (pk[k] >= thr).mean(), 'auc': roc_auc_score(y, sc),
                             'median_persentil': np.median(pk[k])})
    pd.DataFrame(sin_rows).to_csv(OUT + PRE + 'r2_sintetis.csv', index=False)
    log(jalur, 'anomali buatan selesai')
    SKOR[jalur] = dict(per_seed={sd: pd.DataFrame(per_seed[sd]) for sd in SEEDS}, alt=pd.DataFrame(alt))

# ------------------------------------------------------------------ uji kesetiaan SHAP (model v2 tersimpan)
h2 = pd.read_pickle('/mnt/project-files/model-v2/tahap2.pkl')
h3 = pd.read_pickle('/mnt/project-files/model-v2/tahap3.pkl')
GRUP = {'metode_': 'metode', 'jenis_': 'jenis', 'sumber_': 'sumber'}
for jalur in ['perencanaan', 'pelaksanaan']:
    F, m = h2[jalur]['F'], h2[jalur]['model']
    sv = h3[jalur]['shap']
    grp = {}
    for c in F.columns:
        grp.setdefault(next((v for k, v in GRUP.items() if c.startswith(k)), c), []).append(list(F.columns).index(c))
    bg = F.sample(50, random_state=42).values.astype(float)
    rng = np.random.default_rng(5)
    hasil = []
    for kode in sv.index:
        x = F.loc[kode].values.astype(float)
        s0 = m.score(x[None, :])[0]
        urut = sv.loc[kode].sort_values(ascending=False)

        def hapus(gs):
            Y = np.repeat(x[None, :], len(bg), axis=0)
            for g in gs:
                Y[:, grp[g]] = bg[:, grp[g]]
            return s0 - m.score(Y).mean()

        top1, top3 = list(urut.index[:1]), list(urut.index[:3])
        lain = [g for g in sv.columns if g not in top3]
        acak1 = list(rng.choice([g for g in sv.columns if g not in top1], 1))
        acak3 = list(rng.choice(lain, min(3, len(lain)), replace=False))
        hasil.append({'turun_top1': hapus(top1), 'turun_acak1': hapus(acak1),
                      'turun_top3': hapus(top3), 'turun_acak3': hapus(acak3)})
    hs = pd.DataFrame(hasil)
    del_rows.append({'jalur': jalur, 'paket': len(hs),
                     'turun_top1_rata': hs.turun_top1.mean(), 'turun_acak1_rata': hs.turun_acak1.mean(),
                     'top1_lebih_besar_persen': 100 * (hs.turun_top1 > hs.turun_acak1).mean(),
                     'turun_top3_rata': hs.turun_top3.mean(), 'turun_acak3_rata': hs.turun_acak3.mean(),
                     'top3_lebih_besar_persen': 100 * (hs.turun_top3 > hs.turun_acak3).mean()})
    log(jalur, 'uji SHAP', del_rows[-1])
pd.DataFrame(del_rows).to_csv(OUT + PRE + 'r2_shap_deletion.csv', index=False)
pd.to_pickle(SKOR, OUT + PRE + 'r2_skor.pkl')
log('SELESAI')
