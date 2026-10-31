# Hasil uji ide dari project sebelah (31 Oktober 2026)

**Permintaan Tio:** "coba semua yang sekira bisa improve project ini" (fitur, red flag, dan metode dari project "TRAIN ANOMALY DETECTION").

## Jawaban singkat

**Model sekarang tetap yang terbaik.** Satu-satunya yang bisa diambil adalah red flag PDN/UMK untuk jalur pelaksanaan. Model, dashboard, dan naskah belum diubah.

1. **Fitur:** tidak ada fitur project sebelah yang lolos aturan pilih.
   - Empat fitur menaikkan angka, tetapi kenaikannya datang tepat dari red flag yang bocor ke fitur itu (dijelaskan di bawah).
   - Satu fitur, **nilai paket dibanding kebiasaan penyedia**, tidak bocor dan menaikkan lipat terkontrol. Tetapi lipat biasanya turun sedikit, jadi hasilnya hanya "sebagian".
2. **Red flag:** red flag PDN/UMK realisasi < 50% (E4, E5) layak dipakai.
   - Model sekarang sudah 1,3–2,1 kali lebih sering menemukannya, bahkan setelah dikontrol besar pagu dan metode. Ini konsisten di 2024, 2025, dan provinsi uji, dan red flag ini tidak bocor (AUC ≤ 0,63).
   - Kalau set red flag bersih project sebelah (E3–E6) ditambahkan ke jalur pelaksanaan, lipat terkontrol naik dari 0,90 / 1,01 / 1,09 menjadi 1,08 / 1,13 / 1,16.
3. **Metode:** penskalaan robust, posisi peringkat dua arah, dan posisi rasio realisasi tidak lebih baik.
4. **Temuan baru: RF1 (PL mendekati ambang) juga bocor.** log_pagu menebak RF1 dengan AUC 0,90–0,92 di paket PL, sama dengan temuan project sebelah untuk P2.
   - Kebocoran ini tidak menaikkan angka model kita, karena lipat RF1 hanya 0,6–1,2.
   - Tetapi ini perlu ditulis jujur di Bab 4.

## Aturan uji (ditetapkan sebelum melihat hasil)

- Sama dengan eksperimen lanjutan: 2024 untuk memilih, 2025 dan provinsi uji untuk mengecek.
- Varian disebut "lebih baik" bila di 2024:
  - lipat terkontrol (pagu × metode) ≥ model sekarang + 0,05, **dan**
  - lipat 5% berlaku ≥ model sekarang,
  - lalu tetap ≥ model sekarang di 2025.
- Penilai utama: red flag sekarang tanpa RF2, dengan paket RF2 dikeluarkan dari daftar.
- Fitur dengan AUC simetris ≥ 0,70 terhadap salah satu red flag penilai ditandai "berisiko bocor". Ini memakai ambang project sebelah.

## 1. Tabel kebocoran (k2_bocor.csv)

Isinya AUC satu fitur menebak satu red flag. Yang ≥ 0,70 (2024 / 2025):

| Fitur | Red flag yang ditebak | AUC |
|---|---|---|
| log_pagu (fitur kita) | RF2, **RF1**, P4 | 0,96–0,98; **0,87–0,92**; 0,99–1,00 |
| rasio pagu sejenis (fitur kita) | RF2, P4 | 0,91–0,94; 0,71–0,92 |
| rasio pagu satker (fitur kita) | RF2, P4 | 0,77–0,85; 0,77–0,80 |
| pagu kembar di satker | RF3, RF1 | 0,71–0,81; 0,72–0,81 |
| porsi pagu satker | RF5, RF2, C4 | 0,81–0,82; 0,80–0,82; 0,73–0,76 |
| porsi non-kompetitif satker | E6, P4 | 0,75–0,78; 0,65–0,76 |
| jangkauan penyedia | RF6 | 0,80–0,81 |
| posisi pagu dua arah (sejenis, satker) | RF2, RF1, P4 | 0,86–1,00; 0,66–0,80; 0,78–0,92 |
| nilai vs kebiasaan penyedia, posisi rasio realisasi, kebulatan pagu | – | semua ≤ 0,69 |

