# Hasil eksperimen lanjutan (30 Oktober 2026)

**Permintaan Tio:** coba fitur/red flag baru, pra-pemrosesan, normalisasi, seed, kombinasi tahun, dan metodologi lain supaya Precision@K (atau evaluasi lain) valid dan tidak terlalu rendah. Validasi ulang juga apakah paket di peringkat atas memang layak di sana.

**Model, naskah, dan dashboard tidak diubah.** Semua kode dan tabel ada di folder ini.

---

## Jawaban singkat

1. **Tidak ada cara yang sah untuk membuat Precision@K naik banyak.** Semua varian yang menaikkan angka dengan tajam ternyata punya salah satu dari dua masalah:
   - **Menyontek red flag:** fiturnya dibuat dari bahan yang sama dengan red flag.
   - **Kebetulan teknis:** ada sebab lain di luar kemampuan model, misalnya perubahan ambang PL antartahun.

   Kalau varian seperti ini dipakai, dosen bisa membongkarnya dengan satu pertanyaan.
2. **Precision@K rendah terutama bukan karena model jelek, tapi karena cara mengukurnya.**
   - **(a) Banyak paket teratas tidak mungkin kena red flag.** RF1–RF3 hanya berlaku untuk Pengadaan Langsung, dan RF4 hanya untuk Penunjukan Langsung. Padahal 77–79% dari 200 paket teratas perencanaan adalah e-purchasing, tender, atau seleksi, sehingga paket-paket itu otomatis dihitung "salah".
   - **(b) RF1 dan RF3 memang pola yang menyamar jadi normal.** Pagu sengaja dibuat sedikit di bawah ambang, atau paket dipecah jadi kecil-kecil. Model anomali mencari yang menonjol, bukan yang bersembunyi. Ini sudah diuji: model yang SENGAJA diberi fitur "jarak ke ambang PL" pun hanya naik menjadi 1,2–1,4 kali acak untuk RF1.
   - **(c) RF2 bocor:** fitur pagu sudah otomatis membaca RF2.
3. **Model hanya sedikit lebih baik dari aturan sederhana, dan itu pun hanya setelah RF2 dikeluarkan.**
   - Kalau RF2 ikut dihitung, mengurutkan paket dari "pagu dibanding paket sejenis" (tanpa model) memberi lipat red flag yang hampir sama dengan model (perencanaan 2025: 1,95× vs 2,04×).
   - Kalau paket RF2 dikeluarkan, model lebih baik dari semua aturan sederhana:
     - perencanaan: 1,34× vs paling tinggi 0,81×;
     - pelaksanaan: 0,90× vs paling tinggi 0,78×. Pelaksanaan tetap masih di bawah acak.
   - Keunggulan model yang jelas ada di anomali buatan, yaitu kombinasi fitur yang janggal (bagian 4).

4. **Saran:** pertahankan model sekarang dan ubah cara melaporkan evaluasi (bagian 7).
   - Dua varian sempat tampak lebih baik: LOF + AE, dan model per metode tanpa log_pagu.
   - Setelah dicek, kenaikannya hanya karena daftar teratas jadi berisi lebih banyak paket PL dan Penunjukan Langsung, yaitu paket yang memang bisa kena red flag.
   - Kalau dihitung hanya di antara paket yang red flag-nya berlaku, keduanya tidak lebih baik, bahkan sedikit lebih buruk di 2025.

---

## 1. Aturan main eksperimen

- **2024 = tahun pengembangan.** Varian dipilih di tahun ini.
- **2025 = tahun uji.** Tahun ini dipakai untuk mengecek apakah pilihan dari 2024 tetap berlaku.
- Provinsi uji 2025 = provinsi di luar provinsi pilih. Hasilnya juga dilaporkan.
- **Ukuran utama: "lipat 5% (tanpa paket RF2)".**
  - Paket ber-RF2 dikeluarkan dari daftar, lalu dihitung berapa kali lebih sering 5% paket teratas memuat red flag lain dibanding paket acak.
  - 1,0 = sama dengan acak. Di atas 1 = lebih baik dari acak.
  - Ukuran ini dipakai karena RF2 bocor. Angka "dengan RF2" tetap dicantumkan sebagai pembanding.
- **Skor kembar diurutkan secara acak**, bukan menurut urutan kode RUP. Perbaikan ini ditemukan di tengah eksperimen: tanpanya, satu varian tampak 99% benar padahal hanya kebetulan urutan.

## 2. Hasil semua varian

Angka = lipat 5% tanpa paket RF2, untuk tahun 2024 / 2025 / 2025 provinsi uji.

