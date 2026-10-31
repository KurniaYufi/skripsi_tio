"""Banding cara menggabungkan skor: persentil (dipakai) vs min-max (tertulis di naskah, Pers. 2.9),
masing-masing 1 seed dan rata-rata 5 seed. Model, fitur, dan data sama dengan tahap2.pkl (audit v5)."""
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


def mm(s):
    return (s - s.min()) / (s.max() - s.min())


rows, dom = [], []
for j in ['perencanaan', 'pelaksanaan']:
    h = H[j]
    m, F, flags = h['model'], h['F'], h['flags']
    X = m._potong(F.values.astype(float))
    raw = [e.raw(X) for e in m.m]          # skor mentah tiap seed
    pct = [e.pct(X) for e in m.m]          # persentil tiap seed
    var = {
        'persentil, 5 seed (dipakai)': np.mean([sum(p[k] for k in M) / 3 for p in pct], axis=0),
        'persentil, 1 seed': sum(pct[0][k] for k in M) / 3,
        'min-max, 5 seed': np.mean([sum(mm(r[k]) for k in M) / 3 for r in raw], axis=0),
        'min-max, 1 seed (naskah)': sum(mm(raw[0][k]) for k in M) / 3,
    }
    seed_skor = {'persentil': [sum(p[k] for k in M) / 3 for p in pct],
                 'min-max': [sum(mm(r[k]) for k in M) / 3 for r in raw]}
    acuan_top = None
    for v, s in var.items():
        s = pd.Series(s, index=F.index)
        idx = s.sort_values(ascending=False).index
        n5 = int(len(idx) * .05)
        if acuan_top is None:
            acuan_top = set(idx[:n5])
        for semua in [True, False]:
            fl = flags if semua else [f for f in flags if f != 'rf2_pl_lewat_ambang']
            a = RF.loc[idx, fl].any(axis=1).values
            dev = info.provinsi.loc[idx].isin(DEV).values
            rows.append(dict(jalur=j, cara=v, red_flag='semua' if semua else 'tanpa RF2',
                             P50=a[:50].mean(), P100=a[:100].mean(), P200=a[:200].mean(), top5=a[:n5].mean(),
                             uji5=a[~dev][:int((~dev).sum() * .05)].mean(), acuan=a.mean(),
                             sama_5persen_dgn_dipakai=len(acuan_top & set(idx[:n5])) / n5))
        # model mana yang "menguasai" skor: rata-rata sumbangan tiap model di 200 teratas
        if 'min-max' in v:
            parts = {k: np.mean([mm(r[k]) for r in (raw if '5' in v else raw[:1])], axis=0) for k in M}
        else:
            parts = {k: np.mean([p[k] for p in (pct if '5' in v else pct[:1])], axis=0) for k in M}
        top = s.nlargest(200).index
        pos = F.index.get_indexer(top)
        for k in M:
            dom.append(dict(jalur=j, cara=v, model=k, rata_skor_200teratas=parts[k][pos].mean(),
                            median_skor_semua=np.median(parts[k])))
    # kestabilan antar-seed: irisan 5% teratas seed 42 dengan seed lain
    for c, ss in seed_skor.items():
        n5 = int(len(F) * .05)
        tops = [set(F.index[np.argsort(-x)[:n5]]) for x in ss]
        jac = [len(tops[0] & t) / len(tops[0] | t) for t in tops[1:]]
        rows.append(dict(jalur=j, cara=f'{c}: Jaccard 5% seed 42 vs seed lain', red_flag='-',
                         P50=min(jac), P100=np.mean(jac), P200=max(jac)))

R = pd.DataFrame(rows)
D = pd.DataFrame(dom)
R.to_csv(E + 'banding_normalisasi.csv', index=False)
D.to_csv(E + 'dominasi_model.csv', index=False)
pd.set_option('display.width', 250)
print(R.round(3).to_string())
print(D.round(3).to_string())