P4 (penunjukan langsung di atas ambang) bocor ke log_pagu, jadi tidak dipakai sebagai penilai.

## 2. Hasil fitur dan metode (k4_eval.csv)

Angka di tabel: lipat terkontrol, ditulis 2024 / 2025 semua / 2025 provinsi uji. Penilai: red flag sekarang.

### Perencanaan

| Varian | Lipat terkontrol | Lipat 5% berlaku | Dari mana naiknya |
|---|---|---|---|
| Model sekarang | 0,93 / 1,11 / 1,05 | 1,08 / 1,47 / 1,31 | – |
| + pagu kembar | 1,21 / 1,40 / 1,35 | 1,85 / 1,93 / 1,90 | RF1 4,4× dan RF3 2,3×, padahal keduanya bocor ke fitur ini |
| 6 fitur project sebelah | 1,20 / 1,32 / 1,24 | 1,60 / 1,94 / 1,84 | sama, dan 86–94% dari 200 teratas jadi PL/PenL (P@200 84% karena komposisi) |
| + penskalaan robust | 0,92 / 1,14 / 1,12 | 1,15 / 1,54 / 1,44 | naik sedikit di 2025, tidak di 2024: tidak lolos |
| + kebulatan, + porsi non-kompetitif | ≈ model | ≈ / lebih rendah | – |
| + porsi pagu satker, posisi dua arah | lebih rendah | lebih rendah | – |
| Aturan tanpa model: \|posisi pagu sejenis\| | 1,26 / 1,27 / 1,37 | 1,10 / 1,52 / 1,49 | RF1 2,1× (batas bocor). Sama dengan temuan project sebelah: aturan satu fitur mengalahkan model di perencanaan |

### Pelaksanaan

| Varian | Lipat terkontrol | Lipat 5% berlaku | Dari mana naiknya |
|---|---|---|---|
| Model sekarang | 0,90 / 1,01 / 1,09 | 0,75 / 0,90 / 0,86 | – |
| + **kebiasaan penyedia** | **1,21 / 1,15 / 1,26** | 0,74 / 0,78 / 0,76 | RF6 naik (1,0 → 1,5) dan E6 naik (2,7 → 4,8), **tanpa bocor**. Lipat biasa turun sedikit, jadi "sebagian" |
| + jangkauan penyedia | 1,20 / 1,20 / 1,33 | 0,73 / 0,79 / 0,75 | RF6, bocor (AUC 0,80) |
| + porsi pagu satker | 1,04 / 1,18 / 1,32 | 0,72 / 0,91 / 0,93 | RF5 4,0×, bocor (AUC 0,81) |
| + porsi non-kompetitif | 1,01 / 1,06 / 1,21 | 0,79 / 0,96 / 0,97 | E6 3×, bocor |
| 9 fitur project sebelah | 1,38 / 1,22 / 1,28 | 1,30 / 1,19 / 1,15 | RF6 dan E6, bocor |
| + posisi rasio realisasi | 0,91 / 1,02 / 1,12 | 0,76 / 0,91 / 0,91 | ≈ model |
| kebiasaan + posisi rasio | 1,16 / 1,10 / 1,22 | 0,72 / 0,74 / 0,75 | tidak lebih baik dari kebiasaan saja |
| + penskalaan robust, + kebulatan, + pagu kembar | ≈ model | ≈ / lebih rendah | – |

Untuk varian kebiasaan penyedia, isi 200 teratas berubah: hanya 80 dari 200 yang sama dengan model sekarang. 43% di antaranya bernilai lebih dari 10 kali kebiasaan penyedianya.

## 3. Hasil red flag project sebelah (k5_terkontrol_perflag.csv)

Model sekarang, tanpa dilatih ulang. Lipat **terkontrol** pagu × metode per red flag, ditulis 2024 / 2025 / 2025 uji:

