"""Versi total: jumlah pagu semua paket bernama sama di satker, 2025 vs 2024 (mengatasi paket dipecah/digabung)."""
import re, sys, numpy as np, pandas as pd
sys.path.insert(0, '/mnt/project-files/model-v5')
D = '/mnt/project-files/'
x = pd.read_pickle('pasangan_2024.pkl')
t1 = pd.read_pickle(D + 'model-v5/tahap1.pkl'); info = t1['info']; rf = t1['rf']
t2 = pd.read_pickle(D + 'model-v5/tahap2.pkl'); e = t2['perencanaan']['skor']['Ensemble']; rk = e.rank(ascending=False)
x['pagu'] = info.pagu.loc[x.index]
r24 = pd.read_csv(D + 'rup_2024.csv', low_memory=False)
def nama_dasar(t):
    t = re.sub(r'[^a-z ]', ' ', str(t).lower()); return re.sub(r'\s+', ' ', t).strip()
def satker_dasar(s): return re.sub(r'\s+-\s+[\d.]+\s*$', '', str(s)).strip().upper()
p24 = r24[(r24.metode_pengadaan != 'Dikecualikan') & (r24.jenis_pengadaan != '-') & (r24.metode_pengadaan != '-') & (r24.total_nilai > 10000)]
k24 = p24.nama_instansi + '|' + p24.nama_satuan_kerja.map(satker_dasar) + '|' + p24.nama_paket.map(nama_dasar)
tot24 = p24.total_nilai.groupby(k24).sum(); n24 = k24.value_counts()
tot25 = x.groupby('kunci').pagu.sum(); n25 = x.kunci.value_counts()
k = tot25.index.intersection(tot24.index)
g = pd.DataFrame({'tot25': tot25[k], 'tot24': tot24[k], 'n25': n25[k], 'n24': n24[k]})
g['rasio'] = g.tot25 / g.tot24
print('kunci (satker+nama) 2025:', len(tot25), ' berpasangan 2024:', len(k), f'({len(k)/len(tot25):.1%})')
print('paket 2025 di kunci berpasangan:', int(g.n25.sum()))
print('rasio total 2025/2024:', g.rasio.quantile([.05,.25,.5,.75,.95,.99]).round(2).to_dict())
for a in [2,5,10]: print(f'  naik >= {a}x: {(g.rasio>=a).sum()} kunci ({(g.rasio>=a).mean():.1%})')
# jumlah paket berubah drastis = tanda paket dipecah/digabung
g['ubah_n'] = g.n25 / g.n24
print('kunci naik >=5x DAN jumlah paket tidak berubah banyak (0,5-2x):', ((g.rasio>=5)&g.ubah_n.between(.5,2)).sum())
# per paket: rasio total kunci
x['rasio_total'] = x.kunci.map(g.rasio)
c = x.rasio_total.notna()
lr = np.log10(x.rasio_total[c].clip(lower=1))
print('korelasi (Spearman) dengan skor ensemble:', round(lr.corr(e.loc[lr.index], method='spearman'), 3))
# red flag rate: paket di kunci naik >=5x vs lainnya (deskriptif)
anyrf = rf.loc[x.index].any(axis=1)
naik = c & (x.rasio_total >= 5)
print(f'red flag apa saja: kunci naik>=5x {anyrf[naik].mean():.1%} (n={naik.sum()}) vs berpasangan lain {anyrf[c & ~naik].mean():.1%} vs semua {anyrf.mean():.1%}')
for col in rf.columns: print(f'   {col}: {rf.loc[naik[naik].index, col].mean():.1%} vs {rf.loc[c[c & ~naik].index, col].mean():.1%}')
ex = g[(g.rasio >= 5) & g.ubah_n.between(.5, 2)].sort_values('rasio', ascending=False).head(25)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 80)
ex.index = ex.index.str.slice(0, 110); print(ex.round(1).to_string())
g.to_csv('kunci_2024_2025.csv')
