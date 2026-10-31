"""G: apakah satker yang banyak paket tidak lazimnya di 2024 juga banyak di 2025, dan apakah satker yang banyak red flag-nya
di 2024 (tanpa RF2) lebih banyak paket tidak lazimnya di 2025? Paket dan tahunnya berbeda, jadi tidak ada kebocoran di
tingkat paket. Satker dicocokkan lewat provinsi + nama satker tanpa kode di belakang."""
import re
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from lib import muat, RF2, OUT

def kunci(info):
    return info.provinsi + '|' + info.nama_satuan_kerja.str.replace(r'\s*-\s*[\d\.]+$', '', regex=True).str.upper().str.strip()

rows = []
for j in ['perencanaan', 'pelaksanaan']:
    t = {}
    for th in ['2024', '2025']:
        D = muat(th); h = D['H'][j]; P = h['pct_rata']; idx = P.index
        k = kunci(D['info'].loc[idx])
        e = (P.IF + P.LOF + P.AE) / 3
        R = D['rf'].loc[idx, h['flags']]
        t[th] = pd.DataFrame({'anomali': (e >= e.quantile(.95)).groupby(k).mean(),
                              'rf_tanpa_rf2': R.drop(columns=[RF2]).any(axis=1).groupby(k).mean(),
                              'n': k.value_counts()})
    m = t['2024'].join(t['2025'], lsuffix='_24', rsuffix='_25', how='inner')
    m = m[(m.n_24 >= 20) & (m.n_25 >= 20)]
    for a, b, ket in [('anomali_24', 'anomali_25', 'proporsi tidak lazim 2024 vs 2025'),
                      ('rf_tanpa_rf2_24', 'anomali_25', 'red flag (tanpa RF2) 2024 vs tidak lazim 2025'),
                      ('rf_tanpa_rf2_24', 'rf_tanpa_rf2_25', 'red flag (tanpa RF2) 2024 vs 2025 (pembanding)')]:
        r, p = spearmanr(m[a], m[b])
        q = m[a].rank(pct=True) >= 0.8
        rows.append({'jalur': j, 'uji': ket, 'satker': len(m), 'spearman': r, 'p': p,
                     'satker 20% teratas: rata-rata kolom kedua': m.loc[q, b].mean(), 'satker lain': m.loc[~q, b].mean()})
df = pd.DataFrame(rows); df.to_csv(OUT + 'g_satker_lintas_tahun.csv', index=False)
pd.set_option('display.width', 250); print(df.round(3).to_string())
