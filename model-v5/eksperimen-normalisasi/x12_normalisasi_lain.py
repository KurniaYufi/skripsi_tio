"""Banding cara normalisasi lain (5 seed): persentil (dipakai), min-max, skor-z, skor-z robust (median & MAD),
min-max setelah log, dan cara gabung maksimum persentil. Model, fitur, data = tahap2.pkl (audit v5)."""
import json
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5/'
E = O + 'eksperimen-normalisasi/'
info = pd.read_pickle(O + 'tahap1.pkl')['info']
RF = pd.read_pickle(O + 'red_flag_v5.pkl')
DEV = set(json.load(open('/mnt/project-files/model-v1/eksplorasi/provinsi_pilih.json')))
H = pd.read_pickle(O + 'tahap2.pkl')
M = ['IF', 'LOF', 'AE']
NORM = {
    'min-max': lambda s: (s - s.min()) / (s.max() - s.min()),
    'skor-z': lambda s: (s - s.mean()) / s.std(),
    'skor-z robust': lambda s: (s - np.median(s)) / (1.4826 * np.median(np.abs(s - np.median(s)))),
    'log lalu min-max': lambda s: (lambda t: (t - t.min()) / (t.max() - t.min()))(np.log(s - s.min() + 1e-9)),
}
rows, dom = [], []
for j in ['perencanaan', 'pelaksanaan']:
    h = H[j]
    m, F, flags = h['model'], h['F'], h['flags']
    X = m._potong(F.values.astype(float))
    raw = [e.raw(X) for e in m.m]
    pct = [e.pct(X) for e in m.m]
    parts = {'persentil (dipakai)': {k: np.mean([p[k] for p in pct], axis=0) for k in M}}
    for n, f in NORM.items():
        parts[n] = {k: np.mean([f(r[k]) for r in raw], axis=0) for k in M}
    var = {n: sum(p[k] for k in M) / 3 for n, p in parts.items()}
    var['maksimum persentil'] = np.max([parts['persentil (dipakai)'][k] for k in M], axis=0)
    for v, s in var.items():
        s = pd.Series(s, index=F.index)
        idx = s.sort_values(ascending=False).index
        n5 = int(len(idx) * .05)
        for semua in [True, False]:
            fl = flags if semua else [f for f in flags if f != 'rf2_pl_lewat_ambang']
            a = RF.loc[idx, fl].any(axis=1).values
            dev = info.provinsi.loc[idx].isin(DEV).values
            rows.append(dict(jalur=j, cara=v, red_flag='semua' if semua else 'tanpa RF2', P50=a[:50].mean(),
                             P200=a[:200].mean(), top5=a[:n5].mean(), uji5=a[~dev][:int((~dev).sum() * .05)].mean(),
                             acuan=a.mean(), acuan_uji=a[~dev].mean()))
        if v in parts:  # porsi sumbangan tiap model di 200 teratas (dibanding total)
            pos = F.index.get_indexer(s.nlargest(200).index)
            c = {k: parts[v][k][pos] - np.median(parts[v][k]) for k in M}
            tot = sum(np.abs(c[k]).mean() for k in M)
            dom.append(dict(jalur=j, cara=v, **{k: np.abs(c[k]).mean() / tot for k in M}))
R, D = pd.DataFrame(rows), pd.DataFrame(dom)
R.to_csv(E + 'banding_normalisasi_lain.csv', index=False)
D.to_csv(E + 'porsi_model_lain.csv', index=False)
pd.set_option('display.width', 250)
print(R.round(3).to_string())
print(D.round(3).to_string())
