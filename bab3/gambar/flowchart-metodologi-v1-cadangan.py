import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Polygon, Rectangle

plt.rcParams["font.family"] = "Liberation Serif"
plt.rcParams["mathtext.fontset"] = "stix"

OUT = sys.argv[1]

W, H = 9.6, 16.4
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

EDGE = "#404040"
C_PREP = "#E8EDF3"   # persiapan / umum
C_DATA = "#E6EEF5"
C_MODEL = "#DCE6F1"
C_NORM = "#FFF2CC"
C_AVG = "#FCE4D6"
C_OUT = "#E2EFDA"
C_EVAL = "#EDE4F3"
C_LANE = "#F2F2F2"

LANE_X0, LANE_X1 = 0.25, 1.85
MAIN_X0, MAIN_X1 = LANE_X1, W - 0.25
CX = 5.5
FS, FS_SUB = 13, 10.5


def box(cx, cy, w, h, title, sub=None, color=C_PREP, italic_title=False):
    p = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                       boxstyle="round,pad=0,rounding_size=0.06",
                       fc=color, ec=EDGE, lw=1.3, zorder=3)
    ax.add_patch(p)
    if sub:
        ty = cy + h / 2 - 0.2
        ax.text(cx, ty, title, ha="center", va="center", fontsize=FS,
                style="italic" if italic_title else "normal", zorder=4)
        ax.text(cx, (cy - h / 2 + ty - 0.12) / 2, sub, ha="center", va="center", fontsize=FS_SUB,
                style="italic", color="#333333", zorder=4, linespacing=1.15)
    else:
        ax.text(cx, cy, title, ha="center", va="center", fontsize=FS,
                style="italic" if italic_title else "normal", zorder=4, linespacing=1.15)
    return dict(cx=cx, cy=cy, w=w, h=h, top=cy + h / 2, bot=cy - h / 2,
                left=cx - w / 2, right=cx + w / 2)


def oval(cx, cy, w, h, text):
    ax.add_patch(Ellipse((cx, cy), w, h, fc="white", ec=EDGE, lw=1.3, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=FS, zorder=4)
    return dict(cx=cx, cy=cy, top=cy + h / 2, bot=cy - h / 2, left=cx - w / 2, right=cx + w / 2)


def diamond(cx, cy, w, h, text):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, fc="white", ec=EDGE, lw=1.3, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=FS - 0.5, zorder=4, linespacing=1.15)
    return dict(cx=cx, cy=cy, top=cy + h / 2, bot=cy - h / 2, left=cx - w / 2, right=cx + w / 2)


def arrow(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=2,
                arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.3,
                                mutation_scale=13, shrinkA=0, shrinkB=0))


def line(xs, ys):
    ax.plot(xs, ys, color=EDGE, lw=1.3, zorder=2, solid_capstyle="butt")


def poly_arrow(pts):
    """Garis siku; segmen terakhir diberi panah."""
    for (xa, ya), (xb, yb) in zip(pts[:-2], pts[1:-1]):
        line([xa, xb], [ya, yb])
    arrow(*pts[-2], *pts[-1])


def down(a, b):
    arrow(a["cx"], a["bot"], b["cx"], b["top"])


lanes = []  # (y_top, y_bot, label)

BW, BH = 3.5, 0.5
GAP = 0.27
y = H - 0.45

# ---------------- TAHAP 1 ----------------
t1_top = y
start = oval(CX, y - 0.3, 1.5, 0.52, "Mulai")
y = start["bot"] - GAP
idm = box(CX, y - BH / 2, BW, BH, "Identifikasi Masalah")
y = idm["bot"] - GAP
lit = box(CX, y - BH / 2, BW, BH, "Studi Literatur")
down(start, idm)
down(idm, lit)
y = lit["bot"] - 0.16
lanes.append((t1_top, y, "TAHAP 1:\nPERSIAPAN"))

# ---------------- TAHAP 2 ----------------
t2_top = y
y -= 0.16
BH2 = 0.64
kol = box(CX, y - 0.8 / 2, 4.2, 0.8, "Pengumpulan Data",
          "RUP dan realisasi, Data INAPROC\nAPBD pemerintah provinsi, TA 2025–2026", C_DATA)
