# Scraping detail RUP: uji coba 2.000 paket

Folder ini berisi tiga file utama:
- `sampel_scraping.csv`: 2.000 kode RUP jalur perencanaan, yaitu 1.000 skor tertinggi dan 1.000 acak (seed 42, di luar 1.000 teratas). Kolom: kelompok, peringkat, skor, provinsi, satker, nama paket, metode, jenis, pagu.
- `scrape_rup.py`: mengambil halaman detail tiap paket dengan Playwright.
- `analisis_scraping.py`: membandingkan kelompok teratas dengan kelompok acak.

## 1. Persiapan (sekali saja)

```
pip install playwright pandas
playwright install chromium
```

## 2. Cari pola URL

Buka satu halaman detail paket di browser, misalnya kode 57565725, lalu salin URL-nya. Ganti angka kodenya dengan `{kode}`.

Kalau kode tidak muncul di URL (misalnya halaman dibuka lewat pencarian atau pop-up), kirim saja URL dan screenshot-nya. Script-nya nanti disesuaikan.

## 3. Uji satu paket

```
python scrape_rup.py --url "https://ALAMAT/.../{kode}" --cek 57565725 --tampil
```

Yang perlu dicek:
- Layar harus menampilkan `Kolom terbaca: 23 dari 23`, dan nilainya sama dengan CSV yang diunduh manual.
- Kalau ada kolom yang kosong, kirim isi folder `cek/` (HTML, teks, screenshot, JSON jaringan). Dari situ cara membaca halamannya bisa disesuaikan.
- Kalau di bawah muncul "Respons JSON yang memuat kode ini", kirim juga. Itu kemungkinan API situsnya, dan memakainya jauh lebih ringan daripada membuka halaman satu per satu.

## 4. Jalankan

Coba 20 paket dulu:
```
python scrape_rup.py --url "https://ALAMAT/.../{kode}" --batas 20
```

Kalau lancar, jalankan semua:
```
python scrape_rup.py --url "https://ALAMAT/.../{kode}"
```

Cara kerjanya:
- Jeda antar paket diacak 1,5–3 detik, jadi 2.000 paket butuh sekitar 1,5–2,5 jam.
- Bisa dihentikan dengan Ctrl+C, lalu dijalankan lagi dengan perintah yang sama. Paket yang sudah berhasil dilewati.
- Script berhenti sendiri kalau 10 paket berturut-turut gagal, misalnya karena diblokir, diminta captcha, atau situs sedang gangguan. Kalau ini terjadi, tunggu dulu. Jangan kecilkan jedanya dan jangan memaksa melewati captcha.

Hasilnya ada di folder `hasil/`:
- `mentah.jsonl`: teks halaman per paket, bisa dibaca ulang tanpa scraping lagi.
- `detail_rup.csv`: satu baris per paket, 23 kolom.

## 5. Analisis

```
python analisis_scraping.py
```

Hasilnya `hasil/ringkasan.md` dan `hasil/tanda_per_paket.csv`. Yang dibandingkan antara teratas dan acak:

- Uraian atau spesifikasi tidak informatif:
  - kosong;
  - hanya merujuk KAK/TOR/dokumen, misalnya "Uraian pekerjaan pada KAK";
  - sama persis dengan nama paket.
- Volume berupa angka selain "1 Paket", misalnya "88x13".
- Jadwal:
  - pemilihan berakhir November–Desember;
  - pemilihan dimulai sebelum 2025;
  - kontrak hanya 1 bulan;
  - kontrak dimulai sebelum pemilihan.
- Pra DIPA.

Unggah `hasil/detail_rup.csv` dan `hasil/ringkasan.md` ke thread. Kalau tanda "tidak informatif" jauh lebih sering di kelompok teratas, baru layak dipertimbangkan scraping semua paket dan menjadikannya red flag baru.

Script ini sudah diuji pada halaman tiruan dengan tiga bentuk tampilan: tabel, daftar `dt/dd`, dan halaman yang diisi JavaScript. Halaman INAPROC asli belum bisa diuji dari sini, jadi langkah 3 penting.