| # | Varian | Perencanaan | Pelaksanaan | Sah? | Catatan |
|---|---|---|---|---|---|
| 0 | **Model sekarang** (rata-rata IF+LOF+AE) | 1,00 / 1,34 / 1,14 | 0,75 / 0,90 / 0,86 | ya | acuan |
| 1 | LOF + AE (IF dibuang) | 1,13 / 1,59 / 1,36 | 0,93 / 1,12 / 1,12 | semu | naik di semua kolom, tapi di antara paket yang red flag-nya berlaku perencanaan 2025 malah turun (1,47 → 1,32). Kenaikannya datang dari lebih banyak paket PL/PenL kecil di puncak (efek LOF, catatan A) |
| 2 | LOF saja | 2,44 / 2,09 / 1,97 | 1,22 / 1,30 / 1,16 | **tidak** | lihat catatan A |
| 3 | Gabungan lain (maksimum, median, rata-rata peringkat, suara terbanyak, bobot) | 0,92–1,76 / 1,01–1,47 / 0,98–1,37 | 0,75–0,86 / 0,90–0,96 / 0,85–0,96 | ya | tidak lebih baik dari no. 1 |
| 4 | LOF dengan k = 10 / 50 / 100, sampel 100 rb | 1,03–2,64 / 1,51–2,33 / 1,36–2,28 | 1,03–1,33 / 1,16–1,57 / 1,11–1,46 | **tidak** | k kecil = makin mirip catatan A |
| 5 | Model per kelompok metode (PL / e-purchasing / lainnya) | 0,82 / 1,03 / 0,93 | 0,82 / 0,86 / 0,82 | ya | lebih buruk |
| 6 | Data 2024 + 2025 digabung saat latih | 1,00 / 1,08 / 1,00 | 0,76 / 0,89 / 0,87 | ya | tidak membantu |
| 7 | Model tahun lalu menilai tahun ini (silang tahun) | 1,12 / 1,16 / 0,98 | 1,22 / 0,91 / 0,90 | ya | tidak membantu; LOF-nya kena catatan B |
| 8 | + fitur kebulatan pagu (jumlah angka nol) | 0,74 / 1,19 / 1,02 | 0,68 / 0,84 / 0,77 | ya | lebih buruk |
| 9 | + fitur jumlah paket bernama sama di satker | 1,23 / 1,79 / 1,61 | 0,87 / 1,24 / 1,12 | **tidak** | kenaikan seluruhnya dari RF3 (1,12 → 1,90; 1,65 → 2,62), karena RF3 dibuat dari nama paket yang mirip di satker |
| 10 | + fitur jarak ke ambang PL (sengaja bocor) | 1,30 / 1,70 / 1,54 | 0,90 / 1,04 / 0,97 | **tidak** | menyontek RF1/RF2. Itu pun RF1 hanya 1,2–1,4× acak |
| 11 | Tanpa fitur besar pagu mutlak (log_pagu) | 0,95 / 1,08 / 1,07 | 0,66 / 0,76 / 0,74 | ya | lipat turun, tapi 19 proyek besar yang wajar hilang dari 200 teratas perencanaan (bagian 5) |
| 12 | Model per metode + tanpa log_pagu | 1,05 / 1,59 / 1,47 | 0,91 / 0,97 / 0,93 | semu | naik karena peringkat dihitung di dalam tiap metode, sehingga PL otomatis mengisi sekitar 42% puncak. Per red flag tidak lebih baik (RF1 perencanaan 2025: 1,20 → 0,55) |
| 13 | 10 seed, bukan 5 | 1,09 / 1,41 / 1,22 | 0,74 / 0,92 / 0,88 | ya | hampir sama dengan 5 seed (selisih masih dalam goyangan seed) |

Normalisasi (min-max, skor-z, persentil) sudah diuji sebelumnya: persentil tetap yang terbaik (eksperimen-normalisasi/hasil-normalisasi.md).

**Catatan A: kenapa LOF saja tidak sah walau angkanya tinggi.**
- 25 paket teratas LOF umumnya berpagu bulat tepat Rp200 jt, Rp100 jt, atau Rp8 jt, termasuk paket Penunjukan Langsung Rp8 jt yang biasa saja (ATK, sewa kendaraan).
- Penyebabnya, LOF menandai titik di tepi tumpukan nilai yang sama persis. Ini kebetulan teknis, bukan pola yang dirancang.
- Pada uji anomali buatan, LOF saja salah menandai **23%** paket normal di perencanaan. Ensemble hanya 6%.
- Jadi daftar teratas LOF saja tidak berguna untuk pemeriksa.