down(lit, kol)
y = kol["bot"] - GAP
pre = box(CX, y - 0.8 / 2, 4.2, 0.8, "Pra-pemrosesan Data",
          "normalisasi nilai \"-\", agregasi realisasi per kode RUP,\npenyesuaian nama kolom nilai", C_DATA)
down(kol, pre)

LX, RX = CX - 1.55, CX + 1.55
SW = 2.75
y = pre["bot"] - 0.5
splitL = box(LX, y - 0.8 / 2, SW, 0.8, "Jalur Perencanaan", "seluruh paket pada data RUP", C_DATA)
splitR = box(RX, y - 0.8 / 2, SW, 0.8, "Jalur Pelaksanaan",
             "penggabungan RUP dan realisasi\nberdasarkan kode RUP", C_DATA)
ymid = pre["bot"] - 0.24
line([pre["cx"], pre["cx"]], [pre["bot"], ymid])
line([LX, RX], [ymid, ymid])
arrow(LX, ymid, LX, splitL["top"])
arrow(RX, ymid, RX, splitR["top"])
y = splitL["bot"] - GAP
fL = box(LX, y - BH2 / 2, SW, BH2, "Rekayasa Fitur", "fitur perencanaan", C_DATA)
fR = box(RX, y - BH2 / 2, SW, BH2, "Rekayasa Fitur", "fitur pelaksanaan", C_DATA)
down(splitL, fL)
down(splitR, fR)
y = fL["bot"] - 0.16
lanes.append((t2_top, y, "TAHAP 2:\nPENYIAPAN\nDATA"))

# ---------------- TAHAP 3 ----------------
t3_top = y
y -= 0.36
train = box(CX, y - BH2 / 2, 4.2, BH2, "Pelatihan Model per Jalur",
            "data seluruh provinsi dilatih sekaligus (nasional)", C_MODEL)
ymerge = fL["bot"] - 0.24
line([LX, LX], [fL["bot"], ymerge])
line([RX, RX], [fR["bot"], ymerge])
line([LX, RX], [ymerge, ymerge])
arrow(CX, ymerge, CX, train["top"])

MW, MH = 1.75, 0.5
MX = [CX - 2.0, CX, CX + 2.0]
y = train["bot"] - 0.5
models = [box(x, y - MH / 2, MW, MH, t, color=C_MODEL)
          for x, t in zip(MX, ["Isolation Forest", "LOF", "Autoencoder"])]
ysplit = train["bot"] - 0.24
line([CX, CX], [train["bot"], ysplit])
line([MX[0], MX[2]], [ysplit, ysplit])
for m in models:
    arrow(m["cx"], ysplit, m["cx"], m["top"])
y = models[0]["bot"] - GAP
norms = [box(x, y - 0.58 / 2, MW, 0.58, "Normalisasi",
             r"min-max $\tilde{s}_%d(x)$" % (i + 1), C_NORM)
         for i, x in enumerate(MX)]
for m, n in zip(models, norms):
    down(m, n)
y = norms[0]["bot"] - 0.5
avg = box(CX, y - BH2 / 2, 4.2, BH2, "Penggabungan Skor (Ensemble)",
          r"rata-rata skor ternormalisasi $S(x)$", C_AVG)
yj = norms[0]["bot"] - 0.24
for n in norms:
    line([n["cx"], n["cx"]], [n["bot"], yj])
line([MX[0], MX[2]], [yj, yj])
arrow(CX, yj, CX, avg["top"])
y = avg["bot"] - GAP
rank = box(CX, y - BH2 / 2, 4.2, BH2, "Pemeringkatan Paket",
           "urutan paket berdasarkan skor prioritas", C_OUT)
down(avg, rank)
y = rank["bot"] - 0.16
lanes.append((t3_top, y, "TAHAP 3:\nPEMODELAN\nENSEMBLE"))

# ---------------- TAHAP 4 ----------------
t4_top = y
y -= 0.16
BH3 = 0.98
ev = box(CX, y - BH3 / 2, 4.0, BH3, "Evaluasi Model",
         "Precision@K terhadap red flag pengadaan,\ndibandingkan dengan IF, LOF, Autoencoder\n"
         "dan peringkat berdasarkan pagu; stabilitas peringkat", C_EVAL)
