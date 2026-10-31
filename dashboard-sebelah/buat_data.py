"""Ubah data dashboard project "TRAIN ANOMALY DETECTION" ke skema dashboard project ini.

Masukan : data_sebelah.json (DATA yang tertanam di dashboard project sebelah)
Keluaran: dashboard-data-sebelah.json (skema sama dengan model-v5/dashboard-data.json)

Angka per paket diambil dari dashboard sebelah. Angka evaluasi model lain (IF, LOF, AE,
pembanding) dan hasil uji diambil dari laporan project sebelah, karena dashboard mereka
hanya memuat 200 paket teratas nasional per jalur.
"""
import json, math, re, sys

src = sys.argv[1] if len(sys.argv) > 1 else 'data_sebelah.json'
out = sys.argv[2] if len(sys.argv) > 2 else '/mnt/project-files/dashboard-sebelah/dashboard-data-sebelah.json'
D = json.load(open(src))

RF = {  # kode: (nama, bersih?, jumlah kena, yang perlu dicek)
    'P1': ('Indikasi pemecahan paket', True, 18191, 'Apakah paket-paket bernama sama ini sebenarnya satu kegiatan yang bisa digabung?'),
    'P2': ('Pagu 90–100% ambang pengadaan langsung', False, 7326, 'Apakah pagu dihitung dari kebutuhan, atau dibuat sedikit di bawah batas?'),
    'P3': ('Pengadaan langsung melebihi ambang', False, 7009, 'Apakah metode yang tercatat memang sesuai nilai paket?'),
    'P4': ('Penunjukan langsung melebihi ambang', True, 666, 'Apakah alasan penunjukan langsung tercatat dan sesuai aturan?'),
    'P5': ('Paket ≤ Rp15 M tidak dicadangkan untuk usaha kecil', True, 9411, 'Apakah ada alasan paket ini tidak dicadangkan untuk usaha kecil?'),
    'P6': ('Direncanakan bukan produk dalam negeri', True, 4748, 'Apakah memang tidak ada produk dalam negeri yang setara?'),
    'E1': ('Realisasi melebihi pagu', False, 1276, 'Apakah ada perubahan kontrak yang sah, atau salah catat?'),
    'E2': ('Nilai tender ≥ 99% pagu', False, 483, 'Apakah penawaran benar-benar bersaing?'),
    'E3': ('Metode realisasi berbeda dari RUP', True, 139, 'Apakah perubahan metode tercatat dan beralasan?'),
    'E4': ('PDN realisasi < 50% padahal RUP PDN', True, 6623, 'Apakah barang yang dibeli memang bukan produk dalam negeri?'),
    'E5': ('UMK realisasi < 50% padahal dicadangkan', True, 16119, 'Apakah penyedia memang bukan usaha kecil, dan kenapa?'),
    'E6': ('Penyedia menguasai ≥ 50% paket non-katalog satker', True, 495, 'Apakah penyedia ini menang lewat persaingan yang sehat?'),
}
def nama_rf(c):
    n, bersih = RF[c][0], RF[c][1]
    return n if bersih else n + ' (bocor)'

NAMA_FITUR = {
    'z_pagu_kelompok': 'Pagu dibanding paket sejenis',
    'z_pagu_satker': 'Pagu dibanding paket di satker',
    'log_pangsa_pagu_satker': 'Porsi pagu satker yang diserap',
    'kebulatan_pagu': 'Kebulatan pagu',
    'log_pagu_kembar_satker': 'Pagu kembar di satker',
    'pangsa_nilai_nonkompetitif_satker': 'Porsi non-kompetitif satker',
    'z_rasio_real_pagu': 'Realisasi dibanding pagu',
    'log_jangkauan_penyedia': 'Jangkauan penyedia',
    'log_nilai_vs_kebiasaan_penyedia': 'Nilai dibanding kebiasaan penyedia',
}
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
pct = lambda x, d=1: f"{x*100:.{d}f}".replace('.', ',') + '%'
ang = lambda x, d=1: f"{x:.{d}f}".replace('.', ',')

