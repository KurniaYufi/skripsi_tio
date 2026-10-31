"""Tahap 1: penyiapan data, fitur per jalur, dan 6 red flag (hanya untuk evaluasi)."""
import re
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components
from sklearn.feature_extraction.text import TfidfVectorizer

D = '/mnt/project-files/'
OUT = D + 'model-v1/'

rup = pd.read_csv(D + 'data_rup_2025.csv', low_memory=False, dtype={'kode_rup': str})
rea = pd.read_csv(D + 'dara_realisasi_2025.csv', low_memory=False, dtype={'kode_rup': str})

# ---- Lingkup: penyedia, tanpa Dikecualikan, pagu > Rp10.000
p = rup[(rup.cara_pengadaan == 'Penyedia') & (rup.metode_pengadaan != 'Dikecualikan')
        & (rup.jenis_pengadaan != '-') & (rup.metode_pengadaan != '-')].copy()
n_awal = len(p)
p = p[p.total_nilai > 10000].copy()
print('paket penyedia', n_awal, '-> pagu > 10rb', len(p))
p['provinsi'] = p.nama_instansi.str.replace('PROVINSI ', '', regex=False).str.title()
p['satker'] = p.nama_instansi + ' | ' + p.nama_satuan_kerja
p['pagu'] = p.total_nilai.astype(float)
p['jenis'] = p.jenis_pengadaan.replace({'Terintegrasi': 'Pekerjaan Konstruksi'})
p['metode'] = p.metode_pengadaan.replace({
    'Tender Cepat': 'Tender', 'Kontes': 'Lainnya', 'Sayembara': 'Lainnya',
    'Pembayaran untuk Kontrak Tahun Jamak': 'Lainnya'})
p = p.set_index('kode_rup')

# ---- Fitur jalur perencanaan
f = pd.DataFrame(index=p.index)
f['log_pagu'] = np.log10(p.pagu)
med = p.groupby(['jenis', 'metode']).pagu.transform('median')
f['log_rasio_pagu_sejenis'] = np.log10(p.pagu / med)
f['porsi_pagu_satker'] = p.pagu / p.groupby('satker').pagu.transform('sum')
f['log_jumlah_paket_satker'] = np.log10(p.groupby('satker').pagu.transform('size'))
f['proporsi_pl_satker'] = (p.metode == 'Pengadaan Langsung').groupby(p.satker).transform('mean')
f['pdn'] = (p.produk_dalam_negeri == 'Ya').astype(float)
f['umk'] = (p.status_umk == 'Ya').astype(float)
f = f.join(pd.get_dummies(p.metode, prefix='metode', dtype=float))
f = f.join(pd.get_dummies(p.jenis, prefix='jenis', dtype=float))
f_ren = f

# ---- Realisasi: hanya baris dengan satu kode_rup yang ada di lingkup, bukan swakelola
r = rea.dropna(subset=['kode_rup'])
r = r[r.kode_rup.isin(p.index) & (r.sumber_transaksi != 'Pencatatan Swakelola')].copy()
g = r.groupby('kode_rup')
selesai = g.tahapan_pengadaan.agg(lambda s: (s == 'Serah Terima').all())
r = r[r.kode_rup.isin(selesai[selesai].index)]
print('pasangan realisasi', g.ngroups, '-> serah terima', r.kode_rup.nunique())


def modus(s):
    s = s[s != '-']
    return s.mode().iat[0] if len(s) else '-'


g = r.groupby('kode_rup')
a = pd.DataFrame({
    'realisasi': g.total_nilai.sum(),
    'nilai_pdn': g.nilai_pdn.sum(),
    'nilai_umk': g.nilai_umk.sum(),
    'sumber_transaksi': g.sumber_transaksi.agg(lambda s: s.mode().iat[0]),
    'metode_realisasi': g.metode_pengadaan.agg(modus),
    'penyedia': g.nama_penyedia.agg(modus),
})
a = a[a.realisasi > 0]
pl = p.loc[a.index]
fp = f_ren.loc[a.index].copy()
fp['rasio_realisasi'] = (a.realisasi / pl.pagu).clip(upper=5)
fp['log_selisih_realisasi'] = np.log10(1 + (a.realisasi - pl.pagu).abs())
fp['ubah_metode'] = ((a.metode_realisasi != '-') & (a.metode_realisasi != pl.metode_pengadaan)).astype(float)
fp['porsi_pdn'] = (a.nilai_pdn / a.realisasi).clip(0, 1)
fp['porsi_umk'] = (a.nilai_umk / a.realisasi).clip(0, 1)
src = a.sumber_transaksi.replace({'E-Katalog Versi 5.0': 'E-Katalog', 'E-Katalog Versi 6.0': 'E-Katalog',
                                  'Pencatatan Non Tender': 'Non Tender'})
