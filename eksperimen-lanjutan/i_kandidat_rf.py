"""I: kandidat red flag baru dari sumber luar (permintaan Tio 2026-10-30). Aturan pilih DITETAPKAN SEBELUM melihat hasil:
  1. punya sumber (OCP 2024 / Perpres PBJ), 2. bisa dihitung dari data, 3. tidak dibuat dari fitur model jalur itu,
  4. lipat 5% teratas >= 1,2 di 2024 DAN di provinsi uji 2025 (kalau hanya ada di 2025: di 2025 semua dan uji).
Semua kandidat dilaporkan, yang lolos maupun tidak.

Kandidat:
  C1 R054 (OCP 2024): PL yang pagunya <= ambang tetapi realisasinya > ambang PL
  C2 R052 (OCP 2024): penyedia pernah dapat pembelian kecil di satker yang sama tahun lalu, lalu paket tahun ini >= 10x (hanya 2025)
  C3 Perpres 46/2025 Psl 38(8): PL > Rp50 jt hanya lewat "Pencatatan Non Tender" (hanya 2025; aturan berlaku 30 Apr 2025)
  C4 R050 (OCP 2024): penyedia menerima > 40% nilai realisasi satker x jenis (>= 5 paket)
  C5 Perpres Psl 66 & 76(4): RUP mencantumkan PDN, tetapi nilai PDN realisasi 0 (di luar Pencatatan Non Tender)
  C6 Perpres Psl 65(3): RUP ditandai untuk UMK, tetapi nilai UMK realisasi 0 (di luar Pencatatan Non Tender)
  C7 R031 (OCP 2024): realisasi sama dengan atau di atas pagu (tidak ada penghematan), paket non-e-katalog
"""
import re
import numpy as np
import pandas as pd
from lib import muat, urut, DEV, OUT

AMB = {'2025': {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 400e6, 'Jasa Konsultansi': 100e6},
       '2024': {'Barang': 200e6, 'Jasa Lainnya': 200e6, 'Pekerjaan Konstruksi': 200e6, 'Jasa Konsultansi': 100e6}}
T1 = {'2025': '/mnt/project-files/model-v5/tahap1.pkl', '2024': '/mnt/project-files/model-v5-2024/tahap1.pkl'}


def satker_dasar(info):
    return info.provinsi + '|' + info.nama_satuan_kerja.str.replace(r'\s*-\s*[\d\.]+$', '', regex=True).str.upper().str.strip()


def pny(s):
    s = s.fillna('-').str.upper().str.replace(r'[^A-Z0-9 ]', ' ', regex=True)
    s = s.str.replace(r'\b(PT|CV|UD|TB|TOKO|KOPERASI|PERSERO|TBK)\b', ' ', regex=True)
    return s.str.split().str.join(' ').fillna('')


def kandidat(th):
    d = pd.read_pickle(T1[th]); i = d['info']; fp = d['f_pel']
    amb = i.jenis.map(AMB[th])
    pl = i.metode_pengadaan == 'Pengadaan Langsung'
    ada = i.realisasi.notna() & (i.realisasi > 0)
    k = pd.DataFrame(index=i.index)
    k['C1_R054_pl_realisasi_lewat_ambang'] = pl & (i.pagu <= amb) & ada & (i.realisasi > amb)
    sk, p = satker_dasar(i), pny(i.penyedia)
    if th == '2025':
        d0 = pd.read_pickle(T1['2024'])['info']
        lalu = pd.DataFrame({'k': satker_dasar(d0) + '||' + pny(d0.penyedia), 'v': d0.realisasi})
        lalu = lalu[~pny(d0.penyedia).isin(['', '-'])].groupby('k').v.sum()
        v0 = (sk + '||' + p).map(lalu)
        k['C2_R052_kecil_lalu_besar'] = ada & ~p.isin(['', '-']) & v0.notna() & (i.realisasi >= 10 * v0)
        k['C3_psl38_pl_pencatatan'] = pl & ada & (i.pagu > 50e6) & (i.sumber_transaksi == 'Pencatatan Non Tender')
    kk = sk + '|' + i.jenis
    m = ada & ~p.isin(['', '-'])
    tot = i.realisasi[m].groupby(kk[m]).sum(); n = kk[m].value_counts()
    sh = i.realisasi[m].groupby([kk[m], p[m]]).transform('sum') / kk[m].map(tot)
    k['C4_R050_pangsa_satker_jenis'] = False
    k.loc[m[m].index, 'C4_R050_pangsa_satker_jenis'] = ((sh > 0.4) & (kk[m].map(n) >= 5)).values
    bukan_catat = i.sumber_transaksi != 'Pencatatan Non Tender'
    k['C5_psl66_pdn_janji_tidak_terealisasi'] = False
    k.loc[fp.index, 'C5_psl66_pdn_janji_tidak_terealisasi'] = ((i.produk_dalam_negeri.loc[fp.index] == 'Ya') & (fp.porsi_pdn == 0) & bukan_catat.loc[fp.index]).values
    k['C6_psl65_umk_janji_tidak_terealisasi'] = False
    k.loc[fp.index, 'C6_psl65_umk_janji_tidak_terealisasi'] = ((i.status_umk.loc[fp.index] == 'Ya') & (fp.porsi_umk == 0) & bukan_catat.loc[fp.index]).values
    k['C7_R031_tanpa_penghematan'] = ada & (i.realisasi >= i.pagu) & ~i.sumber_transaksi.fillna('').str.startswith('E-Katalog')
    return k


if __name__ == '__main__':
    rows = []
    for th in ['2024', '2025']:
        K = kandidat(th)
        K.to_pickle(OUT + f'kandidat_rf_{th}.pkl')
        D = muat(th)
        for j in ['perencanaan', 'pelaksanaan']:
            P = D['H'][j]['pct_rata']; e = (P.IF + P.LOF + P.AE) / 3
            prov = D['info'].provinsi.loc[e.index]
            for prv in (['semua', 'uji'] if th == '2025' else ['semua']):
                s = e if prv == 'semua' else e[~prov.isin(DEV)]
                o = urut(s); n5 = int(len(o) * .05)
                for c in K:
                    y = K.loc[s.index, c]
                    if y.sum() == 0:
                        continue
                    rows.append({'kandidat': c, 'tahun': th, 'jalur': j, 'provinsi': prv, 'paket kena': int(y.sum()),
                                 'acuan %': 100 * y.mean(), '5% teratas %': 100 * y.loc[o[:n5]].mean(),
                                 'lipat': y.loc[o[:n5]].mean() / y.mean(), 'P@200 %': 100 * y.loc[o[:200]].mean(),
                                 'baru (tanpa RF1-6) %': 100 * (y & ~D['rf'].loc[s.index].any(axis=1)).sum() / y.sum()})
    df = pd.DataFrame(rows); df.to_csv(OUT + 'i_kandidat_rf.csv', index=False)
    pd.set_option('display.width', 250)
    print(df.round(2).to_string())
