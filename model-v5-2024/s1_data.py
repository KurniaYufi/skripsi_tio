# SALINAN model-v5 untuk uji tahun lain (data 2024, permintaan Tio 2026-10-30). Beda: file data 2024, OUT model-v5-2024, ambang PL konstruksi Rp200 jt.
"""Tahap 1 model v5 (2026-10-29): penyiapan data dengan pembersihan yang lebih ketat, fitur per jalur, dan red flag.

Permintaan Tio: "cari keanehan lainnya, dan lakukan preprocessing yang lebih oke". Hasil audit dan alasan tiap aturan:
/mnt/project-files/model-v5/audit-data.md. Fitur dan definisi red flag sama dengan v4 (model-v1/s1_data.py,
validasi-v3/r6_pilih_v3.py, model-v4/s10_bukti_redflag.py); yang berubah hanya data yang masuk.

Aturan baru (B = realisasi, C = penyedia):
B1 baris realisasi bernilai <= 0 dibuang.
B2 baris realisasi yang provinsinya berbeda dengan provinsi RUP-nya dibuang (kode RUP diduga salah ketik).
B3 catatan ganda: dalam satu kode RUP, baris dengan nilai sama persis dihitung sekali, HANYA bila jumlah semua baris
   melebihi pagu (> 101%) dan setelah digabung tidak lagi melebihi pagu. Pesanan berulang di bawah pagu tetap.
B4 nilai PDN/UMK 1-100 rupiah dibaca sebagai persen (contoh: UMK "100" pada paket Rp324 jt).
B5 paket dengan rasio realisasi/pagu < 0,01 atau > 9,5 tidak masuk jalur pelaksanaan (diduga salah satuan/ketik).
   Batas atas semula 10; audit 2026-10-29 malam menemukan 5 paket satu baris di 9,8-9,9 kali pagu (dan tidak ada
   paket satu baris di 8-9,5 kali): pola kelebihan satu angka nol, yang sempat masuk 200 teratas pelaksanaan.
B6 (audit 2026-10-29 malam) paket Tender yang satu kode paketnya punya > 1 penyedia berbeda tidak masuk jalur
   pelaksanaan. Satu tender hanya punya satu pemenang; baris-baris ini (20 kode paket, mis. 3 penyedia masing-masing
   Rp2,8-3,2 M untuk pagu Rp3,6 M) lebih mirip data peserta/tender ulang, sehingga dijumlah menjadi 1,7-2,6 kali pagu.
   Delapan paket seperti ini sempat menempati peringkat 13-80 jalur pelaksanaan.
C1 nama penyedia dirapikan: daftar berulang "A, A" jadi "A"; bentuk usaha (PT, CV, UD, Tbk, ...) diabaikan saat
   mencocokkan penyedia untuk RF5/RF6.
C3 (koreksi) jenis "Terintegrasi" dan metode "Tender Cepat", "Kontes", "Sayembara",
   "Pembayaran untuk Kontrak Tahun Jamak" tidak lagi digabung ke kategori lain.
C2 penyedia yang namanya unit pemerintah (kelurahan, dinas, biro, bendahara, ...) dianggap tidak diketahui ("-")
   untuk RF5/RF6, karena itu pencatatan oleh satker sendiri, bukan penyedia.
"""
import json
import re
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components
from sklearn.feature_extraction.text import TfidfVectorizer

D = '/mnt/project-files/'
OUT = D + 'model-v5-2024/'
LOG = {}

rup = pd.read_csv(D + 'rup_2024.csv', low_memory=False, dtype={'kode_rup': str})
rea = pd.read_csv(D + 'realisasi_2024.csv', low_memory=False, dtype={'kode_rup': str})

# ---- Lingkup RUP (sama dengan v1): penyedia, tanpa Dikecualikan, pagu > Rp10.000
p = rup[(rup.cara_pengadaan == 'Penyedia') & (rup.metode_pengadaan != 'Dikecualikan')
        & (rup.jenis_pengadaan != '-') & (rup.metode_pengadaan != '-')].copy()
LOG['A1 paket penyedia (lingkup)'] = len(p)
p = p[p.total_nilai > 10000].copy()
LOG['A2 pagu > Rp10 rb'] = len(p)
p['provinsi'] = p.nama_instansi.str.replace('PROVINSI ', '', regex=False).str.title()
p['satker'] = p.nama_instansi + ' | ' + p.nama_satuan_kerja
p['pagu'] = p.total_nilai.astype(float)
# Kategori jenis dan metode TIDAK digabung (koreksi Tio 2026-10-29): Tender Cepat adalah metode tersendiri
# (Perpres 46/2025 Pasal 38 ayat 1), dan paket Terintegrasi di data kebanyakan E-Purchasing/PL kecil, bukan konstruksi.
# Terintegrasi tidak punya ambang PL di Perpres, jadi tidak ikut RF1-RF3 (ambang NaN -> tidak pernah terpenuhi).
p['jenis'] = p.jenis_pengadaan
p['metode'] = p.metode_pengadaan
p = p.set_index('kode_rup')

