"""Tahap 4: kalimat penjelasan (templat), ringkasan bukti validitas, dan data JSON untuk dashboard (model v3)."""
import json
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v3')
OUT = os.environ.get('V3_OUT', '/mnt/project-files/model-v3/')  # bisa diganti untuk uji kode
VAL = OUT + 'validasi/'
d = pd.read_pickle('/mnt/project-files/model-v1/tahap1.pkl')
import s2_model  # noqa: F401,E402  (kelas Ensemble3 untuk membuka pickle)
hasil = pd.read_pickle(OUT + 'tahap2.pkl')
sh = pd.read_pickle(OUT + 'tahap3.pkl')
info = d['info']
# Samakan nama provinsi dengan GeoJSON 38 provinsi
info['provinsi'] = info.provinsi.replace({'Bangka Belitung': 'Kepulauan Bangka Belitung',
                                          'Di Yogyakarta': 'Daerah Istimewa Yogyakarta', 'Dki Jakarta': 'DKI Jakarta'})

NAMA_RF = {'rf1_pl_dekat_ambang': 'Pengadaan langsung mendekati ambang',
           'rf2_pl_lewat_ambang': 'Pengadaan langsung melebihi ambang',
           'rf3_pemecahan_paket': 'Indikasi pemecahan paket',
           'rf4_penunjukan_langsung': 'Penunjukan langsung',
           'rf5_penyedia_dominan': 'Penyedia dominan di satker (>40% nilai)',
           'rf6_penyedia_serba_ada': 'Penyedia serba-ada'}
NAMA_F = {'log_pagu': 'Pagu', 'log_rasio_pagu_sejenis': 'Pagu dibanding paket sejenis',
          'porsi_pagu_satker': 'Porsi pagu di satker', 'log_jumlah_paket_satker': 'Jumlah paket satker',
          'proporsi_pl_satker': 'Proporsi pengadaan langsung satker', 'pdn': 'Produk dalam negeri',
          'umk': 'Status UMK', 'metode': 'Metode pengadaan', 'jenis': 'Jenis pengadaan',
          'rasio_realisasi': 'Rasio realisasi terhadap pagu', 'log_selisih_realisasi': 'Selisih realisasi dan pagu',
          'ubah_metode': 'Perubahan metode', 'porsi_pdn': 'Porsi nilai PDN', 'porsi_umk': 'Porsi nilai UMK',
          'sumber': 'Sumber transaksi', 'log_rasio_pagu_satker': 'Pagu dibanding paket lain di satker',
          'porsi_epurchasing_satker': 'Porsi e-purchasing satker',
          'selisih_rasio_realisasi_sejenis': 'Rasio realisasi dibanding paket sejenis',
          'log_rasio_pagu_nama_serupa': 'Pagu dibanding paket bernama serupa'}
NAMA_PEMBANDING = {'Skor-z sederhana': 'Skor-z sederhana', 'Pagu terbesar': 'Pagu terbesar', 'Acak': 'Urutan acak'}


def rp(x):
    x = float(x)
    for b, s in [(1e12, ' T'), (1e9, ' M'), (1e6, ' jt'), (1e3, ' rb')]:
        if abs(x) >= b:
            return 'Rp' + f'{x / b:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + s
    return f'Rp{x:,.0f}'


def pct(x, n=1):
    return f'{100 * x:.{n}f}%'.replace('.', ',')


def angka(x, n=2):
    x = 0.0 if round(x, n) == 0 else x  # hindari tulisan -0,000
    return f'{x:,.{n}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def kali(x):
    """Rasio 'x kali' dengan pemisah ribuan Indonesia."""
    return angka(x, 1) if x < 100 else angka(x, 0)


