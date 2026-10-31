"""Varian kecil saat audit fitur 2026-10-29 malam. Dasar: s2_model.fitur (KOLOM terbaru).
  std   : penskalaan standar (bukan quantile). Pada quantile, paket tepat di batas Rp1 jt (nilai minimum, banyak kembar)
          dipetakan ke ekor paling ekstrem sehingga ~21 paket Rp1 jt masuk 200 teratas perencanaan.
  rata  : rasio pagu satker memakai RATA-RATA satker (bukan median).
  sj    : rasio pagu satker memakai median paket satker dengan JENIS yang sama (kelompok < 4 paket -> 0). Satker yang
          punya ratusan paket super kecil (mis. makan-minum Rp50-300 rb) membuat median satker sangat rendah, sehingga
          semua paket normalnya terlihat 1.000 kali median (42 paket satu satker di 200 teratas).
  tk    : tanpa kekurangan_pdn/kekurangan_umk. Nilai PDN/UMK 0 di realisasi menumpuk di "Pencatatan Non Tender"
          (18,5% / 42,9% paket, Tender 0% / 10,6%), jadi lebih mencerminkan cara pencatatan daripada janji yang tidak ditepati.
  np    : tanpa log_pagu (besar pagu mutlak). Dengan fitur yang semuanya soal pagu, log_pagu membuat puncak hanya berisi
          paket terbesar (kontrak tahun jamak Rp200 M dengan rasio sejenis 1 kali), padahal ukuran besar sendiri bukan
          keanehan; yang dicari adalah pagu yang jauh lebih besar dari pembandingnya.
  nm    : tambah pagu dibanding median paket LAIN bernama sama di satker yang sama (minimal 2 paket lain), satu arah
          (usulan Tio, pola paket A-B-C; eksperimen-nama-satker/).
  ns    : fitur nama hanya untuk nama yang SPESIFIK, yaitu dipakai paling banyak 50 satker se-nasional. Nama seperti
          "Belanja Alat/Bahan untuk Kegiatan Kantor-..." dipakai >1.000 satker: itu nama rekening belanja, bukan nama
          barang, sehingga paket bernama sama isinya beda-beda (mis. ATK Rp6 jt dibanding belanja daring Rp35 rb).
  ss    : fitur nama diskalakan dengan simpangan baku fitur pagu dibanding paket sejenis. Fitur nama 96-97% bernilai 0,
          simpangan bakunya 0,08-0,10, sehingga paket 1,5 kali paket bernama sama sudah tampak 2 simpangan baku.
  tn    : tanpa fitur nama (untuk melihat apakah fitur realisasi tertutup fitur nama di jalur pelaksanaan).
Varian digabung dengan '+', mis. std+sj. Pemakaian: python3 x8_audit_varian.py <jalur> <varian>
"""
import copy
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
from ens3 import Ensemble3  # noqa: E402
import s2_model  # noqa: E402

O = '/mnt/project-files/model-v5/eksperimen-audit/'
jalur, varian = sys.argv[1], sys.argv[2]
opsi = set(varian.split('+'))
d = pd.read_pickle(s2_model.DATA + 'tahap1.pkl')
info = d['info']
sat = info.provinsi + '|' + info.nama_satuan_kerja
F = s2_model.fitur(d, jalur)
kw = copy.deepcopy(s2_model.KONF[jalur]['model'])
if 'std' in opsi:
    kw['skala'] = 'std'
if 'rata' in opsi:
    F['log_rasio_pagu_satker'] = np.log10(info.pagu / info.pagu.groupby(sat).transform('mean')).loc[F.index]
if 'sj' in opsi:
    g = sat + '|' + info.jenis
    med = info.pagu.groupby(g).transform('median')
    n = g.map(g.value_counts())
    F['log_rasio_pagu_satker'] = np.where(n.loc[F.index] >= 4, np.log10(info.pagu / med).loc[F.index], 0.0)
if 'tk' in opsi:
    F = F.drop(columns=['kekurangan_pdn', 'kekurangan_umk'])
if 'np' in opsi:
    F = F.drop(columns=['log_pagu'])
if 'nm' in opsi:
    X = pd.read_pickle(O + '../eksperimen-nama-satker/fitur_nama_satker.pkl')
    ok = X.n_nama_lain.loc[F.index] >= 2
    F['log_rasio_pagu_nama_satker'] = X.log_rasio_pagu_nama_satker.loc[F.index].where(ok, 0.0).fillna(0.0)
    kw['satu_arah'] = {**kw['satu_arah'], 'log_rasio_pagu_nama_satker': 'nol'}
if 'ns' in opsi:
    from x3_nama_satker import nama_dasar
    nd = info.nama_paket.map(nama_dasar)
    nsat = nd.map(pd.Series(sat.values, index=nd.values).groupby(level=0).nunique())
    F['log_rasio_pagu_nama_satker'] = F.log_rasio_pagu_nama_satker.where(nsat.loc[F.index] <= 50, 0.0)
    print('paket dengan fitur nama aktif:', int((F.log_rasio_pagu_nama_satker != 0).sum()), flush=True)
if 'tn' in opsi:
    F = F.drop(columns=['log_rasio_pagu_nama_satker'])
    kw['satu_arah'] = {k: v for k, v in kw['satu_arah'].items() if k != 'log_rasio_pagu_nama_satker'}
    kw.pop('skala_sama', None)
if 'ss' in opsi:
    kw['skala_sama'] = {'log_rasio_pagu_nama_satker': 'log_rasio_pagu_sejenis'}
if kw.get('ae_b') and F.shape[1] <= kw['ae_b']:
    kw['ae_b'] = max(1, F.shape[1] - 1)
print(jalur, varian, F.shape, kw, flush=True)
m = Ensemble3(**kw).fit(F)
Ps = [mm.pct(m._potong(F.values.astype(float))) for mm in m.m]
sk = pd.DataFrame({k: np.mean([p[k] for p in Ps], axis=0) for k in ['IF', 'LOF', 'AE']}, index=F.index)
sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
sk.to_pickle(O + f'skor_{jalur}_{varian}.pkl')
F.to_pickle(O + f'F_{jalur}_{varian}.pkl')
print('selesai', flush=True)
