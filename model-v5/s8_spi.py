"""Tahap 8: uji kelompok dengan data luar (known-groups), memakai Survei Penilaian Integritas (SPI) KPK 2024.

KPK hanya mengumumkan 10 pemerintah provinsi dengan skor SPI 2024 terendah ("paling rentan") dan 10 tertinggi
("paling terjaga"). Bila skor model menangkap risiko pengadaan, proporsi paket anomali di kelompok rentan
seharusnya lebih tinggi. SPI menilai integritas instansi secara umum (bukan khusus pengadaan), jadi hubungan yang
diharapkan lemah; hasil tidak nyata berarti belum terbukti, bukan terbantah.
Sumber angka: 10 tertinggi dari laman KPK (30 Januari 2025); 10 terendah dari GoodStats (data.goodstats.id) yang mengutip
dasbor SPI KPK, dicocokkan dengan detik.com (22 Januari 2025).
"""
import sys
sys.path.insert(0, "/mnt/project-files/model-v5")
import ens3  # noqa: E402,F401  (untuk membuka pickle tahap2)
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

OUT = '/mnt/project-files/model-v5/'
SPI = {  # skor SPI 2024 pemerintah provinsi
    'Papua Pegunungan': 55.10, 'Maluku Utara': 57.35, 'Papua Selatan': 58.05, 'Sumatera Utara': 58.55,
    'Papua Barat': 59.34, 'Sumatera Selatan': 60.63, 'Papua Tengah': 62.69, 'Riau': 62.83, 'Maluku': 63.12,
    'Papua': 63.73,
    'Jawa Tengah': 79.40, 'Bali': 77.97, 'Di Yogyakarta': 74.60, 'Sulawesi Utara': 73.98, 'Jawa Barat': 73.84,
    'Kalimantan Timur': 72.75, 'Dki Jakarta': 72.50, 'Kalimantan Barat': 72.37, 'Gorontalo': 71.79, 'Bengkulu': 71.76,
}
spi = pd.Series(SPI)
rentan = spi.index[spi < 70]
info = pd.read_pickle('/mnt/project-files/model-v5/tahap1.pkl')['info']
H = pd.read_pickle(OUT + 'tahap2.pkl')
rows, prov_rows = [], []
for jalur in ['perencanaan', 'pelaksanaan']:
    h = H[jalur]
    e, R = h['skor'].Ensemble, h['rf']
    prov = info.provinsi.loc[e.index]
    ukuran = {'Proporsi paket anomali (5% teratas)': (e >= e.quantile(0.95)).groupby(prov).mean(),
              'Proporsi paket anomali (1% teratas)': (e >= e.quantile(0.99)).groupby(prov).mean(),
              'Rata-rata skor ensemble': e.groupby(prov).mean(),
              'Proporsi paket ber-red flag': R.any(axis=1).groupby(prov).mean()}
    for c in R:
        ukuran[f'Proporsi {c}'] = R[c].groupby(prov).mean()
    for nama, v in ukuran.items():
        v = v.reindex(spi.index)
        for tanpa_papua in (False, True):
            ix = spi.index[~spi.index.str.contains('Papua')] if tanpa_papua else spi.index
            r, t = v.loc[ix.intersection(rentan)], v.loc[ix.difference(rentan)]
            u = mannwhitneyu(r, t, alternative='greater')
            rho, p = spearmanr(spi.loc[ix], v.loc[ix])
            rows.append({'jalur': jalur, 'ukuran': nama, 'tanpa_papua': tanpa_papua, 'n_rentan': len(r), 'n_terjaga': len(t),
                         'median_rentan': r.median(), 'median_terjaga': t.median(), 'rasio_median': r.median() / t.median(),
                         'p_mannwhitney_rentan_lebih_tinggi': u.pvalue, 'spearman_spi': rho, 'p_spearman': p})
    prov_rows.append(pd.DataFrame({'jalur': jalur, 'provinsi': spi.index, 'skor_spi_2024': spi.values,
                                   'kelompok': np.where(spi < 70, 'rentan', 'terjaga'),
                                   **{k: v.reindex(spi.index).values for k, v in list(ukuran.items())[:4]}}))
pd.DataFrame(rows).to_csv(OUT + 'validasi/v_spi.csv', index=False)
pd.concat(prov_rows).to_csv(OUT + 'validasi/v_spi_provinsi.csv', index=False)
pd.set_option('display.width', 220)
print(pd.DataFrame(rows).round(3).to_string())
print(pd.concat(prov_rows).round(3).to_string())
