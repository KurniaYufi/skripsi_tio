# Hasil latih ulang dan audit detail (29 Oktober 2026 malam)

Permintaan Tio: latih ulang, perhatikan setiap fitur di tiap jalur, cari keanehan sebelum, waktu, dan setelah latih, lalu perbaiki sendiri.

**Yang saya lakukan:** melatih ulang **6 putaran**. Setiap putaran saya cek tiga hal: isi 200 paket teratas, fitur SHAP yang paling sering jadi alasan, dan semua uji. Kalau ada yang aneh, saya perbaiki lalu latih lagi. Totalnya ada **20 temuan**, dan semuanya sudah ditangani.

**Dashboard dan naskah belum diubah.** Dashboard masih versi 9, yaitu versi sebelum audit.

---

## Ringkasnya

1. **Versi lama (dashboard sekarang) terlihat bagus karena ada kebocoran.**
   - Kolom *jenis pengadaan* ikut "menyontek" red flag. Contoh: paket konstruksi lebih sering kena RF1.
   - Kolom jenis sudah dibuang. Sekarang alasan SHAP tidak lagi didominasi "jenis pengadaan".
2. **RF2 hampir sama dengan salah satu fitur.** RF2 adalah pengadaan langsung yang lewat ambang. Fitur "pagu dibanding paket sejenis" sudah otomatis tinggi untuk paket seperti itu, jadi RF2 ikut menaikkan Precision@K. Kalau RF2 tidak dihitung, Precision@K kedua jalur **setara acak**. Penjelasannya ada di bagian 5.
3. **Jalur pelaksanaan membaik.**
   - Di provinsi uji: 33,1% dibanding acak 25,6%. Sebelumnya 26,2%, hampir sama dengan acak.
   - Alasan SHAP sekarang seimbang. Yang terbanyak adalah realisasi dibanding pagu.
4. **Uji anomali buatan sekarang lebih jujur.** Paket buatan yang normal (kontrol) kini hanya 6% (perencanaan) dan 14% (pelaksanaan) yang ikut ditandai. Sebelumnya 27% dan 21%. Artinya, model jarang salah menandai paket normal.
5. **Ditemukan 13 paket dengan data bermasalah** di jalur pelaksanaan. Paket-paket ini sekarang tidak dinilai.

---

## Yang perlu Tio putuskan

1. **Pasang versi baru ke dashboard?**
   - **Saran saya: ya.** Versi lama masih punya kebocoran kolom jenis.
   - Kalau setuju, saya publikasikan. Teks penjelasan di dashboard sudah saya sesuaikan.
2. **Cara melaporkan evaluasi di naskah.** Pilih salah satu:
   - **(a) Saran saya.** Laporkan Precision@K dengan RF2 dan tanpa RF2. Bukti utama bahwa model bekerja diambil dari anomali buatan, kestabilan, dan uji SHAP. Lalu jelaskan bahwa RF1/RF3/RF4 memang pola yang "menyamar jadi normal" (bagian 5).
   - **(b)** Precision@K tetap jadi ukuran utama, dengan RF2 ikut dihitung, dan kebocoran RF2 ditulis di batasan.
   - **(c)** RF2 dibuang dari daftar red flag.
3. **Fitur "pagu dibanding paket bernama sama" (pola A-B-C) sekarang hanya dipakai di jalur perencanaan.** Di pelaksanaan, fitur ini menutupi keanehan realisasi (bagian 3, temuan 16). Setuju?

---

## 1. Sebelum latih: masalah di fitur

| # | Fitur | Masalahnya | Tindakan |
|---|---|---|---|
| 1 | jenis pengadaan (kategori) | Jenis yang jarang (Konsultansi, Terintegrasi) otomatis dianggap aneh. Jenis jadi alasan SHAP terbesar di 152 dari 200 paket, dan 114 dari 200 paket teratas perencanaan adalah Konsultansi. Jenis juga berkaitan dengan RF1 (konstruksi) dan RF3 (konsultansi) | dibuang. Konteks jenis sudah ada di fitur "pagu dibanding paket sejenis" |
| 2 | sumber transaksi (kategori) | Tender hanya 2,6% paket, jadi otomatis dianggap aneh. Sumber juga mewakili metode, padahal metode sengaja tidak dipakai | dibuang |
| 3 | tanda PDN/UMK di RUP | 98% dan 96% paket bernilai "ya", jadi paket "tidak" otomatis dianggap aneh | dibuang |
| 4 | metode berubah dari RUP ke realisasi | hanya 161 paket (0,15%), jadi kolomnya hampir selalu 0 | dibuang (lebih cocok sebagai penanda seperti red flag) |
| 5 | porsi PL dan porsi e-purchasing di satker | dua kolom ini kembar (korelasi −0,98) dan bocor ke RF1/RF3 | dibuang |
| 6 | pagu dibanding rata-rata satker | kembar dengan "pagu dibanding median satker" (korelasi 0,87) | dibuang, median yang dipakai |
| 7 | selisih rasio realisasi dengan paket sejenis | hampir sama dengan "realisasi dibanding pagu" | dibuang |

