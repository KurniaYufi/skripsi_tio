"""Tahap 6: uji kesetiaan SHAP (deletion test) pada model v3.

Untuk tiap paket di 200 teratas: nilai fitur teratas menurut SHAP diganti nilai paket latar (background),
lalu dilihat seberapa turun skornya, dibanding bila fitur yang dipilih acak yang diganti. Penjelasan yang
setia harus membuat skor turun jauh lebih besar.
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v3')
import s2_model  # noqa: F401,E402

OUT = os.environ.get('V3_OUT', '/mnt/project-files/model-v3/')  # bisa diganti untuk uji kode
GRUP = {'metode_': 'metode', 'jenis_': 'jenis', 'sumber_': 'sumber'}
h2 = pd.read_pickle(OUT + 'tahap2.pkl')
h3 = pd.read_pickle(OUT + 'tahap3.pkl')
rows = []
for jalur in ['perencanaan', 'pelaksanaan']:
    F, m = h2[jalur]['F'], h2[jalur]['model']
    sv = h3[jalur]['shap']
    grp = {}
    for c in F.columns:
        grp.setdefault(next((v for k, v in GRUP.items() if c.startswith(k)), c), []).append(list(F.columns).index(c))
    bg = F.sample(50, random_state=42).values.astype(float)
    rng = np.random.default_rng(5)
    hasil = []
    for kode in sv.index:
        x = F.loc[kode].values.astype(float)
        s0 = m.score(x[None, :])[0]
        urut = sv.loc[kode].sort_values(ascending=False)

        def hapus(gs):
            Y = np.repeat(x[None, :], len(bg), axis=0)
            for g in gs:
                Y[:, grp[g]] = bg[:, grp[g]]
            return s0 - m.score(Y).mean()

        top1, top3 = list(urut.index[:1]), list(urut.index[:3])
        lain = [g for g in sv.columns if g not in top3]
        acak1 = list(rng.choice([g for g in sv.columns if g not in top1], 1))
        acak3 = list(rng.choice(lain, min(3, len(lain)), replace=False))
        hasil.append({'turun_top1': hapus(top1), 'turun_acak1': hapus(acak1),
                      'turun_top3': hapus(top3), 'turun_acak3': hapus(acak3)})
    hs = pd.DataFrame(hasil)
    rows.append({'jalur': jalur, 'paket': len(hs),
                 'turun_top1_rata': hs.turun_top1.mean(), 'turun_acak1_rata': hs.turun_acak1.mean(),
                 'top1_lebih_besar_persen': 100 * (hs.turun_top1 > hs.turun_acak1).mean(),
                 'turun_top3_rata': hs.turun_top3.mean(), 'turun_acak3_rata': hs.turun_acak3.mean(),
                 'top3_lebih_besar_persen': 100 * (hs.turun_top3 > hs.turun_acak3).mean()})
    print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(OUT + 'validasi/v_shap_hapus.csv', index=False)