# ---- Fitur jalur perencanaan (sama dengan v1)
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

# ---- Realisasi
r = rea.dropna(subset=['kode_rup'])
r = r[r.kode_rup.isin(p.index) & (r.sumber_transaksi != 'Pencatatan Swakelola')].copy()
LOG['B0 baris realisasi di lingkup'] = len(r)
r = r[r.total_nilai > 0]
LOG['B1 baris bernilai > 0'] = len(r)
r = r[r.nama_instansi.values == p.nama_instansi.reindex(r.kode_rup).values]
LOG['B2 baris dengan provinsi sama dengan RUP'] = len(r)

g = r.groupby('kode_rup')
selesai = g.tahapan_pengadaan.agg(lambda s: (s == 'Serah Terima').all())
r = r[r.kode_rup.isin(selesai[selesai].index)].copy()
LOG['B serah terima: paket'] = r.kode_rup.nunique()
LOG['B serah terima: baris'] = len(r)

# B3 catatan ganda
pagu_r = p.pagu.reindex(r.kode_rup).values
jumlah = r.groupby('kode_rup').total_nilai.transform('sum').values
kembar = r.duplicated(['kode_rup', 'total_nilai'], keep='first').values
punya_kembar = r.duplicated(['kode_rup', 'total_nilai'], keep=False).values
jumlah_tanpa = r[~kembar].groupby('kode_rup').total_nilai.sum().reindex(r.kode_rup).values
ganda = (jumlah > 1.01 * pagu_r) & (jumlah_tanpa <= 1.01 * pagu_r) & punya_kembar
paket_ganda = set(r.kode_rup[ganda])
buang = ganda & kembar
LOG['B3 paket dengan catatan ganda'] = len(paket_ganda)
LOG['B3 baris ganda dibuang'] = int(buang.sum())
r = r[~buang].copy()

# B4 PDN/UMK yang tertulis sebagai persen
for c in ['nilai_pdn', 'nilai_umk']:
    persen = (r[c] > 0) & (r[c] <= 100) & (r.total_nilai > 10000)
    LOG[f'B4 {c} dibaca sebagai persen (baris)'] = int(persen.sum())
    r.loc[persen, c] = r.total_nilai[persen] * r[c][persen] / 100
    r[c] = np.minimum(r[c], r.total_nilai)

# C1-C2 penyedia
BENTUK = r'\b(PT|CV|UD|TB|TK|PD|FA|FIRMA|PERSERO|TBK|KOPERASI|KPRI|PO)\b'
PEMERINTAH = (r'\b(KELURAHAN|KECAMATAN|DINAS|BADAN|PUSKESMAS|RSUD|SEKRETARIAT|BENDAHARA|UPTD|UPT|SATPOL|'
              r'INSPEKTORAT|BIRO|SMAN|SMKN|SLBN|SMA NEGERI|SMK NEGERI|PEMERINTAH|PEMPROV|SETDA)\b')
USAHA = r'\b(PT|CV|UD|KOPERASI|KPRI|TOKO|TB|PO|FIRMA|PERSERO)\b'


def rapikan(nama):
    """Nama tampilan: daftar berulang 'A, A' menjadi 'A'."""
    nama = str(nama).strip()
    if nama in ('-', '', 'nan'):
        return '-'
    bagian = [b.strip() for b in re.split(r',(?!\s*TBK\b)', nama, flags=re.I) if b.strip()]
    unik = list(dict.fromkeys(bagian))
    return unik[0] if len(set(kunci_dasar(b) for b in unik)) == 1 else ', '.join(unik)


def kunci_dasar(nama):
    s = re.sub(r'[^A-Z0-9 ]', ' ', str(nama).upper())
    s = re.sub(BENTUK, ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


r['penyedia'] = r.nama_penyedia.map(rapikan)
up = r.penyedia.str.upper()
pemerintah = up.str.contains(PEMERINTAH) & ~up.str.contains(USAHA)
LOG['C1 nama penyedia berulang dirapikan (baris)'] = int((r.penyedia != r.nama_penyedia.astype(str).str.strip()).sum())
LOG['C2 penyedia unit pemerintah -> "-" (baris)'] = int(pemerintah.sum())
r['penyedia_tampil'] = r.penyedia
r.loc[pemerintah, 'penyedia'] = '-'


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
    'penyedia': g.penyedia.agg(modus),
    'penyedia_tampil': g.penyedia_tampil.agg(modus),
})
a = a[a.realisasi > 0]
tender = r[r.sumber_transaksi == 'Tender'].assign(k=lambda x: x.penyedia_tampil.map(kunci_dasar)).groupby('kode_paket').agg(
    n=('k', 'nunique'), rup=('kode_rup', 'first'))
