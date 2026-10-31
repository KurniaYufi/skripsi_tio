"""Validasi v3, bagian 1: bukti red flag di data (tanpa model).

1. Uji penumpukan (bunching) di sekitar ambang pengadaan langsung (OCP R002; metode Kleven & Waseem
   seperti dipakai Coviello et al., 2022): apakah pagu menumpuk tepat di bawah ambang?
2. Kemunculan bersama red flag (tingkat paket) dan validitas konvergen tingkat satker
   (satker yang sering kena satu red flag juga sering kena red flag lain?).
3. Variasi definisi red flag (ambang sensitivitas) dan kandidat red flag baru dari panduan OCP.
Keluaran: CSV di folder ini + bunching.pkl untuk gambar.
"""
import re
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import TfidfVectorizer

V1 = '/mnt/project-files/model-v1/'
OUT = '/mnt/project-files/validasi-v3/'
d = pd.read_pickle(V1 + 'tahap1.pkl')
info, rf = d['info'], d['rf']
idx_pel = d['f_pel'].index
satker = info.provinsi + '|' + info.nama_satuan_kerja
AMBANG = {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 400e6, 'Jasa Konsultansi': 100e6}
amb = info.jenis.map(AMBANG)
is_pl = info.metode_pengadaan == 'Pengadaan Langsung'

# ---------------------------------------------------------------- 1. Bunching
def bunching(x, T, lebar=0.01, lo=0.5, hi=1.5, jendela=(0.9, 1.1), derajat=7):
    """Hitung jumlah paket per bin 1% ambang lalu bandingkan dengan perkiraan tanpa ambang.

    Perkiraan = polinomial + dummy angka bulat (kelipatan 5/10/25/50% ambang) yang dipasang
    di luar jendela, sehingga penumpukan karena angka bulat tidak dihitung sebagai efek ambang.
    """
    r = x / T
    tepi = np.round(np.arange(lo, hi + 1e-9, lebar), 4)
    n, _ = np.histogram(r, bins=tepi)
    # bin tertutup kanan (a, b]: nilai tepat di ambang masuk bin terakhir di bawah ambang
    n = np.array([((r > a) & (r <= b)).sum() for a, b in zip(tepi[:-1], tepi[1:])])
    kanan = tepi[1:]
    tengah = (tepi[:-1] + tepi[1:]) / 2 - 1
    pct = np.round(kanan * 100).astype(int)
    X = np.column_stack([tengah ** k for k in range(derajat + 1)] +
                        [(pct % m == 0).astype(float) for m in (5, 10, 25, 50)])
    luar = ~((kanan > jendela[0] + 1e-9) & (kanan <= jendela[1] + 1e-9))
    beta, *_ = np.linalg.lstsq(X[luar], n[luar], rcond=None)
    pred = np.clip(X @ beta, 0, None)
    bawah = (kanan > jendela[0] + 1e-9) & (kanan <= 1 + 1e-9)
    atas = (kanan > 1 + 1e-9) & (kanan <= jendela[1] + 1e-9)
    return dict(kanan=kanan, n=n, pred=pred, aktual_bawah=n[bawah].sum(), pred_bawah=pred[bawah].sum(),
                aktual_atas=n[atas].sum(), pred_atas=pred[atas].sum(),
                tepat_ambang=int((x == T).sum()))


def bunching_ci(x, T, B=300, seed=0):
    """Selang kepercayaan 95% rasio aktual/perkiraan di bawah ambang (bootstrap paket)."""
    rng = np.random.default_rng(seed)
    x = np.asarray(x)
    v = []
    for _ in range(B):
        b = bunching(x[rng.integers(0, len(x), len(x))], T)
        v.append(b['aktual_bawah'] / max(b['pred_bawah'], 1e-9))
    return np.percentile(v, [2.5, 97.5])


