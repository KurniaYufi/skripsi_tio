"""Scraping halaman detail paket penyedia RUP (INAPROC) dengan Playwright, untuk uji coba 2.000 paket.

Persiapan (sekali saja, di komputer Tio):
    pip install playwright pandas
    playwright install chromium

Langkah 1 - cari pola URL:
    Buka satu halaman detail paket di browser, misalnya kode 57565725, lalu salin URL-nya.
    Ganti angka kode RUP di URL itu dengan {kode}. Contoh bentuknya (BUKAN URL asli):
        https://contoh.inaproc.id/rup/detail/{kode}

Langkah 2 - uji satu paket (hasil dicetak, HTML + teks + screenshot + JSON jaringan disimpan di folder cek/):
    python scrape_rup.py --url "https://.../{kode}" --cek 57565725 --tampil

    Pastikan 23 kolom terbaca dan nilainya sama dengan CSV yang Tio unduh manual.
    Kalau ada yang kosong, kirim isi folder cek/ supaya cara membacanya bisa disesuaikan.

Langkah 3 - jalankan semua (bisa dihentikan dengan Ctrl+C dan dilanjutkan; paket yang sudah berhasil dilewati):
    python scrape_rup.py --url "https://.../{kode}"

Hasil:
    hasil/mentah.jsonl     satu baris per paket: kode, status, teks halaman, kolom terbaca (bisa dibaca ulang tanpa scraping lagi)
    hasil/detail_rup.csv   tabel lebar: satu baris per paket, satu kolom per Deskripsi

Etika: jeda acak 1,5-3 detik antar paket, satu tab saja, berhenti otomatis kalau 10 kali berturut-turut gagal
(kemungkinan diblokir, captcha, atau situs sedang gangguan). Jangan kecilkan jedanya dan jangan memaksa melewati captcha.
"""
import argparse, json, os, random, re, sys, time
from pathlib import Path

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

# 23 label dari contoh CSV "detail_paket_penyedia_*.csv"
LABEL = [
    'Kode RUP', 'Nama Paket', 'Nama KLPD', 'Satuan Kerja', 'Tahun Anggaran', 'Metode Pemilihan', 'Jenis Pengadaan',
    'Total Pagu', 'Volume Pekerjaan', 'Uraian Pekerjaan', 'Spesifikasi Pekerjaan', 'Produk Dalam Negeri',
    'Usaha Kecil/Koperasi', 'Pra DIPA / DPA', 'Aspek Ekonomi', 'Aspek Sosial', 'Aspek Lingkungan',
    'Jadwal Pemilihan Penyedia Mulai', 'Jadwal Pemilihan Penyedia Akhir',
    'Jadwal Pelaksanaan Kontrak Mulai', 'Jadwal Pelaksanaan Kontrak Akhir',
    'Pemanfaatan Barang/Jasa Mulai', 'Pemanfaatan Barang/Jasa Akhir',
]
DIR = Path(__file__).resolve().parent
OUT = DIR / 'hasil'

# Dijalankan di halaman: cari elemen terdalam yang teksnya sama dengan label, lalu ambil teks elemen sesudahnya
# (sel tabel berikutnya, <dd> sesudah <dt>, atau kolom berikutnya). Naik sampai 3 tingkat kalau perlu.
JS_BACA = r"""
(labels) => {
  const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const bersih = (s) => norm(s).replace(/^[:\s]+/, '');
  const sama = (t, lab) => t.replace(/[:\s]+$/, '').toLowerCase() === lab.toLowerCase();
  const semua = Array.from(document.querySelectorAll('body *'));
  const out = {};
  for (const lab of labels) {
    const cocok = semua.filter((e) => sama(norm(e.textContent), lab) &&
      !Array.from(e.children).some((c) => sama(norm(c.textContent), lab)));
    if (!cocok.length) continue;
    let cur = cocok[0], v = null;
    for (let i = 0; i < 3 && cur && v === null; i++) {
      let sib = cur.nextElementSibling;
      while (sib && !bersih(sib.textContent)) sib = sib.nextElementSibling;
      if (sib) v = bersih(sib.textContent);
      cur = cur.parentElement;
    }
    if (v !== null && labels.some((l) => sama(v, l))) v = null;  // yang terbaca ternyata label lain
    out[lab] = v;
  }
  return out;
}
"""


def baca_teks(teks):
    """Cadangan dari teks halaman: baris yang sama dengan label, nilainya = baris tidak kosong berikutnya
    (atau sisa baris yang sama kalau formatnya 'Label: nilai' / 'Label<TAB>nilai')."""
    baris = [b.strip() for b in teks.splitlines()]
    out = {}
    for i, b in enumerate(baris):
        for lab in LABEL:
            if lab in out:
                continue
            m = re.match(rf'^{re.escape(lab)}\s*[:\t]?\s*(.*)$', b, flags=re.I)
            if not m:
                continue
            v = m.group(1).strip()
            if not v:
                v = next((x for x in baris[i + 1:i + 4] if x), '')
            if v and not any(v.lower() == l.lower() for l in LABEL):
                out[lab] = v
    return out


def ambil(page, url, tunggu):
    resp = page.goto(url, wait_until='domcontentloaded', timeout=45000)
    try:
        page.wait_for_load_state('networkidle', timeout=15000)
    except PWTimeout:
        pass
    # tunggu sampai label kunci muncul (halaman yang dirender JavaScript)
    try:
        page.get_by_text('Total Pagu', exact=False).first.wait_for(timeout=tunggu * 1000)
    except PWTimeout:
        pass
    teks = page.inner_text('body')
    kolom = page.evaluate(JS_BACA, LABEL)
    cadangan = baca_teks(teks)
    for k, v in cadangan.items():
        if not kolom.get(k):
            kolom[k] = v
    kolom = {k: v for k, v in kolom.items() if v}
    return (resp.status if resp else None), teks, kolom


