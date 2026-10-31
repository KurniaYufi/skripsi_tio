"""Uji tahun lain: model yang sama (fitur, pengaturan, red flag) di data 2024 dibanding hasil 2025."""
import json, sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, '/mnt/project-files/model-v5')
DIR = {'2025': '/mnt/project-files/model-v5/', '2024': '/mnt/project-files/model-v5-2024/'}
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))


def ukur(th, jalur):
    t1 = pd.read_pickle(DIR[th] + 'tahap1.pkl')
    h = pd.read_pickle(DIR[th] + 'tahap2.pkl')[jalur]
    info, rf = t1['info'], t1['rf']
    sk = h['skor'].sort_values('Ensemble', ascending=False)
    R = rf.loc[sk.index, h['flags']]
    a = R.any(axis=1).values
    b = R.drop(columns=['rf2_pl_lewat_ambang']).any(axis=1).values
    n, n5 = len(sk), int(len(sk) * 0.05)
    dev = info.provinsi.loc[sk.index].isin(DEV).values
    o = {'tahun': th, 'jalur': jalur, 'paket': n, 'acuan': a.mean()}
    for K in [50, 100, 200]:
        o[f'P@{K}'] = a[:K].mean()
    o['5% teratas'] = a[:n5].mean()
    o['lift 5%'] = o['5% teratas'] / o['acuan']
    o['uji 5%'] = a[~dev][:int((~dev).sum() * 0.05)].mean()
    o['acuan uji'] = a[~dev].mean()
    o['tanpa RF2: 5%'] = b[:n5].mean()
    o['tanpa RF2: acuan'] = b.mean()
    o['tanpa RF2: uji 5%'] = b[~dev][:int((~dev).sum() * 0.05)].mean()
    o['tanpa RF2: acuan uji'] = b[~dev].mean()
    for c in h['flags']:
        o[f'{c} 5%/acuan'] = f"{R[c].values[:n5].mean():.1%} / {R[c].mean():.1%}"
    top = info.loc[sk.index[:200]]
    o['200 teratas: pagu < Rp10 jt'] = (top.pagu < 1e7).mean()
    o['200 teratas: satker terbanyak'] = int((top.provinsi + '|' + top.nama_satuan_kerja).value_counts().iloc[0])
    o['200 teratas: jenis'] = top.jenis.value_counts(normalize=True).round(2).to_dict()
    o['200 teratas: metode'] = top.metode_pengadaan.value_counts(normalize=True).round(2).to_dict()
    prov = info.provinsi.loc[sk.index]
    peta = sk.anomali.groupby(prov).mean()
    return o, peta, sk


rows, md = [], ['# Uji tahun lain: model yang sama di data 2024', '']
for jalur in ['perencanaan', 'pelaksanaan']:
    (o25, p25, s25), (o24, p24, s24) = ukur('2025', jalur), ukur('2024', jalur)
    k = p25.index.intersection(p24.index)
    rho, pv = spearmanr(p25[k], p24[k])
    o24['peta: Spearman provinsi 2024 vs 2025'] = f'{rho:.2f} (p = {pv:.3f}, {len(k)} provinsi)'
    rows += [o25, o24]
    tab = pd.DataFrame([o25, o24]).set_index('tahun').T
    md += [f'## Jalur {jalur}', '', '| Ukuran | 2025 | 2024 |', '|---|---|---|']
    for idx, r in tab.iterrows():
        f = lambda v: f'{v:.1%}' if isinstance(v, float) and abs(v) <= 1 and 'lift' not in idx else (f'{v:.2f}' if isinstance(v, float) else str(v))
        md.append(f'| {idx} | {f(r["2025"])} | {f(r["2024"])} |')
    gab = pd.DataFrame({'2025': p25, '2024': p24}).sort_values('2025', ascending=False)
    md += ['', 'Proporsi paket tidak lazim per provinsi (10 teratas 2025):', '', '| Provinsi | 2025 | 2024 |', '|---|---|---|']
    md += [f'| {i} | {r["2025"]:.1%} | {r["2024"]:.1%} |' for i, r in gab.head(10).iterrows()]
    md.append('')
    print(tab.to_string()); print(f'peta rho {rho:.2f} p {pv:.3f}')
open('/mnt/project-files/model-v5-2024/banding_2024_2025.md', 'w').write('\n'.join(md))
