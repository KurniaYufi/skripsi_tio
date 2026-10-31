"""Diagram metodologi TA (format Masukan | Proses | Luaran, acuan TA Anas Ghifari).

Pemakaian: python3 flowchart_v2.py <folder_keluaran>
Menghasilkan dua gambar: bagian 1 dan bagian 2.
"""
import sys
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Rectangle, Circle, Polygon

plt.rcParams["font.family"] = "Liberation Sans"

OUT_DIR = sys.argv[1]

W = 9.1
X_IN, X_PROC, X_OUT = 1.1, 4.45, 7.95
GROUP_W, BOX_W, BOX_H = 4.2, 2.75, 0.46
ROW = 0.74            # jarak antarbaris proses
PARA_W, PARA_H, SKEW = 1.55, 0.95, 0.2
FS, FS_HEAD, FS_GROUP = 11, 12.5, 10.5
LW = 1.0
K = "black"


class Canvas:
    def __init__(self):
        self.items = []  # fungsi gambar ditunda sampai tinggi total diketahui

    def add(self, fn):
        self.items.append(fn)


def draw_part(build, fname):
    fig = plt.figure(figsize=(W, 30))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(0, W)

    def rect(cx, cy, text, w=BOX_W, h=BOX_H):
        ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc="white", ec=K, lw=LW, zorder=3))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=FS, zorder=4)
        return dict(cx=cx, cy=cy, top=cy + h / 2, bot=cy - h / 2, left=cx - w / 2, right=cx + w / 2)

    def circle(cx, cy, text, r=0.32, fs=FS):
        ax.add_patch(Circle((cx, cy), r, fc="white", ec=K, lw=LW, zorder=3))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, zorder=4)
        return dict(cx=cx, cy=cy, top=cy + r, bot=cy - r)

    def para(cx, cy, text):
        w, h, s = PARA_W, PARA_H, SKEW
        pts = [(cx - w / 2 - s / 2, cy - h / 2), (cx + w / 2 - s / 2, cy - h / 2),
               (cx + w / 2 + s / 2, cy + h / 2), (cx - w / 2 + s / 2, cy + h / 2)]
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=K, lw=LW, zorder=3))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=FS - 0.5, zorder=4, linespacing=1.2)
        return dict(cx=cx, cy=cy, left=cx - w / 2, right=cx + w / 2)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=2,
                    arrowprops=dict(arrowstyle="-|>", color=K, lw=LW, mutation_scale=11,
                                    shrinkA=0, shrinkB=0))

    def down(a, b):
        arrow(a["cx"], a["bot"], b["cx"], b["top"])

    def star(cx, cy, label, R=0.17, r=0.05):
        """Ikon bintang empat sudut (seperti ikon LLM pada TA Anas Ghifari)."""
        pts = []
        for i in range(8):
            ang = math.pi / 2 + i * math.pi / 4
            rr = R if i % 2 == 0 else r
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        ax.add_patch(Polygon(pts, closed=True, fc=K, ec=K, lw=0.5, zorder=3))
        ax.text(cx, cy - R - 0.11, label, ha="center", va="center", fontsize=FS - 1.5, zorder=4)

    def group(top, title, steps, inputs=(), output=None, actor=None):
        """Kelompok proses bergaris putus-putus. inputs: daftar (teks, indeks proses tujuan).
        actor: (indeks proses, label) untuk ikon alat bantu di sisi kiri proses tersebut."""
        h = 0.5 + len(steps) * ROW + 0.08
        bot = top - h
        ax.add_patch(Rectangle((X_PROC - GROUP_W / 2, bot), GROUP_W, h, fc="none", ec=K,
                               lw=0.9, ls=(0, (4, 3)), zorder=1))
        ax.text(X_PROC, top - 0.24, title, ha="center", va="center", fontsize=FS_GROUP, zorder=4)
        boxes = []
        y = top - 0.5 - ROW / 2 + 0.06
        for s in steps:
            boxes.append(rect(X_PROC, y, s))
            y -= ROW
        for a, b in zip(boxes, boxes[1:]):
            down(a, b)
        gl, gr = X_PROC - GROUP_W / 2, X_PROC + GROUP_W / 2
        if actor:
            idx, label = actor
            b = boxes[idx]
            sx = (gl + b["left"]) / 2
            star(sx, b["cy"] + 0.05, label)
            arrow(sx + 0.19, b["cy"], b["left"], b["cy"])
        # masukan: parallelogram di kolom kiri, panah ke tepi kiri kelompok
        if inputs:
            n = len(inputs)
            span = (n - 1) * (PARA_H + 0.25)
            mid = (top + bot) / 2
            for i, (text, idx) in enumerate(inputs):
                py = mid + span / 2 - i * (PARA_H + 0.25)
                p = para(X_IN, py, text)
                ty = boxes[idx]["cy"]
                xm = (p["right"] + gl) / 2
                if abs(py - ty) < 1e-6:
                    arrow(p["right"], py, gl, ty)
                else:
                    ax.plot([p["right"], xm, xm], [py, py, ty], color=K, lw=LW, zorder=2)
                    arrow(xm, ty, gl, ty)
        if output:
            oy = (top + bot) / 2
            p = para(X_OUT, oy, output)
            arrow(gr, oy, p["left"], oy)
        return dict(cx=X_PROC, top=top, bot=bot, boxes=boxes)

    y_end = build(ax, rect, circle, group, down, arrow)

    for x, t in ((X_IN, "MASUKAN"), (X_PROC, "PROSES"), (X_OUT, "LUARAN")):
        ax.text(x, -0.35, t, ha="center", va="center", fontsize=FS_HEAD, weight="bold")
    ax.set_ylim(y_end - 0.15, 0.05)
    fig.set_size_inches(W, 0.05 - (y_end - 0.15))
    fig.savefig(os.path.join(OUT_DIR, fname), dpi=300, facecolor="white")
    plt.close(fig)