multi = set(tender.rup[tender.n > 1])
LOG['B6 paket Tender dengan > 1 penyedia (tidak dinilai)'] = int(a.index.isin(multi).sum())
a = a[~a.index.isin(multi)]
rasio = a.realisasi / p.pagu.loc[a.index]
LOG['B5 paket rasio < 0,01'] = int((rasio < 0.01).sum())
LOG['B5 paket rasio > 9,5'] = int((rasio > 9.5).sum())
a = a[(rasio >= 0.01) & (rasio <= 9.5)]
LOG['Paket jalur pelaksanaan (sebelum batas pagu model)'] = len(a)

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

# ---- Red flag (definisi v3)
AMBANG = {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 200e6, 'Jasa Konsultansi': 100e6}  # 2024: Perpres 12/2021 (ambang PL konstruksi Rp200 jt)
amb = p.jenis.map(AMBANG)
is_pl = p.metode == 'Pengadaan Langsung'
rf = pd.DataFrame(index=p.index)
rf['rf1_pl_dekat_ambang'] = (is_pl & (p.pagu >= 0.9 * amb) & (p.pagu <= amb)) | (
    is_pl & (p.jenis == 'Pekerjaan Konstruksi') & (p.pagu >= 180e6) & (p.pagu <= 200e6))
rf['rf2_pl_lewat_ambang'] = is_pl & (p.pagu > amb)


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
    S = X @ X.T
    S.data = (S.data >= 0.8).astype(np.int8)
    S.eliminate_zeros()
    _, lab = connected_components(S, directed=False)
    sz, tot = np.bincount(lab), np.bincount(lab, weights=grp.pagu.values)
    hit = (sz[lab] >= 2) & (tot[lab] > AMBANG[grp.jenis.iat[0]])
    rf3.loc[grp.index[hit]] = True
rf['rf3_pemecahan_paket'] = rf3
rf['rf4_penunjukan_langsung'] = p.metode == 'Penunjukan Langsung'

# RF5 (OCP R040) dan RF6 (OCP R048): kunci penyedia tanpa bentuk usaha
pp = pl[['satker', 'jenis']].join(a[['penyedia', 'realisasi']])
pp = pp[pp.penyedia != '-']
pp['pny'] = pp.penyedia.map(kunci_dasar)
pp = pp[pp.pny != '']
sat_n, sat_v = pp.groupby('satker').size(), pp.groupby('satker').realisasi.sum()
sp = pp.groupby(['satker', 'pny']).realisasi.sum().reset_index()
sp['share'] = sp.realisasi / sp.satker.map(sat_v)
dom = sp[(sp.share > 0.4) & (sp.satker.map(sat_n) >= 5)]
rf['rf5_penyedia_dominan'] = False
rf.loc[pp.index, 'rf5_penyedia_dominan'] = (pp.satker + '||' + pp.pny).isin(set(dom.satker + '||' + dom.pny)).values
rf['rf6_penyedia_serba_ada'] = False
rf.loc[pp.index, 'rf6_penyedia_serba_ada'] = (pp.pny.map(pp.groupby('pny').jenis.nunique()) >= 3).values
LOG['red flag (seluruh lingkup)'] = rf.sum().astype(int).to_dict()
LOG['red flag RF5/RF6 di jalur pelaksanaan'] = rf.loc[f_pel.index, ['rf5_penyedia_dominan', 'rf6_penyedia_serba_ada']].sum().astype(int).to_dict()

info = p[['provinsi', 'nama_satuan_kerja', 'nama_paket', 'metode_pengadaan', 'jenis', 'pagu',
          'produk_dalam_negeri', 'status_umk']].join(a[['realisasi', 'sumber_transaksi', 'metode_realisasi', 'penyedia',
                                                         'penyedia_tampil']])
info['penyedia'] = info.penyedia.fillna('-')
pd.to_pickle(dict(f_ren=f_ren, f_pel=f_pel, rf=rf, info=info, paket_ganda=sorted(paket_ganda)), OUT + 'tahap1.pkl')
rf.to_pickle(OUT + 'red_flag_v5.pkl')
json.dump(LOG, open(OUT + 'log_pembersihan.json', 'w'), indent=1, ensure_ascii=False, default=int)
for k, v in LOG.items():
    print(k, ':', v)
