"""Per red flag (paket ber-RF2 dikeluarkan, hanya paket yang red flag-nya berlaku): dari mana kenaikan skor berasal?"""
import sys, glob, os
import pandas as pd
from lib import muat, ukur
pd.set_option('display.width', 250)
vs = sys.argv[1:]
rows = []
for th in ['2024', '2025']:
    for j in ['perencanaan', 'pelaksanaan']:
        src = {'model sekarang': muat(th)['H'][j]['pct_rata']}
        for v in vs:
            f = f'/mnt/project-files/eksperimen-lanjutan/skor/{v}__{th}__{j}.pkl'
            if os.path.exists(f):
                src[v] = pd.read_pickle(f)
        for v, P in src.items():
            s = (P.IF + P.LOF + P.AE) / 3
            o = ukur(s, th, j, buang_rf2=True)
            rows.append({'tahun': th, 'jalur': j, 'varian': v, **{k.replace(': lipat', ''): o[k] for k in o if k.endswith(': lipat') and k.startswith('rf')}})
df = pd.DataFrame(rows)
print(df.round(2).to_string())