## 2. Waktu latih

| # | Masalahnya | Tindakan |
|---|---|---|
| 8 | Autoencoder berhenti di iterasi ke-60 padahal belum selesai belajar. Muncul peringatan "belum konvergen" di kelima seed | Batas dinaikkan menjadi 300. Autoencoder sekarang berhenti sendiri di sekitar iterasi 160, dan peringatannya hilang. Hasil autoencoder berubah cukup banyak: 5% teratasnya hanya 55–68% sama dengan versi lama |
| 9 | Penskalaan *quantile* di perencanaan: 21 paket yang pagunya tepat Rp1 jt masuk 200 teratas, karena nilai terkecil yang kembar dianggap ekstrem | Diganti penskalaan standar (z-score) |

## 3. Setelah latih: keanehan di hasil

| # | Putaran | Keanehannya | Tindakan |
|---|---|---|---|
| 10 | 1 | Satu satker NTB punya 42 paket di 200 teratas. Satker itu punya ratusan paket mikro (median Rp300 ribu), sehingga semua paket normalnya terlihat 1.000 kali median satker | "Pagu dibanding satker" sekarang dihitung per satker **dan jenis**, hanya untuk kelompok minimal 4 paket |
| 11 | 1 | Fitur "kekurangan PDN/UMK" menumpuk di "Pencatatan Non Tender" (18,5% dan 42,9% paket, Tender 0%). Ini cara mencatat, bukan janji yang tidak ditepati | dibuang |
| 12 | 2 | Dicoba tanpa fitur besar pagu (log_pagu) | Hasilnya setara acak di kedua jalur, jadi fitur ini **tetap dipakai** |
| 13 | 3 | Fitur nama (pola A-B-C) aktif untuk nama rekening umum seperti "Belanja Alat/Bahan untuk Kegiatan Kantor-…", yang dipakai lebih dari 1.000 satker. Contoh: ATK Rp6 jt terlihat 169 kali "paket bernama sama" yang ternyata belanja daring Rp35 ribu | Fitur nama hanya untuk nama yang **spesifik**, yaitu nama yang dipakai paling banyak 50 satker se-nasional |
| 14 | 4 | Fitur nama 96% bernilai 0, jadi selisih kecil sudah tampak ekstrem. 88 paket teratas perencanaan dan 75 paket teratas pelaksanaan naik hanya karena pagunya **1–2 kali** paket bernama sama | Fitur nama diberi skala yang sama dengan fitur "pagu dibanding paket sejenis". Paket teratas yang alasannya nama sekarang punya pagu minimal 2,8 kali paket bernama sama (median 11 kali) |
| 15 | 4 | Uji anomali buatan menaikkan fitur satker/nama walaupun paketnya tidak punya pembanding. Akibatnya uji "dekat ambang" dan "pagu digelembungkan" tampak 85–99% tertangkap | Diperbaiki: fitur yang memang 0 tetap 0 |
| 16 | 5 | Di pelaksanaan, fitur nama menjadi alasan SHAP terbesar di **176 dari 200** paket dan menutupi keanehan realisasi. Hanya 21 paket teratas yang realisasinya melebihi pagu (tanpa fitur nama: 100 paket) | Fitur nama hanya di perencanaan. Pola nama adalah pola pagu, jadi sudah tertangkap di jalur perencanaan |
| 17 | 5 | **Data:** 8 paket Tender punya 2–3 "pemenang" untuk satu kode paket. Contoh: 3 penyedia masing-masing Rp2,8–3,2 M untuk pagu Rp3,6 M. Jumlahnya menjadi 1,7–2,6 kali pagu, dan semuanya ada di peringkat 13–80 pelaksanaan | Aturan baru **B6**: paket seperti ini tidak dinilai. Satu tender hanya punya satu pemenang, jadi data ini kemungkinan berisi peserta tender atau tender ulang |
| 18 | 5 | **Data:** 5 paket dengan realisasi satu baris 9,8–9,9 kali pagu. Tidak ada satu pun paket di rentang 8–9,5 kali. Polanya: kelebihan satu angka nol | Batas atas aturan B5 diturunkan dari 10 ke 9,5 kali pagu |
| 19 | 6 | Uji "pagu digelembungkan" mengalikan pagu paket itu sendiri. Karena paket yang dipilih umumnya kecil, banyak hasilnya baru sampai ukuran wajar | Diubah: pagu dibuat 5–20 kali **median paket sejenis**. Ternyata 22–25% paket asli memang sudah 5 kali lebih besar dari paket sejenisnya. Jadi "5–20 kali" masih biasa di data ini, dan wajar bila hanya 18–20% yang ditandai |
| 20 | 2 | **RF2 bocor ke fitur** | penjelasan di bagian 5 |