fp = fp.join(pd.get_dummies(src, prefix='sumber', dtype=float))
f_pel = fp
print('fitur perencanaan', f_ren.shape, 'pelaksanaan', f_pel.shape)

# ---- Red flag
AMBANG = {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 400e6, 'Jasa Konsultansi': 100e6}
amb = p.jenis.map(AMBANG)
is_pl = p.metode == 'Pengadaan Langsung'
rf = pd.DataFrame(index=p.index)
rf['rf1_pl_dekat_ambang'] = is_pl & (p.pagu >= 0.9 * amb) & (p.pagu <= amb)
rf['rf2_pl_lewat_ambang'] = is_pl & (p.pagu > amb)

# Pemecahan paket: PL di satker & jenis yang sama, nama mirip (TF-IDF cosine >= 0,8),
# jumlah pagu kelompok melebihi ambang padahal tiap paket di bawah ambang.
def bersih(t):
    t = re.sub(r'[\d\.\-/]+', ' ', str(t).lower())
    return re.sub(r'\s+', ' ', t).strip()

q = p[is_pl & (p.pagu <= amb)].copy()
q['nm'] = q.nama_paket.map(bersih)
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit(q.nm)
rf3 = pd.Series(False, index=p.index)
for _, grp in q.groupby(['satker', 'jenis']):
    if len(grp) < 2:
        continue
    X = vec.transform(grp.nm)
    S = (X @ X.T)
    S.data = (S.data >= 0.8).astype(np.int8)
    S.eliminate_zeros()
    nk, lab = connected_components(S, directed=False)
    sz = np.bincount(lab)
    tot = np.bincount(lab, weights=grp.pagu.values)
    batas = AMBANG[grp.jenis.iat[0]]
    hit = (sz[lab] >= 2) & (tot[lab] > batas)
    rf3.loc[grp.index[hit]] = True
rf['rf3_pemecahan_paket'] = rf3
rf['rf4_penunjukan_langsung'] = p.metode == 'Penunjukan Langsung'

# Red flag 5-6 butuh nama penyedia (hanya jalur pelaksanaan)
pp = pl[['satker', 'jenis']].join(a[['penyedia', 'realisasi']])
pp = pp[pp.penyedia != '-']
pp['pny'] = pp.penyedia.str.upper().str.replace(r'[^A-Z0-9 ]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()
sat_n = pp.groupby('satker').size()
sat_v = pp.groupby('satker').realisasi.sum()
sp = pp.groupby(['satker', 'pny']).agg(n=('realisasi', 'size'), v=('realisasi', 'sum')).reset_index()
sp['share'] = sp.v / sp.satker.map(sat_v)
sp['n_satker'] = sp.satker.map(sat_n)
p95 = sp.n.quantile(0.95)
dom = sp[((sp.share > 0.5) & (sp.n_satker >= 5)) | (sp.n > p95)]
key = pp.satker + '||' + pp.pny
rf5 = key.isin(set(dom.satker + '||' + dom.pny))
nj = pp.groupby('pny').jenis.nunique()
rf6 = pp.pny.map(nj) >= 3
rf['rf5_penyedia_dominan'] = False
rf['rf6_penyedia_serba_ada'] = False
rf.loc[pp.index, 'rf5_penyedia_dominan'] = rf5.values
rf.loc[pp.index, 'rf6_penyedia_serba_ada'] = rf6.values
print('p95 paket penyedia per satker', p95)
print(rf.sum())
print('rf5/6 di jalur pelaksanaan', rf.loc[f_pel.index, ['rf5_penyedia_dominan', 'rf6_penyedia_serba_ada']].sum().to_dict())

info = p[['provinsi', 'nama_satuan_kerja', 'nama_paket', 'metode_pengadaan', 'jenis', 'pagu',
          'produk_dalam_negeri', 'status_umk']].join(a[['realisasi', 'sumber_transaksi', 'metode_realisasi', 'penyedia']])
pd.to_pickle(dict(f_ren=f_ren, f_pel=f_pel, rf=rf, info=info), OUT + 'tahap1.pkl')
