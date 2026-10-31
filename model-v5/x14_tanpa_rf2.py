"""X14: RF2 (PL melebihi ambang) dihilangkan dari red flag penilai dan dashboard (permintaan Tio 2026-10-31: "hilangkan RF sekarang").
Alasan: RF2 = pagu > ambang PL, sehingga ikut terbaca dari fitur pagu (AUC 0,90) dan membuat Precision@K tampak tinggi.
Model TIDAK dilatih ulang: hanya flags, rf, jumlah_rf, dan eval di tahap2.pkl yang dihitung ulang. Paket ber-RF2 tetap ada
di daftar (hanya tidak dihitung sebagai red flag). Cadangan versi dengan RF2: arsip-dengan-rf2/.
"""
import pandas as pd
import s2_model  # noqa: F401  (kelas Ensemble3 untuk membuka pickle)

O = '/mnt/project-files/model-v5/'
RF2 = 'rf2_pl_lewat_ambang'
H = pd.read_pickle(O + 'tahap2.pkl')
for jalur, h in H.items():
    flags = [f for f in h['flags'] if f != RF2]
    R = h['rf'][flags]
    sk = h['skor']
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
    h.update(flags=flags, rf=R, skor=sk, eval=pd.DataFrame(ev))
    print('==', jalur, flags); print(h['eval'].round(3).to_string(index=False))
pd.to_pickle(H, O + 'tahap2.pkl')
