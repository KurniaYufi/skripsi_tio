"""Tahap 10: bukti tiap red flag per paket, untuk ditampilkan di dashboard (permintaan Tio 2026-10-29).

Untuk setiap paket yang punya red flag, disusun:
- ringkas : satu kalimat kenapa red flag itu terpenuhi, dengan angka paketnya;
- anggota : daftar paket terkait (RF3: paket bernama mirip di kelompoknya; RF5: paket penyedia itu di satker);
- cek     : hal yang perlu dicek penelaah.
Aturan dan ambang sama persis dengan red_flag_v3.pkl (model-v1/s1_data.py dan validasi-v3/r6_pilih_v3.py).
Keluaran: bukti_redflag.pkl = {kode_rup: [ {rf, ringkas, rincian, anggota, cek}, ... ]}
"""
import re
import numpy as np
import pandas as pd
from scipy.sparse.csgraph import connected_components
from sklearn.feature_extraction.text import TfidfVectorizer

OUT = '/mnt/project-files/model-v4/'
d = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')
info = d['info']
RF = pd.read_pickle('/mnt/project-files/validasi-v3/red_flag_v3.pkl')
idx_pel = d['f_pel'].index
satker = info.provinsi + '|' + info.nama_satuan_kerja
AMBANG = {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 400e6, 'Jasa Konsultansi': 100e6}
amb = info.jenis.map(AMBANG)
is_pl = info.metode_pengadaan == 'Pengadaan Langsung'
MAKS_ANGGOTA = 15


def rp(x):
    x = float(x)
    for b, s in [(1e12, ' T'), (1e9, ' M'), (1e6, ' jt'), (1e3, ' rb')]:
        if abs(x) >= b:
            return 'Rp' + f'{x / b:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.').removesuffix(',0') + s
    return f'Rp{x:,.0f}'


def pct(x):
    return f'{100 * x:.0f}%' if x >= 0.1 else f'{100 * x:.1f}%'.replace('.', ',')


def kali(x):
    return f'{x:.1f}'.replace('.', ',') if x < 10 else f'{x:,.0f}'.replace(',', '.')


bukti = {}


def tambah(kode, **isi):
    bukti.setdefault(kode, []).append(isi)


# ---- RF1 dan RF2: pengadaan langsung dan ambang
for kode in RF.index[RF.rf1_pl_dekat_ambang]:
    i = info.loc[kode]
    A = AMBANG[i.jenis]
    if i.jenis == 'Pekerjaan Konstruksi' and i.pagu <= 200e6:
        A, catatan = 200e6, ' (ambang lama sebelum Perpres 46/2025, yang masih banyak dipakai di 2025)'
    else:
        catatan = ''
    tambah(kode, rf='rf1_pl_dekat_ambang',
           ringkas=f'Pagu {rp(i.pagu)} = {pct(i.pagu / A)} dari batas pengadaan langsung {i.jenis.lower()} {rp(A)}{catatan}. '
                   + (f'Selisihnya hanya {rp(A - i.pagu)}.' if A > i.pagu else 'Pagu tepat sama dengan batas.'),
           cek='Apakah nilai paket memang dihitung dari kebutuhan, atau dibuat sedikit di bawah batas agar cukup pengadaan langsung, tanpa tender?')
for kode in RF.index[RF.rf2_pl_lewat_ambang]:
    i = info.loc[kode]
    A = AMBANG[i.jenis]
    tambah(kode, rf='rf2_pl_lewat_ambang',
           ringkas=f'Metodenya pengadaan langsung, tetapi pagu {rp(i.pagu)} = {kali(i.pagu / A)} kali batas pengadaan langsung '
                   f'{i.jenis.lower()} ({rp(A)}).',
           cek='Apakah ada dasar pengecualian yang sah, atau metode di RUP salah isi? Paket sebesar ini biasanya harus lewat tender atau seleksi.')

# ---- RF3: kelompok paket bernama mirip (aturan sama dengan s1_data.py)


def bersih(t):
    t = re.sub(r'[\d\.\-/]+', ' ', str(t).lower())
    return re.sub(r'\s+', ' ', t).strip()