def uraian(g, kode, F, med):
    """Nilai fitur paket dalam kalimat biasa, dibandingkan dengan median nasional jalurnya."""
    i, f = info.loc[kode], F.loc[kode]
    if g == 'log_pagu':
        return f'pagu {rp(i.pagu)}, median nasional {rp(10 ** med["log_pagu"])}'
    if g == 'log_rasio_pagu_sejenis':
        return f'pagu {kali(10 ** f[g])} kali median paket {i.jenis.lower()} dengan metode yang sama'
    if g == 'porsi_pagu_satker':
        return f'pagu ini {pct(f[g])} dari total pagu satker (median {pct(med[g])})'
    if g == 'log_jumlah_paket_satker':
        return f'satker memiliki {10 ** f[g]:,.0f} paket (median {10 ** med[g]:,.0f})'.replace(',', '.')
    if g == 'proporsi_pl_satker':
        return f'{pct(f[g])} paket satker lewat pengadaan langsung (median {pct(med[g])})'
    if g == 'pdn':
        return 'memakai produk dalam negeri' if f[g] else 'tidak memakai produk dalam negeri (sebagian besar paket memakai)'
    if g == 'umk':
        return 'paket untuk UMK' if f[g] else 'bukan paket untuk UMK (sebagian besar paket untuk UMK)'
    if g == 'metode':
        return f'metode {i.metode_pengadaan.lower()}'
    if g == 'jenis':
        return f'jenis {i.jenis.lower()}'
    if g == 'rasio_realisasi':
        return f'realisasi {pct(f[g])} dari pagu (median {pct(med[g])})'
    if g == 'log_selisih_realisasi':
        return f'selisih realisasi dan pagu {rp(abs(i.realisasi - i.pagu))}'
    if g == 'ubah_metode':
        return (f'metode berubah dari {i.metode_pengadaan.lower()} ke {str(i.metode_realisasi).lower()}'
                if f[g] else 'metode tidak berubah')
    if g == 'porsi_pdn':
        return f'porsi nilai PDN {pct(f[g])} (median {pct(med[g])})'
    if g == 'porsi_umk':
        return f'porsi nilai UMK {pct(f[g])} (median {pct(med[g])})'
    if g == 'log_rasio_pagu_satker':
        return f'pagu {kali(10 ** f[g])} kali median paket lain di satker yang sama'
    if g == 'porsi_epurchasing_satker':
        return f'{pct(f[g])} paket satker lewat e-purchasing (median {pct(med[g])})'
    if g == 'selisih_rasio_realisasi_sejenis':
        return f'rasio realisasi {pct(F.loc[kode, "rasio_realisasi"])}, selisih {pct(f[g])} dari median paket sejenis'
    if g == 'sumber':
        return f'sumber transaksi {str(i.sumber_transaksi)}'
    if g == 'log_rasio_pagu_nama_serupa':
        return f'pagu {kali(10 ** f[g])} kali median 30 paket yang namanya paling mirip'
    return g


# ------------------------------------------------------------------ bukti validitas (dari validasi/*.csv)
KV = pd.read_csv(VAL + 'v_konvergen.csv')
BT = pd.read_csv(VAL + 'v_bootstrap.csv')
ST = pd.read_csv(VAL + 'v_stabilitas.csv')
AM = pd.read_csv(VAL + 'v_ambang.csv')
SI = pd.read_csv(VAL + 'v_sintetis.csv')
PR = pd.read_csv(VAL + 'v_prediktif.csv')
SH = pd.read_csv(VAL + 'v_shap_hapus.csv')
AB = pd.read_csv(VAL + 'v_ablasi.csv') if os.path.exists(VAL + 'v_ablasi.csv') else None
ABS = pd.read_csv(VAL + 'v_ablasi_sintetis.csv') if os.path.exists(VAL + 'v_ablasi_sintetis.csv') else None
SPI = pd.read_csv(VAL + 'v_spi.csv') if os.path.exists(VAL + 'v_spi.csv') else None
UTAMA = 'IF+LOF+AE (rata-rata, dipakai)'


