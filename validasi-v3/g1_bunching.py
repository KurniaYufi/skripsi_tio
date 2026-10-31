"""Gambar penumpukan pagu di sekitar ambang pengadaan langsung (data r1_bunching.pkl)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

B = pd.read_pickle('/mnt/project-files/validasi-v3/r1_bunching.pkl')
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
BAR, LINE, BAND = '#2a78d6', '#eb6834', '#efeeea'
panel = [('Barang & Jasa Lainnya (200 jt)', 'Barang dan Jasa Lainnya, ambang Rp200 juta'),
         ('Pekerjaan Konstruksi (200 jt, aturan lama)', 'Pekerjaan Konstruksi, ambang lama Rp200 juta'),
         ('Pekerjaan Konstruksi (400 jt, aturan baru)', 'Pekerjaan Konstruksi, ambang baru Rp400 juta'),
         ('Jasa Konsultansi (100 jt)', 'Jasa Konsultansi, ambang Rp100 juta')]
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2, 'xtick.color': INK2,
                     'ytick.color': INK2, 'text.color': INK})
fig, axs = plt.subplots(2, 2, figsize=(10, 6.4), facecolor=SURF)
for ax, (key, judul) in zip(axs.flat, panel):
    b = B[(key, 'semua metode')]
    x = b['kanan'] * 100 - 0.5
    ax.set_facecolor(SURF)
    ax.axvspan(90, 100, color=BAND, zorder=0, lw=0)
    ax.bar(x, b['n'], width=0.82, color=BAR, zorder=2, label='Jumlah paket sebenarnya')
    ax.plot(x, b['pred'], color=LINE, lw=2, zorder=3, label='Perkiraan tanpa ambang')
    ax.axvline(100, color=INK2, lw=1, ls=(0, (3, 2)), zorder=4)
    ymax = max(b['n'].max(), b['pred'].max())
    ax.text(100.8, ymax * 0.96, 'ambang', color=INK2, fontsize=8, va='top')
    r = b['aktual_bawah'] / b['pred_bawah']
    rb = f'{r:.1f}'.replace('.', ',')
    ax.text(0.02, 0.97, f'90–100% ambang: {int(b["aktual_bawah"]):,} paket\nperkiraan tanpa ambang {b["pred_bawah"]:,.0f}'.replace(',', '.') + f' ({rb}×)',
            transform=ax.transAxes, va='top', fontsize=8, color=INK)
    ax.set_title(judul, fontsize=9.5, loc='left', color=INK, pad=6)
    ax.set_xlim(50, 150)
    ax.grid(axis='y', color=GRID, lw=0.6, zorder=1)
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_xlabel('Pagu sebagai % ambang (bin 1%)')
    ax.set_ylabel('Jumlah paket')
h, l = axs[0, 0].get_legend_handles_labels()
fig.legend(h, l, loc='lower center', ncol=2, frameon=False, fontsize=9)
fig.tight_layout(rect=(0, 0.05, 1, 1))
fig.savefig('/mnt/project-files/validasi-v3/gambar/penumpukan-ambang.png', dpi=200, facecolor=SURF)
print('ok')
