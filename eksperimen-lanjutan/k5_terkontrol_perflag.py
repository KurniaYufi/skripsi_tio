"""K5: lipat TERKONTROL pagu x metode untuk tiap red flag (sekarang dan project sebelah), untuk model sekarang dan varian
yang tidak bocor. Menjawab: apakah keselarasan dengan red flag PDN/UMK (P5, P6, E4, E5) bertahan setelah ukuran paket dan
metode disamakan? (Pelajaran kandidat-red-flag-baru.md: efek PDN/UMK sempat hilang setelah dikontrol.)"""
import os
import pandas as pd
from lib import muat, urut, DEV, OUT, RF2
from j3_eval_rancangan import strata
from k4_eval_sebelah import LAMA, BARU, skor_semua
from k1_fitur_sebelah import R

PILIH = ['Model sekarang', '+ kebiasaan', '+ zrasio', '+ kebzr', '+ robust', 'Tanpa model: acak']
rows = []
for th in ['2024', '2025']:
    D = muat(th); info = D['info']; rf = D['rf'].join(pd.read_pickle(R + f'rf_{th}.pkl'))
    for j in ['perencanaan', 'pelaksanaan']:
        for nama, s in skor_semua(th, j).items():
            if nama not in PILIH:
                continue
            for prv in (['semua', 'uji'] if th == '2025' else ['semua']):
                ss = s if prv == 'semua' else s[~info.provinsi.loc[s.index].isin(DEV)]
                ss = ss[~rf.loc[ss.index, RF2]]
                o = urut(ss); top = o[:int(len(o) * .05)]
                st = strata(info.loc[ss.index]); w = st.loc[top].value_counts(normalize=True)
                r = {'tahun': th, 'jalur': j, 'provinsi': prv, 'skor': nama}
                for f in LAMA[j] + BARU[j]:
                    y = rf.loc[ss.index, f].astype(bool)
                    harap = (w * y.groupby(st).mean().reindex(w.index)).sum()
                    r[f] = y.loc[top].mean() / harap if harap else float('nan')
                rows.append(r)
df = pd.DataFrame(rows); df.to_csv(OUT + 'k5_terkontrol_perflag.csv', index=False)
pd.set_option('display.width', 300); pd.set_option('display.max_columns', 30)
print(df.round(2).to_string())
