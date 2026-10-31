"""A0: model sekarang vs pembanding tanpa model, dengan evaluasi yang adil (lib.ukur). Tidak melatih ulang."""
import pandas as pd
from lib import ukur, pembanding, skor_model, OUT

KOL = ['P@200', 'P@200 tanpa RF2', '5%: semua', 'acuan: semua', 'lipat: semua', 'lipat: tanpa RF2',
       'berlaku 5%: semua', 'berlaku acuan: semua', 'berlaku lipat: semua', 'berlaku lipat: tanpa RF2',
       'berlaku p: tanpa RF2', 'berlaku AUC: tanpa RF2', 'porsi 200 teratas yang red flag-nya berlaku']
rows = []
for th in ['2024', '2025']:
    for jalur in ['perencanaan', 'pelaksanaan']:
        for prov in (['semua', 'uji'] if th == '2025' else ['semua']):
            for nama, s in {**skor_model(th, jalur), **pembanding(th, jalur)}.items():
                rows.append({'tahun': th, 'jalur': jalur, 'provinsi': prov, 'skor': nama, **ukur(s, th, jalur, prov)})
df = pd.DataFrame(rows)
df.to_csv(OUT + 'a0_evaluasi_adil.csv', index=False)
pd.set_option('display.width', 250)
for (th, j, p), g in df.groupby(['tahun', 'jalur', 'provinsi'], sort=False):
    print(f'\n=== {th} {j} provinsi {p}')
    print(g.set_index('skor')[KOL].round(3).to_string())
    print(g.set_index('skor')[[c for c in g.columns if c.endswith(': lipat') and c.startswith('rf')]].round(2).to_string())
