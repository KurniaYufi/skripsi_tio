"""Tahap 3: Kernel SHAP pada skor ensemble untuk 200 paket teratas per jalur."""
import sys
import numpy as np
import pandas as pd
import shap

sys.path.insert(0, '/mnt/project-files/model-v2')
import s2_model  # noqa: F401  (kelas Ensemble2 untuk membuka pickle)

OUT = '/mnt/project-files/model-v2/'
hasil = pd.read_pickle(OUT + 'tahap2.pkl')
GRUP = {'metode_': 'metode', 'jenis_': 'jenis', 'sumber_': 'sumber'}

out = {}
for jalur in ['perencanaan', 'pelaksanaan']:
    h = hasil[jalur]
    F = h['F']
    m, sk = h['model'], h['skor']
    top = sk.Ensemble.sort_values(ascending=False).index[:200]
    bg = F.sample(50, random_state=42).values.astype(float)
    ex = shap.KernelExplainer(m.score, bg)
    sv = ex.shap_values(F.loc[top].values.astype(float), nsamples=300, silent=True)
    sv = pd.DataFrame(sv, index=top, columns=F.columns)
    # Gabungkan kolom one-hot menjadi satu fitur (nilai SHAP bersifat aditif)
    grp = {}
    for c in F.columns:
        g = next((v for k, v in GRUP.items() if c.startswith(k)), c)
        grp.setdefault(g, []).append(c)
    svg = pd.DataFrame({g: sv[cs].sum(axis=1) for g, cs in grp.items()})
    out[jalur] = dict(shap=svg, base=float(ex.expected_value))
    print(jalur, 'base', round(float(ex.expected_value), 3), 'rata |shap|:')
    print(svg.abs().mean().sort_values(ascending=False).round(4).to_string())
pd.to_pickle(out, OUT + 'tahap3.pkl')