def uraian(f, v, p):
    if f in ('z_pagu_kelompok', 'z_pagu_satker', 'z_rasio_real_pagu'):
        q = Phi(v)
        kel = {'z_pagu_kelompok': 'paket sejenis dengan metode yang sama',
               'z_pagu_satker': 'paket lain di satker yang sama',
               'z_rasio_real_pagu': 'paket sebanding (jenis, metode, besar pagu)'}[f]
        obj = 'rasio realisasi/pagu' if f == 'z_rasio_real_pagu' else 'pagu'
        if f == 'z_pagu_satker' and v == 0:
            return 'nilainya 0: satker punya kurang dari 5 paket, atau paket berada tepat di tengah'
        return f"{obj} lebih {'besar' if v >= 0 else 'kecil'} dari {pct(q if v >= 0 else 1-q, 2)} {kel} (posisi {ang(v, 2).replace('-', '−')})"
    if f == 'log_pangsa_pagu_satker':
        return f"paket ini menyerap {pct(10**v)} dari total pagu satker"
    if f == 'kebulatan_pagu':
        return f"tingkat kebulatan {ang(v, 2)} (1 = semua angka di belakang nol, 0 = tidak bulat)"
    if f == 'log_pagu_kembar_satker':
        n = round(10**v)
        return 'tidak ada paket lain di satker dengan pagu persis sama' if v == 0 else f"{n} paket di satker ini punya pagu persis sama"
    if f == 'pangsa_nilai_nonkompetitif_satker':
        return f"{pct(v)} nilai pagu satker memakai pengadaan/penunjukan langsung"
    if f == 'log_jangkauan_penyedia':
        return f"penyedia utama melayani {round(10**v)} satker"
    if f == 'log_nilai_vs_kebiasaan_penyedia':
        r = 10**v
        if v == 0:
            return 'tidak dihitung: penyedia punya kurang dari 3 paket'
        return (f"nilai paket {ang(r)} kali nilai tengah paket penyedia ini" if r >= 1
                else f"nilai paket hanya {pct(r, 2 if r < 0.01 else 1)} dari nilai tengah paket penyedia ini")
    return ang(v, 2)

def poin_dari_kalimat(k):
    m = re.search(r'terutama karena (.*?)\. Perlu ditelaah', k or '')
    if not m:
        return []
    parts = re.split(r'; dan |; ', m.group(1))
    return [s[0].upper() + s[1:] + '.' for s in parts if s]