def cek(args):
    d = DIR / 'cek'
    d.mkdir(exist_ok=True)
    jaringan = []
    with sync_playwright() as p:
        br = p.chromium.launch(headless=not args.tampil)
        page = br.new_page()

        def simpan_json(r):
            try:
                if 'json' in (r.headers.get('content-type') or ''):
                    body = r.text()
                    jaringan.append({'url': r.url, 'status': r.status, 'ada_kode': args.cek in body, 'isi': body[:20000]})
            except Exception:
                pass
        page.on('response', simpan_json)
        status, teks, kolom = ambil(page, args.url.format(kode=args.cek), args.tunggu)
        (d / f'{args.cek}.html').write_text(page.content(), encoding='utf-8')
        (d / f'{args.cek}.txt').write_text(teks, encoding='utf-8')
        page.screenshot(path=str(d / f'{args.cek}.png'), full_page=True)
        br.close()
    (d / f'{args.cek}_jaringan.json').write_text(json.dumps(jaringan, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'HTTP {status}. Kolom terbaca: {len(kolom)} dari {len(LABEL)}')
    for lab in LABEL:
        print(f'  {lab:35s} {kolom.get(lab, "-- TIDAK TERBACA --")}')
    api = [j['url'] for j in jaringan if j['ada_kode']]
    if api:
        print('\nRespons JSON yang memuat kode ini (mungkin API yang lebih cepat dipakai):')
        for u in api:
            print('  ', u)
    print(f'\nFile cek tersimpan di {d}')


def jalan(args):
    OUT.mkdir(exist_ok=True)
    mentah = OUT / 'mentah.jsonl'
    sampel = pd.read_csv(args.input, dtype={'kode_rup': str})
    kode = sampel.kode_rup.tolist()
    if args.batas:
        kode = kode[:args.batas]
    selesai = set()
    if mentah.exists():
        for b in mentah.read_text(encoding='utf-8').splitlines():
            try:
                r = json.loads(b)
                if r.get('status') == 'ok':
                    selesai.add(r['kode'])
            except json.JSONDecodeError:
                pass
    sisa = [k for k in kode if k not in selesai]
    print(f'{len(selesai)} paket sudah ada, {len(sisa)} paket akan diambil.')
    gagal_beruntun = 0
    with sync_playwright() as p, open(mentah, 'a', encoding='utf-8') as f:
        br = p.chromium.launch(headless=not args.tampil)
        page = br.new_page()
        for i, k in enumerate(sisa, 1):
            rec = {'kode': k, 'url': args.url.format(kode=k), 'waktu': time.strftime('%Y-%m-%d %H:%M:%S')}
            for coba in range(3):
                try:
                    status, teks, kolom = ambil(page, rec['url'], args.tunggu)
                    ok = status == 200 and len(kolom) >= 10 and kolom.get('Kode RUP', k).replace('.', '') == k
                    rec.update(status='ok' if ok else 'kurang', http=status, n_kolom=len(kolom), kolom=kolom, teks=teks[:20000])
                    if ok:
                        break
                except Exception as e:  # jaringan putus, timeout, dll.
                    rec.update(status='error', error=str(e)[:300])
                time.sleep(5 * (coba + 1))
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
            f.flush()
            gagal_beruntun = 0 if rec['status'] == 'ok' else gagal_beruntun + 1
            print(f'[{i}/{len(sisa)}] {k}: {rec["status"]} ({rec.get("n_kolom", 0)} kolom)')
            if gagal_beruntun >= 10:
                print('10 paket berturut-turut gagal. Berhenti dulu: cek apakah situs memblokir, minta captcha, atau sedang gangguan.')
                break
            time.sleep(random.uniform(args.jeda, args.jeda * 2))
        br.close()
    tabel(mentah)


def tabel(mentah):
    rows = []
    for b in mentah.read_text(encoding='utf-8').splitlines():
        r = json.loads(b)
        if r.get('status') == 'ok':
            rows.append({'kode_rup': r['kode'], **r['kolom']})
    if not rows:
        print('Belum ada paket yang berhasil.')
        return
    df = pd.DataFrame(rows).drop_duplicates('kode_rup', keep='last').reindex(columns=['kode_rup'] + LABEL)
    df.to_csv(OUT / 'detail_rup.csv', index=False)
    print(f'{len(df)} paket tersimpan di {OUT / "detail_rup.csv"}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True, help='pola URL halaman detail, dengan {kode} di tempat kode RUP')
    ap.add_argument('--input', default=str(DIR / 'sampel_scraping.csv'))
    ap.add_argument('--cek', help='uji satu kode RUP saja')
    ap.add_argument('--jeda', type=float, default=1.5, help='jeda minimum antar paket (detik); jeda acak = jeda sampai 2x jeda')
    ap.add_argument('--tunggu', type=int, default=20, help='batas menunggu isi halaman muncul (detik)')
    ap.add_argument('--batas', type=int, help='ambil N paket pertama saja (untuk uji)')
    ap.add_argument('--tampil', action='store_true', help='tampilkan jendela browser')
    a = ap.parse_args()
    if '{kode}' not in a.url:
        sys.exit('URL harus memuat {kode}, misalnya https://.../detail/{kode}')
    cek(a) if a.cek else jalan(a)
