"""Kandidat red flag khusus tahap pelaksanaan dari OCP (2024) (permintaan Tio 2026-10-29: "cari, jelaskan, jangan train dulu").
Tidak melatih model: hanya menghitung jumlah paket, tumpang tindih dengan RF1-RF6, dan Precision@K skor v5 yang SUDAH ada.

Semua kandidat memakai penyedia (baru diketahui di tahap pelaksanaan) dan tidak menjadi fitur model v5.
  K1 (OCP R049) penyedia sama menerima >= 2 paket pengadaan/penunjukan langsung dari satker yang sama,
     masing-masing 90-100% ambang PL (dekat ambang).
  K2 (OCP R055) penyedia sama menerima >= 2 paket langsung dari satker yang sama (jenis sama), masing-masing di bawah
     ambang PL, tetapi jumlahnya melewati ambang.
  K3 (OCP R050) penyedia menguasai > 40% nilai realisasi satu "pasar" = satker x jenis pengadaan (pasar >= 5 paket).
  K4 (OCP R051) pasar provinsi x jenis dengan HHI > 1.800 (pasar terkonsentrasi). Tingkat pasar, bukan paket.
Keluaran: eksperimen-rf-pelaksanaan/kandidat.csv dan ringkasan di layar.
"""
import json
import re
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5/'
E = O + 'eksperimen-rf-pelaksanaan/'
d = pd.read_pickle(O + 'tahap1.pkl')
info = d['info']
RF = pd.read_pickle(O + 'red_flag_v5.pkl')
H = pd.read_pickle(O + 'tahap2.pkl')['pelaksanaan']
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
AMBANG = {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 400e6, 'Jasa Konsultansi': 100e6}
BENTUK = r'\b(PT|CV|UD|TB|TK|PD|FA|FIRMA|PERSERO|TBK|KOPERASI|KPRI|PO)\b'


def kunci(nama):
    s = re.sub(r'[^A-Z0-9 ]', ' ', str(nama).upper())
    return re.sub(r'\s+', ' ', re.sub(BENTUK, ' ', s)).strip()


idx = H['skor'].index  # paket jalur pelaksanaan
p = info.loc[idx].copy()
p['satker'] = p.provinsi + '|' + p.nama_satuan_kerja
p['pny'] = p.penyedia.map(kunci)
p.loc[(p.penyedia == '-') | (p.pny == ''), 'pny'] = np.nan
p['amb'] = p.jenis.map(AMBANG)
langsung = p.metode_pengadaan.isin(['Pengadaan Langsung', 'Penunjukan Langsung'])
ada = p.pny.notna()

K = pd.DataFrame(False, index=idx, columns=['K1_R049', 'K2_R055', 'K3_R050', 'K4_R051'])
# K1 R049: >= 2 paket langsung dekat ambang dari satker yang sama ke penyedia yang sama
dekat = langsung & ada & (p.pagu >= 0.9 * p.amb) & (p.pagu <= p.amb)
g = p[dekat].groupby(['satker', 'pny']).pagu.transform('size')
K.loc[g.index, 'K1_R049'] = (g >= 2).values
# K2 R055: >= 2 paket langsung di bawah ambang (satker, penyedia, jenis sama), jumlahnya melewati ambang
bawah = langsung & ada & (p.pagu <= p.amb)
q = p[bawah]
n = q.groupby(['satker', 'pny', 'jenis']).pagu.transform('size')
tot = q.groupby(['satker', 'pny', 'jenis']).pagu.transform('sum')
K.loc[q.index, 'K2_R055'] = ((n >= 2) & (tot > q.amb)).values
# K3 R050: pangsa penyedia di pasar satker x jenis > 40%, pasar minimal 5 paket
m = p[ada]
pasar = m.satker + '|' + m.jenis
nilai = m.realisasi
share = nilai.groupby([pasar, m.pny]).transform('sum') / nilai.groupby(pasar).transform('sum')
besar = pasar.map(pasar.value_counts()) >= 5
K.loc[m.index, 'K3_R050'] = ((share > 0.4) & besar).values
# K4 R051: HHI pasar provinsi x jenis
pasar2 = m.provinsi + '|' + m.jenis
sh2 = nilai.groupby([pasar2, m.pny]).sum() / nilai.groupby(pasar2).sum()
hhi = (sh2 ** 2 * 10000).groupby(level=0).sum()
K.loc[m.index, 'K4_R051'] = pasar2.map(hhi).gt(1800).values
K.to_pickle(E + 'kandidat.pkl')

s = H['skor'].Ensemble.sort_values(ascending=False)
o = s.index
dev = info.provinsi.loc[o].isin(DEV).values
lama = RF.loc[o].any(axis=1).values
rows = []
for c in K.columns:
    a = K.loc[o, c].values
    n5, nu = int(len(a) * .05), int((~dev).sum() * .05)
    rows.append({'kandidat': c, 'jumlah paket': int(a.sum()), 'porsi paket': a.mean(),
                 'yang tidak punya RF1-6': int((a & ~lama).sum()),
                 'tumpang tindih RF1': int((a & RF.loc[o, 'rf1_pl_dekat_ambang'].values).sum()),
                 'tumpang tindih RF3': int((a & RF.loc[o, 'rf3_pemecahan_paket'].values).sum()),
                 'tumpang tindih RF5': int((a & RF.loc[o, 'rf5_penyedia_dominan'].values).sum()),
                 'P@50': a[:50].mean(), 'P@200': a[:200].mean(), '5% teratas': a[:n5].mean(), 'acuan': a.mean(),
                 'uji 5%': a[~dev][:nu].mean(), 'acuan uji': a[~dev].mean(),
                 'pagu median (jt)': info.pagu.loc[o][a].median() / 1e6})
R = pd.DataFrame(rows)
R.to_csv(E + 'kandidat.csv', index=False)
pd.set_option('display.width', 250)
print(R.round(3).T.to_string())
print('HHI provinsi x jenis:', hhi.describe().round(0).to_dict(), 'pasar > 1800:', int((hhi > 1800).sum()), 'dari', len(hhi))
