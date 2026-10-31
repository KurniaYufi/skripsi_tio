"""H: telaah paket peringkat teratas 2025 (permintaan Tio: 'cek hasil peringkat paket2 nya ini bener ga bisa di posisi atas')."""
import numpy as np
import pandas as pd
from lib import muat, OUT

D = muat('2025')
S = pd.read_pickle('/mnt/project-files/model-v5/tahap3.pkl')
for jalur, n in [('perencanaan', 40), ('pelaksanaan', 40)]:
    h = D['H'][jalur]
    sk = h['skor'].Ensemble.sort_values(ascending=False)
    top = sk.index[:n]
    info, F, R = D['info'].loc[top], h['F'].loc[top], D['rf'].loc[top, h['flags']]
    t = pd.DataFrame({'peringkat': range(1, n + 1), 'provinsi': info.provinsi, 'satker': info.nama_satuan_kerja.str.slice(0, 45),
                      'nama_paket': info.nama_paket.str.slice(0, 70), 'jenis': info.jenis, 'metode': info.metode_pengadaan,
                      'pagu_jt': (info.pagu / 1e6).round(1),
                      'x_sejenis': (10 ** F.log_rasio_pagu_sejenis).round(1), 'x_satker': (10 ** F.log_rasio_pagu_satker).round(1)})
    if 'log_rasio_pagu_nama_satker' in F:
        t['x_nama_sama'] = (10 ** F.log_rasio_pagu_nama_satker).round(1)
    if 'rasio_realisasi' in F:
        t['realisasi_jt'] = (info.realisasi / 1e6).round(1)
        t['realisasi/pagu'] = F.rasio_realisasi.round(2)
    t['red_flag'] = R.apply(lambda r: ','.join(c[:3].upper() for c in R.columns if r[c]), axis=1)
    sv = S[jalur]['shap'].reindex(top)
    t['faktor_utama'] = sv.abs().idxmax(axis=1)
    t.to_csv(OUT + f'h_telaah_{jalur}.csv', index_label='kode_rup')
    pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 70)
    print(f'\n##### {jalur}'); print(t.to_string())
