"""Uji tambahan jalur perencanaan: penggabungan maks pada fitur paket saja, dan varian B tanpa fitur bauran metode satker."""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, '/mnt/project-files/model-v1/eksplorasi')
import exp2 as E  # noqa: E402

_asli = E.fitur


def fitur(jalur, extra=False, satker_level=True, pdn_umk=True, tanpa_bauran=False):
    F = _asli(jalur, extra=extra, satker_level=satker_level, pdn_umk=pdn_umk)
    if tanpa_bauran:  # porsi e-purchasing dan pengadaan langsung satker ikut "membocorkan" porsi penunjukan langsung
        F = F.drop(columns=[c for c in ['proporsi_pl_satker', 'porsi_epurchasing_satker'] if c in F])
    return F


E.fitur = fitur
H0 = E.H0
HB = {'IF': (('max_samples', 2048),), 'LOF': (('k', 20),), 'AE': (('b', 3),)}
KAND = [('C: fitur paket saja, gabung maks', dict(extra=False, pdn_umk=False, satker_level=False), 'quantile', H0, 'maks'),
        ('B2: B tanpa bauran metode satker', dict(extra=True, pdn_umk=False, satker_level=True, tanpa_bauran=True), 'quantile', HB, 'rata'),
        ('B2: B tanpa bauran metode satker, maks', dict(extra=True, pdn_umk=False, satker_level=True, tanpa_bauran=True), 'quantile', HB, 'maks')]
rows = []
jalur = 'perencanaan'
for label, fk, skala, hp, cara in KAND:
    fk = tuple(sorted(fk.items()))
    R = E.rf.loc[E.fitur(jalur, **dict(fk)).index, E.FL[jalur]]
    for sd in E.SEEDS:
        P = {m: E.skor(jalur, fk, skala, m, hp[m], sd) for m in ['IF', 'LOF', 'AE']}
        for nama, s in [('Ensemble', E.gabung(P, cara)), ('IF', P['IF']), ('LOF', P['LOF']), ('AE', P['AE'])]:
            mt = E.metrik(s, jalur)
            top = s.sort_values(ascending=False).index[:200]
            row = {'kandidat': label, 'jalur': jalur, 'seed': sd, 'model': nama, **{k: mt[k] for k in ['P@50', 'P@100', 'P@200', 'uji_rata', 'pilih_rata', 'rata_tanpaRF4', 'lift_1persen', 'satker_maks_top200']}}
            row.update({c: R.loc[top, c].mean() for c in R})
            rows.append(row)
        print(label, sd, flush=True)
df = pd.DataFrame(rows)
df.to_csv(E.OUT + 'hasil_banding2.csv', index=False)
pd.set_option('display.width', 300)
print(df.groupby(['kandidat', 'model'], sort=False).mean(numeric_only=True).drop(columns='seed').round(3).to_string())
