"""Perbandingan akhir v1 vs kandidat hasil eksplorasi, 3 seed, dengan rincian per red flag."""
import json
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v1/eksplorasi')
import exp2 as E  # noqa: E402

_fitur_asli = E.fitur


def fitur(jalur, extra=False, satker_level=True, pdn_umk=True, metode=False):
    if metode:  # v1: fitur asli lengkap dengan one-hot metode
        return (E.d['f_ren'] if jalur == 'perencanaan' else E.d['f_pel']).copy()
    return _fitur_asli(jalur, extra=extra, satker_level=satker_level, pdn_umk=pdn_umk)


E.fitur = fitur
H0 = E.H0
KAND = [
    ('v1 (awal)', 'perencanaan', dict(metode=True), 'std', H0, 'rata'),
    ('B: hasil aturan pilih', 'perencanaan', dict(extra=True, pdn_umk=False, satker_level=True), 'quantile',
     {'IF': (('max_samples', 2048),), 'LOF': (('k', 20),), 'AE': (('b', 3),)}, 'rata'),
    ('C: fitur paket saja', 'perencanaan', dict(extra=False, pdn_umk=False, satker_level=False), 'quantile', H0, 'rata'),
    ('v1 (awal)', 'pelaksanaan', dict(metode=True), 'std', H0, 'rata'),
    ('B: hasil aturan pilih', 'pelaksanaan', dict(extra=True, pdn_umk=True, satker_level=True), 'std', H0, 'rata'),
    ('C: fitur paket saja', 'pelaksanaan', dict(extra=False, pdn_umk=False, satker_level=False), 'std', H0, 'rata'),
]
rows = []
for label, jalur, fk, skala, hp, cara in KAND:
    fk = tuple(sorted(fk.items()))
    R = E.rf.loc[E.fitur(jalur, **dict(fk)).index, E.FL[jalur]]
    for sd in E.SEEDS:
        P = {m: E.skor(jalur, fk, skala, m, hp[m], sd) for m in ['IF', 'LOF', 'AE']}
        for nama, s in [('Ensemble', E.gabung(P, cara)), ('IF', P['IF']), ('LOF', P['LOF']), ('AE', P['AE'])]:
            mt = E.metrik(s, jalur)
            top = s.sort_values(ascending=False).index[:200]
            row = {'kandidat': label, 'jalur': jalur, 'seed': sd, 'model': nama,
                   'P@50': mt['P@50'], 'P@100': mt['P@100'], 'P@200': mt['P@200'], 'uji_rata': mt['uji_rata'],
                   'pilih_rata': mt['pilih_rata'], 'tanpaRF4': mt['rata_tanpaRF4'], 'lift1%': mt['lift_1persen'],
                   'satker_maks': mt['satker_maks_top200'], 'acuan': mt['acuan']}
            row.update({f'top200_{c}': R.loc[top, c].mean() for c in R})
            row.update({f'acuan_{c}': R[c].mean() for c in R})
            rows.append(row)
        print(label, jalur, sd, 'ens P@200', round(rows[-4]['P@200'], 3), flush=True)
    pd.DataFrame(rows).to_csv(E.OUT + 'hasil_banding.csv', index=False)
df = pd.DataFrame(rows)
g = df.groupby(['jalur', 'kandidat', 'model'], sort=False).mean(numeric_only=True).drop(columns='seed')
print(g.round(3).to_string())
