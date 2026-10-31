"""K4: nilai varian K3 dan red flag project sebelah.

Aturan pilih (DITETAPKAN SEBELUM melihat hasil, sama dengan eksperimen lanjutan):
  - Ukuran utama: lipat terkontrol pagu x metode dan lipat 5% berlaku, red flag sekarang tanpa RF2 (paket RF2 keluar dari daftar).
  - Varian disebut "lebih baik" bila di 2024 (tahun pengembangan) lipat terkontrol >= model sekarang + 0,05 DAN lipat 5% berlaku
    >= model sekarang, lalu dicek di 2025 semua dan 2025 provinsi uji (harus tetap >= model sekarang).
  - Fitur yang AUC simetrisnya >= 0,70 terhadap red flag di set penilai (k2_bocor.csv) ditandai "berisiko bocor".
Set red flag:
  'sekarang'          RF1, RF3, RF4 (+ RF5, RF6 pelaksanaan), tanpa RF2
  'sekarang + sebelah' ditambah red flag bersih project sebelah yang tidak bocor ke fitur model sekarang:
                       perencanaan P5, P6; pelaksanaan E3, E4, E5, E6 (P4 bocor ke log_pagu, AUC 0,99-1,00)
  'sebelah'           set penilai project sebelah sejauh bisa dihitung: perencanaan RF3 (= P1), P5, P6; pelaksanaan E3-E6
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import hypergeom
from lib import muat, urut, DEV, OUT, RF2
from j3_eval_rancangan import strata, berlaku as berlaku_lama
from k2_bocor import berlaku as berlaku_baru
from k1_fitur_sebelah import R

LAMA = {'perencanaan': ['rf1_pl_dekat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung'],
        'pelaksanaan': ['rf1_pl_dekat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung', 'rf5_penyedia_dominan',
                        'rf6_penyedia_serba_ada']}
BARU = {'perencanaan': ['P5_tidak_dicadangkan_umk', 'P6_bukan_pdn'],
        'pelaksanaan': ['E3_metode_berubah', 'E4_pdn_kurang', 'E5_umk_kurang', 'E6_penyedia_kuasai_satker']}
SEB = {'perencanaan': ['rf3_pemecahan_paket', 'P5_tidak_dicadangkan_umk', 'P6_bukan_pdn'],
       'pelaksanaan': ['E3_metode_berubah', 'E4_pdn_kurang', 'E5_umk_kurang', 'E6_penyedia_kuasai_satker']}


def berlaku(info, f):
    return berlaku_lama(info, f) if f.startswith('rf') else berlaku_baru(info, f)


def ukur(skor, Y, info):
    o = urut(skor)
    y = Y.any(axis=1).loc[skor.index]
    E = pd.concat([berlaku(info.loc[skor.index], f) for f in Y.columns], axis=1).any(axis=1)
    n = int(len(o) * .05); top = o[:n]
    r = {'P@100': y.loc[o[:100]].mean(), 'P@200': y.loc[o[:200]].mean(), 'acuan': y.mean(), 'lipat 5%': y.loc[top].mean() / y.mean()}
    oe = urut(skor[E]); ne = int(len(oe) * .05); x = int(y.loc[oe[:ne]].sum())
    r['lipat 5% berlaku'] = (x / ne) / y[E].mean()
    r['p berlaku'] = float(hypergeom.sf(x - 1, int(E.sum()), int(y[E].sum()), ne))
    st = strata(info.loc[skor.index]); w = st.loc[top].value_counts(normalize=True)
    harap = (w * y.groupby(st).mean().reindex(w.index)).sum()
    r['lipat terkontrol'] = y.loc[top].mean() / harap
    r['porsi PL+PenL di 200 teratas'] = info.loc[o[:200]].metode_pengadaan.isin(['Pengadaan Langsung', 'Penunjukan Langsung']).mean()
    r['pagu < Rp10 jt di 200 teratas'] = (info.loc[o[:200]].pagu < 1e7).mean()
    for f in Y.columns:
        e = berlaku(info.loc[skor.index], f)
        yy = Y.loc[e[e].index, f]
        if yy.sum() >= 20:
            oo = urut(skor[e]); nn = max(int(len(oo) * .05), 1)
            r[f] = Y.loc[oo[:nn], f].mean() / yy.mean()
    return r


def skor_semua(th, jalur):
    D = muat(th)
    P = D['H'][jalur]['pct_rata']
    S = {'Model sekarang': (P.IF + P.LOF + P.AE) / 3}
    pref = 'skor_' + ('ren' if jalur == 'perencanaan' else 'pel') + '_'
    for f in sorted(os.listdir(R)):
        if f.startswith(pref) and f.endswith(f'_{th}.pkl'):
            S['+ ' + f[len(pref):-9]] = pd.read_pickle(R + f).Ensemble
    b = OUT + f'skor/plus_bulat__{th}__{jalur}.pkl'
    if os.path.exists(b):
        x = pd.read_pickle(b); S['+ bulat'] = x[['IF', 'LOF', 'AE']].mean(axis=1)
    X = pd.read_pickle(R + f'fitur_{th}.pkl').loc[P.index]
    S['Tanpa model: acak'] = pd.Series(np.random.default_rng(0).random(len(P)), index=P.index)
    S['Tanpa model: aturan sebelah (z pagu sejenis)'] = X.k_z_sejenis.abs()
    if jalur == 'pelaksanaan':
        S['Tanpa model: aturan sebelah (jangkauan penyedia)'] = -X.k_jangkauan
    return S


if __name__ == '__main__':
    rows = []
    for th in ['2024', '2025']:
        D = muat(th); info = D['info']; rf = D['rf'].join(pd.read_pickle(R + f'rf_{th}.pkl'))
        for jalur in ['perencanaan', 'pelaksanaan']:
            for nama, s in skor_semua(th, jalur).items():
                for prv in (['semua', 'uji'] if th == '2025' else ['semua']):
                    ss = s if prv == 'semua' else s[~info.provinsi.loc[s.index].isin(DEV)]
                    s_l = ss[~rf.loc[ss.index, RF2]]
                    for set_nama, flags in [('sekarang', LAMA[jalur]), ('sekarang + sebelah', LAMA[jalur] + BARU[jalur]),
                                            ('sebelah', SEB[jalur])]:
                        r = ukur(s_l, rf.loc[s_l.index, flags], info)
                        rows.append({'tahun': th, 'jalur': jalur, 'provinsi': prv, 'skor': nama, 'red flag': set_nama, **r})
    df = pd.DataFrame(rows)
    df.to_csv(OUT + 'k4_eval.csv', index=False)
    pd.set_option('display.width', 300); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 400)
    for (j, rs), g in df.groupby(['jalur', 'red flag']):
        print(f'\n##### {j} | red flag {rs}')
        g = g.assign(kol=g.tahun + ' ' + g.provinsi)
        for v in ['lipat terkontrol', 'lipat 5% berlaku', 'P@200']:
            print('--', v)
            print(g.pivot_table(index='skor', columns='kol', values=v).round(3).to_string())
