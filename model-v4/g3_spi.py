"""Gambar: proporsi paket tidak lazim per provinsi terhadap skor SPI KPK 2024 (data validasi/v_spi_provinsi.csv)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

OUT = '/mnt/project-files/model-v4/'
P = pd.read_csv(OUT + 'validasi/v_spi_provinsi.csv')
S = pd.read_csv(OUT + 'validasi/v_spi.csv')
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
WARNA = {'rentan': '#c2410c', 'terjaga': '#256abf'}
KOL = 'Proporsi paket anomali (5% teratas)'
plt.rcParams.update({'font.size': 9, 'text.color': INK, 'xtick.color': INK2, 'ytick.color': INK2, 'axes.edgecolor': GRID})
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=SURF)
for ax, jalur in zip(axs, ['perencanaan', 'pelaksanaan']):
    d = P[P.jalur == jalur]
    ax.set_facecolor(SURF)
    for kel, g in d.groupby('kelompok'):
        papua = g.provinsi.str.contains('Papua')
        ax.scatter(g.skor_spi_2024[~papua], 100 * g[KOL][~papua], s=46, color=WARNA[kel], edgecolor=SURF, lw=1.5, zorder=3,
                   label=f'10 SPI {"terendah" if kel == "rentan" else "tertinggi"}')
        ax.scatter(g.skor_spi_2024[papua], 100 * g[KOL][papua], s=46, facecolor=SURF, edgecolor=WARNA[kel], lw=1.6, zorder=3,
                   label='provinsi Papua' if kel == 'rentan' else None)
    for _, r in d.nlargest(3, KOL).iterrows():
        ax.annotate(r.provinsi, (r.skor_spi_2024, 100 * r[KOL]), xytext=(6, 0), textcoords='offset points', va='center',
                    fontsize=8, color=INK2)
    ax.axhline(5, color=INK2, lw=0.8, ls=(0, (3, 2)))
    ax.text(1, 5, 'rata-rata nasional 5% ', transform=ax.get_yaxis_transform(), ha='right', va='bottom', fontsize=8, color=INK2)
    s = S[(S.jalur == jalur) & (S.ukuran == KOL)].set_index('tanpa_papua')
    p1, p2 = s.loc[False].p_mannwhitney_rentan_lebih_tinggi, s.loc[True].p_mannwhitney_rentan_lebih_tinggi
    fp = (lambda p: 'p < 0,001' if p < 0.001 else f'p = {p:.3f}'.replace('.', ','))
    ax.set_title(f'Jalur {jalur}', loc='left', fontsize=10, color=INK, pad=18)
    ax.text(0, 1.01, f'beda kelompok: {fp(p1)}; tanpa Papua: {fp(p2)}', transform=ax.transAxes, fontsize=8, color=INK2, va='bottom')
    ax.set_xlabel('Skor SPI 2024 pemerintah provinsi (makin tinggi makin terjaga)')
    ax.set_ylabel('Paket tidak lazim (% paket provinsi)')
    ax.grid(axis='y', color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for sp in ['top', 'right']:
        ax.spines[sp].set_visible(False)
    ax.set_ylim(0, None)
axs[1].legend(frameon=False, fontsize=8, loc='upper right')
fig.text(0.01, 0.01, 'Sumber SPI: KPK (2025) untuk 10 tertinggi; GoodStats (2025), mengutip dasbor SPI KPK, untuk 10 terendah. '
         'Provinsi lain tidak diumumkan skornya.', fontsize=8, color=INK2)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(OUT + 'gambar-spi.png', dpi=200, facecolor=SURF)
print('ok')
