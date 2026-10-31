"""B1: cara menggabungkan IF/LOF/AE (tanpa latih ulang, dari persentil rata-rata 5 seed). Pilih di 2024, uji di 2025."""
import numpy as np
import pandas as pd
from lib import muat, ukur, OUT

def varian(P):
    r = {c: P[c].rank(pct=True) for c in P}
    return {
        'rata-rata 3 model (sekarang)': (P.IF + P.LOF + P.AE) / 3,
        'IF saja': P.IF, 'LOF saja': P.LOF, 'AE saja': P.AE,
        'IF + LOF': (P.IF + P.LOF) / 2, 'LOF + AE': (P.LOF + P.AE) / 2, 'IF + AE': (P.IF + P.AE) / 2,
        'bobot LOF 1/2, IF 1/4, AE 1/4': 0.5 * P.LOF + 0.25 * P.IF + 0.25 * P.AE,
        'maksimum 3 model': P.max(axis=1),
        'median 3 model': P.median(axis=1),
        'rata-rata peringkat': (r['IF'] + r['LOF'] + r['AE']) / 3,
        'suara terbanyak (>=2 model di 5% teratas)': sum((r[c] >= 0.95).astype(float) for c in r) + (P.IF + P.LOF + P.AE) / 300,
    }

rows = []
for th in ['2024', '2025']:
    for jalur in ['perencanaan', 'pelaksanaan']:
        P = muat(th)['H'][jalur]['pct_rata']
        for prov in (['semua', 'uji'] if th == '2025' else ['semua']):
            for nama, s in varian(P).items():
                a = ukur(s, th, jalur, prov)
                b = ukur(s, th, jalur, prov, buang_rf2=True)
                rows.append({'tahun': th, 'jalur': jalur, 'provinsi': prov, 'gabungan': nama,
                             'P@200': a['P@200'], 'lipat 5%': a['lipat: semua'],
                             'lipat 5% tanpa paket RF2': b['lipat: semua'], 'P@200 tanpa paket RF2': b['P@200'],
                             'acuan tanpa paket RF2': b['acuan: semua'], 'p tanpa paket RF2': b['berlaku p: semua'],
                             'lipat berlaku tanpa paket RF2': b['berlaku lipat: semua']})
df = pd.DataFrame(rows); df.to_csv(OUT + 'b1_gabung_model.csv', index=False)
pd.set_option('display.width', 250)
for k, g in df.groupby(['tahun', 'jalur', 'provinsi'], sort=False):
    print(k); print(g.set_index('gabungan').drop(columns=['tahun', 'jalur', 'provinsi']).round(3).to_string())