**Catatan B: kenapa model silang tahun tampak 99% benar.**
- Model 2024 yang menilai data 2025 menaruh 200 paket PL konstruksi berpagu ±Rp196 jt di puncak, dan 196 di antaranya kena RF1.
- Sebabnya, ambang PL konstruksi naik dari Rp200 jt (2024) menjadi Rp400 jt (2025). Paket yang masih menumpuk di bawah ambang lama tampak asing bagi model 2024.
- Ini temuan menarik: banyak paket 2025 masih menempel ambang lama. Tapi ini efek perubahan aturan, bukan kemampuan model, jadi tidak bisa dijadikan bukti akurasi.

## 3. Seed

- Rata-rata 5 seed: Precision@200 tiap seed perencanaan 2025 bervariasi 14,5–22%. Rata-ratanya stabil (Jaccard top-200 = 0,73 terhadap 5 seed lain).
- Hasil 10 seed: 200 teratasnya 75–86% sama dengan versi 5 seed (Jaccard 0,75–0,86), dan 5% teratasnya 82–86% sama. Angka red flag-nya praktis sama.
- Jadi 5 seed sudah cukup.
- Seed hanya mengurangi goyangan peringkat dan tidak menaikkan Precision@K. Itu memang bukan fungsinya.

## 4. Pembanding tanpa model: jawaban untuk "buat apa pakai model?"

**Lipat 5% dengan red flag lengkap** (2025 semua provinsi / 2025 provinsi uji):

| Cara mengurutkan | Perencanaan | Pelaksanaan |
|---|---|---|
| Model sekarang | 2,04 / 1,97 | 1,43 / 1,29 |
| Urut "pagu dibanding sejenis" (tanpa model) | 1,95 / 1,72 | 1,18 / 1,14 |
| Urut pagu terbesar | 1,08 / 0,86 | 1,00 / 0,73 |
| Rata-rata skor-z fitur (aturan sederhana) | 1,29 / 1,04 | 1,16 / 0,89 |
| Acak | 1,0 | 1,0 |

- Dengan RF2 ikut dihitung, model hanya sedikit di atas aturan satu fitur, karena aturan "pagu dibanding sejenis" juga menyontek RF2.
- Kalau paket ber-RF2 dikeluarkan (2024 / 2025 / 2025 uji):

| Cara mengurutkan | Perencanaan | Pelaksanaan |
|---|---|---|
| Model sekarang | 1,00 / 1,34 / 1,14 | 0,75 / 0,90 / 0,86 |
| Urut "pagu dibanding sejenis" | 0,73 / 0,81 / 0,83 | 0,77 / 0,78 / 0,70 |
| Rata-rata skor-z fitur | 0,32 / 0,36 / 0,42 | 0,56 / 0,56 / 0,62 |
| Urut pagu terbesar | 0,10 / 0,12 / 0,10 | 0,38 / 0,44 / 0,40 |

- Jadi setelah kebocoran dibuang:
  - model lebih baik dari aturan sederhana, walau di perencanaan hanya sedikit di atas acak;
  - di pelaksanaan semuanya di bawah acak.
- **Model jelas lebih unggul di anomali buatan.** Data dari validasi/v_sintetis.csv; angka = paket buatan yang masuk 5% teratas:

| Jenis anomali buatan | Ensemble | Aturan skor-z sederhana |
|---|---|---|
| Kombinasi fitur janggal (tiap fitur wajar, gabungannya tidak) | 40% / 55% | 2% / 2% |
| Anomali lokal (sedikit di luar kelompoknya) | 30% / 52% | 15% / 29% |
| Anomali ekstrem (global) | 93% / 100% | 82% / 94% |
| Paket normal ikut ditandai (makin kecil makin baik) | 6% / 14% | 4% / 4% |

(perencanaan / pelaksanaan)

- **Kesimpulannya, nilai tambah model adalah menangkap paket yang janggal karena gabungan beberapa hal sekaligus.** Aturan yang melihat satu fitur, termasuk red flag, tidak bisa menangkapnya.
- Itu sebabnya Precision@K terhadap red flag memang tidak cocok sebagai satu-satunya ukuran.

## 5. Telaah paket peringkat atas (2025, 40 teratas per jalur)

File: h_telaah_perencanaan.csv dan h_telaah_pelaksanaan.csv. Penilaiannya dari membaca data, bukan pemeriksaan lapangan.

**Perencanaan:**
- Sekitar **31 dari 40 layak diperiksa**. Contohnya:
  - makan-minum Rp9,5 M lewat Pengadaan Langsung;
  - sosialisasi Perda Rp13 M lewat e-purchasing;
  - obat Rp8,5 M (74× paket bernama sama di satker yang sama);
  - jamuan tamu Rp3,3 M lewat PL;
  - PJLP DKI Rp15–37 M lewat PL.
