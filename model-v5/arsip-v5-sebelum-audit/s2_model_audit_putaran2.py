"""Model v5 (2026-10-29): sama dengan v4, tetapi memakai data hasil pembersihan s1_data.py v5
(audit: audit-data.md). Model v4 (2026-10-29), turunan model v3 (2026-10-28): red flag v3, fitur hasil pemilihan, skor rata-rata 5 seed, lalu evaluasi Precision@K.

Perubahan dari v2 (alasan lengkap: /mnt/project-files/validasi-v3/ringkasan-validasi-v3.md):
- Red flag v3 (validasi-v3/r6_pilih_v3.py): RF1 untuk pekerjaan konstruksi memakai dua jendela, 180-200 jt
  (ambang lama) dan 360-400 jt (ambang Perpres 46/2025), karena 2025 tahun peralihan dan penumpukan paket
  masih terjadi di ambang lama. RF5 memakai definisi OCP R040: satu penyedia menerima > 40% nilai realisasi
  satker yang punya >= 5 paket. RF2, RF3, RF4, RF6 tetap.
- Skor = rata-rata 5 kali pelatihan dengan seed berbeda (Ensemble3) agar peringkat stabil.
- Fitur: pelaksanaan sama dengan v2; perencanaan tanpa profil metode satker (lihat KONF).

Perubahan v4 (2026-10-29, dipilih Tio; uji di /mnt/project-files/validasi-v3/pagu-kecil/hasil-pagu-kecil.md):
- Jalur perencanaan: paket berpagu < Rp1 jt tidak ikut model (lebih mirip salah isi data atau belanja sangat kecil).
- Jalur perencanaan: fitur pagu satu arah. Rasio pagu (sejenis, satker) dipotong di 0, jadi hanya pagu yang lebih
  besar dari biasanya yang menaikkan skor. Pemotongan ada di dalam model (ens3.Ensemble3). log_pagu tidak dipotong:
  versi yang ikut memotong log_pagu di median (hasilnya di arsip-BS/) setara di 5% teratas provinsi pilih, tetapi
  200 teratasnya lebih jarang ber-red flag dan kurang stabil (validasi-v3/pagu-kecil/u4_banding.csv).
- Jalur pelaksanaan tidak berubah dari v3.

Perubahan v5 lainnya (2026-10-29, eksperimen-satker-kecil/hasil-satker-kecil.md, diterapkan sementara atas permintaan Tio):
- Dua jalur: porsi_pagu_satker diganti log_rasio_pagu_rata_satker = log10(pagu / rata-rata pagu paket satker), satu arah,
  dan log_jumlah_paket_satker dibuang. Sebelumnya satker yang hanya punya 1-4 paket (porsi 100%, jumlah 1) menguasai
  puncak perencanaan; dengan fitur ini paket tunggal di satkernya bernilai wajar (1 kali rata-rata).

Data dan fitur dasar diambil dari tahap 1 model v5 (/mnt/project-files/model-v5/tahap1.pkl).
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
from ens3 import Ensemble3  # noqa: E402

V1 = '/mnt/project-files/model-v1/'
V3 = '/mnt/project-files/validasi-v3/'
OUT = '/mnt/project-files/model-v5/'
DATA = OUT  # v5: tahap1.pkl dan red_flag_v5.pkl dari s1_data.py (data dibersihkan)
FLAGS = {'perencanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung'],
         'pelaksanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung',
                         'rf5_penyedia_dominan', 'rf6_penyedia_serba_ada']}
# varian fitur: 'v2' = fitur model v2; N = tambah pagu dibanding paket bernama serupa; L = profil metode satker
# dihitung tanpa paket itu sendiri; E = profil metode satker (proporsi PL dan porsi e-purchasing) dibuang.
# Perencanaan memakai E: dengan profil metode satker, model mengangkat penunjukan langsung (RF4) lewat kebiasaan
# satker, bukan lewat ciri paketnya. Tanpa profil itu, 5% teratas lebih sering punya red flag lain di provinsi
# pilih dan provinsi uji (validasi-v3/r6c_lima_persen.py). Pelaksanaan tetap v2 (terbaik menurut aturan r6).
KONF = {
    'perencanaan': dict(varian='E', pdn_umk=False, batas_bawah=1e6,
                        model=dict(skala='std', if_max_samples=2048, lof_k=20, ae_b=2,
                                   satu_arah={'log_rasio_pagu_sejenis': 'nol', 'log_rasio_pagu_satker': 'nol',
                                              'log_rasio_pagu_nama_satker': 'nol'})),
    'pelaksanaan': dict(varian='v2', pdn_umk=True, model=dict(skala='std', if_max_samples='auto', lof_k=20, ae_b=3,
                                                              satu_arah={'log_rasio_pagu_sejenis': 'nol',
                                                                         'log_rasio_pagu_satker': 'nol',
                                                                         'log_rasio_pagu_nama_satker': 'nol'})),
}
# Audit fitur 2026-10-29 malam (permintaan Tio: "perhatikan setiap detail fitur"). Kolom akhir tiap jalur.
# Dibuang: one-hot jenis (jenis jarang dianggap aneh: 114 dari 200 teratas perencanaan Jasa Konsultansi, SHAP jenis
# terbesar di 152 paket; konteks jenis sudah ada di rasio pagu sejenis), one-hot sumber transaksi (Tender 2,6% jarang,
# dan sumber = wakil metode, padahal metode sengaja tidak dipakai), pdn/umk biner RUP (98%/96% bernilai 1, jadi yang 0
# otomatis aneh), ubah_metode (hanya 161 paket = 0,15%, satu kolom biner langka akan mengisi puncak; ini lebih cocok
# sebagai penanda seperti red flag), profil metode satker (proporsi PL dan porsi e-purchasing: korelasi -0,98 satu sama
# lain, dan jalur bocor ke RF1/RF3; di perencanaan sudah dibuang sejak v3), rasio pagu terhadap RATA-RATA satker
# (korelasi 0,87 dengan rasio terhadap MEDIAN satker; median dipilih karena paket besar ikut menaikkan rata-rata
# satkernya sendiri sehingga menutupi dirinya), selisih rasio realisasi sejenis (hampir sama dengan |rasio realisasi - 1|).
# Putaran audit kedua (setelah melihat isi peringkat atas, eksperimen-audit/ dan x8/x9/x10):
# - Perencanaan memakai penskalaan standar, bukan quantile: pada quantile, paket tepat Rp1 jt (nilai minimum, banyak
#   kembar) dipetakan ke ekor paling ekstrem sehingga 21 paket Rp1 jt masuk 200 teratas.
# - log_rasio_pagu_satker = pagu dibanding median paket satker dengan JENIS yang sama (kelompok < 4 paket -> 0).
#   Median seluruh satker jatuh sangat rendah di satker yang punya ratusan paket super kecil (makan-minum Rp50-300 rb),
#   sehingga semua paket normalnya terlihat 1.000 kali median (satu satker NTB 42 paket di 200 teratas).
# - kekurangan_pdn/umk dibuang lagi: nilai PDN/UMK 0 di realisasi menumpuk di "Pencatatan Non Tender" (18,5% / 42,9%
#   paket, Tender 0% / 10,6%), jadi lebih mencerminkan cara pencatatan daripada janji yang tidak ditepati.
# - Ditambah log_rasio_pagu_nama_satker = pagu dibanding median paket LAIN bernama sama di satker yang sama (minimal 2
#   paket lain, satu arah): pola paket A-B-C usulan Tio, konsisten dengan fitur pagu relatif lainnya.
# - log_pagu tetap dipakai: tanpa log_pagu, peringkat tidak lagi sejalan dengan red flag mana pun (eksperimen np).
KOLOM = {
    'perencanaan': ['log_pagu', 'log_rasio_pagu_sejenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_satker'],
    'pelaksanaan': ['log_pagu', 'log_rasio_pagu_sejenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_satker',
                    'rasio_realisasi', 'log_selisih_realisasi'],
}
NAMA_SATKER = OUT + 'eksperimen-nama-satker/fitur_nama_satker.pkl'  # dibuat x3_nama_satker.hitung_fitur


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
    sj = satker + '|' + info.jenis
    n_sj = sj.map(sj.value_counts())
    F['log_rasio_pagu_satker'] = np.where(n_sj.loc[F.index] >= 4,
                                          np.log10(info.pagu / info.pagu.groupby(sj).transform('median')).loc[F.index], 0.0)
    if not os.path.exists(NAMA_SATKER):
        from x3_nama_satker import hitung_fitur
        hitung_fitur(info).to_pickle(NAMA_SATKER)
    X = pd.read_pickle(NAMA_SATKER)
    F['log_rasio_pagu_nama_satker'] = X.log_rasio_pagu_nama_satker.loc[F.index].where(
        X.n_nama_lain.loc[F.index] >= 2, 0.0).fillna(0.0)
    F = F[KOLOM[jalur]]
    if KONF[jalur].get('batas_bawah'):
        F = F[info.pagu.loc[F.index] >= KONF[jalur]['batas_bawah']]
    return F

if os.environ.get('PEL_BATAS'):  # varian uji: jalur pelaksanaan juga tanpa pagu < Rp1 jt
    KONF['pelaksanaan']['batas_bawah'] = 1e6
    OUT = OUT + 'varian-pel1jt/'


def main():
    d = pd.read_pickle(DATA + 'tahap1.pkl')
    rf = pd.read_pickle(DATA + 'red_flag_v5.pkl')
    satker = d['info'].provinsi + '|' + d['info'].nama_satuan_kerja
    hasil = {}
    for jalur in ['pelaksanaan', 'perencanaan']:
        flags = FLAGS[jalur]
        F = fitur(d, jalur)
        m = Ensemble3(**KONF[jalur]['model']).fit(F)
        Ps = [mm.pct(m._potong(F.values.astype(float))) for mm in m.m]  # persentil tiap seed
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
