"""Eksperimen data 2024 (permintaan Tio 2026-10-30): profil RUP/realisasi 2024 dan seberapa banyak paket 2025
punya pasangan di 2024 (satker sama + nama paket sama setelah dirapikan)."""
import re, sys, numpy as np, pandas as pd
sys.path.insert(0, '/mnt/project-files/model-v5')
D = '/mnt/project-files/'
def nama_dasar(t):
    t = re.sub(r'[^a-z ]', ' ', str(t).lower()); return re.sub(r'\s+', ' ', t).strip()
def satker_dasar(s):
    return re.sub(r'\s+-\s+[\d.]+\s*$', '', str(s)).strip().upper()

r24 = pd.read_csv(D + 'rup_2024.csv', low_memory=False, dtype={'kode_rup': str})
print('RUP 2024 baris', len(r24), 'tahun', r24.tahun_anggaran.value_counts().to_dict())
print('instansi', r24.nama_instansi.nunique(), 'cara', r24.cara_pengadaan.value_counts().to_dict())
p24 = r24[(r24.cara_pengadaan == 'Penyedia') & (r24.metode_pengadaan != 'Dikecualikan') & (r24.jenis_pengadaan != '-')
          & (r24.metode_pengadaan != '-') & (r24.total_nilai > 10000)].copy()
print('lingkup 2024 (sama aturan 2025):', len(p24), ' kode unik', p24.kode_rup.nunique())
print(p24.metode_pengadaan.value_counts().to_dict())

t1 = pd.read_pickle(D + 'model-v5/tahap1.pkl'); info = t1['info']
t2 = pd.read_pickle(D + 'model-v5/tahap2.pkl')
ren = t2['perencanaan']['skor']; idx = ren.index
i25 = info.loc[idx].copy()
rup25 = pd.read_csv(D + 'data_rup_2025.csv', low_memory=False, dtype={'kode_rup': str}, usecols=['kode_rup', 'nama_instansi', 'nama_satuan_kerja']).drop_duplicates('kode_rup').set_index('kode_rup')
i25['instansi'] = rup25.nama_instansi.reindex(i25.index)
i25['kunci'] = i25.instansi + '|' + i25.nama_satuan_kerja.map(satker_dasar) + '|' + i25.nama_paket.map(nama_dasar)
p24['kunci'] = p24.nama_instansi + '|' + p24.nama_satuan_kerja.map(satker_dasar) + '|' + p24.nama_paket.map(nama_dasar)
g = p24.groupby('kunci').total_nilai.agg(['median', 'size', 'sum'])
i25 = i25.join(g, on='kunci')
cocok = i25['median'].notna()
print(f'\n2025 perencanaan {len(i25)}; punya pasangan 2024: {cocok.sum()} ({cocok.mean():.1%})')
# kode RUP yang sama persis (paket lanjutan / tahun jamak)
print('kode RUP 2025 yang juga ada di RUP 2024:', i25.index.isin(p24.kode_rup).sum())
# satker cocok?
sk25 = set(i25.instansi + '|' + i25.nama_satuan_kerja.map(satker_dasar)); sk24 = set(p24.nama_instansi + '|' + p24.nama_satuan_kerja.map(satker_dasar))
print('satker 2025 yang ada di 2024:', len(sk25 & sk24), '/', len(sk25))
rasio = (i25.pagu / i25['median'])[cocok]
q = rasio.quantile([.05, .25, .5, .75, .95, .99]).round(2).to_dict()
print('rasio pagu 2025 / median 2024 (paket berpasangan):', q)
for a in [2, 5, 10]:
    print(f'  >= {a}x: {(rasio >= a).sum()} ({(rasio >= a).mean():.1%})   <= 1/{a}: {(rasio <= 1/a).sum()}')
# hubungan dengan skor sekarang
e = ren['Ensemble']; rk = e.rank(ascending=False)
top5 = rk <= len(e) * 0.05
print('\npunya pasangan, di 5% teratas:', (cocok & top5).sum(), '/', top5.sum(), ';  di 200 teratas:', (cocok & (rk <= 200)).sum())
lr = np.log10(rasio.clip(lower=1))
F = t2['perencanaan']['F'].loc[lr.index]
print('korelasi Spearman log rasio 2024 vs fitur sekarang:'); print(F.assign(r24=lr).corr('spearman')['r24'].round(3).to_dict())
print('korelasi dengan skor ensemble:', round(pd.Series(lr).corr(e.loc[lr.index], method='spearman'), 3))
ext = rasio[rasio >= 10].index
print('paket naik >=10x: median peringkat sekarang', int(rk.loc[ext].median()), '; masuk 5% teratas', top5.loc[ext].mean().round(3))
i25.loc[cocok].assign(rasio_2024=rasio, peringkat=rk.loc[cocok.index[cocok]].astype(int)).sort_values('rasio_2024', ascending=False)[
    ['provinsi', 'nama_satuan_kerja', 'nama_paket', 'pagu', 'median', 'size', 'rasio_2024', 'peringkat']].head(40).to_csv('contoh_kenaikan_terbesar.csv')
i25[['kunci', 'median', 'size']].rename(columns={'median': 'median_pagu_2024', 'size': 'n_paket_2024'}).to_pickle('pasangan_2024.pkl')