hasil_b, simpan_b = [], {}
for nama, jenis, T in [('Barang & Jasa Lainnya (200 jt)', ['Barang', 'Jasa Lainnya'], 200e6),
                       ('Pekerjaan Konstruksi (400 jt, aturan baru)', ['Pekerjaan Konstruksi'], 400e6),
                       ('Pekerjaan Konstruksi (200 jt, aturan lama)', ['Pekerjaan Konstruksi'], 200e6),
                       ('Jasa Konsultansi (100 jt)', ['Jasa Konsultansi'], 100e6)]:
    for lingkup, mask in [('semua metode', np.ones(len(info), bool)), ('pengadaan langsung', is_pl.values)]:
        x = info.pagu[info.jenis.isin(jenis).values & mask].values
        b = bunching(x, T)
        lo_ci, hi_ci = bunching_ci(x, T)
        simpan_b[(nama, lingkup)] = b
        hasil_b.append({'ambang': nama, 'lingkup': lingkup, 'paket_50_150persen': int(b['n'].sum()),
                        'aktual_90_100persen': int(b['aktual_bawah']), 'perkiraan_90_100persen': round(b['pred_bawah'], 1),
                        'rasio_bawah': round(b['aktual_bawah'] / max(b['pred_bawah'], 1e-9), 2),
                        'ci95_bawah': f'{lo_ci:.2f}-{hi_ci:.2f}',
                        'aktual_100_110persen': int(b['aktual_atas']), 'perkiraan_100_110persen': round(b['pred_atas'], 1),
                        'rasio_atas': round(b['aktual_atas'] / max(b['pred_atas'], 1e-9), 2),
                        'tepat_di_ambang': b['tepat_ambang']})
hb = pd.DataFrame(hasil_b)
hb.to_csv(OUT + 'r1_bunching.csv', index=False)
pd.to_pickle(simpan_b, OUT + 'r1_bunching.pkl')
print(hb.to_string(index=False), flush=True)

# Bunching per provinsi (semua jenis, rasio aktual/perkiraan di 90-100% ambang, hanya angka kasar):
# dipakai untuk melihat apakah penumpukan merata atau terpusat.
prov_b = []
for prov, g in info.groupby('provinsi'):
    r = (g.pagu / g.jenis.map(AMBANG))
    dekat = ((r > 0.9) & (r <= 1.0)).sum()
    seb = ((r > 0.8) & (r <= 0.9)).sum()
    ses = ((r > 1.0) & (r <= 1.1)).sum()
    prov_b.append({'provinsi': prov, 'paket': len(g), 'di_80_90persen': seb, 'di_90_100persen': dekat,
                   'di_100_110persen': ses, 'rasio_90_100_vs_80_90': round(dekat / max(seb, 1), 2)})
pd.DataFrame(prov_b).sort_values('rasio_90_100_vs_80_90', ascending=False).to_csv(OUT + 'r1_bunching_provinsi.csv', index=False)

# ---------------------------------------------------------------- 2. Kemunculan bersama
def phi(a, b):
    a, b = a.astype(float), b.astype(float)
    return np.corrcoef(a, b)[0, 1]


rows = []
for jalur, idx, cols in [('perencanaan', info.index, list(rf.columns[:4])), ('pelaksanaan', idx_pel, list(rf.columns))]:
    R = rf.loc[idx, cols]
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            pa, pb, pab = R[a].mean(), R[b].mean(), (R[a] & R[b]).mean()
            rows.append({'jalur': jalur, 'rf_a': a, 'rf_b': b, 'n_a': int(R[a].sum()), 'n_b': int(R[b].sum()),
                         'n_ab': int((R[a] & R[b]).sum()), 'phi': round(phi(R[a], R[b]), 3),
                         'lift': round(pab / (pa * pb), 2) if pa * pb > 0 else np.nan})
pd.DataFrame(rows).to_csv(OUT + 'r1_kemunculan_bersama.csv', index=False)