TEKS = {  # dari laporan project sebelah
    'perencanaan': {
        'acuan': 0.089,
        'lain': [  # model, P@100, P@200
            ('IF', 0.066, 0.068), ('LOF', 0.070, 0.063), ('AE', 0.110, 0.265),
            ('Aturan satu fitur (pagu vs sejenis)', 0.100, 0.090, True), ('Pagu terbesar', 0.070, 0.045, True)],
        'validasi': [
            ('Paket teratas lebih sering punya red flag (bersih)?', '200 teratas: 7,1% (rentang 5 seed 6,0–8,5%), acak 8,9%, jadi 0,80× acak. 5% teratas: 1,11× acak.', 'Setara acak terhadap red flag yang tidak bocor.', 'tidak'),
            ('Berlaku juga di provinsi uji (8 provinsi)?', '5% teratas 1,53× acak, 1% teratas 1,66×. Aturan satu fitur (pagu vs sejenis) 2,70× di 5% teratas.', 'Lebih baik dari acak, tetapi kalah dari aturan satu fitur.', 'sebagian'),
            ('Red flag bocor dikeluarkan dari acuan?', 'P2 dan P3 dapat ditebak hampir sempurna oleh satu fitur (AUC 0,90–1,00).', 'Angka P@K utama tidak menyontek dari aturan yang sama.', 'ya'),
            ('Anomali buatan naik peringkat?', 'Pagu ×30: masuk 5% teratas 5,7% → 13,3%. Pagu ×30 dan dibulatkan: → 34,3%.', 'Bereaksi, tetapi hanya sedang terhadap pagu yang dinaikkan.', 'sebagian'),
            ('SHAP menunjuk faktor yang benar?', '3 fitur SHAP teratas dinetralkan: skor 0,99 → 0,56 (100% paket turun). 3 fitur acak: → 0,85.', 'Penjelasan SHAP memang menunjuk penggerak skor.', 'ya'),
            ('Stabil bila seed diganti?', 'Irisan 200 teratas antar-seed rata-rata 0,735 (0,635–0,805).', 'Sekitar seperempat isi 200 teratas berganti.', 'sebagian'),
            ('Telaah manual 40 teratas', '15 layak ditelaah, 11 kesalahan data (mis. pagu Rp1.958), 14 wajar.', 'Banyak salah isi data di puncak karena pagu sangat kecil tidak dibuang.', 'tidak'),
        ]},
    'pelaksanaan': {
        'acuan': 0.179,
        'lain': [
            ('IF', 0.288, 0.316), ('LOF', 0.066, 0.078), ('AE', 0.192, 0.189),
            ('Aturan satu fitur (jangkauan penyedia)', 0.208, 0.201, True), ('Pagu terbesar', 0.120, 0.140, True)],
        'validasi': [
            ('Paket teratas lebih sering punya red flag (bersih)?', '200 teratas: 31,4% (rentang seed 29,5–33,0%), acak 17,9%, jadi 1,75× acak. 5% teratas: 1,14×.', 'Lebih tinggi dari acak di daftar teratas.', 'sebagian'),
            ('Tetap unggul tanpa red flag E6?', 'Tanpa E6 (penyedia dominan): 1,42× di K = 100–200, 0,98× di 5% teratas.', 'Keunggulan terutama dari E6, yang berkaitan dengan fitur porsi non-kompetitif satker.', 'tidak'),
            ('Berlaku juga di provinsi uji (8 provinsi)?', '1% teratas 1,87× acak, 5% teratas 1,47×. Pagu terbesar 1,68× di 5% teratas.', 'Lebih baik dari acak, tetapi tidak lebih baik dari urutan pagu.', 'sebagian'),
            ('Red flag bocor dikeluarkan dari acuan?', 'E1 dan E2 dapat ditebak oleh satu fitur (AUC ≥ 0,85).', 'Angka P@K utama tidak menyontek dari aturan yang sama.', 'ya'),
            ('Anomali buatan naik peringkat?', 'Realisasi 2,5× pagu: masuk 5% teratas 5,3% → 75%. Pagu dan realisasi ×50: → 24%.', 'Kuat untuk realisasi jauh di atas pagu, sedang untuk paket yang sekadar besar.', 'sebagian'),
            ('SHAP menunjuk faktor yang benar?', '3 fitur SHAP teratas dinetralkan: skor 0,99 → 0,51 (100% paket turun). 3 fitur acak: → 0,88.', 'Penjelasan SHAP memang menunjuk penggerak skor.', 'ya'),
            ('Stabil bila seed diganti?', 'Irisan 200 teratas antar-seed rata-rata 0,756 (0,700–0,810).', 'Sekitar seperempat isi 200 teratas berganti.', 'sebagian'),
            ('Telaah manual 40 teratas', '15 layak ditelaah, 6 kesalahan data (mis. realisasi Rp720), 19 wajar.', 'Kurang dari separuh layak ditelaah.', 'tidak'),
        ]},
}

hasil = {'jalur': {}, 'versi': 'project sebelah', 'total_rup': 339608,
         'rf_nama': [], 'rf_cek': {}}
for c, (n, bersih, cnt, cek) in RF.items():
    hasil['rf_cek'][nama_rf(c)] = cek

