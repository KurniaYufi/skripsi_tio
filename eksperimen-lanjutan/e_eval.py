"""E: evaluasi semua varian di skor/ dengan ukuran yang sama dengan model sekarang. Pilih di 2024, uji di 2025."""
import glob
import os
import pandas as pd
from lib import muat, ukur, OUT

def gabungan(P):
    g = {}
    if {'IF', 'LOF', 'AE'} <= set(P):
        g['rata-rata 3 model'] = (P.IF + P.LOF + P.AE) / 3
        g['LOF + AE'] = (P.LOF + P.AE) / 2
    g['LOF saja'] = P.LOF
    return g

sumber = {('model sekarang', th, j): muat(th)['H'][j]['pct_rata'] for th in ['2024', '2025'] for j in ['perencanaan', 'pelaksanaan']}
for f in sorted(glob.glob(OUT + 'skor/*.pkl')):
    v, th, j = os.path.basename(f)[:-4].split('__')
    sumber[(v, th, j)] = pd.read_pickle(f)
rows = []
for (v, th, j), P in sumber.items():
    for g, s in gabungan(P).items():
        for prov in (['semua', 'uji'] if th == '2025' else ['semua']):
            a, b = ukur(s, th, j, prov), ukur(s, th, j, prov, buang_rf2=True)
            rows.append(dict(varian=v, gabungan=g, tahun=th, jalur=j, provinsi=prov,
                             **{'P@200': a['P@200'], 'lipat 5%': a['lipat: semua'], 'P@200 (tanpa paket RF2)': b['P@200'],
                                'lipat 5% (tanpa paket RF2)': b['lipat: semua'], 'acuan (tanpa paket RF2)': b['acuan: semua'],
                                'lipat berlaku (tanpa paket RF2)': b['berlaku lipat: semua'],
                                'p (tanpa paket RF2)': b['berlaku p: semua']}))
df = pd.DataFrame(rows)
df.to_csv(OUT + 'e_eval.csv', index=False)
pd.set_option('display.width', 250)
for (j, th, prov), g in df.groupby(['jalur', 'tahun', 'provinsi']):
    print(f'\n=== {j} {th} provinsi {prov}')
    print(g.drop(columns=['jalur', 'tahun', 'provinsi']).set_index(['varian', 'gabungan']).round(3).to_string())
