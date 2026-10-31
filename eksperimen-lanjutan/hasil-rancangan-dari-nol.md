# Hasil uji rancangan dari nol (30 Oktober 2026)

**Pertanyaan Tio:** apakah rancangan fitur dan red flag "dari nol" ([rancangan-dari-nol.md](rancangan-dari-nol.md)) hasilnya lebih bagus dari model sekarang?

**Jawaban singkat: tidak.** Rancangan dari nol tidak lebih bagus.
- Perencanaan: setara atau lebih buruk.
- Pelaksanaan: lebih buruk.

Model sekarang tetap yang terbaik di antara yang dicoba. Model, naskah, dan dashboard tidak diubah.

## Yang dijalankan

**Fitur baru dihitung untuk 2024 dan 2025:**
- pagu dibanding jenis saja (tanpa metode);
- pagu dibanding paket bernama sama di satker tahun lalu (hanya 2025);
- lonjakan pagu satker × jenis dari tahun lalu (hanya 2025);
- kekaburan nama;
- UMK tidak dicadangkan;
- selisih PDN dan selisih UMK (pelaksanaan).

**Red flag rancangan:**
- dari set lama: RF1, RF3, RF4, RF6;
- baru: R050 (per satker × jenis), R052 (kecil lalu besar, hanya 2025), Pasal 38 ayat (8) (hanya 2025).

**Tujuh varian dilatih dengan pengaturan yang sama dengan model sekarang** (5 seed, IF + LOF + AE):

| Varian | Jalur | Isi |
|---|---|---|
| penuh | perencanaan 2025 | 8 fitur |
| lintas | perencanaan 2025 | 4 fitur dasar + 2 fitur tahun lalu |
| tanpalintas | perencanaan 2024 dan 2025 | 6 fitur tanpa tahun lalu |
| penuh | pelaksanaan 2024 dan 2025 | 7 fitur |
| tanpapdnumk | pelaksanaan 2025 | 5 fitur tanpa PDN/UMK |

**Dua set red flag sebagai penguji:**
- set lama, dengan paket RF2 dikeluarkan dari daftar;
- set rancangan.

**Pembanding tanpa model:** acak, urut pagu, pagu dibanding jenis, dan rata-rata skor-z.

**Ukuran yang dipakai:**
- lipat 5% teratas;
- **lipat terkontrol pagu + metode**: dibanding paket acak dengan komposisi besar pagu dan metode yang sama;
- P@200;
- p hipergeometrik.

## Masalah yang ditemukan dan diperbaiki dulu

1. **Fitur tahun lalu (versi pertama) salah.** SHAP terbesar di 92 dari 200 paket teratas berasal dari fitur ini. Penyebabnya, pembandingnya paket 2024 berpagu Rp10–50 rb. Contoh: "Bahan Cetak" di Maluku, 2025 Rp10 jt dibanding 2024 Rp20 rb, jadi tampak naik 500 kali.
   - Perbaikan: pembanding hanya paket 2024 berpagu ≥ Rp1 jt dan bernama spesifik.
   - Setelah diperbaiki, hanya 9,7% paket punya pembanding tahun lalu.
   - Versi lama disimpan di rancangan/versi1-tanpa-batas/.
2. **Pelaksanaan penuh gagal cek SHAP.** Selisih PDN menjadi alasan terbesar di **155 dari 200** paket teratas, dan 74% paket teratas adalah E-Purchasing. Ini masalah yang sama dengan audit v5: fitur yang 97% bernilai 0 membuat yang 1 tampak "aneh".

## Hasil utama (2025 semua / 2025 provinsi uji)

### Perencanaan, red flag set lama tanpa RF2

| Skor | Lipat 5% | Lipat terkontrol | P@200 |
|---|---|---|---|
| **Model sekarang** | **1,34 / 1,14** | **1,11 / 1,05** | 3% / 7% |
| Rancangan penuh | 0,85 / 0,71 | 0,99 / 0,89 | 7% / 8% |
| Rancangan lintas (fitur tahun lalu) | 0,87 / 0,78 | 1,06 / 0,97 | 8% / 12% |
| Rancangan tanpa lintas | 1,02 / 0,87 | 1,12 / 1,05 | 8% / 6% |
| Acak | 1,01 / 0,99 | 1,02 / 1,01 | 11% / 12% |

Di 2024, rancangan tanpa lintas: lipat 0,73 dan terkontrol 0,98. Model sekarang: 1,00 dan 0,93.

### Pelaksanaan, red flag set rancangan

| Skor | Lipat 5% | Lipat terkontrol | P@200 |
|---|---|---|---|
| **Model sekarang** | **1,31 / 1,17** | 1,04 / 1,13 | **40% / 53%** |
| Rancangan penuh | 0,87 / 0,84 | 0,96 / 1,00 | 26% / 24% |
| Rancangan tanpa PDN/UMK | 1,06 / 1,02 | 0,99 / 1,10 | 44% / 38% |
| Acak | 0,99 / 0,98 | 1,01 / 1,01 | 26% / 27% |

Dengan red flag set lama tanpa RF2, polanya sama:
- model sekarang 0,90 / 0,86;
- rancangan tanpa PDN/UMK 0,81 / 0,84;
- rancangan penuh 0,69 / 0,78.

Tabel lengkap ada di rancangan/j3_eval.csv.

## Kesimpulan

1. **Fitur tahun lalu tidak menaikkan keselarasan dengan red flag.** Fitur ini mudah dijelaskan ("naik 10 kali dari tahun lalu"), tetapi hanya 10% paket punya pembanding. Selain itu, red flag perencanaan (PL dekat ambang, pemecahan, penunjukan langsung) tidak berhubungan dengan kenaikan dari tahun lalu.
2. **Fitur jarang (PDN, UMK) merusak.** Pelajaran audit v5 terulang.
3. **Pagu dibanding jenis saja tidak lebih baik** dari pagu dibanding jenis + metode. Varian tanpa lintas setara dengan model sekarang setelah dikontrol, tetapi lebih rendah di lipat biasa.
4. **Mengganti set red flag lebih berpengaruh daripada mengganti fitur.**
   - Dengan model yang sama, lipat pelaksanaan 2025 naik dari 0,90 (set lama tanpa RF2) menjadi 1,31 (set rancangan), dengan p < 0,001.
   - Tetapi setelah dikontrol pagu dan metode, kenaikannya tinggal 1,04 / 1,13.
   - Red flag baru ini dipilih setelah melihat hasil, jadi catatannya sama dengan [kandidat-red-flag-baru.md](kandidat-red-flag-baru.md).
5. **P@200 perencanaan memang selalu di bawah acak.** Red flag perencanaan hanya bisa berlaku di PL dan Penunjukan Langsung (±43% paket), sedangkan puncak peringkat banyak berisi E-Purchasing. Ini sudah dibahas di laporan eksperimen lanjutan.

**Saran:** tetap pakai model sekarang. Rancangan dari nol bisa disebut di Bab 5 sebagai percobaan tambahan: fitur lintas tahun dan fitur PDN/UMK sudah diuji dan tidak memperbaiki hasil.

## File

- j1_fitur_rancangan.py: fitur dan red flag rancangan → rancangan/fitur_*.pkl, rf_*.pkl
- j2_latih_rancangan.py: latih 7 varian → rancangan/skor_*.pkl, model_*.pkl
- j3_eval_rancangan.py → rancangan/j3_eval.csv
- j4_shap_rancangan.py: cek SHAP dan komposisi 200 teratas → rancangan/shap_*.pkl, log/j4_*.log
