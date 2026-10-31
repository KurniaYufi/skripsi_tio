"""Model v3 (2026-10-28): red flag v3, fitur hasil pemilihan, skor rata-rata 5 seed, lalu evaluasi Precision@K.

Perubahan dari v2 (alasan lengkap: /mnt/project-files/validasi-v3/ringkasan-validasi-v3.md):
- Red flag v3 (validasi-v3/r6_pilih_v3.py): RF1 untuk pekerjaan konstruksi memakai dua jendela, 180-200 jt
  (ambang lama) dan 360-400 jt (ambang Perpres 46/2025), karena 2025 tahun peralihan dan penumpukan paket
  masih terjadi di ambang lama. RF5 memakai definisi OCP R040: satu penyedia menerima > 40% nilai realisasi
  satker yang punya >= 5 paket. RF2, RF3, RF4, RF6 tetap.
- Skor = rata-rata 5 kali pelatihan dengan seed berbeda (Ensemble3) agar peringkat stabil.
- Fitur: pelaksanaan sama dengan v2; perencanaan tanpa profil metode satker (lihat KONF).

Data dan fitur dasar diambil dari tahap 1 model v1 (/mnt/project-files/model-v1/tahap1.pkl).
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v3')
from ens3 import Ensemble3  # noqa: E402

V1 = '/mnt/project-files/model-v1/'
V3 = '/mnt/project-files/validasi-v3/'
OUT = '/mnt/project-files/model-v3/'
FLAGS = {'perencanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung'],
         'pelaksanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung',
                         'rf5_penyedia_dominan', 'rf6_penyedia_serba_ada']}
# varian fitur: 'v2' = fitur model v2; N = tambah pagu dibanding paket bernama serupa; L = profil metode satker
# dihitung tanpa paket itu sendiri; E = profil metode satker (proporsi PL dan porsi e-purchasing) dibuang.
# Perencanaan memakai E: dengan profil metode satker, model mengangkat penunjukan langsung (RF4) lewat kebiasaan
# satker, bukan lewat ciri paketnya. Tanpa profil itu, 5% teratas lebih sering punya red flag lain di provinsi
# pilih dan provinsi uji (validasi-v3/r6c_lima_persen.py). Pelaksanaan tetap v2 (terbaik menurut aturan r6).
KONF = {
    'perencanaan': dict(varian='E', pdn_umk=False, model=dict(skala='quantile', if_max_samples=2048, lof_k=20, ae_b=3)),
    'pelaksanaan': dict(varian='v2', pdn_umk=True, model=dict(skala='std', if_max_samples='auto', lof_k=20, ae_b=None)),
}


def fitur(d, jalur):
    info = d['info']
    satker = info.provinsi + '|' + info.nama_satuan_kerja
    varian = KONF[jalur]['varian']
    F = (d['f_ren'] if jalur == 'perencanaan' else d['f_pel']).copy()
    # One-hot metode dibuang: kategori penunjukan langsung = red flag 4
    F = F.drop(columns=[c for c in F if c.startswith('metode_')])
    F['log_rasio_pagu_satker'] = np.log10(info.pagu / info.pagu.groupby(satker).transform('median')).loc[F.index]
    F['porsi_epurchasing_satker'] = (info.metode_pengadaan == 'E-Purchasing').groupby(satker).transform('mean').loc[F.index]
    if jalur == 'pelaksanaan':
        r = F['rasio_realisasi']
        grp = (info.jenis + '|' + info.metode_pengadaan).loc[F.index]
        F['selisih_rasio_realisasi_sejenis'] = (r - r.groupby(grp).transform('median')).abs()
    if not KONF[jalur]['pdn_umk']:
        F = F.drop(columns=['pdn', 'umk'])
    if 'N' in varian:
        F['log_rasio_pagu_nama_serupa'] = pd.read_pickle(V3 + 'fitur_nama_serupa.pkl')['log_rasio_pagu_nama_serupa'].loc[F.index]
    if 'L' in varian:
        n = info.groupby(satker).pagu.transform('size')
        for c, metode in [('proporsi_pl_satker', 'Pengadaan Langsung'), ('porsi_epurchasing_satker', 'E-Purchasing')]:
            sendiri = (info.metode_pengadaan == metode).astype(float)
            jumlah = sendiri.groupby(satker).transform('sum')
            F[c] = ((jumlah - sendiri) / (n - 1).clip(lower=1)).loc[F.index]
    if 'E' in varian:
        F = F.drop(columns=['proporsi_pl_satker', 'porsi_epurchasing_satker'])
    return F


def main():
    d = pd.read_pickle(V1 + 'tahap1.pkl')
    rf = pd.read_pickle(V3 + 'red_flag_v3.pkl')
    satker = d['info'].provinsi + '|' + d['info'].nama_satuan_kerja
    hasil = {}
    for jalur in ['pelaksanaan', 'perencanaan']:
        flags = FLAGS[jalur]
        F = fitur(d, jalur)
        m = Ensemble3(**KONF[jalur]['model']).fit(F)
        Ps = [mm.pct(F.values.astype(float)) for mm in m.m]  # persentil tiap seed
        per_seed = pd.DataFrame({sd: (p['IF'] + p['LOF'] + p['AE']) / 3 for sd, p in zip(m.seeds, Ps)}, index=F.index)
        sk = pd.DataFrame({k: np.mean([p[k] for p in Ps], axis=0) for k in ['IF', 'LOF', 'AE']}, index=F.index)
        sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)  # sama dengan m.score(F)
        pct_rata = sk[['IF', 'LOF', 'AE']].copy()  # persentil rata-rata seed sebelum diubah ke peringkat
        for c in ['IF', 'LOF', 'AE']:
            sk[c] = sk[c].rank(pct=True)
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
        print('\n==', jalur, F.shape, list(F.columns), flush=True)
        print(ev.round(3).to_string(index=False))
        print('satker terbanyak di 200 teratas:', satker.loc[sk.Ensemble.nlargest(200).index].value_counts().iloc[0], flush=True)
        hasil[jalur] = dict(model=m, skor=sk, eval=ev, flags=flags, F=F, rf=R, per_seed=per_seed, pct_rata=pct_rata)
    pd.to_pickle(hasil, OUT + 'tahap2.pkl')


if __name__ == '__main__':
    main()
