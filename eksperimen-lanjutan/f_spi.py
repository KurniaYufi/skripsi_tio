"""F: uji dengan data luar SPI KPK 2024 (10 provinsi terendah vs 10 tertinggi), sekarang juga dengan DATA 2024,
yang tahunnya sama dengan survei. Ukuran: proporsi paket 5% teratas nasional di tiap provinsi."""
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
from lib import muat

# Angka sama dengan model-v5/s8_spi.py (sumber: KPK, GoodStats, detik.com)
SPI = {  # skor SPI 2024 pemerintah provinsi
    'Papua Pegunungan': 55.10, 'Maluku Utara': 57.35, 'Papua Selatan': 58.05, 'Sumatera Utara': 58.55,
    'Papua Barat': 59.34, 'Sumatera Selatan': 60.63, 'Papua Tengah': 62.69, 'Riau': 62.83, 'Maluku': 63.12,
    'Papua': 63.73,
    'Jawa Tengah': 79.40, 'Bali': 77.97, 'Di Yogyakarta': 74.60, 'Sulawesi Utara': 73.98, 'Jawa Barat': 73.84,
    'Kalimantan Timur': 72.75, 'Dki Jakarta': 72.50, 'Kalimantan Barat': 72.37, 'Gorontalo': 71.79, 'Bengkulu': 71.76,
}

spi = pd.Series(SPI)
rentan = spi.index[spi < 70]


def spi_uji(skor, th):
    prov = muat(th)['info'].provinsi.loc[skor.index]
    v = (skor >= skor.quantile(0.95)).groupby(prov).mean().reindex(spi.index)
    o = {}
    for tp in (False, True):
        ix = spi.index[~spi.index.str.contains('Papua')] if tp else spi.index
        r, t = v.loc[ix.intersection(rentan)], v.loc[ix.difference(rentan)]
        k = ' tanpa Papua' if tp else ''
        o['median rentan' + k], o['median terjaga' + k] = r.median(), t.median()
        o['p' + k] = mannwhitneyu(r, t, alternative='greater').pvalue
        o['spearman SPI' + k] = spearmanr(spi.loc[ix], v.loc[ix])[0]
    return o


if __name__ == '__main__':
    pd.set_option('display.width', 250)
    rows = []
    for th in ['2024', '2025']:
        for j in ['perencanaan', 'pelaksanaan']:
            P = muat(th)['H'][j]['pct_rata']
            for g, s in {'rata-rata 3 model (sekarang)': (P.IF + P.LOF + P.AE) / 3, 'LOF + AE': (P.LOF + P.AE) / 2,
                         'LOF saja': P.LOF}.items():
                rows.append({'tahun': th, 'jalur': j, 'gabungan': g, **spi_uji(s, th)})
    df = pd.DataFrame(rows)
    df.to_csv('/mnt/project-files/eksperimen-lanjutan/f_spi.csv', index=False)
    print(df.round(3).to_string())