q = info[is_pl & (info.pagu <= amb)].copy()
q['nm'] = q.nama_paket.map(bersih)
q['satker'] = satker.loc[q.index]
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit(q.nm)
rf3 = pd.Series(False, index=info.index)
for _, grp in q.groupby(['satker', 'jenis']):
    if len(grp) < 2:
        continue
    X = vec.transform(grp.nm)
    S = X @ X.T
    S.data = (S.data >= 0.8).astype(np.int8)
    S.eliminate_zeros()
    _, lab = connected_components(S, directed=False)
    sz, tot = np.bincount(lab), np.bincount(lab, weights=grp.pagu.values)
    A = AMBANG[grp.jenis.iat[0]]
    for k in np.unique(lab[(sz[lab] >= 2) & (tot[lab] > A)]):
        g = grp[lab == k].sort_values('pagu', ascending=False)
        rf3.loc[g.index] = True
        anggota = [[kd, r.nama_paket, float(r.pagu)] for kd, r in g.head(MAKS_ANGGOTA).iterrows()]
        for kd in g.index:
            tambah(kd, rf='rf3_pemecahan_paket',
                   ringkas=f'Ada {len(g)} paket pengadaan langsung {g.jenis.iat[0].lower()} bernama mirip di satker yang sama. '
                           f'Masing-masing di bawah batas {rp(A)}, tetapi jumlahnya {rp(g.pagu.sum())} = {kali(g.pagu.sum() / A)} kali batas.',
                   rincian=(f'Ditampilkan {MAKS_ANGGOTA} paket dengan pagu terbesar.' if len(g) > MAKS_ANGGOTA else ''),
                   anggota=anggota, total=float(g.pagu.sum()), n=int(len(g)),
                   cek='Apakah paket-paket ini sebenarnya satu kegiatan yang bisa digabung dan ditender? Bila memang beda lokasi '
                       'atau waktu (misalnya belanja rutin bulanan), red flag ini bisa diabaikan.')
beda = (rf3 != RF.rf3_pemecahan_paket).sum()
print('RF3 dihitung ulang, beda dengan red_flag_v3:', beda, flush=True)

# ---- RF4: penunjukan langsung
for kode in RF.index[RF.rf4_penunjukan_langsung]:
    tambah(kode, rf='rf4_penunjukan_langsung',
           ringkas='Penyedia ditunjuk langsung tanpa persaingan. Metode ini hanya boleh untuk keadaan tertentu, '
                   'misalnya keadaan darurat atau pekerjaan yang hanya bisa dikerjakan satu penyedia.',
           cek='Apakah alasan penunjukan langsung tercatat dan sesuai keadaan yang dibolehkan aturan?')

# ---- RF5 dan RF6: penyedia (jalur pelaksanaan, aturan sama dengan validasi-v3/r1_redflag.py)
pp = info.loc[idx_pel, ['jenis', 'pagu', 'realisasi', 'penyedia', 'nama_paket']].copy()
pp['satker'] = satker.loc[idx_pel]
pp = pp[pp.penyedia != '-']
pp['pny'] = pp.penyedia.str.upper().str.replace(r'[^A-Z0-9 ]', '', regex=True).str.replace(r'\s+', ' ', regex=True).str.strip()
sat_n, sat_v = pp.groupby('satker').size(), pp.groupby('satker').realisasi.sum()
for (s, pny), g in pp.groupby(['satker', 'pny']):
    share = g.realisasi.sum() / sat_v[s]
    if not (share > 0.4 and sat_n[s] >= 5):
        continue
    g = g.sort_values('realisasi', ascending=False)
    anggota = [[kd, r.nama_paket, float(r.realisasi)] for kd, r in g.head(MAKS_ANGGOTA).iterrows()]
    for kd in g.index:
        tambah(kd, rf='rf5_penyedia_dominan',
               ringkas=f'Penyedia {g.penyedia.iat[0]} menerima {rp(g.realisasi.sum())} dari total realisasi satker {rp(sat_v[s])} '
                       f'({pct(share)}), lewat {len(g)} dari {sat_n[s]} paket satker ini. Batas red flag: lebih dari 40%.',
               rincian=(f'Ditampilkan {MAKS_ANGGOTA} paket dengan realisasi terbesar.' if len(g) > MAKS_ANGGOTA else ''),
               anggota=anggota, total=float(g.realisasi.sum()), n=int(len(g)), nilai='realisasi',
               cek='Apakah penyedia ini menang lewat persaingan yang sehat? Adakah penyedia lain yang sebenarnya mampu mengerjakan?')
nj = pp.groupby('pny').jenis.agg(lambda s: s.value_counts().to_dict())
for kd, r in pp.iterrows():
    jj = nj[r.pny]
    if len(jj) >= 3:
        rinci = ', '.join(f'{j.lower()} ({n} paket)' for j, n in jj.items())
        tambah(kd, rf='rf6_penyedia_serba_ada',
               ringkas=f'Penyedia {r.penyedia} memenangkan paket di {len(jj)} jenis pengadaan berbeda di seluruh provinsi: {rinci}.',
               cek='Apakah penyedia ini punya izin usaha dan pengalaman untuk semua jenis pekerjaan itu, atau hanya "meminjamkan nama"?')

# Pastikan setiap red flag di red_flag_v3 punya bukti
for c in RF.columns:
    punya = {k for k, v in bukti.items() if any(b['rf'] == c for b in v)}
    kurang = set(RF.index[RF[c]]) - punya
    print(c, 'tanpa bukti:', len(kurang), flush=True)
pd.to_pickle(bukti, OUT + 'bukti_redflag.pkl')
print('paket dengan bukti', len(bukti))