down(rank, ev)
# red flag sebagai pembanding (masukan samping)
rf = box(MAIN_X0 + 0.12 + 0.6, ev["cy"], 1.2, 0.66, "Indikator\nRed Flag", color="white")
arrow(rf["right"], rf["cy"], ev["left"], ev["cy"])

y = ev["bot"] - 0.27
DW, DH = 2.8, 0.95
dec = diamond(CX, y - DH / 2, DW, DH, "Apakah hasil\nmodel layak?")
down(ev, dec)
# loop "Tidak"
adj = box(MAIN_X1 - 0.1 - 1.3 / 2, dec["cy"], 1.3, 0.78, "Penyesuaian\nFitur dan\nParameter", color="white")
arrow(dec["right"], dec["cy"], adj["left"], adj["cy"])
ax.text((dec["right"] + adj["left"]) / 2, dec["cy"] + 0.1, "Tidak", ha="center", va="bottom", fontsize=FS_SUB + 1)
poly_arrow([(adj["cx"], adj["top"]), (adj["cx"], train["cy"]), (train["right"], train["cy"])])

y = dec["bot"] - GAP
shap = box(CX, y - BH2 / 2, 4.2, BH2, "Interpretasi dengan SHAP",
           "kontribusi fitur pada paket berperingkat atas", C_EVAL)
down(dec, shap)
ax.text(CX + 0.1, (dec["bot"] + shap["top"]) / 2, "Ya", ha="left", va="center", fontsize=FS_SUB + 1)
y = shap["bot"] - GAP
tel = box(CX, y - BH2 / 2, 4.2, BH2, "Telaah Sampel Paket Prioritas",
          "memeriksa kewajaran paket berperingkat atas", C_EVAL)
down(shap, tel)
y = tel["bot"] - 0.16
lanes.append((t4_top, y, "TAHAP 4:\nEVALUASI DAN\nINTERPRETASI"))

# ---------------- TAHAP 5 ----------------
t5_top = y
y -= 0.16
agg = box(CX, y - BH2 / 2, 4.2, BH2, "Agregasi Hasil per Provinsi",
          "proporsi paket anomali di setiap provinsi", C_OUT)
down(tel, agg)
y = agg["bot"] - GAP
dash = box(CX, y - BH3 / 2, 4.2, BH3, "Pengembangan Dashboard",
           "peta choropleth 38 provinsi, pilihan tampilan\nPerencanaan/Pelaksanaan, peringkat paket,\n"
           "rincian paket dan penjelasan SHAP", C_OUT)
down(agg, dash)
y = dash["bot"] - 0.16
lanes.append((t5_top, y, "TAHAP 5:\nPENGEMBANGAN\nDASHBOARD"))

# ---------------- TAHAP 6 ----------------
t6_top = y
y -= 0.16
rep = box(CX, y - BH / 2, BW, BH, "Analisis Hasil dan Pelaporan")
down(dash, rep)
y = rep["bot"] - GAP
end = oval(CX, y - 0.26, 1.5, 0.52, "Selesai")
down(rep, end)
y = end["bot"] - 0.22
lanes.append((t6_top, y, "TAHAP 6:\nANALISIS DAN\nPELAPORAN"))

# ---------------- lajur tahap ----------------
for top, bot, label in lanes:
    ax.add_patch(Rectangle((LANE_X0, bot), LANE_X1 - LANE_X0, top - bot,
                           fc=C_LANE, ec=EDGE, lw=1.0, zorder=0))
    ax.add_patch(Rectangle((MAIN_X0, bot), MAIN_X1 - MAIN_X0, top - bot,
                           fc="white", ec=EDGE, lw=1.0, zorder=0))
    ax.text((LANE_X0 + LANE_X1) / 2, (top + bot) / 2, label, ha="center", va="center",
            fontsize=FS - 1, weight="bold", linespacing=1.25, zorder=1)

ax.set_ylim(lanes[-1][1] - 0.15, H - 0.3)
fig.set_size_inches(W, H - 0.3 - (lanes[-1][1] - 0.15))
fig.savefig(OUT, dpi=300, facecolor="white")
print("bottom", lanes[-1][1])