# Validitas konvergen tingkat satker: korelasi Spearman antar-tingkat red flag (satker >= 30 paket)
rows = []
for jalur, idx, cols, nmin in [('perencanaan', info.index, list(rf.columns[:4]), 30), ('pelaksanaan', idx_pel, list(rf.columns), 20)]:
    R = rf.loc[idx, cols].astype(float)
    g = R.groupby(satker.loc[idx])
    n = g.size()
    rate = g.mean()[n >= nmin]
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            rho, p = spearmanr(rate[a], rate[b])
            rows.append({'jalur': jalur, 'satker': len(rate), 'rf_a': a, 'rf_b': b, 'spearman': round(rho, 3), 'p': p})
kv = pd.DataFrame(rows)
kv.to_csv(OUT + 'r1_konvergen_satker.csv', index=False)
print(kv.round(4).to_string(index=False), flush=True)

# ---------------------------------------------------------------- 3. Variasi definisi & kandidat baru
var = {}
for f in (0.95, 0.98):
    var[f'rf1_dekat_ambang_{int(f * 100)}persen'] = is_pl & (info.pagu >= f * amb) & (info.pagu <= amb)
var['rf1_tepat_di_ambang'] = is_pl & (info.pagu == amb)


def bersih(t):
    t = re.sub(r'[\d\.\-/]+', ' ', str(t).lower())
    return re.sub(r'\s+', ' ', t).strip()


q = info[is_pl & (info.pagu <= amb)].copy()
q['nm'] = q.nama_paket.map(bersih)
q['satker'] = satker.loc[q.index]
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit(q.nm)
for cut in (0.7, 0.9):
    r3 = pd.Series(False, index=info.index)
    for _, grp in q.groupby(['satker', 'jenis']):
        if len(grp) < 2:
            continue
        X = vec.transform(grp.nm)
        S = X @ X.T
        S.data = (S.data >= cut).astype(np.int8)
        S.eliminate_zeros()
        _, lab = connected_components(S, directed=False)
        sz, tot = np.bincount(lab), np.bincount(lab, weights=grp.pagu.values)
        hit = (sz[lab] >= 2) & (tot[lab] > AMBANG[grp.jenis.iat[0]])
        r3.loc[grp.index[hit]] = True
    var[f'rf3_pemecahan_cos{int(cut * 100)}'] = r3