- Sekitar **8 adalah proyek besar yang wajar**, misalnya Jembatan Pulau Laut Rp290–424 M, NCICD dan sewerage Jakarta (kontrak tahun jamak), dan rehab sekolah Rp383 M. Paket-paket ini naik terutama karena ukurannya.
- **1 remeh:** ATK Rp27,7 jt yang tampak 1.152× hanya karena paket pembandingnya bernilai puluhan ribu.

**Pelaksanaan:**
- Sekitar **28 dari 40 layak diperiksa**. Contohnya:
  - gaji PPSU kelurahan DKI yang realisasinya 1,2–1,9× pagu;
  - realisasi 4–5× pagu;
  - e-purchasing yang realisasinya 1,4–2× pagu.
- Sekitar **8 proyek besar wajar** dengan realisasi = pagu.
- Sekitar **4 meragukan**: konsultansi seleksi dengan realisasi 0,2–0,5× pagu, yang cukup umum terjadi.

Varian no. 11 (tanpa log_pagu) membuang ke-19 proyek ≥Rp5 M lewat tender/seleksi/tahun jamak dari 200 teratas perencanaan. Lipat red flag-nya turun dari 1,34 ke 1,08, jadi ada tukar-guling antara angka red flag dan kualitas daftar.

## 6. Validasi lain yang mendukung (semuanya bukan dari red flag, jadi tidak bocor)

| Uji | Hasil |
|---|---|
| Konsistensi satker antartahun | Satker yang masuk 20% paling banyak paket tidak lazim di 2024 punya **10,5%** paket tidak lazim di 2025, satker lain hanya **2,9%** (3,6×). Spearman 0,42 di kedua jalur, p < 0,001, 2.372 dan 877 satker. Paketnya berbeda dan tahunnya berbeda, jadi model menangkap pola yang menetap, bukan acak |
| Konsistensi provinsi antartahun | Spearman 0,70 / 0,71 (model-v5-2024/banding_2024_2025.md) |
| Red flag satker 2024 vs paket tidak lazim 2025 (tanpa RF2) | perencanaan Spearman 0,18 (p < 0,001); pelaksanaan tidak ada hubungan |
| SPI KPK 2024 dengan data 2024 (tahun yang sama dengan survei) | Provinsi rentan punya lebih banyak paket tidak lazim: perencanaan 8,0% vs 4,3% (p = 0,02), pelaksanaan 10,8% vs 6,4% (p = 0,009). **Tanpa Papua tidak nyata** (p 0,22–0,38). Sama seperti hasil 2025 |
| Anomali buatan | bagian 4 |

## 7. Saran cara melapor di naskah

1. **Precision@K tetap dilaporkan**, tapi sebagai "keselarasan dengan red flag", bukan "akurasi". Laporkan tiga versi:
   - dengan semua red flag;
   - tanpa RF2 (bocor);
   - hanya pada paket yang red flag-nya bisa berlaku.

   Tulis jujur bahwa aturan satu fitur memberi angka yang mirip.
2. **Bukti utama bahwa model bekerja:**
   - anomali buatan, dibandingkan dengan aturan sederhana (bagian 4);
   - konsistensi antartahun di tingkat satker dan provinsi;
   - telaah paket teratas.
3. **Batasan:** red flag dekat ambang (RF1) dan pemecahan paket (RF3) adalah pola yang menyamar jadi normal, jadi tidak tertangkap model anomali. Itu sebabnya red flag tetap ditampilkan di samping skor di dashboard.
4. Referensi pendukung bahwa red flag hanya proksi sudah ada (bab2/referensi-precision-at-k-v1.md: Schiavon et al. 2026; Medina-Hernández et al. 2025).

## 8. Yang perlu Tio putuskan

1. **Model:** tetap rata-rata 3 model dengan 5 seed (saran). Tidak ada varian yang benar-benar lebih baik setelah dicek dari mana kenaikannya berasal.
2. **Fitur log_pagu:** tetap dipakai (saran), atau dibuang supaya proyek besar yang wajar tidak memenuhi puncak.
3. **Cara melapor evaluasi:** ikuti bagian 7, atau tetap seperti sekarang.

## File

- lib.py: evaluasi yang adil.
- a0_evaluasi_adil.py: model vs pembanding tanpa model.
- b1_gabung_model.py: cara menggabungkan model.
- c_latih.py: 12 varian latih ulang; skor di skor/.
- e_eval.py dan e_perflag.py: evaluasi varian dan cek sumber kenaikan per red flag.
- f_spi.py: uji SPI.
- g_satker_lintas_tahun.py: konsistensi satker.
- h_telaah.py: daftar 40 paket teratas.
- Tabel CSV: a0_evaluasi_adil.csv, b1_gabung_model.csv, e_eval.csv, f_spi.csv, g_satker_lintas_tahun.csv.