| Red flag | Lipat terkontrol | Bocor? | Pakai? |
|---|---|---|---|
| E4 PDN realisasi < 50% padahal RUP PDN | **1,90 / 2,10 / 2,11** | tidak (≤ 0,63) | **ya** |
| E5 UMK realisasi < 50% padahal dicadangkan | **1,47 / 1,40 / 1,31** | tidak | **ya** |
| E3 metode realisasi ≠ RUP | 0,89 / 1,44 / 1,49 | tidak | ya, tetapi hanya 143 paket |
| E6 penyedia kuasai ≥ 50% paket non-katalog | 2,70 / 1,55 / 1,15 | tidak (≤ 0,72) | ya |
| P5 tidak dicadangkan UMK (RUP) | 0,88 / 1,34 / 1,05 | tidak | tidak konsisten |
| P6 bukan PDN (RUP) | 0,97 / 1,29 / 0,90 | tidak | tidak konsisten |
| P4 penunjukan langsung > ambang | – | **bocor** (log_pagu 0,99–1,00) | tidak |

**Efek menambah E3–E6 ke penilai pelaksanaan (model sekarang):**

| Ukuran | Sebelum | Sesudah |
|---|---|---|
| Lipat terkontrol | 0,90 / 1,01 / 1,09 | 1,08 / 1,13 / 1,16 |
| Lipat 5% berlaku | 0,75 / 0,90 / 0,86 | 0,97 / 1,10 / 1,03 |
| P@200 | 22% / 22% / 24% | 40% / 36% / 36% |

Acuan acak P@200 juga ikut naik (45% / 36% / 38%), karena E5 berlaku di 16% paket. Jadi **P@200 tetap setara acak**. Yang naik adalah lipat terkontrol.

**Catatan:** dulu red flag PDN/UMK versi "realisasi PDN/UMK = 0, di luar Pencatatan Non Tender" (C5, C6) hilang setelah dikontrol. Versi project sebelah ("< 50%", termasuk Pencatatan) bertahan. Bedanya ada di definisi.

**Perbandingan langsung dengan project sebelah.** Model kita dinilai dengan set red flag bersih mereka (E3–E6), di data kita:

| Ukuran | Model kita | Laporan project sebelah |
|---|---|---|
| 5% teratas berlaku | 1,44 / 1,49 / 1,32 | 1,14× |
| P@200 | 30% / 20% / 20%, acak 19% / 18% / 22% | 31,4%, acak 17,9% |

Datanya tidak persis sama, karena pembersihan berbeda.

## Kesimpulan dan pilihan untuk Tio

1. **Tidak ada fitur yang perlu diganti.** Semua kenaikan besar berasal dari kebocoran. Ini pola yang sama dengan eksperimen lanjutan.
2. **Red flag E4 dan E5 (dan E3, E6) layak menjadi uji tambahan jalur pelaksanaan.**
   - Sumbernya Perpres Pasal 65–66 dan rancangan project lain yang dibuat terpisah.
   - Tetap harus ditulis sebagai uji tambahan, karena dipilih setelah melihat hasil.
3. **Fitur kebiasaan penyedia** bisa dicoba lebih jauh, tetapi belum lolos aturan pilih.
   - Kalau dipakai, dashboard dan SHAP harus dihitung ulang.
4. **RF1 bocor ke log_pagu.** Ini perlu disebut di Bab 4, bersama RF2.

## File

- k1_fitur_sebelah.py: fitur dan red flag sebelah → sebelah/fitur_*.pkl, rf_*.pkl
- k2_bocor.py → k2_bocor.csv
- k3_latih_sebelah.py, jalankan_k.sh: 15 varian × 2 tahun → sebelah/skor_*.pkl
- k4_eval_sebelah.py → k4_eval.csv (tiga set red flag: sekarang, sekarang + sebelah, sebelah)
- k5_terkontrol_perflag.py → k5_terkontrol_perflag.csv
