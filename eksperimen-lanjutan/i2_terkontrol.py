"""I2: lipat kandidat red flag yang DIKONTROL pagu dan metode. Paket teratas model cenderung berpagu besar; kalau red flag
juga lebih sering di paket besar, lipat biasa bisa tinggi hanya karena ukuran. Di sini 5% teratas dibandingkan dengan paket
acak yang punya komposisi kelompok pagu (10 kelompok) x metode (PL / e-purchasing / lainnya) yang sama."""
import numpy as np
import pandas as pd
from lib import muat, urut, DEV, OUT

rows = []
for th in ['2024', '2025']:
    K = pd.read_pickle(OUT + f'kandidat_rf_{th}.pkl')
    D = muat(th)
    K = K.join(D['rf'][['rf5_penyedia_dominan', 'rf6_penyedia_serba_ada', 'rf3_pemecahan_paket', 'rf1_pl_dekat_ambang']])
    for j in ['perencanaan', 'pelaksanaan']:
        P = D['H'][j]['pct_rata']; e = (P.IF + P.LOF + P.AE) / 3
        info = D['info'].loc[e.index]
        for prv in (['semua', 'uji'] if th == '2025' else ['semua']):
            s = e if prv == 'semua' else e[~info.provinsi.isin(DEV)]
            inf = info.loc[s.index]
            met = np.where(inf.metode_pengadaan == 'Pengadaan Langsung', 'PL', np.where(inf.metode_pengadaan == 'E-Purchasing', 'EP', 'lain'))
            strata = pd.Series(pd.qcut(np.log10(inf.pagu), 10, labels=False, duplicates='drop').astype(str) + met, index=s.index)
            o = urut(s); top = o[:int(len(o) * .05)]
            w = strata.loc[top].value_counts(normalize=True)
            for c in K:
                y = K.loc[s.index, c].astype(bool)
                if y.sum() < 30:
                    continue
                rate = y.groupby(strata).mean()
                harap = (w * rate.reindex(w.index)).sum()
                rows.append({'kandidat': c, 'tahun': th, 'jalur': j, 'provinsi': prv, 'lipat': y.loc[top].mean() / y.mean(),
                             'lipat terkontrol pagu+metode': y.loc[top].mean() / harap if harap else np.nan})
df = pd.DataFrame(rows); df.to_csv(OUT + 'i2_terkontrol.csv', index=False)
df['kol'] = df.jalur.str.slice(0, 4) + ' ' + df.tahun + ' ' + df.provinsi
pd.set_option('display.width', 250)
for v in ['lipat', 'lipat terkontrol pagu+metode']:
    print('##', v); print(df.pivot_table(index='kandidat', columns='kol', values=v).round(2).to_string())
