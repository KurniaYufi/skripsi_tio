"""Tahap 7: ablasi ensemble. Apakah ketiga model (IF, LOF, AE) memang perlu digabung?

1. Kombinasi model (rata-rata persentil): IF+LOF+AE, tiap pasangan, tiap model tunggal, serta aturan gabung lain
   (maksimum dan median), diukur dengan kesesuaian red flag (P@K, ambang 5%, provinsi pilih/uji).
2. Anomali buatan yang sama dengan tahap 5 (rng 7) untuk tiap kombinasi.
3. Keragaman antarmodel: korelasi skor dan irisan 5% teratas. Ensemble hanya berguna bila anggotanya berbeda.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ns = {}
src = open('/mnt/project-files/model-v4/s5_validasi.py').read().split('\nK_rows, rf_rows')[0]
exec(src, ns)  # memuat data, fungsi ukur() dan buat_sintetis() milik tahap 5 tanpa menjalankan ujinya
H, VAL, satker, info, DEV = ns['H'], ns['VAL'], ns['satker'], ns['info'], ns['DEV']
ukur, buat_sintetis, log = ns['ukur'], ns['buat_sintetis'], ns['log']

GABUNG = {
    'IF+LOF+AE (rata-rata, dipakai)': lambda P: (P['IF'] + P['LOF'] + P['AE']) / 3,
    'IF+LOF': lambda P: (P['IF'] + P['LOF']) / 2,
    'IF+AE': lambda P: (P['IF'] + P['AE']) / 2,
    'LOF+AE': lambda P: (P['LOF'] + P['AE']) / 2,
    'IF saja': lambda P: P['IF'],
    'LOF saja': lambda P: P['LOF'],
    'AE saja': lambda P: P['AE'],
    'IF+LOF+AE (maksimum)': lambda P: np.maximum(np.maximum(P['IF'], P['LOF']), P['AE']),
    'IF+LOF+AE (median)': lambda P: np.median(np.vstack([P['IF'], P['LOF'], P['AE']]), axis=0),
}
rows, srows, krows = [], [], []
for jalur in ['pelaksanaan', 'perencanaan']:
    h = H[jalur]
    F, m, R, pr = h['F'], h['model'], h['rf'], h['pct_rata']
    ada = R.any(axis=1)
    ada_t4 = R.drop(columns='rf4_penunjukan_langsung').any(axis=1)
    P = {k: pr[k].values for k in ['IF', 'LOF', 'AE']}
    skor = {nama: pd.Series(f(P), index=F.index) for nama, f in GABUNG.items()}
    for nama, s in skor.items():
        o = ukur(s, ada, ada_t4, R.sum(axis=1))
        rows.append({'jalur': jalur, 'gabungan': nama, **{k: o[k] for k in [
            'P@50', 'P@100', 'P@200', 'presisi_5persen', 'lift_5persen', 'pilih_5persen', 'uji_5persen',
            'tanpaRF4_5persen', 'acuan', 'acuan_pilih', 'acuan_uji', 'acuan_tanpaRF4', 'satker_maks_top200', 'auc_redflag']}})
    log(jalur, 'kombinasi selesai')

    # anomali buatan: data dan urutan acak sama dengan tahap 5
    sint = buat_sintetis(F, jalur, R, h['skor'].Ensemble, np.random.default_rng(7))
    thr = {nama: s.quantile(0.95) for nama, s in skor.items()}
    for tipe, Y in sint.items():
        PY = m.pct(Y)
        for nama, f in GABUNG.items():
            srows.append({'jalur': jalur, 'tipe': tipe, 'gabungan': nama, 'terdeteksi_5persen': (f(PY) >= thr[nama]).mean()})
    log(jalur, 'anomali buatan selesai')

    # keragaman antarmodel
    samp = np.random.default_rng(0).choice(len(F), min(50000, len(F)), replace=False)
    n5 = int(len(F) * 0.05)
    top = {k: set(pr[k].nlargest(n5).index) for k in ['IF', 'LOF', 'AE']}
    for a, b in [('IF', 'LOF'), ('IF', 'AE'), ('LOF', 'AE')]:
        krows.append({'jalur': jalur, 'pasangan': f'{a}-{b}', 'spearman_skor': spearmanr(pr[a].values[samp], pr[b].values[samp])[0],
                      'jaccard_5persen': len(top[a] & top[b]) / len(top[a] | top[b])})
    ens5 = skor['IF+LOF+AE (rata-rata, dipakai)'].nlargest(n5).index
    jml = sum(pd.Series(ens5.isin(list(top[k])), index=ens5).astype(int) for k in top)
    krows.append({'jalur': jalur, 'pasangan': 'anomali ensemble yang juga 5% teratas di: 0/1/2/3 model',
                  'persen_0': 100 * (jml == 0).mean(), 'persen_1': 100 * (jml == 1).mean(),
                  'persen_2': 100 * (jml == 2).mean(), 'persen_3': 100 * (jml == 3).mean()})

pd.DataFrame(rows).to_csv(VAL + 'v_ablasi.csv', index=False)
pd.DataFrame(srows).to_csv(VAL + 'v_ablasi_sintetis.csv', index=False)
pd.DataFrame(krows).to_csv(VAL + 'v_keragaman.csv', index=False)
pd.set_option('display.width', 220)
print(pd.DataFrame(rows).round(3).to_string())
print(pd.DataFrame(srows).pivot_table(index=['jalur', 'tipe'], columns='gabungan', values='terdeteksi_5persen').round(2).to_string())
print(pd.DataFrame(krows).round(3).to_string())
log('SELESAI')