Yang sudah dicek dan **tidak** bermasalah:
- Satker kecil tidak lagi menguasai peringkat atas. Satker terbanyak di 200 teratas: 14 paket (perencanaan) dan 11 paket (pelaksanaan).
- Paket dengan pagu ≤ Rp1 jt tidak menumpuk di peringkat atas.
- Paket "Terintegrasi" ikut dinilai lagi dan tidak menumpuk.

## 4. Fitur akhir

Semua fitur berupa angka. Tidak ada lagi kolom kategori.

| Fitur | Arti | Perencanaan | Pelaksanaan |
|---|---|---|---|
| log_pagu | besar pagu | ✓ | ✓ |
| pagu dibanding paket sejenis | dibanding median nasional untuk jenis + metode yang sama | ✓ satu arah | ✓ satu arah |
| pagu dibanding satker | dibanding median paket satker dengan jenis yang sama (kelompok ≥ 4 paket) | ✓ satu arah | ✓ satu arah |
| pagu dibanding paket bernama sama | dibanding median paket lain bernama spesifik sama di satker yang sama (≥ 2 paket lain) | ✓ satu arah | – |
| realisasi dibanding pagu | realisasi dibagi pagu (maksimal 5) | – | ✓ |
| besar selisih realisasi | selisih rupiah antara realisasi dan pagu | – | ✓ |

"Satu arah" artinya hanya pagu yang lebih besar dari pembandingnya yang menaikkan skor.

## 5. Temuan penting: red flag dan model melihat hal yang berbeda

**Precision@K (5% teratas, provinsi uji)**

| | Sebelum audit | Sesudah | Acak |
|---|---|---|---|
| Perencanaan, semua red flag | 33,7% | 27,1% | 13,8% |
| Perencanaan, tanpa RF2 | 23,9% | 12,0% | 12,3% |
| Pelaksanaan, semua red flag | 26,2% | 33,1% | 25,6% |
| Pelaksanaan, tanpa RF2 | 18,5% | 18,2% | 24,0% |

Artinya:
- **Perencanaan versi lama**: angka 23,9% tanpa RF2 berasal dari kebocoran kolom jenis. Setelah kolom itu dibuang, hasilnya setara acak.
- **Mengapa RF2 bocor:** fitur "pagu dibanding paket sejenis" membandingkan paket dengan paket yang **jenis dan metodenya sama**. Pengadaan langsung yang melewati ambang (RF2) pasti puluhan kali median pengadaan langsung, jadi otomatis skornya tinggi.
- **Mengapa RF1, RF3, dan RF4 tidak tertangkap:** pola ini memang dibuat supaya **terlihat normal**.
  - Paket dibuat tepat di bawah ambang (RF1).
  - Paket dipecah menjadi beberapa paket kecil yang wajar (RF3).
  - Penunjukan langsung pagunya biasa saja (RF4).

  Model anomali mencari yang **berbeda** dari kebanyakan paket. Jadi wajar kalau model tidak menangkap pola "menyamar jadi normal". Ini bukan kesalahan model. Red flag dan model memang mengukur hal yang berbeda, dan bisa ditulis sebagai temuan di Bab 4/5.
- Yang **ditangkap** model: pagu yang jauh lebih besar dari pembandingnya, dan realisasi yang menyimpang jauh dari pagu (bagian 6).

**Precision@K lengkap (versi akhir)**

| | Perencanaan | Pelaksanaan |
|---|---|---|
| P@50 | 22% | 46% |
| P@100 | 19% | 36% |
| P@200 | 18% | 37% |
| 5% teratas | 32,3% | 37,7% |
| Acuan (acak) | 15,8% | 26,3% |
| Provinsi pilih / uji, 5% | 38,2% / 27,1% | 42,1% / 33,1% |

