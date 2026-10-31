"""K2: tabel kebocoran ala project sebelah. Untuk setiap fitur (model sekarang + kandidat) x red flag (sekarang + kandidat):
AUC satu fitur menebak red flag, dihitung hanya di paket yang red flag itu bisa berlaku. AUC simetris = max(AUC, 1 - AUC),
karena model anomali menandai ekor mana pun. >= 0,85 = bocor, 0,70-0,85 = batas (ambang yang dipakai project sebelah).
Fitur satu arah model sekarang dihitung setelah dipotong di 0, seperti yang dilihat model."""
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from lib import muat, OUT, PL, PENL
from k1_fitur_sebelah import R

SATU_ARAH = ['log_rasio_pagu_sejenis', 'log_rasio_pagu_satker', 'log_rasio_pagu_nama_satker']
FLAG = {'perencanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung',
                        'P4_penl_lewat_ambang', 'P5_tidak_dicadangkan_umk', 'P6_bukan_pdn'],
        'pelaksanaan': ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung',
                        'rf5_penyedia_dominan', 'rf6_penyedia_serba_ada', 'E3_metode_berubah', 'E4_pdn_kurang',
                        'E5_umk_kurang', 'E6_penyedia_kuasai_satker', 'C4_R050_satker_jenis']}
KAND = {'perencanaan': ['k_pangsa_satker', 'k_kembar_satker', 'k_bulat', 'k_nonkomp_satker', 'k_z_sejenis', 'k_z_satker'],
        'pelaksanaan': ['k_pangsa_satker', 'k_kembar_satker', 'k_bulat', 'k_nonkomp_satker', 'k_z_sejenis', 'k_z_satker',
                        'k_z_rasio', 'k_jangkauan', 'k_kebiasaan']}


def berlaku(i, f):
    m = i.metode_pengadaan
    if f in ('rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket'):
        return m == PL
    if f in ('rf4_penunjukan_langsung',):
        return pd.Series(True, index=i.index)  # RF4 = metode itu sendiri; dinilai di semua paket
    if f == 'P4_penl_lewat_ambang':
        return m == PENL
    if f == 'P5_tidak_dicadangkan_umk':
        return i.jenis.isin(['Barang', 'Pekerjaan Konstruksi', 'Jasa Lainnya']) & (i.pagu <= 15e9)
    if f == 'E4_pdn_kurang':
        return i.produk_dalam_negeri == 'Ya'
    if f == 'E5_umk_kurang':
        return i.status_umk == 'Ya'
    if f in ('rf5_penyedia_dominan', 'rf6_penyedia_serba_ada', 'E6_penyedia_kuasai_satker', 'C4_R050_satker_jenis'):
        return i.penyedia.fillna('-') != '-'
    return pd.Series(True, index=i.index)


if __name__ == '__main__':
    rows = []
    for th in ['2024', '2025']:
        D = muat(th); X = pd.read_pickle(R + f'fitur_{th}.pkl'); Yk = pd.read_pickle(R + f'rf_{th}.pkl')
        Y = D['rf'].join(Yk)
        for j in ['perencanaan', 'pelaksanaan']:
            F = D['H'][j]['F'].copy()
            for c in SATU_ARAH:
                if c in F:
                    F[c] = F[c].clip(lower=0)
            F = F.join(X.loc[F.index, KAND[j]])
            i = D['info'].loc[F.index]
            for f in FLAG[j]:
                e = berlaku(i, f)
                y = Y.loc[F.index, f][e].astype(bool)
                if y.sum() < 20 or y.all():
                    continue
                for c in F:
                    a = roc_auc_score(y, F.loc[e[e].index, c])
                    rows.append({'tahun': th, 'jalur': j, 'red flag': f, 'fitur': c, 'AUC': a, 'AUC simetris': max(a, 1 - a),
                                 'kandidat': c.startswith('k_'), 'n kena': int(y.sum()), 'n berlaku': int(e.sum())})
    df = pd.DataFrame(rows)
    df.to_csv(OUT + 'k2_bocor.csv', index=False)
    pd.set_option('display.width', 300); pd.set_option('display.max_columns', 30)
    for (th, j), g in df.groupby(['tahun', 'jalur']):
        print(f'\n##### {th} {j} (AUC simetris)')
        print(g.pivot_table(index='fitur', columns='red flag', values='AUC simetris').round(2).to_string())