def peringkat_ablasi():
    """Peringkat tiap kombinasi model pada 6 ukuran per jalur (1 = terbaik dari 9 kombinasi)."""
    rel = ['lokal', 'dependensi', 'berkelompok', 'realisasi_lewat_pagu', 'dekat_ambang', 'pagu_digelembungkan']
    cak = ABS[ABS.tipe.isin(rel)].groupby(['jalur', 'gabungan']).terdeteksi_5persen.mean()
    alarm = ABS[ABS.tipe == 'kontrol_normal'].set_index(['jalur', 'gabungan']).terdeteksi_5persen
    t = AB.set_index(['jalur', 'gabungan'])
    out = {}
    for j in ['perencanaan', 'pelaksanaan']:
        g = t.loc[j]
        out[j] = pd.DataFrame({'P@200': g['P@200'].rank(ascending=False), '5%': g.presisi_5persen.rank(ascending=False),
                               'uji 5%': g.uji_5persen.rank(ascending=False), 'cakupan': cak.loc[j].rank(ascending=False),
                               'alarm': alarm.loc[j].rank(), 'satker': g.satker_maks_top200.rank()})
    return out


def pval(p):
    return 'p < 0,001' if p < 0.001 else f'p = {angka(p, 3)}'


def validasi(jalur):
    k = KV[KV.jalur == jalur].set_index('metode')
    e = k.loc['Ensemble']
    b = BT[(BT.jalur == jalur)].set_index('metode')
    rows = []
    status = 'ya' if e['pval@200'] < 0.05 else 'tidak'
    rows.append({'uji': 'Paket teratas lebih sering punya red flag?',
                 'hasil': f"200 paket teratas: {pct(e['P@200'])} punya red flag, rata-rata semua paket {pct(e['acuan'])} "
                          f"({pval(e['pval@200'])}; selang bootstrap per satker {pct(b.loc['Ensemble', 'ci_lo'], 0)}–{pct(b.loc['Ensemble', 'ci_hi'], 0)})",
                 'arti': 'Skor model sejalan dengan red flag, jauh di atas tebakan acak.' if status == 'ya'
                         else 'Skor model belum sejalan dengan red flag.', 'status': status})
    u1, u2 = e['uji_rata'] > 1.2 * e['acuan_uji'], e['uji_5persen'] > 1.2 * e['acuan_uji']
    st = 'ya' if (u1 and u2) else ('sebagian' if (u1 or u2) else 'tidak')
    rows.append({'uji': 'Berlaku juga di provinsi yang tidak dipakai saat memilih pengaturan?',
                 'hasil': f"19 provinsi uji: 50–200 teratas {pct(e['uji_rata'])}, 5% teratas {pct(e['uji_5persen'])}, rata-rata {pct(e['acuan_uji'])}. "
                          f"19 provinsi pilih: {pct(e['pilih_rata'])}, {pct(e['pilih_5persen'])}, rata-rata {pct(e['acuan_pilih'])}",
                 'arti': {'ya': 'Hasil tidak hanya berlaku di provinsi tempat pengaturan dipilih.',
                          'sebagian': ('Di provinsi uji, puncak daftar unggul tetapi 5% teratas hampir sama dengan rata-rata.' if u1 else
                                       'Di provinsi uji, 5% teratas unggul tetapi puncak daftar belum.'),
                          'tidak': 'Di provinsi uji model belum lebih baik dari acak.'}[st], 'status': st})
    t4 = e['tanpaRF4_rata'] > e['acuan_tanpaRF4']
    t45 = e['tanpaRF4_5persen'] > 1.2 * e['acuan_tanpaRF4']
    rows.append({'uji': 'Tetap sejalan bila red flag penunjukan langsung tidak dihitung?',
                 'hasil': f"tanpa RF4: 50–200 teratas {pct(e['tanpaRF4_rata'])}, 5% teratas {pct(e['tanpaRF4_5persen'])}; "
                          f"rata-rata semua paket {pct(e['acuan_tanpaRF4'])}",
                 'arti': ('Kesesuaian tidak hanya datang dari penunjukan langsung.' if t4 and t45 else
                          'Di 5% teratas (dasar peta) red flag lain ikut terangkat, tetapi puncak daftar (50–200 paket) '
                          'belum lebih sering punya red flag selain penunjukan langsung.' if t45 else
                          'Di puncak daftar red flag lain terangkat, tetapi pada 5% teratas tidak.' if t4 else
                          'Kesesuaian terutama datang dari penunjukan langsung.'),
                 'status': 'ya' if (t4 and t45) else ('sebagian' if (t4 or t45) else 'tidak')})
    pemb = ['Skor-z sederhana', 'Pagu terbesar', 'Acak']
    unggul = [p for p in pemb if k.loc[p, 'P@200'] > e['P@200']]
    rows.append({'uji': 'Lebih baik dari cara sederhana?',
                 'hasil': '; '.join(f"{NAMA_PEMBANDING[p]} {pct(k.loc[p, 'P@200'])}" for p in pemb) + f"; ensemble {pct(e['P@200'])} (P@200)",
                 'arti': 'Ensemble lebih sering mengenai red flag daripada cara sederhana.' if not unggul else
                         f"{', '.join(NAMA_PEMBANDING[p] for p in unggul)} lebih sering mengenai red flag. Sebagian red flag dihitung dari besaran "
                         'yang sama (pagu, porsi pagu di satker), jadi cara satu-fitur mudah menemukannya. Keunggulan ensemble ada pada pola gabungan (baris anomali buatan).',
                 'status': 'ya' if not unggul else 'sebagian'})
    si = SI[SI.jalur == jalur].pivot(index='tipe', columns='metode', values='terdeteksi_5persen')
    rows.append({'uji': 'Menangkap anomali buatan yang sengaja disisipkan?',
                 'hasil': f"pola ekstrem {pct(si.loc['global', 'Ensemble'], 0)}; pola gabungan antarfitur {pct(si.loc['dependensi', 'Ensemble'], 0)} "
                          f"(skor-z {pct(si.loc['dependensi', 'Skor-z sederhana'], 0)}); kelompok kembar {pct(si.loc['berkelompok', 'Ensemble'], 0)}; "
                          f"pagu digelembungkan 5–20 kali {pct(si.loc['pagu_digelembungkan', 'Ensemble'], 0)}; dinaikkan ke dekat ambang {pct(si.loc['dekat_ambang', 'Ensemble'], 0)} "
                          f"(paket wajar ikut tertandai {pct(si.loc['kontrol_normal', 'Ensemble'], 0)})",
                 'arti': 'Kuat untuk pola tidak lazim yang ekstrem atau gabungan. Lemah untuk manipulasi yang sengaja dibuat tampak wajar '
                         '(pagu digelembungkan, dekat ambang), karena itu red flag tetap ditampilkan di samping skor.',
                 'status': 'sebagian'})
    s1 = ST[(ST.jalur == jalur) & ST.perbandingan.str.startswith('satu')].iloc[0]
    s5 = ST[(ST.jalur == jalur) & ST.perbandingan.str.startswith('rata')].iloc[0]
    rows.append({'uji': 'Hasil stabil bila model dilatih ulang?',
                 'hasil': f"Kesamaan 200 teratas antar dua pelatihan (Jaccard): {angka(s5.jaccard_top200)}; satu seed saja: {angka(s1.jaccard_top200)}. "
                          f"Kesamaan 5% paket tidak lazim: {angka(s5.jaccard_anomali5persen)}",
                 'arti': ('Merata-ratakan 5 seed membuat daftar teratas jauh lebih stabil' if s5.jaccard_top200 > s1.jaccard_top200 + 0.1
                          else 'Rata-rata 5 seed sedikit menaikkan kestabilan')
                         # Jaccard J antara dua daftar 200 paket -> irisan = 400J/(1+J) paket
                         + f": sekitar {round(10 * 2 * s5.jaccard_top200 / (1 + s5.jaccard_top200))} dari 10 paket di 200 teratas tetap sama.",
                 'status': 'ya' if s5.jaccard_top200 >= 0.6 else 'sebagian'})
    am = AM[(AM.jalur == jalur) & AM.ambang.isin(['1%', '5%', '10%'])].set_index('ambang')
    rho = AM[(AM.jalur == jalur) & AM.ambang.str.startswith('peringkat provinsi 1% vs 10%')].spearman_provinsi_redflag.iloc[0]
    rows.append({'uji': 'Kesimpulan berubah bila ambang "tidak lazim" diganti?',
                 'hasil': f"persentase ber-red flag pada ambang 1% / 5% / 10%: {pct(am.loc['1%', 'presisi_redflag'])} / "
                          f"{pct(am.loc['5%', 'presisi_redflag'])} / {pct(am.loc['10%', 'presisi_redflag'])} (rata-rata {pct(am.loc['5%', 'acuan'])}); "
                          f"urutan provinsi ambang 1% vs 10%: ρ = {angka(rho)}",
                 'arti': 'Ambang 5% bukan satu-satunya pilihan yang memberi hasil baik.', 'status': 'ya' if rho > 0.7 else 'sebagian'})
    a5 = am.loc['5%']
    rows.append({'uji': 'Peta provinsi sejalan dengan red flag?',
                 'hasil': f"korelasi proporsi paket tidak lazim dengan tingkat red flag 38 provinsi: ρ = {angka(a5.spearman_provinsi_redflag)} "
                          f"({pval(a5.p)}); tanpa provinsi Papua ρ = {angka(a5.spearman_tanpa_papua)}",
                 'arti': 'Provinsi yang gelap di peta memang lebih banyak punya red flag.' if a5.p < 0.05 else
                         'Urutan provinsi di peta belum sejalan dengan red flag.', 'status': 'ya' if a5.p < 0.05 else 'tidak'})
    s = SH[SH.jalur == jalur].iloc[0]
    rows.append({'uji': 'Penjelasan SHAP benar-benar menunjuk fitur penyebab?',
                 'hasil': f"mengganti 3 fitur teratas SHAP menurunkan skor {angka(s.turun_top3_rata, 3)}, mengganti 3 fitur acak {angka(s.turun_acak3_rata, 3)} "
                          f"({angka(s.top3_lebih_besar_persen, 0)}% paket turun lebih besar)",
                 'arti': 'Fitur yang disebut di kalimat penjelasan memang yang paling menaikkan skor.', 'status': 'ya' if s.top3_lebih_besar_persen >= 80 else 'sebagian'})
    if jalur == 'perencanaan':
        p = PR.set_index('target')
        bagian = []
        for t, lbl in [('R055 PL berulang ke penyedia sama, jumlah lewat ambang', 'PL berulang lewat ambang (R055)'),
                       ('RF5 penyedia dominan (OCP R040)', 'penyedia dominan (RF5)'),
                       ('R049 PL dekat ambang berulang ke penyedia sama', 'PL dekat ambang berulang (R049)')]:
            r = p.loc[t]
            bagian.append(f"{lbl} {angka(r.lift_top5, 1)} kali (setelah dikontrol ukuran paket {angka(r.lift_terkontrol_top5, 1)} kali)")
        ok = (p.lift_terkontrol_top5 > 1.2).sum()
        rows.append({'uji': 'Paket perencanaan yang tidak lazim lebih sering bermasalah saat pelaksanaan?',
                     'hasil': '5% paket perencanaan teratas, dibanding rata-rata: ' + '; '.join(bagian),
                     'arti': 'Skor yang dihitung hanya dari RUP memberi tanda awal untuk masalah yang baru terlihat saat pelaksanaan.'
                             if ok >= 2 else 'Tanda awal dari RUP ke pelaksanaan masih lemah setelah ukuran paket dikontrol.',
                     'status': 'ya' if ok >= 2 else 'sebagian'})
    if AB is not None and ABS is not None:
        pk = peringkat_ablasi()
        rata = pd.concat(pk.values()).groupby(level=0).mean().mean(axis=1).sort_values()
        buruk = pd.concat(pk.values()).groupby(level=0).max().max(axis=1)
        g = AB[AB.jalur == jalur].set_index('gabungan')
        tunggal = g.loc[['IF saja', 'LOF saja', 'AE saja'], 'presisi_5persen']
        ok = rata.index[0] == UTAMA and (buruk < buruk.loc[UTAMA]).sum() == 0
        rows.append({'uji': 'Perlu menggabungkan tiga model?',
                     'hasil': f"5% teratas jalur ini ber-red flag: ensemble {pct(g.loc[UTAMA, 'presisi_5persen'])}; "
                              + ', '.join(f"{n.split()[0]} saja {pct(v)}" for n, v in tunggal.items())
                              + f". Dari 9 cara (3 model tunggal, 3 pasangan, rata-rata, maksimum, median) pada 6 ukuran di dua jalur, "
                              f"peringkat rata-rata ensemble {angka(rata.loc[UTAMA], 1)} "
                              + ('(paling baik dari 9 cara)' if rata.index[0] == UTAMA else f"(terbaik: {rata.index[0]} {angka(rata.iloc[0], 1)})")
                              + f"; peringkat terburuknya {angka(buruk.loc[UTAMA], 0)} dari 9",
                     'arti': 'Tidak ada model tunggal yang unggul di semua ukuran. Rata-rata tiga model paling konsisten: tidak pernah '
                             'menjadi yang terburuk' + (', sedangkan tiap model tunggal pernah berada di urutan terakhir pada salah satu ukuran.'
                                                        if all(buruk.loc[n] == 9 for n in ['IF saja', 'LOF saja', 'AE saja']) else '.') if ok else
                             f"Kombinasi {rata.index[0]} lebih konsisten daripada rata-rata tiga model.",
                     'status': 'ya' if ok else 'sebagian'})
    if SPI is not None:
        s = SPI[(SPI.jalur == jalur) & (SPI.ukuran == 'Proporsi paket anomali (5% teratas)')].set_index('tanpa_papua')
        a, b = s.loc[False], s.loc[True]
        st = 'ya' if (a.p_mannwhitney_rentan_lebih_tinggi < 0.05 and b.p_mannwhitney_rentan_lebih_tinggi < 0.05) else (
            'sebagian' if a.p_mannwhitney_rentan_lebih_tinggi < 0.05 else 'tidak')
        rows.append({'uji': 'Sejalan dengan penilaian lembaga lain (SPI KPK 2024)?',
                     'hasil': f"10 provinsi dengan skor integritas SPI terendah: median {pct(a.median_rentan)} paket tidak lazim; "
                              f"10 provinsi tertinggi: {pct(a.median_terjaga)} ({pval(a.p_mannwhitney_rentan_lebih_tinggi)}). "
                              f"Tanpa provinsi Papua: {pct(b.median_rentan)} vs {pct(b.median_terjaga)} ({pval(b.p_mannwhitney_rentan_lebih_tinggi)})",
                     'arti': {'ya': 'Provinsi yang dinilai KPK paling rentan memang punya lebih banyak paket tidak lazim, '
                                    'juga bila provinsi Papua dikeluarkan.',
                              'sebagian': 'Beda terlihat, tetapi terutama karena provinsi Papua.',
                              'tidak': 'Belum terlihat beda yang nyata. SPI menilai integritas instansi secara umum, bukan khusus pengadaan.'}[st],
                     'status': st})
    return rows


