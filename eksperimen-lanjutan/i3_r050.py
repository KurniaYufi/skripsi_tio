"""I3: R050 (pangsa penyedia > 40% di satker x jenis) versi ketat: penyedia itu punya >= 2 paket di satker x jenis tsb,
supaya tidak terkena hanya karena SATU paket besar (yang sudah terbaca dari fitur pagu dibanding satker). Lalu efeknya
pada Precision@K bila ditambahkan sebagai red flag."""
import numpy as np
import pandas as pd
from lib import muat, urut, DEV, OUT, RF2
from i_kandidat_rf import satker_dasar, pny, T1

hasil = []
for th in ['2024', '2025']:
    i = pd.read_pickle(T1[th])['info']
    p, kk = pny(i.penyedia), satker_dasar(i) + '|' + i.jenis
    m = i.realisasi.notna() & (i.realisasi > 0) & ~p.isin(['', '-'])
    g = pd.DataFrame({'kk': kk[m], 'p': p[m], 'v': i.realisasi[m]})
    tot, n = g.groupby('kk').v.sum(), g.kk.value_counts()
    g['share'] = g.groupby(['kk', 'p']).v.transform('sum') / g.kk.map(tot)
    g['npk'] = g.groupby(['kk', 'p']).v.transform('size')
    c4 = pd.Series(False, index=i.index); c4b = c4.copy()
    c4.loc[g.index] = (g.share > .4) & (g.kk.map(n) >= 5)
    c4b.loc[g.index] = (g.share > .4) & (g.kk.map(n) >= 5) & (g.npk >= 2)
    D = muat(th)
    for j in ['perencanaan', 'pelaksanaan']:
        P = D['H'][j]['pct_rata']; e = (P.IF + P.LOF + P.AE) / 3
        R = D['rf'].loc[e.index, D['H'][j]['flags']]
        for prv in (['semua', 'uji'] if th == '2025' else ['semua']):
            s = e if prv == 'semua' else e[~D['info'].provinsi.loc[e.index].isin(DEV)]
            s = s[~R.loc[s.index, RF2]]  # paket RF2 dikeluarkan
            o = urut(s); top = o[:int(len(o) * .05)]
            lama = R.loc[s.index].drop(columns=[RF2]).any(axis=1)
            r = {'tahun': th, 'jalur': j, 'provinsi': prv, 'paket R050 ketat': int(c4b.loc[s.index].sum()),
                 'lipat R050 ketat': c4b.loc[top].mean() / c4b.loc[s.index].mean()}
            for nama, y in [('red flag sekarang', lama), ('+ R050', lama | c4.loc[s.index]), ('+ R050 ketat', lama | c4b.loc[s.index])]:
                r[f'lipat 5%: {nama}'] = y.loc[top].mean() / y.mean()
                r[f'P@200: {nama}'] = y.loc[o[:200]].mean()
            hasil.append(r)
df = pd.DataFrame(hasil); df.to_csv(OUT + 'i3_r050.csv', index=False)
pd.set_option('display.width', 250); print(df.round(3).T.to_string())
