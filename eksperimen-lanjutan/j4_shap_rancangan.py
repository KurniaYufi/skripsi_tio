"""J4: cek wajib setelah latih (cek-setelah-latih-model): fitur SHAP terbesar di 200 teratas, komposisi 200 teratas."""
import sys
import numpy as np
import pandas as pd
import shap
sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: F401,E402
from lib import muat, OUT  # noqa: E402

R = OUT + 'rancangan/'
for v in sys.argv[1:]:
    th = v.rsplit('_', 1)[1]
    jalur = 'perencanaan' if v.startswith('ren') else 'pelaksanaan'
    d = pd.read_pickle(R + f'model_{v}.pkl'); m, cols = d['model'], d['cols']
    F = pd.read_pickle(R + f'fitur_{th}_{jalur}.pkl')[cols]
    sk = pd.read_pickle(R + f'skor_{v}.pkl').Ensemble
    top = sk.sort_values(ascending=False).index[:200]
    bg = F.sample(50, random_state=42).values.astype(float)
    ex = shap.KernelExplainer(m.score, bg)
    sv = pd.DataFrame(ex.shap_values(F.loc[top].values.astype(float), nsamples=150, silent=True), index=top, columns=cols)
    sv.to_pickle(R + f'shap_{v}.pkl')
    info = muat(th)['info'].loc[top]
    print(f'##### {v}')
    print('fitur SHAP terbesar (jumlah paket):', sv.idxmax(axis=1).value_counts().to_dict())
    print('rata |SHAP|:', sv.abs().mean().sort_values(ascending=False).round(3).to_dict())
    print('nilai asli median di 200 teratas:', F.loc[top].median().round(2).to_dict())
    for c in ['metode_pengadaan', 'jenis']:
        print(c, '200 teratas:', info[c].value_counts(normalize=True).round(2).to_dict())
        print(c, 'semua      :', muat(th)['info'].loc[F.index, c].value_counts(normalize=True).round(2).head(5).to_dict())
    print('satker terbanyak di 200 teratas:', info.nama_satuan_kerja.value_counts().head(3).to_dict(), flush=True)
