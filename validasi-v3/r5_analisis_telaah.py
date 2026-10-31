"""Hitung hasil telaah buta setelah lembar diisi.

Pakai: python3 r5_analisis_telaah.py lembar-penelaah1.xlsx [lembar-penelaah2.xlsx]
Uji: proporsi "janggal" (nilai 3) pada paket pilihan model vs paket acak (uji eksak Fisher, satu arah);
bila ada dua penelaah, kesepakatan antarpenelaah (kappa Cohen berbobot).
"""
import sys
import pandas as pd
from scipy.stats import fisher_exact
from sklearn.metrics import cohen_kappa_score

D = '/mnt/project-files/validasi-v3/telaah-buta/'
KOL = 'Penilaian (1 wajar / 2 ragu / 3 janggal)'
kunci = pd.read_csv(D + 'kunci-JANGAN-DIBUKA-dulu.csv')


def baca(path):
    x = pd.concat([pd.read_excel(path, sheet_name=s) for s in ['Perencanaan', 'Pelaksanaan']])
    return x[['ID', KOL]].merge(kunci, on='ID')


nilai = [baca(p) for p in sys.argv[1:]]
for jalur in ['perencanaan', 'pelaksanaan', 'semua']:
    x = nilai[0] if jalur == 'semua' else nilai[0][nilai[0].jalur == jalur]
    jg = x[KOL] == 3
    a, b = jg[x.kelompok == 'model'].sum(), (~jg)[x.kelompok == 'model'].sum()
    c, e = jg[x.kelompok == 'acak'].sum(), (~jg)[x.kelompok == 'acak'].sum()
    p = fisher_exact([[a, b], [c, e]], alternative='greater').pvalue
    print(f'{jalur}: janggal model {a}/{a + b}, acak {c}/{c + e}, p = {p:.4f}')
if len(nilai) == 2:
    m = nilai[0].merge(nilai[1], on='ID', suffixes=('_1', '_2'))
    print('kappa berbobot:', round(cohen_kappa_score(m[KOL + '_1'], m[KOL + '_2'], weights='linear'), 3))
