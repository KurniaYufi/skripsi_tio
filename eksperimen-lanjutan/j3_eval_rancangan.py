"""J3: bandingkan model RANCANGAN dengan model sekarang dan pembanding tanpa model, dengan dua set red flag:
  - 'lama tanpa RF2' : red flag model sekarang, paket RF2 dikeluarkan dari daftar (cara lapor eksperimen lanjutan)
  - 'rancangan'      : 7 red flag rancangan (perencanaan: RF1, RF3, RF4; pelaksanaan: + R050, RF6, R052*, Psl 38(8)*)
Ukuran: P@100, P@200, lipat 5% teratas (semua paket / paket yang red flag-nya berlaku), p hipergeometrik,
lipat terkontrol pagu (10 kelompok) x metode (PL / EP / lain).
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import hypergeom
from lib import muat, urut, DEV, OUT, RF2, PL, PENL

R = OUT + 'rancangan/'
PENYEDIA = ('r050_penyedia_dominan_satker_jenis', 'rf6_penyedia_serba_ada', 'r052_kecil_lalu_besar', 'rf5_penyedia_dominan')


def berlaku(info, f):
    m = info.metode_pengadaan
    if f in ('rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang', 'rf3_pemecahan_paket', 'psl38_pl_pencatatan'):
        return m == PL
    if f == 'rf4_penunjukan_langsung':
        return m == PENL
    return info.penyedia.fillna('-') != '-'


def strata(info):
    met = np.where(info.metode_pengadaan == PL, 'PL', np.where(info.metode_pengadaan == 'E-Purchasing', 'EP', 'lain'))
    q = pd.qcut(np.log10(info.pagu), 10, labels=False, duplicates='drop').astype(str)
    return pd.Series(q.values + met, index=info.index)


def ukur(skor, Y, info):
    o = urut(skor)
    y = Y.any(axis=1).loc[skor.index]
    E = pd.concat([berlaku(info, f) for f in Y.columns], axis=1).any(axis=1).loc[skor.index]
    n = int(len(o) * .05); top = o[:n]
    r = {'P@100': y.loc[o[:100]].mean(), 'P@200': y.loc[o[:200]].mean(), 'acuan': y.mean(),
         'lipat 5%': y.loc[top].mean() / y.mean()}
    oe = urut(skor[E]); ne = int(len(oe) * .05); x = int(y.loc[oe[:ne]].sum())
    r['lipat 5% berlaku'] = (x / ne) / y[E].mean()
    r['p berlaku'] = float(hypergeom.sf(x - 1, int(E.sum()), int(y[E].sum()), ne))
    st = strata(info.loc[skor.index]); w = st.loc[top].value_counts(normalize=True)
    harap = (w * y.groupby(st).mean().reindex(w.index)).sum()
    r['lipat terkontrol'] = y.loc[top].mean() / harap
    r['porsi 200 teratas berlaku'] = E.loc[o[:200]].mean()
    for f in Y.columns:
        e = berlaku(info, f).loc[skor.index]
        if Y.loc[e[e].index, f].sum() >= 20:
            oo = urut(skor[e]); nn = int(len(oo) * .05)
            r[f'{f}'] = Y.loc[oo[:nn], f].mean() / Y.loc[e[e].index, f].mean()
    return r


def skor_semua(th, jalur):
    D = muat(th)
    P = D['H'][jalur]['pct_rata']
    S = {'Model sekarang': (P.IF + P.LOF + P.AE) / 3}
    for f in sorted(os.listdir(R)):
        if f.startswith('skor_' + {'perencanaan': 'ren', 'pelaksanaan': 'pel'}[jalur]) and f.endswith(f'_{th}.pkl'):
            v = f[5:-4]
            S['Rancangan: ' + v.rsplit('_', 1)[0].split('_', 1)[1]] = pd.read_pickle(R + f).Ensemble
    F = pd.read_pickle(R + f'fitur_{th}_{jalur}.pkl')
    rng = np.random.default_rng(0)
    S['Tanpa model: acak'] = pd.Series(rng.random(len(F)), index=F.index)
    S['Tanpa model: urut pagu'] = F.log_pagu
    S['Tanpa model: pagu dibanding jenis'] = F.log_rasio_pagu_jenis
    Z = (F - F.mean()) / F.std()
    S['Tanpa model: rata skor-z fitur rancangan'] = Z.clip(lower=0).mean(axis=1)
    return S


if __name__ == '__main__':
    rows = []
    for th in ['2024', '2025']:
        D = muat(th); info = D['info']; rf = D['rf']
        Yr = pd.read_pickle(R + f'rf_{th}.pkl')
        for jalur in ['perencanaan', 'pelaksanaan']:
            S = skor_semua(th, jalur)
            lama = [f for f in D['H'][jalur]['flags'] if f != RF2]
            baru = ['rf1_pl_dekat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung'] if jalur == 'perencanaan' else list(Yr.columns)
            for nama, s in S.items():
                for prv in (['semua', 'uji'] if th == '2025' else ['semua']):
                    ss = s if prv == 'semua' else s[~info.provinsi.loc[s.index].isin(DEV)]
                    s_l = ss[~rf.loc[ss.index, RF2]]
                    for set_nama, sc, Y in [('lama tanpa RF2', s_l, rf[lama]), ('rancangan', ss, Yr[baru])]:
                        r = ukur(sc, Y, info)
                        rows.append({'tahun': th, 'jalur': jalur, 'provinsi': prv, 'skor': nama, 'red flag': set_nama, **r})
    df = pd.DataFrame(rows)
    df.to_csv(R + 'j3_eval.csv', index=False)
    pd.set_option('display.width', 300); pd.set_option('display.max_columns', 40)
    for (j, rs), g in df.groupby(['jalur', 'red flag']):
        print(f'\n##### {j} | red flag {rs}')
        g = g.assign(kol=g.tahun + ' ' + g.provinsi)
        for v in ['lipat 5% berlaku', 'lipat terkontrol', 'P@200', 'p berlaku']:
            print('--', v)
            print(g.pivot_table(index='skor', columns='kol', values=v).round(3).to_string())
