"""Diagram alir per proses Bab 3 (gaya Gambar 3.11 dst. pada TA Anas Ghifari).

Pemakaian: python3 gambar-3-diagram-alir.py <folder_keluaran>
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch

plt.rcParams["font.family"] = "Liberation Sans"
OUT = sys.argv[1]
FS, LW, K = 10.5, 1.0, "black"
BW, BH = 3.3, 0.5          # kotak proses
GAP = 0.32


class Chart:
    def __init__(self, width=8.0):
        self.fig = plt.figure(figsize=(width, 30))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.axis("off")
        self.W = width
        self.ax.set_xlim(0, width)
        self.lowest = 0

    def _track(self, y):
        self.lowest = min(self.lowest, y)

    def arrow(self, x0, y0, x1, y1):
        self.ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=2,
                         arrowprops=dict(arrowstyle="-|>", color=K, lw=LW, mutation_scale=10,
                                         shrinkA=0, shrinkB=0))

    def line(self, xs, ys):
        self.ax.plot(xs, ys, color=K, lw=LW, zorder=2)

    def term(self, cx, top, text):
        w, h = 1.5, 0.46
        self.ax.add_patch(FancyBboxPatch((cx - w / 2, top - h), w, h, boxstyle="round,pad=0,rounding_size=0.23",
                                         fc="white", ec=K, lw=LW, zorder=3))
        self.ax.text(cx, top - h / 2, text, ha="center", va="center", fontsize=FS, zorder=4)
        self._track(top - h)
        return dict(cx=cx, top=top, bot=top - h, left=cx - w / 2, right=cx + w / 2, cy=top - h / 2)

    def proc(self, cx, top, text, w=BW, h=BH):
        self.ax.add_patch(Rectangle((cx - w / 2, top - h), w, h, fc="white", ec=K, lw=LW, zorder=3))
        self.ax.text(cx, top - h / 2, text, ha="center", va="center", fontsize=FS, zorder=4, linespacing=1.15)
        self._track(top - h)
        return dict(cx=cx, top=top, bot=top - h, left=cx - w / 2, right=cx + w / 2, cy=top - h / 2)

    def data(self, cx, top, text, w=BW, h=0.62, s=0.22):
        b = top - h
        pts = [(cx - w / 2 - s / 2, b), (cx + w / 2 - s / 2, b), (cx + w / 2 + s / 2, top), (cx - w / 2 + s / 2, top)]
        self.ax.add_patch(Polygon(pts, closed=True, fc="white", ec=K, lw=LW, zorder=3))
        self.ax.text(cx, top - h / 2, text, ha="center", va="center", fontsize=FS, zorder=4, linespacing=1.15)
        self._track(b)
        return dict(cx=cx, top=top, bot=b, left=cx - w / 2, right=cx + w / 2, cy=top - h / 2)

    def dec(self, cx, top, text, w=3.0, h=1.15):
        cy = top - h / 2
        pts = [(cx, top), (cx + w / 2, cy), (cx, top - h), (cx - w / 2, cy)]
        self.ax.add_patch(Polygon(pts, closed=True, fc="white", ec=K, lw=LW, zorder=3))
        self.ax.text(cx, cy, text, ha="center", va="center", fontsize=FS - 0.5, zorder=4, linespacing=1.15)
        self._track(top - h)
        return dict(cx=cx, top=top, bot=top - h, left=cx - w / 2, right=cx + w / 2, cy=cy)

    def label(self, x, y, t):
        self.ax.text(x, y, t, ha="center", va="center", fontsize=FS - 1, zorder=4,
                     bbox=dict(fc="white", ec="none", pad=0.5))

    def down(self, a, b):
        self.arrow(a["cx"], a["bot"], b["cx"], b["top"])

    def save(self, name):
        lo = self.lowest - 0.2
        self.ax.set_ylim(lo, 0.2)
        self.fig.set_size_inches(self.W, 0.2 - lo)
        self.fig.savefig(os.path.join(OUT, name), dpi=300, facecolor="white")
        plt.close(self.fig)


def chain(c, cx, start, items):
    """items: daftar (jenis, teks); jenis = proc | data | term."""
    prev = start
    out = []
    for kind, text in items:
        top = prev["bot"] - GAP
        node = getattr(c, kind)(cx, top, text)
        c.down(prev, node)
        out.append(node)
        prev = node
    return out


# Gambar A: penyiapan dataset per jalur
def fig_dataset():
    c = Chart(8.0)
    X = 3.6
    s = c.term(X, -0.1, "Mulai")
    n = chain(c, X, s, [
        ("data", "Data RUP dan\nData Realisasi"),
        ("proc", "Penyaringan paket pemerintah\nprovinsi bersumber APBD"),
        ("proc", "Penghapusan data duplikat"),
        ("proc", "Penyeragaman nilai kosong\ndan format nilai"),
        ("proc", "Penggabungan baris realisasi\ndengan kode RUP yang sama"),
        ("proc", "Pembentukan dataset jalur\nperencanaan (seluruh paket RUP)"),
    ])
    d = c.dec(X, n[-1]["bot"] - GAP, "Paket memiliki\npasangan data\nrealisasi?")
    c.down(n[-1], d)
    ya = c.proc(X, d["bot"] - GAP - 0.1, "Pemasukan paket ke dataset\njalur pelaksanaan")
    c.down(d, ya)
    c.label(X + 0.22, d["bot"] - 0.2, "Ya")
    tx = 6.55
    tidak = c.proc(tx, d["cy"] + 0.25, "Paket hanya\ndinilai pada jalur\nperencanaan", w=1.95, h=0.72)
    c.arrow(d["right"], d["cy"], tidak["left"], d["cy"])
    c.label((d["right"] + tidak["left"]) / 2, d["cy"] + 0.16, "Tidak")
    rf = c.proc(X, ya["bot"] - GAP - 0.1, "Rekayasa fitur setiap jalur")
    c.down(ya, rf)
    jy = (ya["bot"] + rf["top"]) / 2
    c.line([tx, tx, X], [tidak["bot"], jy, jy])
    n2 = chain(c, X, rf, [("data", "Dataset fitur jalur\nperencanaan dan pelaksanaan"), ("term", "Selesai")])
    c.save("gambar-3-5-diagram-alir-penyiapan-dataset.png")


# Gambar B: pengembangan model ensemble
def fig_ensemble():
    c = Chart(8.0)
    X = 4.0
    s = c.term(X, -0.1, "Mulai")
    n = chain(c, X, s, [
        ("data", "Dataset fitur per jalur"),
        ("proc", "Standardisasi fitur"),
    ])
    top = n[-1]["bot"] - GAP - 0.25
    xs = [1.45, 4.0, 6.55]
    names = ["Isolation Forest", "LOF", "Autoencoder"]
    skor = ["Skor isolasi", "Skor kepadatan lokal", "Galat rekonstruksi"]
    split_y = n[-1]["bot"] - 0.2
    c.line([X, X], [n[-1]["bot"], split_y])
    c.line([xs[0], xs[-1]], [split_y, split_y])
    models, outs = [], []
    for x, nm, sk in zip(xs, names, skor):
        m = c.proc(x, top, "Pelatihan\n" + nm, w=2.2, h=0.62)
        c.arrow(x, split_y, x, m["top"])
        o = c.data(x, m["bot"] - GAP, sk, w=1.95, h=0.5, s=0.18)
        c.down(m, o)
        models.append(m)
        outs.append(o)
    join_y = outs[0]["bot"] - 0.22
    for o in outs:
        c.line([o["cx"], o["cx"]], [o["bot"], join_y])
    c.line([xs[0], xs[-1]], [join_y, join_y])
    nm_ = c.proc(X, join_y - 0.25, "Normalisasi min-max\nskor setiap model")
    c.arrow(X, join_y, X, nm_["top"])
    chain(c, X, nm_, [
        ("proc", "Perhitungan rata-rata\nskor ternormalisasi"),
        ("proc", "Pengurutan paket berdasarkan\nskor ensemble"),
        ("data", "Skor anomali dan\nperingkat paket"),
        ("term", "Selesai"),
    ])
    c.save("gambar-3-6-diagram-alir-model-ensemble.png")


# Gambar C: evaluasi model
def fig_eval():
    c = Chart(8.0)
    X = 3.6
    s = c.term(X, -0.1, "Mulai")
    n = chain(c, X, s, [
        ("data", "Peringkat paket ensemble\ndan model individual"),
        ("proc", "Penandaan indikator red flag\npada setiap paket"),
        ("proc", "Pemilihan satu model\ndan satu nilai K"),
        ("proc", "Pengambilan K paket\ndengan skor tertinggi"),
        ("proc", "Perhitungan Precision@K"),
    ])
    pick = n[2]
    d = c.dec(X, n[-1]["bot"] - GAP, "Semua model\ndan nilai K sudah\ndihitung?", w=3.1, h=1.25)
    c.down(n[-1], d)
    lx = 6.4
    c.line([d["right"], lx, lx], [d["cy"], d["cy"], pick["cy"]])
    c.arrow(lx, pick["cy"], pick["right"], pick["cy"])
    c.label((d["right"] + lx) / 2, d["cy"] + 0.16, "Tidak")
    rest = chain(c, X, d, [
        ("proc", "Perbandingan Precision@K ensemble\ndengan model individual"),
        ("proc", "Penelaahan jumlah red flag pada\npaket peringkat teratas"),
        ("proc", "Perhitungan SHAP pada\npaket peringkat teratas"),
        ("data", "Hasil evaluasi dan\nkontribusi fitur"),
        ("term", "Selesai"),
    ])
    c.label(X + 0.22, d["bot"] - 0.16, "Ya")
    c.save("gambar-3-7-diagram-alir-evaluasi-model.png")


fig_dataset()
fig_ensemble()
fig_eval()
print("ok")
