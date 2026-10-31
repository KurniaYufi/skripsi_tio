"""Uji kestabilan: konfigurasi yang sama dijalankan dengan beberapa seed acak (sampel latih LOF/AE dan pohon IF berbeda)."""
import json
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v1/eksplorasi')
import exp  # noqa: E402

KONF = json.load(open(exp.OUT + 'kandidat.json'))  # [{label, jalur, fitur, skala, hp, gabung}]
SEEDS = [42, 1, 2, 3, 4]
rows = []
for k in KONF:
    fk = tuple(sorted(k['fitur'].items()))
    hp = {m: tuple(sorted(v.items())) for m, v in k['hp'].items()}
    for s in SEEDS:
        exp.SEED = s
        exp.CACHE.clear()
        P = {m: exp.skor_model(k['jalur'], fk, k['skala'], m, hp[m]) for m in ['IF', 'LOF', 'AE']}
        row = {'label': k['label'], 'jalur': k['jalur'], 'seed': s}
        row.update({f'ens_{a}': b for a, b in exp.evaluasi(exp.gabung(P, k['gabung']), k['jalur']).items()})
        for m in ['IF', 'LOF', 'AE']:
            e = exp.evaluasi(P[m], k['jalur'])
            row.update({f'{m}_{a}': b for a, b in e.items()})
        rows.append(row)
        pd.DataFrame(rows).to_csv(exp.OUT + 'hasil_kestabilan.csv', index=False)
        print(k['jalur'], k['label'], 'seed', s, 'ens semua_rata', round(row['ens_semua_rata'], 3),
              'IF', round(row['IF_semua_rata'], 3), 'LOF', round(row['LOF_semua_rata'], 3), 'AE', round(row['AE_semua_rata'], 3), flush=True)
df = pd.DataFrame(rows)
cols = ['ens_semua_rata', 'ens_uji_rata', 'ens_semua_rata_tanpaRF4', 'IF_semua_rata', 'LOF_semua_rata', 'AE_semua_rata']
print(df.groupby(['jalur', 'label'])[cols].agg(['mean', 'std']).round(3).to_string())
