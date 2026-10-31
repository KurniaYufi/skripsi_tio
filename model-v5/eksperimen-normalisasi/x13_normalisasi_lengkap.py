"""Uji lengkap cara normalisasi, dengan kriteria yang ditetapkan SEBELUM melihat hasil (permintaan Tio: "jangan bias").
Kriteria (dua jalur, masing-masing):
  1. anomali buatan: rata-rata persen pola anomali yang masuk 5% teratas DIKURANGI persen paket kontrol (tidak pakai red flag)
  2. 5% teratas provinsi uji, semua red flag
  3. 5% teratas provinsi uji, tanpa RF2 (RF2 bocor lewat fitur sejenis)
  4. lift 5% teratas untuk red flag yang datanya tidak masuk fitur: RF4 (dan RF5 di pelaksanaan)
  5. kestabilan: rata-rata Jaccard 5% teratas antar-seed
  6. keseimbangan: porsi sumbangan model terbesar di 200 teratas (makin dekat 33% makin benar-benar ensemble)
Cara yang menang di paling banyak kriteria dianggap paling baik. Selisih kecil dibanding noise antar-seed dicatat."""
import itertools
import sys
import numpy as np
import pandas as pd

S5 = '/mnt/project-files/model-v5/s5_validasi.py'
src = open(S5).read()
exec(src[:src.index('K_rows, rf_rows')])  # definisi & data yang sama dengan s5 (buat_sintetis, info, AKTIF, H, ...)

E = '/mnt/project-files/model-v5/eksperimen-normalisasi/'
RFv = pd.read_pickle(DATA + 'red_flag_v5.pkl')
MD = ['IF', 'LOF', 'AE']


def n_pct(ref, s): return np.searchsorted(np.sort(ref), s, side='right') / len(ref)
def n_mm(ref, s): return (s - ref.min()) / (ref.max() - ref.min())
def n_z(ref, s): return (s - ref.mean()) / ref.std()
def n_rz(ref, s):
    md = np.median(ref)
    return (s - md) / (1.4826 * np.median(np.abs(ref - md)))
def n_logmm(ref, s):
    lo = ref.min()
    t = lambda v: np.log(np.maximum(v - lo, 0) + 1e-9)
    tr = t(ref)
    return (t(s) - tr.min()) / (tr.max() - tr.min())


NORM = {'persentil': n_pct, 'min-max': n_mm, 'skor-z': n_z, 'skor-z robust': n_rz, 'log lalu min-max': n_logmm}
rows, rinci = [], []
for jalur in ['perencanaan', 'pelaksanaan']:
    h = H[jalur]
    F, m, sk, R = h['F'], h['model'], h['skor'], h['rf']
    X = m._potong(F.values.astype(float))
    raw = [e.raw(X) for e in m.m]
    sint = buat_sintetis(F, jalur, R, sk.Ensemble, np.random.default_rng(7))
    raw_s = {t: [e.raw(m._potong(Y)) for e in m.m] for t, Y in sint.items()}
    idx_all = F.index
    dev = info.provinsi.loc[idx_all].isin(DEV).values
    flags = h['flags']
    cara = list(NORM) + ['maksimum persentil']
    for c in cara:
        f = NORM.get(c, n_pct)
        gab = (lambda P: np.max(P, axis=0)) if c == 'maksimum persentil' else (lambda P: np.mean(P, axis=0))
        per_seed = [gab([f(r[k], r[k]) for k in MD]) for r in raw]
        s = pd.Series(np.mean(per_seed, axis=0), index=idx_all)
        thr = s.quantile(0.95)
        # 1. anomali buatan
        det = {}
        for t in sint:
            v = np.mean([gab([f(raw[i][k], raw_s[t][i][k]) for k in MD]) for i in range(len(raw))], axis=0)
            det[t] = (v >= thr).mean()
        pola = [t for t in det if t != 'kontrol_normal']
        rinci += [dict(jalur=jalur, cara=c, pola=t, terdeteksi=det[t]) for t in det]
        # 2-4. red flag
        order = s.sort_values(ascending=False).index
        pos = idx_all.get_indexer(order)
        dv = dev[pos]
        def p5(cols, uji=True):
            a = RFv.loc[order, cols].any(axis=1).values
            a = a[~dv] if uji else a
            return a[:int(len(a) * .05)].mean(), a.mean()
        u_all, acu = p5(flags)
        u_tr2, acu2 = p5([x for x in flags if x != 'rf2_pl_lewat_ambang'])
        lifts = {}
        for rfn in ['rf4_penunjukan_langsung', 'rf5_penyedia_dominan']:
            if rfn in flags:
                a, b = p5([rfn], uji=False)
                lifts[rfn] = a / b
        # 5. kestabilan antar-seed
        n5 = int(len(idx_all) * .05)
        tops = [set(np.argsort(-x)[:n5]) for x in per_seed]
        jac = np.mean([len(a & b) / len(a | b) for a, b in itertools.combinations(tops, 2)])
        # 6. keseimbangan
        top = np.argsort(-s.values)[:200]
        if c == 'maksimum persentil':
            P = np.mean([[n_pct(r[k], r[k]) for k in MD] for r in raw], axis=0)
            menang = np.bincount(P[:, top].argmax(axis=0), minlength=3) / 200
            porsi = menang.max()
        else:
            parts = [np.mean([f(r[k], r[k]) for r in raw], axis=0) for k in MD]
            cc = [np.abs(p[top] - np.median(p)).mean() for p in parts]
            porsi = max(cc) / sum(cc)
        rows.append(dict(jalur=jalur, cara=c, buatan_selisih=np.mean([det[t] for t in pola]) - det['kontrol_normal'],
                         buatan_kontrol=det['kontrol_normal'], uji5=u_all, acuan_uji=acu, uji5_tanpa_rf2=u_tr2,
                         acuan_uji_tanpa_rf2=acu2, lift_rf4=lifts.get('rf4_penunjukan_langsung'),
                         lift_rf5=lifts.get('rf5_penyedia_dominan'), jaccard_seed=jac, porsi_model_terbesar=porsi))
        print(rows[-1], flush=True)
R_ = pd.DataFrame(rows)
R_.to_csv(E + 'banding_normalisasi_lengkap.csv', index=False)
pd.DataFrame(rinci).to_csv(E + 'banding_normalisasi_buatan.csv', index=False)
pd.set_option('display.width', 250)
print(R_.round(3).to_string())
print(pd.DataFrame(rinci).pivot_table(index=['jalur', 'pola'], columns='cara', values='terdeteksi').round(2).to_string())
