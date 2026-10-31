"""Validasi v3, bagian 5: lembar telaah buta (opsional, diisi manusia).

Per jalur: 20 paket dari 200 teratas model (maks 2 paket per satker) + 20 paket acak dari 95% paket
lainnya, diacak urutannya. Penelaah menilai kewajaran tanpa tahu asal paket. Kunci disimpan terpisah.
Pakai: python3 r5_telaah_buta.py [folder model, bawaan model-v2]
"""
import sys
import numpy as np
import pandas as pd

MODEL = sys.argv[1] if len(sys.argv) > 1 else 'model-v2'
sys.path.insert(0, f'/mnt/project-files/{MODEL}')
import s2_model  # noqa: F401,E402  (kelas model untuk membuka pickle)

OUT = '/mnt/project-files/validasi-v3/telaah-buta/'
d = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')
info = d['info']
satker = info.provinsi + '|' + info.nama_satuan_kerja
h = pd.read_pickle(f'/mnt/project-files/{MODEL}/tahap2.pkl')
rng = np.random.default_rng(2026)
lembar, kunci = {}, []
for jalur in ['perencanaan', 'pelaksanaan']:
    s = h[jalur]['skor'].Ensemble.sort_values(ascending=False)
    top, hit = [], {}
    for k in s.index[:200]:
        if hit.get(satker[k], 0) < 2:
            top.append(k)
            hit[satker[k]] = hit.get(satker[k], 0) + 1
    pilih_top = list(rng.choice(top, 20, replace=False))
    sisa = s.index[int(len(s) * 0.05):]
    pilih_acak = list(rng.choice(sisa, 20, replace=False))
    semua = pilih_top + pilih_acak
    urut = rng.permutation(len(semua))
    kol = ['provinsi', 'nama_satuan_kerja', 'nama_paket', 'jenis', 'metode_pengadaan', 'pagu']
    if jalur == 'pelaksanaan':
        kol += ['realisasi', 'penyedia', 'sumber_transaksi', 'metode_realisasi']
    rows = []
    for no, i in enumerate(urut, 1):
        k = semua[i]
        r = {'ID': f'{jalur[:3].upper()}-{no:02d}', 'kode_rup': k, **info.loc[k, kol].to_dict(),
             'Penilaian (1 wajar / 2 ragu / 3 janggal)': '', 'Alasan singkat': ''}
        rows.append(r)
        kunci.append({'ID': r['ID'], 'jalur': jalur, 'kode_rup': k,
                      'kelompok': 'model' if i < 20 else 'acak', 'skor_ensemble': s[k]})
    lembar[jalur] = pd.DataFrame(rows)

import os  # noqa: E402
os.makedirs(OUT, exist_ok=True)
with pd.ExcelWriter(OUT + 'lembar-telaah-buta.xlsx') as w:
    pd.DataFrame({'Petunjuk': [
        'Nilai setiap paket tanpa mencari tahu skornya: 1 = wajar, 2 = ragu-ragu, 3 = janggal/perlu dicek.',
        'Boleh membuka RUP/SPSE/INAPROC untuk melihat detail paket (kode RUP tersedia).',
        'Isi kolom alasan dengan singkat, mis. "pagu terlalu besar untuk ATK" atau "wajar".',
        'Jangan membuka file kunci sebelum semua paket selesai dinilai.',
        'Bila ada penelaah kedua, gunakan salinan lembar ini yang terpisah.']}).to_excel(w, sheet_name='Petunjuk', index=False)
    for j, df in lembar.items():
        df.to_excel(w, sheet_name=j.capitalize(), index=False)
pd.DataFrame(kunci).to_csv(OUT + 'kunci-JANGAN-DIBUKA-dulu.csv', index=False)
print('ok', {j: len(df) for j, df in lembar.items()})
