"""Tahap 9: keselarasan di tingkat satker. Satker yang banyak paket tidak lazimnya apakah juga banyak red flag-nya?

Satker dengan minimal 30 paket. Dihitung korelasi Spearman antara proporsi paket tidak lazim (5% teratas nasional)
dan proporsi paket ber-red flag; juga per red flag. Ini jembatan antara bukti tingkat paket dan tingkat provinsi.
"""
import pandas as pd
from scipy.stats import spearmanr

OUT = '/mnt/project-files/model-v4/'
info = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')['info']
satker = info.provinsi + '|' + info.nama_satuan_kerja
H = pd.read_pickle(OUT + 'tahap2.pkl')
rows = []
for jalur in ['perencanaan', 'pelaksanaan']:
    e, R = H[jalur]['skor'].Ensemble, H[jalur]['rf']
    s = satker.loc[e.index]
    n = s.map(s.value_counts())
    ok = (n >= 30).values
    g = s[ok]
    an = (e >= e.quantile(0.95))[ok].groupby(g).mean()
    target = {'ada red flag': R.any(axis=1), **{c: R[c] for c in R}}
    for nama, t in target.items():
        tr = t[ok].groupby(g).mean()
        rho, p = spearmanr(an, tr.loc[an.index])
        rows.append({'jalur': jalur, 'satker': len(an), 'red_flag': nama, 'spearman': rho, 'p': p})
pd.DataFrame(rows).to_csv(OUT + 'validasi/v_satker.csv', index=False)
print(pd.DataFrame(rows).round(3).to_string())