200 teratas perencanaan sekarang berisi paket besar:
- 69% berpagu di atas Rp1 M (dari semua paket hanya 3,7%);
- 19% Tender;
- 31,5% konstruksi.

Paket sebesar ini memang jarang memenuhi syarat RF1–RF4 yang khusus pengadaan langsung, jadi P@200 rendah.

## 6. Anomali buatan (persen yang masuk 5% teratas)

| Pola buatan | Perencanaan | Pelaksanaan | Sebelum audit (Per / Pel) |
|---|---|---|---|
| Ekstrem (global) | 93% | 100% | 95% / 100% |
| Berkelompok | 96% | 100% | 100% / 86% |
| Lokal | 30% | 52% | 51% / 71% |
| Hubungan antarfitur rusak | 40% | 55% | 59% / 45% |
| Realisasi melebihi pagu 1,3–3 kali | – | 67% | – / 61% |
| Pagu 5–20 kali paket sejenis | 18% | 20% | (uji lama, tidak sebanding) |
| PL dinaikkan ke dekat ambang | 31% | 21% | 13% / 19% |
| **Kontrol (paket buatan normal)** | **6%** | **14%** | **27% / 21%** |

Cara membacanya: bandingkan setiap pola dengan baris kontrol.
- Sebelum audit, kontrol 27% dan 21%. Artinya model sering menandai paket normal, sehingga angka pola lain terlihat bagus padahal tidak berarti banyak.
- Sekarang kontrol 6% dan 14%. Pola ekstrem, berkelompok, dan realisasi melebihi pagu jelas tertangkap.

## 7. Uji lain

- **Kestabilan:** 5 seed dibandingkan dengan 5 seed lain.
  - Urutan skor hampir sama (Spearman 0,96).
  - 5% teratas sama 69–75% (Jaccard).
  - 200 teratas sama 65–73%.
- **Pengaruh acak:** model dilatih ulang dengan tiga set seed.

  | Jalur | 5% teratas | Provinsi uji 5% | P@200 |
  |---|---|---|---|
  | Perencanaan | 31,6–32,8% | 26,9–27,8% | 11,5–19% |
  | Pelaksanaan | 35,6–38,6% | 32,1–34,2% | 37–46,5% |

  P@200 bisa bergeser sampai 9 poin hanya karena acak. Karena itu P@200 sebaiknya tidak dijadikan angka utama; pakai 5% teratas dan laporkan rentangnya.
- **Kesetiaan SHAP:**
  - Kalau 3 fitur SHAP teratas diganti nilai normal, skor turun lebih besar daripada kalau 3 fitur acak yang diganti.
  - Ini terjadi di 100% paket, di kedua jalur.
- **Alasan SHAP terbesar di 200 paket teratas:**
  - Perencanaan: nama 148, besar pagu 28, satker 13, sejenis 11. Nama dominan, tetapi semua kasusnya pagu minimal 2,8 kali paket bernama sama, jadi memang pola A-B-C yang Tio cari.
  - Pelaksanaan: realisasi/pagu 88, besar pagu 45, satker 31, sejenis 22, selisih realisasi 14.
- **Ensemble dibanding model tunggal (5% teratas, provinsi uji):**

  | Jalur | Ensemble | LOF+AE | LOF saja | IF saja |
  |---|---|---|---|---|
  | Perencanaan | 27,1% | 30,2% | 28,9% | 13,9% |
  | Pelaksanaan | 33,1% | 37,1% | 32,4% | 26,7% |

  Ensemble tidak selalu menang, tetapi juga tidak pernah paling buruk. Selisihnya masih dalam rentang acak.
- **SPI KPK:** provinsi yang rentan menurut SPI punya lebih banyak paket tidak lazim di perencanaan (7,4% dibanding 4,0%, p = 0,004). Tetapi kalau provinsi Papua tidak dihitung, selisihnya tidak lagi bermakna (p = 0,08).

## 8. Lokasi file

- Kode: `s1_data.py` (aturan B5, B6), `s2_model.py` (komentar alasan setiap perubahan ada di atas KOLOM), `s5_validasi.py`, dan `ens2.py` di model-v2 (pilihan `ae_iter` dan `skala_sama`).
- Arsip tiap putaran: `arsip-v5-sebelum-audit/` (versi dashboard sekarang), `arsip-audit-putaran2/` sampai `arsip-audit-putaran5/`.
- Eksperimen varian: `eksperimen-audit/` (skrip x8, x9, x10).
- Audit isi peringkat: `log/a1.log`.
- `hasil-evaluasi-v5.md` dan `ringkasan-metode-v5.md` sudah **usang**. Yang berlaku adalah file ini.