GAP = 0.32


def part1(ax, rect, circle, group, down, arrow):
    start = circle(X_PROC, -1.05, "Mulai")
    idm = rect(X_PROC, start["bot"] - GAP - BOX_H / 2, "Identifikasi dan Perumusan Masalah")
    lit = rect(X_PROC, idm["bot"] - GAP - BOX_H / 2, "Studi Literatur")
    down(start, idm)
    down(idm, lit)
    g1 = group(lit["bot"] - GAP, "Pengumpulan dan Penyiapan Data",
               ["Pengumpulan Data", "Pra-pemrosesan Data", "Pembentukan Dataset per Jalur",
                "Rekayasa Fitur"],
               inputs=[("Data RUP dan\nRealisasi\nPengadaan", 0)],
               output="Dataset Fitur\nJalur Perencanaan\ndan Pelaksanaan")
    arrow(X_PROC, lit["bot"], X_PROC, g1["top"])
    g2 = group(g1["bot"] - GAP, "Pengembangan Model Ensemble",
               ["Pelatihan Model Individual", "Normalisasi Skor", "Penggabungan Skor",
                "Pemeringkatan Paket"],
               inputs=[("Dataset Fitur\nJalur Perencanaan\ndan Pelaksanaan", 0)],
               output="Skor Anomali\ndan Peringkat\nPaket")
    arrow(X_PROC, g1["bot"], X_PROC, g2["top"])
    con = circle(X_PROC, g2["bot"] - GAP - 0.26, "A", r=0.26)
    arrow(X_PROC, g2["bot"], X_PROC, con["top"])
    return con["bot"]


def part2(ax, rect, circle, group, down, arrow):
    con = circle(X_PROC, -0.95, "A", r=0.26)
    g3 = group(con["bot"] - GAP, "Evaluasi dan Interpretasi Model",
               ["Evaluasi Model", "Interpretasi Hasil Model", "Penyusunan Kalimat Penjelasan",
                "Verifikasi Kalimat Penjelasan", "Telaah Sampel Paket Prioritas"],
               inputs=[("Skor Anomali\ndan Peringkat\nPaket", 0), ("Indikator\nRed Flag", 0)],
               output="Hasil Evaluasi\ndan Kalimat\nPenjelasan",
               actor=(2, "LLM"))
    arrow(X_PROC, con["bot"], X_PROC, g3["top"])
    g4 = group(g3["bot"] - GAP, "Pengembangan Dashboard",
               ["Agregasi Hasil per Provinsi", "Perancangan Dashboard", "Implementasi Dashboard"],
               inputs=[("Peringkat Paket\ndan Kalimat\nPenjelasan", 0)],
               output="Dashboard\nPemeringkatan dan\nSebaran Anomali")
    arrow(X_PROC, g3["bot"], X_PROC, g4["top"])
    ana = rect(X_PROC, g4["bot"] - GAP - BOX_H / 2, "Analisis Hasil dan Pembahasan")
    arrow(X_PROC, g4["bot"], X_PROC, ana["top"])
    lap = rect(X_PROC, ana["bot"] - GAP - BOX_H / 2, "Penyusunan Laporan Tugas Akhir")
    down(ana, lap)
    end = circle(X_PROC, lap["bot"] - GAP - 0.32, "Selesai")
    down(lap, end)
    return end["bot"]


draw_part(part1, "gambar-3-1-metodologi-bagian-1.png")
draw_part(part2, "gambar-3-2-metodologi-bagian-2.png")
print("ok")
