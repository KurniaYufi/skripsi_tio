"""Seberapa besar Precision@K berubah hanya karena seed acak? Melatih ensemble v5 dengan dua set seed lain (5-9, 10-14).
Data dan fitur sama persis dengan s2_model.py. Keluaran: eksperimen-seed/hasil.csv."""
import json
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
from ens3 import Ensemble3  # noqa: E402
import s2_model  # noqa: E402

O = '/mnt/project-files/model-v5/eksperimen-seed/'
os.makedirs(O, exist_ok=True)
d = pd.read_pickle(s2_model.DATA + 'tahap1.pkl')
info = d['info']
RF = pd.read_pickle(s2_model.DATA + 'red_flag_v5.pkl')
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
H = pd.read_pickle(s2_model.OUT + 'tahap2.pkl')


def ukur(s, flags):
    idx = s.sort_values(ascending=False).index
    a = RF.loc[idx, flags].any(axis=1).values
    dev = info.provinsi.loc[idx].isin(DEV).values
    return {'P@200': a[:200].mean(), '5% teratas': a[:int(len(a) * .05)].mean(),
            'uji 5%': a[~dev][:int((~dev).sum() * .05)].mean(), 'pagu<10jt top200': (info.pagu.loc[idx[:200]] < 1e7).mean()}


rows = []
for jalur in sys.argv[1:] or ['perencanaan', 'pelaksanaan']:
    flags = s2_model.FLAGS[jalur]
    F = s2_model.fitur(d, jalur)
    base = H[jalur]['skor'].Ensemble
    rows.append({'jalur': jalur, 'seed': '42,1,2,3,4 (dipakai)', 'jaccard200 vs dipakai': 1.0, **ukur(base, flags)})
    for seeds in [[5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]:
        m = Ensemble3(seeds=seeds, **s2_model.KONF[jalur]['model']).fit(F)
        s = pd.Series(m.score(F.values.astype(float)), index=F.index)
        A, B = set(base.nlargest(200).index), set(s.nlargest(200).index)
        rows.append({'jalur': jalur, 'seed': ','.join(map(str, seeds)), 'jaccard200 vs dipakai': len(A & B) / len(A | B),
                     **ukur(s, flags)})
        print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(O + 'hasil.csv', index=False)
print(pd.DataFrame(rows).round(3).to_string())
