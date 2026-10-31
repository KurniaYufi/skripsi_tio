"""Validasi v3, bagian 4: validitas prediktif lintas tahap.

Apakah paket yang dinilai janggal di tahap PERENCANAAN (model hanya melihat data RUP) lebih sering
bermasalah di tahap PELAKSANAAN? Red flag pelaksanaan (penyedia, realisasi) tidak pernah dilihat
model perencanaan, jadi tidak ada kebocoran.
"""
import sys
import numpy as np
import pandas as pd
from scipy.stats import hypergeom, mannwhitneyu

sys.path.insert(0, '/mnt/project-files/model-v2')
import s2_model  # noqa: F401,E402

OUT = '/mnt/project-files/validasi-v3/'
d = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')
info, rf = d['info'], d['rf']
V = pd.read_pickle(OUT + 'r1_variasi_red_flag.pkl')
h = pd.read_pickle('/mnt/project-files/model-v2/tahap2.pkl')
s = h['perencanaan']['skor'].Ensemble
idx = d['f_pel'].index  # paket yang punya realisasi selesai
s = s.loc[idx]
target = {
    'RF5 penyedia dominan': rf.loc[idx, 'rf5_penyedia_dominan'],
    'RF5 versi OCP (porsi > 40%)': V.loc[idx, 'rf5_porsi40_n5'],
    'RF6 penyedia serba-ada': rf.loc[idx, 'rf6_penyedia_serba_ada'],
    'R049 PL dekat ambang berulang': V.loc[idx, 'baru_R049_pl_dekat_ambang_berulang'],
    'R055 PL berulang lewat ambang': V.loc[idx, 'baru_R055_pl_berulang_lewat_ambang'],
    'R068 realisasi > pagu': V.loc[idx, 'baru_R068_realisasi_lewat_pagu'],
    'Realisasi menyimpang > 30% dari pagu': (info.realisasi.loc[idx] / info.pagu.loc[idx] - 1).abs() > 0.3,
}
target['Salah satu red flag tahap pelaksanaan (RF5/RF6)'] = target['RF5 penyedia dominan'] | target['RF6 penyedia serba-ada']
rows = []
srt = s.sort_values(ascending=False)
N = len(srt)
for nama, t in target.items():
    a = t.loc[srt.index].values
    M = int(a.sum())
    o = {'target': nama, 'acuan_persen': 100 * M / N}
    for q in (0.01, 0.05, 0.10):
        K = int(N * q)
        k = int(a[:K].sum())
        o[f'top{int(q * 100)}persen'] = 100 * k / K
        o[f'lift_top{int(q * 100)}persen'] = (k / K) / (M / N)
        o[f'pval_top{int(q * 100)}persen'] = hypergeom.sf(k - 1, N, M, K)
    o['mannwhitney_p'] = mannwhitneyu(srt[a], srt[~a], alternative='greater').pvalue
    rows.append(o)
df = pd.DataFrame(rows)
df.to_csv(OUT + 'r4_prediktif.csv', index=False)
pd.set_option('display.width', 250)
print(df.round(4).to_string(index=False))