def conv(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))


data = {'jalur': {}, 'versi': 'v3'}
for jalur in ['perencanaan', 'pelaksanaan']:
    h, s = hasil[jalur], sh[jalur]
    F = h['F']
    sk, flags, R = h['skor'], h['flags'], h['rf']
    med = F.median()
    sk['peringkat'] = sk.Ensemble.rank(ascending=False, method='first').astype(int)
    inf = info.loc[sk.index]

    # Ringkasan per provinsi
    prov = pd.DataFrame({'n': sk.groupby(inf.provinsi).size(),
                         'anomali': sk.anomali.groupby(inf.provinsi).sum(),
                         'pagu': inf.pagu.groupby(inf.provinsi).sum(),
                         'pagu_anomali': inf.pagu[sk.anomali].groupby(inf.provinsi[sk.anomali]).sum()}).fillna(0)
    prov['proporsi'] = prov.anomali / prov.n
    prov['cakupan'] = prov.n / info.groupby('provinsi').size().loc[prov.index]
    for c in flags:
        prov[c] = R[c].groupby(inf.provinsi).sum()

    # Paket yang ditampilkan: 200 teratas nasional (ada SHAP) + 25 teratas tiap provinsi
    pilih = set(s['shap'].index)
    for _, grp in sk.groupby(inf.provinsi):
        pilih |= set(grp.Ensemble.nlargest(25).index)
    paket = []
    for kode in sk.loc[list(pilih)].sort_values('peringkat').index:
        i, r_ = inf.loc[kode], sk.loc[kode]
        row = {'kode': kode, 'rank': int(r_.peringkat), 'skor': round(float(r_.Ensemble), 4),
               'IF': round(float(r_.IF), 3), 'LOF': round(float(r_.LOF), 3), 'AE': round(float(r_.AE), 3),
               'prov': i.provinsi, 'satker': i.nama_satuan_kerja.split(' - ')[0], 'nama': i.nama_paket,
               'metode': i.metode_pengadaan, 'jenis': i.jenis, 'pagu': float(i.pagu),
               'rf': [NAMA_RF[c] for c in flags if R.at[kode, c]]}
        if jalur == 'pelaksanaan':
            row.update(realisasi=float(i.realisasi), penyedia=str(i.penyedia), sumber=str(i.sumber_transaksi))
        if kode in s['shap'].index:
            v = s['shap'].loc[kode].sort_values(key=abs, ascending=False)
            row['shap'] = [[NAMA_F[g], round(float(x), 4), uraian(g, kode, F, med)] for g, x in v.items()]
            naik = [g for g, x in v.items() if x > 0][:3]
            alasan = '; '.join(uraian(g, kode, F, med) for g in naik)
            row['kalimat'] = (f'Paket ini berada di peringkat {r_.peringkat} dari {len(sk):,} paket jalur {jalur}. '.replace(',', '.')
                              + f'Faktor yang paling menaikkan skornya: {alasan}. '
                              + 'Ini penanda untuk ditelaah lebih lanjut, bukan bukti pelanggaran.')
        paket.append(row)

    ev = h['eval'].copy()
    kv = KV[(KV.jalur == jalur) & KV.metode.isin(list(NAMA_PEMBANDING))]
    ev_pemb = [{'model': NAMA_PEMBANDING[r.metode], 'pembanding': True, **{f'P@{K}': r[f'P@{K}'] for K in [50, 100, 200]},
                **{f'rata_rf@{K}': r[f'rata_rf@{K}'] for K in [50, 100, 200]}} for _, r in kv.iterrows()]
    data['jalur'][jalur] = {
        'n': int(len(sk)), 'anomali': int(sk.anomali.sum()), 'ambang': round(float(sk.Ensemble.quantile(0.95)), 4),
        'base': s['base'],
        'prov': {p: {k: (float(v) if not isinstance(v, str) else v) for k, v in r.items()} for p, r in prov.iterrows()},
        'paket': paket,
        'eval': ev.round(3).to_dict(orient='records') + [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()} for r in ev_pemb],
        'rf_total': {NAMA_RF[c]: int(R[c].sum()) for c in flags},
        'rf_dist_top200': sk.loc[sk.peringkat <= 200, 'jumlah_rf'].value_counts().sort_index().to_dict(),
        'rf_dist_semua': (sk.jumlah_rf.value_counts(normalize=True).sort_index()).round(4).to_dict(),
        'shap_global': {NAMA_F[g]: round(float(x), 4) for g, x in s['shap'].abs().mean().sort_values(ascending=False).items()},
        'korelasi': sk[['IF', 'LOF', 'AE']].corr('spearman').round(2).to_dict(),
        'validasi': validasi(jalur),
    }
    print(jalur, 'paket ditampilkan', len(paket), 'dengan SHAP', sum('shap' in p for p in paket))

data['total_rup'] = int(len(info))
data['rf_nama'] = list(NAMA_RF.values())
json.dump(data, open(OUT + 'dashboard-data.json', 'w'), ensure_ascii=False, default=conv)
for j in data['jalur']:
    print(j, data['jalur'][j]['paket'][0]['kalimat'])
    for r in data['jalur'][j]['validasi']:
        print(' -', r['status'], '|', r['uji'], '|', r['hasil'])
