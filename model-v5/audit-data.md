# Audit data dan pra-pemrosesan v5

Tanggal: 29 Oktober 2026. Kode: `s1_data.py` (pembersihan), `s2_model.py` (model, sama dengan v4), `b1_banding_v4.py` (perbandingan). Model v4 dan dashboard **tidak diubah**.

## 1. Keanehan yang ditemukan dan apa yang dilakukan

### Diperbaiki (aturan baru)

| Kode | Keanehan | Jumlah | Aturan v5 |
|---|---|---|---|
| B1 | Baris realisasi bernilai 0 atau negatif | 235 baris | Dibuang |
| B2 | Baris realisasi yang provinsinya berbeda dengan RUP-nya (misalnya RUP Jawa Timur tercatat di Jawa Barat) | 11 baris | Dibuang, karena kode RUP diduga salah ketik |
| B3 | **Catatan ganda**: satu kode RUP punya dua baris atau lebih dengan nilai sama persis sehingga realisasi melebihi pagu (contoh: RUP 53670226 Gaji PPSU, 2 × Rp4,79 M) | 980 paket, 1.362 baris | Baris bernilai sama dihitung sekali, **hanya bila** realisasinya melebihi pagu dan setelah digabung tidak lagi melebihi pagu. Pesanan berulang di bawah pagu tidak disentuh |
| B4 | Nilai UMK ditulis "100" (atau 1–100) padahal paketnya ratusan juta. 92% paket ini di RUP berstatus UMK = Ya, jadi angka itu persen, bukan rupiah | 379 baris | Dibaca sebagai persen |
| B5 | Rasio realisasi/pagu < 0,01 (realisasi hampir nol, misalnya Rp3.973 untuk pagu Rp4,6 jt) atau > 10 (sampai 1.000 kali pagu, diduga salah satuan) | 59 paket | Tidak masuk jalur pelaksanaan |
| C1 | Nama penyedia berulang dalam satu sel ("Serambi, Serambi") dan bentuk usaha yang tidak seragam ("PT X" vs "X") | 5.068 baris | Dirapikan. Bentuk usaha diabaikan saat mencocokkan penyedia untuk RF5 dan RF6 |
| C2 | Penyedia yang ternyata unit pemerintah, yaitu satker mencatat dirinya sendiri (contoh: "Kelurahan Pekayon", "Cabang Dinas Pendidikan Wil VI", "Bendahara Dinas Sosial") | 986 baris | Dianggap penyedia tidak diketahui untuk RF5 dan RF6 |

Dampaknya ke red flag:
- RF1 sampai RF4 tidak berubah.
- RF5 (penyedia dominan) turun dari 2.910 menjadi 2.640 paket.
- RF6 (penyedia serba ada) turun dari 4.766 menjadi 4.503 paket.

### Diperiksa, sengaja tidak diubah

| Keanehan | Jumlah | Alasan tidak diubah |
|---|---|---|
| RUP "kembar": satker, nama, pagu, metode, dan jenis sama, tetapi kode RUP berbeda (contoh: "Bahan Pemulihan Ekonomi Paket 1" dua kali di BPBD) | 19.564 paket dalam 6.950 kelompok | Kebanyakan belanja rutin kecil (median Rp2,7 jt). Pada banyak kelompok, tiap paket punya realisasinya sendiri, jadi memang pembelian terpisah. Pola berulang ini sudah ditangkap RF3 (pemecahan paket) |
| Pagu angka bulat (Rp100 jt, Rp200 jt, Rp190 jt, ...) | 18% paket kelipatan Rp1 jt | Wajar di tahap perencanaan. Pagu dekat batas sudah menjadi RF1 |
| Nama paket sangat pendek ("Snack", "Map", "-") atau tanpa huruf | 677 dan 22 paket | Jumlahnya kecil; hanya berpengaruh pada pencocokan nama RF3 |
| Metode tidak cocok dengan jenis (misalnya Seleksi untuk Barang, Tender untuk Konsultansi) | sekitar 60 paket | Jumlahnya sangat kecil |
| Satker di realisasi berbeda dengan satker di RUP (umumnya UPT dan dinas induknya, atau kelurahan dan kecamatannya) | 9.626 baris | Satker yang dipakai tetap satker di RUP |
| E-Katalog v5 mencatat per barang ("Kentang", "Oncom", ...) | ribuan baris | Sudah dijumlahkan per kode RUP sejak v1 |
| Realisasi > pagu yang tidak bisa dijelaskan oleh catatan ganda | 1.188 paket di jalur pelaksanaan (226 di antaranya sekitar 2 kali) | Bisa jadi memang terjadi, jadi tetap dihitung dan dinilai model |

## 2. Hasil: v4 vs v5

**Jalur perencanaan sama persis.** Pembersihan hanya menyentuh data realisasi, jadi 200 teratasnya 100% sama.

**Jalur pelaksanaan:**

| | v4 | v5 | Acuan |
|---|---|---|---|
| Paket bermasalah data di 200 teratas | **58** | **17** | – |
| … catatan ganda | 34 | 1 | – |
| … rasio ekstrem / UMK persen | 8 | 0 | – |
| … penyedia unit pemerintah | 22 | 17 | – |
| 200 teratas ber-red flag (definisi v3) | 48,0% | **50,0%** | 24,7% |
| 5% teratas ber-red flag | 29,2% | 28,9% | 24,7% |
| 5% teratas, provinsi uji | 25,3% | 25,0% | 24,7% |
| 200 teratas yang sama dengan v4 | – | 49% | – |

- Bagian atas daftar jadi jauh lebih bersih: paket yang naik karena kesalahan data turun dari 58 menjadi 17.
- Kesesuaian dengan red flag sedikit naik di 200 teratas, dan di 5% teratas tetap sama.
- Jalur pelaksanaan di 5% teratas tetap hanya sedikit di atas rata-rata, sama seperti v4.
- 17 paket yang tersisa adalah paket yang penyedianya satker sendiri. Ini tidak memengaruhi fitur, hanya label RF5 dan RF6.

**Varian tambahan: pelaksanaan juga tanpa pagu < Rp1 jt.** Hasilnya 5% teratas 30,4%, uji 26,3%, tetapi 200 teratas turun ke 45,5%. Hasilnya campuran, jadi tidak disarankan.

## 3. Pilihan lanjutan

1. **Pakai v5** di dashboard dan naskah, dengan subbab pra-pemrosesan berisi 7 aturan di atas. Ini yang disarankan.
2. v5 ditambah satu aturan lagi: paket yang penyedianya satker sendiri dikeluarkan dari jalur pelaksanaan, karena lebih mirip swakelola. Jumlahnya 885 paket.
3. Tetap v4, dan keanehan data ditulis sebagai batasan.