# Penyedia (jalur pelaksanaan)
pp = info.loc[idx_pel, ['jenis', 'pagu', 'realisasi', 'penyedia', 'metode_pengadaan', 'metode_realisasi', 'nama_paket']].copy()
pp['satker'] = satker.loc[idx_pel]
pp = pp[pp.penyedia != '-']
pp['pny'] = pp.penyedia.str.upper().str.replace(r'[^A-Z0-9 ]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()
sat_n, sat_v = pp.groupby('satker').size(), pp.groupby('satker').realisasi.sum()
sp = pp.groupby(['satker', 'pny']).agg(n=('realisasi', 'size'), v=('realisasi', 'sum')).reset_index()
sp['share'] = sp.v / sp.satker.map(sat_v)
sp['n_satker'] = sp.satker.map(sat_n)
key = pp.satker + '||' + pp.pny  # kunci satker||penyedia


def tandai(sel):
    s = pd.Series(False, index=info.index)
    s.loc[pp.index] = key.isin(set(sel.satker + '||' + sel.pny)).values
    return s


var['rf5_porsi40_n5'] = tandai(sp[(sp.share > 0.4) & (sp.n_satker >= 5)])  # OCP R040 (contoh ambang 40%)
var['rf5_porsi50_n5'] = tandai(sp[(sp.share > 0.5) & (sp.n_satker >= 5)])
var['rf5_jumlah_p95'] = tandai(sp[sp.n > sp.n.quantile(0.95)])
nj = pp.groupby('pny').jenis.nunique()
npk = pp.groupby('pny').size()
s6 = pd.Series(False, index=info.index)
s6.loc[pp.index] = ((pp.pny.map(nj) >= 3) & (pp.pny.map(npk) >= 5)).values
var['rf6_serba_ada_min5paket'] = s6

# Kandidat baru (OCP): R055 beberapa PL dari satker yang sama ke penyedia yang sama, jumlahnya melewati ambang
ppl = pp[pp.metode_pengadaan == 'Pengadaan Langsung']
g = ppl.groupby(['satker', 'pny', 'jenis'])
agg = g.agg(n=('pagu', 'size'), tot=('realisasi', 'sum')).reset_index()
agg['T'] = agg.jenis.map(AMBANG)
hit = agg[(agg.n >= 2) & (agg.tot > agg['T'])]
k55 = ppl.satker + '||' + ppl.pny + '||' + ppl.jenis
s = pd.Series(False, index=info.index)
s.loc[ppl.index] = k55.isin(set(hit.satker + '||' + hit.pny + '||' + hit.jenis)).values
var['baru_R055_pl_berulang_lewat_ambang'] = s
# R049: penyedia menerima > 1 PL dari satker yang sama, masing-masing di 90-100% ambang
dekat = ppl[(ppl.pagu >= 0.9 * ppl.jenis.map(AMBANG)) & (ppl.pagu <= ppl.jenis.map(AMBANG))]
c = dekat.groupby(['satker', 'pny']).size()
c = c[c >= 2].reset_index()
s = pd.Series(False, index=info.index)
s.loc[dekat.index] = (dekat.satker + '||' + dekat.pny).isin(set(c.satker + '||' + c.pny)).values
var['baru_R049_pl_dekat_ambang_berulang'] = s
# R012 (mirip): direncanakan tender/seleksi/e-purchasing tetapi direalisasikan lewat penunjukan/pengadaan langsung
inf = info.loc[idx_pel]
s = pd.Series(False, index=info.index)
s.loc[idx_pel] = (inf.metode_pengadaan.isin(['Tender', 'Seleksi', 'Tender Cepat', 'E-Purchasing'])
                  & inf.metode_realisasi.isin(['Penunjukan Langsung', 'Pengadaan Langsung'])).values
var['baru_R012_ubah_ke_langsung'] = s
# opentender ICW: judul paket sangat pendek (< 20 karakter)
var['baru_judul_pendek_20'] = info.nama_paket.astype(str).str.strip().str.len() < 20
# R068: realisasi melebihi pagu (hanya informasi; bentrok dengan fitur rasio realisasi)
s = pd.Series(False, index=info.index)
s.loc[idx_pel] = (inf.realisasi > inf.pagu * 1.0001).values
var['baru_R068_realisasi_lewat_pagu'] = s

V = pd.DataFrame(var)
asli = {'rf1': 'rf1_pl_dekat_ambang', 'rf3': 'rf3_pemecahan_paket', 'rf5': 'rf5_penyedia_dominan', 'rf6': 'rf6_penyedia_serba_ada'}
rows = []
for c in V:
    for jalur, idx in [('perencanaan', info.index), ('pelaksanaan', idx_pel)]:
        a = V.loc[idx, c]
        if a.sum() == 0:
            continue
        o = asli.get(c[:3])
        jac = np.nan
        if o:
            b = rf.loc[idx, o]
            jac = (a & b).sum() / max((a | b).sum(), 1)
        rows.append({'red_flag': c, 'jalur': jalur, 'jumlah': int(a.sum()), 'persen': round(100 * a.mean(), 2),
                     'jaccard_dg_asli': round(jac, 3) if o else ''})
pd.DataFrame(rows).to_csv(OUT + 'r1_variasi_red_flag.csv', index=False)
V.to_pickle(OUT + 'r1_variasi_red_flag.pkl')
print(pd.DataFrame(rows).to_string(index=False))
