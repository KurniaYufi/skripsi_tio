"""J1: fitur dan red flag RANCANGAN DARI NOL (rancangan-dari-nol.md, permintaan Tio 2026-10-30 "coba experiment rancangan kamu").
Keluaran: rancangan/fitur_{th}_{jalur}.pkl dan rancangan/rf_{th}.pkl.

Fitur perencanaan: log_pagu, rasio pagu sejenis (JENIS saja), rasio pagu satker x jenis, rasio pagu nama di satker,
  rasio pagu thd paket bernama sama di satker tahun lalu*, lonjakan pagu satker x jenis thd tahun lalu*,
  kekaburan nama (log jumlah satker se-nasional yang memakai nama itu), label UMK tidak dipakai (paket <= Rp15 M bukan UMK).
Fitur pelaksanaan: log_pagu, sejenis (jenis saja), satker x jenis, rasio realisasi, selisih realisasi, selisih PDN, selisih UMK.
(* hanya 2025, karena butuh data tahun sebelumnya)
Red flag rancangan: RF1, RF3, RF4 (lama), R050 penyedia > 40% satker x jenis, RF6 serba-ada, R052 kecil-lalu-besar*,
  Psl 38(8) PL > Rp50 jt lewat Pencatatan*. RF2 (PL lewat ambang) TIDAK dipakai sebagai penguji.
"""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, '/mnt/project-files/model-v5')
from x3_nama_satker import nama_dasar  # noqa: E402
from lib import muat, OUT  # noqa: E402
from i_kandidat_rf import satker_dasar, T1  # noqa: E402

R = OUT + 'rancangan/'


def log_rasio(a, b):
    return np.log10(a / b).replace([np.inf, -np.inf], np.nan)


def fitur(th):
    D = muat(th); info = D['info']
    nd = info.nama_paket.map(nama_dasar)
    sk = satker_dasar(info)
    X = pd.DataFrame(index=info.index)
    X['log_pagu'] = np.log10(info.pagu)
    X['log_rasio_pagu_jenis'] = log_rasio(info.pagu, info.groupby('jenis').pagu.transform('median'))
    n_satker_nama = nd.map(pd.Series(sk.values, index=nd.values).groupby(level=0).nunique())
    X['log_kekaburan_nama'] = np.log10(n_satker_nama)
    X['umk_tidak_dicadangkan'] = ((info.pagu <= 15e9) & (info.status_umk != 'Ya')).astype(float)
    if th == '2025':
        i0 = muat('2024')['info']
        # Pembanding tahun lalu: hanya paket 2024 berpagu >= Rp1 jt (batas model) dan bernama SPESIFIK (dipakai <= 50
        # satker), pelajaran fitur nama v5. Versi pertama tanpa batas ini terdongkrak paket 2024 berpagu Rp10-50 rb
        # ("Bahan Cetak" Maluku: 2025 Rp10 jt vs 2024 Rp20 rb = 500x).
        nd0 = i0.nama_paket.map(nama_dasar); sk0 = satker_dasar(i0)
        n_sat0 = nd0.map(pd.Series(sk0.values, index=nd0.values).groupby(level=0).nunique())
        ok0 = (i0.pagu >= 1e6) & (n_sat0 <= 50)
        k0 = (sk0 + '||' + nd0)[ok0]
        med0 = i0.pagu[ok0].groupby(k0).median()
        X['log_rasio_pagu_tahun_lalu'] = log_rasio(info.pagu, (sk + '||' + nd).map(med0)).fillna(0.0)
        X['ada_tahun_lalu'] = (sk + '||' + nd).isin(med0.index)
        sj0 = i0.pagu.groupby(satker_dasar(i0) + '|' + i0.jenis).sum()
        sj = sk + '|' + info.jenis
        tot = info.pagu.groupby(sj).transform('sum')
        X['log_lonjakan_satker'] = log_rasio(tot, sj.map(sj0)).fillna(0.0)
        X['satker_ada_tahun_lalu'] = sj.isin(sj0.index)
    out = {}
    for j in ['perencanaan', 'pelaksanaan']:
        F0 = D['H'][j]['F']
        F = pd.DataFrame(index=F0.index)
        F['log_pagu'] = F0.log_pagu
        F['log_rasio_pagu_jenis'] = X.log_rasio_pagu_jenis.loc[F.index]
        F['log_rasio_pagu_satker'] = F0.log_rasio_pagu_satker
        if j == 'perencanaan':
            F['log_rasio_pagu_nama_satker'] = F0.log_rasio_pagu_nama_satker
            if th == '2025':
                F['log_rasio_pagu_tahun_lalu'] = X.log_rasio_pagu_tahun_lalu.loc[F.index]
                F['log_lonjakan_satker'] = X.log_lonjakan_satker.loc[F.index]
            F['log_kekaburan_nama'] = X.log_kekaburan_nama.loc[F.index]
            F['umk_tidak_dicadangkan'] = X.umk_tidak_dicadangkan.loc[F.index]
        else:
            fp = pd.read_pickle(T1[th])['f_pel'].loc[F.index]
            inf = info.loc[F.index]
            catat = inf.sumber_transaksi == 'Pencatatan Non Tender'
            F['rasio_realisasi'] = F0.rasio_realisasi
            F['log_selisih_realisasi'] = F0.log_selisih_realisasi
            F['selisih_pdn'] = np.where(catat, 0.0, (inf.produk_dalam_negeri == 'Ya') * (1 - fp.porsi_pdn.fillna(1)))
            F['selisih_umk'] = np.where(catat, 0.0, (inf.status_umk == 'Ya') * (1 - fp.porsi_umk.fillna(1)))
        out[j] = F
        F.to_pickle(R + f'fitur_{th}_{j}.pkl')
    return X, out


def red_flag(th):
    D = muat(th); rf = D['rf']
    K = pd.read_pickle(OUT + f'kandidat_rf_{th}.pkl')
    Y = pd.DataFrame(index=rf.index)
    Y['rf1_pl_dekat_ambang'] = rf.rf1_pl_dekat_ambang
    Y['rf3_pemecahan_paket'] = rf.rf3_pemecahan_paket
    Y['rf4_penunjukan_langsung'] = rf.rf4_penunjukan_langsung
    Y['r050_penyedia_dominan_satker_jenis'] = K.C4_R050_pangsa_satker_jenis.reindex(rf.index).fillna(False)
    Y['rf6_penyedia_serba_ada'] = rf.rf6_penyedia_serba_ada
    if th == '2025':
        Y['r052_kecil_lalu_besar'] = K.C2_R052_kecil_lalu_besar.reindex(rf.index).fillna(False)
        Y['psl38_pl_pencatatan'] = K.C3_psl38_pl_pencatatan.reindex(rf.index).fillna(False)
    Y = Y.astype(bool)
    Y.to_pickle(R + f'rf_{th}.pkl')
    return Y


if __name__ == '__main__':
    pd.set_option('display.width', 250)
    for th in ['2024', '2025']:
        X, out = fitur(th)
        Y = red_flag(th)
        print('=====', th)
        if th == '2025':
            print('paket punya pembanding nama tahun lalu:', X.ada_tahun_lalu.mean().round(3),
                  '| satker x jenis ada tahun lalu:', X.satker_ada_tahun_lalu.mean().round(3))
        for j, F in out.items():
            print('--', j, F.shape)
            print(F.describe(percentiles=[.5, .9, .99]).T.round(3).to_string())
            print('porsi nilai 0:', (F == 0).mean().round(3).to_dict())
        print('red flag (porsi):', Y.mean().round(4).to_dict())