for jalur, X in D.items():
    pref = 'P' if jalur == 'perencanaan' else 'E'
    bersih = [c for c in RF if c.startswith(pref) and RF[c][1]]
    up2geo = {p['provinsi']: p['nama_geojson'] for p in X['provinsi']}
    prov = {p['nama_geojson']: {'n': p['n_paket'], 'anomali': p['n_anomali'], 'proporsi': p['proporsi_anomali'],
                                'pagu_anomali': None, 'ci': [p['ci95_bawah'], p['ci95_atas']]} for p in X['provinsi']}
    n = sum(p['n_paket'] for p in X['provinsi'])
    paket, sg = [], {}
    for p in X['paket']:
        kode = [c for c in (p['red_flag'] or '').split(',') if c]
        sh = sorted(([NAMA_FITUR[f], round(v, 4), uraian(f, p['nilai'][f], p), f] for f, v in p['shap'].items()),
                    key=lambda d: -abs(d[1]))
        for d in sh:
            sg[d[0]] = sg.get(d[0], 0) + abs(d[1])
        paket.append({
            'kode': p['kode_rup'], 'rank': p['peringkat'], 'skor': round(p['skor'], 4),
            'IF': None, 'LOF': None, 'AE': None,
            'prov': up2geo.get(p['provinsi'], p['provinsi'].title()),
            'satker': p['satker'].split(' - ')[0], 'nama': p['nama'], 'metode': p['metode'], 'jenis': p['jenis'],
            'pagu': p['pagu'], 'rf': [nama_rf(c) for c in kode], 'kode_rf': kode,
            'realisasi': p['nilai_real'], 'penyedia': p['penyedia'] or '–', 'sumber': '–',
            'bukti': [{'rf': nama_rf(c), 'ringkas': f"{c}: {RF[c][0]}." + ('' if RF[c][1] else ' Red flag ini bocor (bisa ditebak dari fitur), jadi tidak dipakai untuk menilai model.')} for c in kode],
            'shap': sh, 'poin': poin_dari_kalimat(p['kalimat']), 'kalimat': p['kalimat'],
        })
    paket.sort(key=lambda r: r['rank'])

    def prec(k):
        top = paket[:k]
        kena = [len([c for c in r['kode_rf'] if c in bersih]) for r in top]
        return round(sum(1 for x in kena if x) / k, 3), round(sum(kena) / k, 3)
    T = TEKS[jalur]
    ev = {'model': 'Ensemble'}
    for k in (50, 100, 200):
        ev['P@%d' % k], ev['rata_rf@%d' % k] = prec(k)
    rows = [ev]
    for r in T['lain']:
        row = {'model': r[0], 'P@50': None, 'P@100': r[1], 'P@200': r[2],
               'rata_rf@50': None, 'rata_rf@100': None, 'rata_rf@200': None}
        if len(r) > 3:
            row['pembanding'] = True
        rows.append(row)
    a = T['acuan']
    rows.append({'model': 'Semua paket (acuan)', 'P@50': a, 'P@100': a, 'P@200': a,
                 'rata_rf@50': None, 'rata_rf@100': None, 'rata_rf@200': None})

    rf_total = {nama_rf(c): RF[c][2] for c in RF if c.startswith(pref)}
    shap_global = dict(sorted(((k, round(v / len(paket), 4)) for k, v in sg.items()), key=lambda x: -x[1]))
    anomali = sum(p['n_anomali'] for p in X['provinsi'])
    hasil['jalur'][jalur] = {
        'n': n, 'anomali': anomali, 'ambang': None, 'nasional': X['nasional'], 'prov': prov, 'paket': paket,
        'eval': rows, 'rf_total': rf_total, 'rf_bersih': [nama_rf(c) for c in bersih],
        'shap_global': shap_global,
        'validasi': [dict(zip(('uji', 'hasil', 'arti', 'status'), v)) for v in T['validasi']],
    }
    print(jalur, 'n', n, 'anomali', anomali, 'paket', len(paket), 'eval ensemble', ev)
hasil['rf_nama'] = list(hasil['rf_cek'])
json.dump(hasil, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print('tulis', out)
