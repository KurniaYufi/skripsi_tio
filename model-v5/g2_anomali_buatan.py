"""Gambar: persentase anomali buatan yang masuk 5% skor teratas, per tipe dan metode (data validasi/v_sintetis.csv)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

OUT = '/mnt/project-files/model-v5/'
S = pd.read_csv(OUT + 'validasi/v_sintetis.csv')
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
RAMP = ['#f1f6fd', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b']
METODE = [('Ensemble', 'Ensemble'), ('IF', 'IF'), ('LOF', 'LOF'), ('AE', 'AE'), ('Skor-z sederhana', 'Skor-z'),
          ('ECOD', 'ECOD'), ('HBOS', 'HBOS')]
TIPE = [('global', 'Ekstrem (global)'), ('lokal', 'Lokal'), ('dependensi', 'Gabungan antarfitur'),
        ('berkelompok', 'Kelompok kembar'), ('realisasi_lewat_pagu', 'Realisasi 1,3–3× pagu'),
        ('pagu_digelembungkan', 'Pagu 5–20× paket sejenis'), ('dekat_ambang', 'Dinaikkan ke dekat ambang PL'),
        ('kontrol_normal', 'Kontrol: paket wajar')]
cmap = matplotlib.colors.ListedColormap(RAMP)
plt.rcParams.update({'font.size': 9, 'text.color': INK, 'xtick.color': INK2, 'ytick.color': INK})
fig, axs = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=SURF)
for ax, jalur in zip(axs, ['perencanaan', 'pelaksanaan']):
    p = S[S.jalur == jalur].pivot(index='tipe', columns='metode', values='terdeteksi_5persen')
    tipe = [(k, v) for k, v in TIPE if k in p.index]
    M = np.array([[p.loc[k, m] for m, _ in METODE] for k, _ in tipe])
    ax.set_facecolor(SURF)
    ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect='auto')
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            ax.text(j, i, f'{100 * v:.0f}', ha='center', va='center', fontsize=8.5,
                    color='#ffffff' if v >= 0.55 else INK)
    ax.set_xticks(range(len(METODE)), [b for _, b in METODE])
    ax.set_yticks(range(len(tipe)), [b for _, b in tipe])
    ax.tick_params(length=0)
    ax.xaxis.tick_top()
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-.5, len(METODE)), minor=True)
    ax.set_yticks(np.arange(-.5, len(tipe)), minor=True)
    ax.grid(which='minor', color=SURF, lw=2)
    ax.tick_params(which='minor', length=0)
    ax.axhline(len(tipe) - 1.5, color=INK2, lw=0.8, ls=(0, (3, 2)))
    ax.set_title(f'Jalur {jalur}', loc='left', fontsize=10, pad=24, color=INK)
fig.text(0.01, 0.015, 'Angka = persentase 1.000 paket buatan yang masuk 5% skor teratas metode itu. '
         'Baris terakhir adalah paket wajar buatan (makin kecil makin baik).', fontsize=8.5, color=INK2)
fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.savefig(OUT + 'gambar-anomali-buatan.png', dpi=200, facecolor=SURF)
print('ok')
