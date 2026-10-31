"""Tahap 3: Kernel SHAP pada skor ensemble (rata-rata 5 seed) untuk 200 paket teratas per jalur.

Pakai: python3 s3_shap.py [jalur ...]   (bawaan: kedua jalur; hasil per jalur disimpan terpisah lalu digabung)
"""
import os
import sys
import time
import pandas as pd
import shap

sys.path.insert(0, '/mnt/project-files/model-v5')
import s2_model  # noqa: F401,E402  (kelas Ensemble3 untuk membuka pickle)

OUT = os.environ.get('V3_OUT', '/mnt/project-files/model-v5/')  # bisa diganti untuk uji kode
GRUP = {'metode_': 'metode', 'jenis_': 'jenis', 'sumber_': 'sumber'}
JALUR = sys.argv[1:] or ['perencanaan', 'pelaksanaan']
TOPN, NS = int(os.environ.get('V3_TOP', 200)), int(os.environ.get('V3_NS', 300))  # bisa dikecilkan untuk uji kode
T0 = time.time()
hasil = pd.read_pickle(OUT + 'tahap2.pkl')

for jalur in JALUR:
    h = hasil[jalur]
    F, m, sk = h['F'], h['model'], h['skor']
    top = sk.Ensemble.sort_values(ascending=False).index[:TOPN]
    bg = F.sample(50, random_state=42).values.astype(float)
    ex = shap.KernelExplainer(m.score, bg)
    sv = ex.shap_values(F.loc[top].values.astype(float), nsamples=NS, silent=True)
    sv = pd.DataFrame(sv, index=top, columns=F.columns)
    # Gabungkan kolom one-hot menjadi satu fitur (nilai SHAP bersifat aditif)
    grp = {}
    for c in F.columns:
        grp.setdefault(next((v for k, v in GRUP.items() if c.startswith(k)), c), []).append(c)
    svg = pd.DataFrame({g: sv[cs].sum(axis=1) for g, cs in grp.items()})
    pd.to_pickle(dict(shap=svg, base=float(ex.expected_value)), OUT + f'tahap3_{jalur}.pkl')
    print(f'[{time.time() - T0:6.0f}s]', jalur, 'base', round(float(ex.expected_value), 3), 'rata |shap|:', flush=True)
    print(svg.abs().mean().sort_values(ascending=False).round(4).to_string(), flush=True)

if all(os.path.exists(OUT + f'tahap3_{j}.pkl') for j in ['perencanaan', 'pelaksanaan']):
    pd.to_pickle({j: pd.read_pickle(OUT + f'tahap3_{j}.pkl') for j in ['perencanaan', 'pelaksanaan']}, OUT + 'tahap3.pkl')
    print('tahap3.pkl lengkap')
