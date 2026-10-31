"""Model v2 (hasil eksplorasi 2026-10-28): fitur dan pengaturan per jalur, lalu evaluasi Precision@K.

Data, fitur dasar, dan red flag diambil dari tahap 1 model v1 (/mnt/project-files/model-v1/tahap1.pkl).
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v2')
from ens2 import Ensemble2  # noqa: E402

V1 = '/mnt/project-files/model-v1/'
OUT = '/mnt/project-files/model-v2/'
KONF = {
    'perencanaan': dict(pdn_umk=False, model=dict(skala='quantile', if_max_samples=2048, lof_k=20, ae_b=3)),
    'pelaksanaan': dict(pdn_umk=True, model=dict(skala='std', if_max_samples='auto', lof_k=20, ae_b=None)),
}


def fitur(d, jalur, pdn_umk):
    info = d['info']
    satker = info.provinsi + '|' + info.nama_satuan_kerja
    F = (d['f_ren'] if jalur == 'perencanaan' else d['f_pel']).copy()
    # One-hot metode dibuang: kategori penunjukan langsung = red flag 4
    F = F.drop(columns=[c for c in F if c.startswith('metode_')])
    F['log_rasio_pagu_satker'] = np.log10(info.pagu / info.pagu.groupby(satker).transform('median')).loc[F.index]
    F['porsi_epurchasing_satker'] = (info.metode_pengadaan == 'E-Purchasing').groupby(satker).transform('mean').loc[F.index]
    if jalur == 'pelaksanaan':
        r = F['rasio_realisasi']
        grp = (info.jenis + '|' + info.metode_pengadaan).loc[F.index]
        F['selisih_rasio_realisasi_sejenis'] = (r - r.groupby(grp).transform('median')).abs()
    if not pdn_umk:
        F = F.drop(columns=['pdn', 'umk'])
    return F


def main():
    d = pd.read_pickle(V1 + 'tahap1.pkl')
    rf = d['rf']
    hasil = {}
    for jalur, flags in [('perencanaan', ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket',
                                          'rf4_penunjukan_langsung']), ('pelaksanaan', list(rf.columns))]:
        F = fitur(d, jalur, KONF[jalur]['pdn_umk'])
        m = Ensemble2(**KONF[jalur]['model']).fit(F)
        sk = pd.DataFrame(m.pct(F.values.astype(float)), index=F.index)
        for c in ['IF', 'LOF', 'AE']:
            sk[c] = sk[c].rank(pct=True)
        sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
        sk['anomali'] = sk.Ensemble >= sk.Ensemble.quantile(0.95)
        R = rf.loc[F.index, flags]
        sk['jumlah_rf'] = R.sum(axis=1)
        ev = []
        for mdl in ['Ensemble', 'IF', 'LOF', 'AE']:
            order = sk[mdl].sort_values(ascending=False).index
            row = {'model': mdl}
            for K in [50, 100, 200]:
                top = sk.loc[order[:K], 'jumlah_rf']
                row[f'P@{K}'] = (top > 0).mean()
                row[f'rata_rf@{K}'] = top.mean()
            ev.append(row)
        ev.append({'model': 'Semua paket (acuan)', **{f'P@{K}': (sk.jumlah_rf > 0).mean() for K in [50, 100, 200]},
                   **{f'rata_rf@{K}': sk.jumlah_rf.mean() for K in [50, 100, 200]}})
        ev = pd.DataFrame(ev)
        print('\n==', jalur, F.shape, list(F.columns))
        print(ev.round(3).to_string(index=False))
        print('satker terbanyak di 200 teratas:', (d['info'].provinsi + '|' + d['info'].nama_satuan_kerja).loc[sk.Ensemble.nlargest(200).index].value_counts().iloc[0])
        hasil[jalur] = dict(model=m, skor=sk, eval=ev, flags=flags, F=F)
    pd.to_pickle(hasil, OUT + 'tahap2.pkl')


if __name__ == '__main__':
    main()
