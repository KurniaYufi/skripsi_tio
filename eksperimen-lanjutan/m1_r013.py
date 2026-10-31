"""M1 (2026-10-31, usulan Tio): red flag perencanaan R013 OCP "High use of non-competitive methods".
Definisi OCP: satker ditandai bila proporsi paket bermetode non-kompetitif >= pagar atas Q3 + 1,5 IQR (semua satker).
Non-kompetitif = Pengadaan Langsung + Penunjukan Langsung. Satker = provinsi + nama satker tanpa akhiran kode, >= 5 paket.
Varian label paket:
  A  paket PL/PenL di satker yang ditandai (berlaku: paket PL/PenL di satker >= 5 paket)
  B  semua paket di satker yang ditandai (berlaku: semua paket di satker >= 5 paket)
Dinilai pada skor model perencanaan sekarang (tanpa latih ulang). Juga dicek kebocoran (AUC simetris fitur vs label)."""
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from lib import muat, urut, DEV, OUT, RF2, PL, PENL
from j3_eval_rancangan import strata
sys.path.insert(0, '/mnt/project-files/model-v5')
from tambahan_sebelah import satker_dasar  # noqa: E402

LAMA = ['rf1_pl_dekat_ambang', 'rf3_pemecahan_paket', 'rf4_penunjukan_langsung']


def r013(i, ukuran='jumlah'):
    sk = satker_dasar(i)
    nk = i.metode_pengadaan.isin([PL, PENL])
    n = sk.map(sk.value_counts())
    if ukuran == 'jumlah':
        por = nk.groupby(sk).mean()
    else:
        por = (i.pagu * nk).groupby(sk).sum() / i.pagu.groupby(sk).sum()
    besar = sk.value_counts()[lambda s: s >= 5].index
    p = por.loc[besar]
    q1, q3 = p.quantile([.25, .75]); pagar = min(q3 + 1.5 * (q3 - q1), 1.0)
    tanda = sk.map(por).ge(pagar) & n.ge(5)
    return dict(A=tanda & nk, B=tanda, eA=n.ge(5) & nk, eB=n.ge(5), pagar=pagar, satker=int((p >= pagar).sum()), n_satker=len(p))


rows, bocor = [], []
for th in ['2024', '2025']:
    D = muat(th); H = D['H']['perencanaan']; P = H['pct_rata']
    s_all = (P.IF + P.LOF + P.AE) / 3
    i = D['info'].loc[s_all.index]; rf = D['rf'].loc[s_all.index]
    for uk in ['jumlah', 'nilai']:
        R = r013(i, uk)
        print(th, uk, 'pagar', round(R['pagar'], 3), 'satker ditandai', R['satker'], '/', R['n_satker'],
              'paket A', int(R['A'].sum()), 'B', int(R['B'].sum()), flush=True)
        F = H['F'].loc[s_all.index]
        for v in 'AB':
            e = R['e' + v]
            for c in F.columns:
                a = roc_auc_score(R[v][e], F.loc[e, c]); bocor.append(dict(tahun=th, ukuran=uk, varian=v, fitur=c, auc=max(a, 1 - a)))
        for prv in (['semua', 'uji'] if th == '2025' else ['semua']):
            for buang in [False, True]:
                s = s_all if prv == 'semua' else s_all[~i.provinsi.isin(DEV)]
                if buang:
                    s = s[~rf.loc[s.index, RF2]]
                o = urut(s); n5 = int(len(o) * .05); top = o[:n5]
                st = strata(i.loc[s.index]); w = st.loc[top].value_counts(normalize=True)
                for nama, Y in [('sekarang', rf.loc[s.index, LAMA]),
                                ('+ R013 A', rf.loc[s.index, LAMA].assign(r=R['A'].loc[s.index])),
                                ('+ R013 B', rf.loc[s.index, LAMA].assign(r=R['B'].loc[s.index])),
                                ('R013 A saja', R['A'].loc[s.index].to_frame()), ('R013 B saja', R['B'].loc[s.index].to_frame())]:
                    if nama == 'sekarang' and uk == 'nilai':
                        continue
                    y = Y.any(axis=1)
                    harap = (w * y.groupby(st).mean().reindex(w.index)).sum()
                    r = dict(tahun=th, provinsi=prv, buang_rf2=buang, ukuran=uk, set=nama, acuan=y.mean(),
                             **{f'P@{k}': y.loc[o[:k]].mean() for k in (50, 100, 200)},
                             lipat5=y.loc[top].mean() / y.mean(), lipat_terkontrol=y.loc[top].mean() / harap)
                    if 'saja' in nama:  # lipat di paket yang red flag-nya berlaku
                        e = R['e' + nama[5]].loc[s.index]; oe = urut(s[e]); ne = int(len(oe) * .05)
                        r['lipat5_berlaku'] = y.loc[oe[:ne]].mean() / y[e].mean()
                    rows.append(r)
df = pd.DataFrame(rows); df.to_csv(OUT + 'r013/m1_eval.csv', index=False)
bk = pd.DataFrame(bocor); bk.to_csv(OUT + 'r013/m1_bocor.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 20); pd.set_option('display.max_rows', 200)
print(bk.pivot_table(index=['ukuran', 'varian', 'fitur'], columns='tahun', values='auc').round(2))
print(df.round(3).to_string())
