# Persentil vs min-max (30 Oktober 2026)

Model, fitur, dan data sama dengan model audit v5. Hanya cara menggabungkan skor tiga model yang diganti.
Kode: x11_normalisasi.py. Angka lengkap: banding_normalisasi.csv, dominasi_model.csv.

## Precision@K

| | Persentil, 5 seed (dipakai) | Min-max, 1 seed (naskah) | Acak |
|---|---|---|---|
| Perencanaan P@50 / P@200 | 22% / 18% | 48% / 27% | 15,8% |
| Perencanaan P@200 tanpa RF2 | 2% | 4% | 13,4% |
| Perencanaan 5% teratas | 32,3% | 18,3% | 15,8% |
| Perencanaan 5% provinsi uji | **27,1%** | 13,9% | 13,8% |
| Pelaksanaan P@50 / P@200 | 46% / 37% | 58% / 52,5% | 26,3% |
| Pelaksanaan P@200 tanpa RF2 | 17% | 16,5% | 23,5% |
| Pelaksanaan 5% teratas | 37,7% | 34,9% | 26,3% |
| Pelaksanaan 5% provinsi uji | **33,1%** | 25,9% | 25,6% |

Min-max 5 seed hasilnya hampir sama dengan min-max 1 seed.

## Kenapa min-max terlihat unggul di 200 teratas

1. **Min-max dikuasai Isolation Forest.** LOF dan Autoencoder punya beberapa skor yang sangat ekstrem. Setelah dibagi nilai maksimum, hampir semua paket lain jadi mendekati 0 (median LOF 0,001; median AE 0,000–0,003). Di 200 teratas, sumbangan rata-rata IF 0,81–0,86, sedangkan LOF hanya 0,01–0,06. Jadi min-max hampir sama dengan memakai **IF saja**, dan tidak lagi berbentuk ensemble.
2. **Kenaikan P@K-nya hampir seluruhnya dari RF2.** Itu red flag yang bocor lewat fitur sejenis. Tanpa RF2, min-max dan persentil sama-sama rendah.
3. **Di 5% teratas dan provinsi uji, min-max setara acak.** Persentil tetap sekitar dua kali acak di perencanaan.

## Kenapa 5 seed

- Dengan persentil 1 seed, 5% teratas seed 42 hanya 38–66% sama dengan seed lain (Jaccard). Rata-rata 5 seed membuat peringkat stabil (uji ulang: Spearman 0,96, Jaccard 0,69–0,75).
- Min-max lebih stabil antar-seed (Jaccard 0,75–0,89), tapi hanya karena IF yang menguasai skornya memang stabil.

## Kesimpulan

Persentil dipertahankan, karena ketiga model menyumbang setara (rata-rata 0,98–0,99 di 200 teratas). Naskah (Pers. 2.9, 3.2.4.2) perlu diganti ke normalisasi peringkat persentil, dengan alasan di atas, dan perlu rujukan gratis untuk cara ini.

---

## Cara lain (uji kedua, x12_normalisasi_lain.py, semua rata-rata 5 seed)

| Cara | Perencanaan 5% uji (acak 13,8) | tanpa RF2 (acak 12,3) | Pelaksanaan 5% uji (acak 25,6) | tanpa RF2 (acak 24,0) | Porsi sumbangan IF / LOF / AE (perencanaan) |
|---|---|---|---|---|---|
| **Persentil (dipakai)** | **27,1** | 12,0 | 33,1 | 18,3 | **32 / 33 / 35** |
| Min-max | 13,9 | 7,0 | 26,0 | 14,5 | 69 / 1 / 30 |
| Skor-z (rata-rata & simpangan baku) | 16,0 | 9,8 | 29,0 | 18,4 | 11 / 50 / 39 |
| Skor-z robust (median & MAD) | 21,2 | 16,1 | **39,4** | **29,3** | 0,5 / 1 / **98** |
| Log lalu min-max | 23,4 | 12,0 | 35,6 | 20,7 | 21 / 19 / 60 |
| Maksimum persentil (bukan rata-rata) | 19,0 | 14,4 | 29,2 | 19,3 | – |

Porsi sumbangan = seberapa besar tiap model mendorong skor 200 teratas.

Cara membacanya:
- **Hanya persentil yang membuat ketiga model menyumbang setara.** Cara lain selalu dikuasai satu model:
  - min-max dikuasai IF;
  - skor-z robust dikuasai Autoencoder (92–98%), jadi hampir sama dengan "AE saja";
  - log lalu min-max juga condong ke AE.
- Skor-z robust unggul di pelaksanaan, tanpa RF2 bahkan di atas acak (29,3 vs 24,0). Tapi di perencanaan kalah, dan model ini sebenarnya bukan ensemble lagi.
- Persentil terbaik di perencanaan 5% uji, dan kedua di pelaksanaan setelah cara yang hanya AE.
- Catatan jujur: memilih cara normalisasi setelah melihat hasil di provinsi uji akan membuat provinsi uji tidak lagi "bersih". Karena itu, saran saya tetap persentil, yang sudah dipakai sejak v1 sebelum hasil ini dilihat.

---

## Uji lengkap tanpa bias (x13_normalisasi_lengkap.py)

Kriteria ditetapkan **sebelum** hasil dilihat (tertulis di kepala skrip). Ada 6 ukuran per jalur, dan juaranya dihitung.

| Ukuran | Perencanaan: juara (persentil) | Pelaksanaan: juara (persentil) |
|---|---|---|
| 1. Anomali buatan (pola − kontrol) | **persentil 44,8** | log+min-max 47,1 (persentil 45,7, beda tipis) |
| 2. 5% provinsi uji, semua red flag | **persentil 27,1** | skor-z robust 39,4 (33,1) |
| 3. 5% provinsi uji, tanpa RF2 | skor-z robust 16,1 (12,0 ≈ acak) | skor-z robust 29,3 (18,3) |
| 4. Lift red flag tak bocor (RF4; RF5) | maksimum persentil 3,2× (1,8×) | RF4: skor-z robust 3,6× (2,4×); RF5: min-max 3,0× (2,4×) |
| 5. Kestabilan antar-seed (Jaccard) | min-max 0,81 (0,54) | min-max 0,82 (0,48) |
| 6. Keseimbangan 3 model | **persentil 35%** | **persentil 34%** |
| Salah tanda (kontrol, makin kecil makin baik) | min-max 4,5% (6,4%) | min-max 4,8% (13,5%) |

**Hitungan juara:** persentil 4, skor-z robust 4, min-max 3, lainnya 1. **Tidak ada yang menang mutlak.**

Ciri tiap cara:
- **Persentil.** Terbaik di perencanaan. Satu-satunya cara yang benar-benar menggabungkan 3 model. Salah tanda rendah.
- **Skor-z robust.** Terbaik di pelaksanaan dan di red flag yang tidak bocor. Tapi 92–98% skornya dari Autoencoder, jadi pada praktiknya "AE saja". Salah tandanya paling tinggi (12,7% / 16,6%), dan peringkatnya paling tidak stabil antar-seed (0,46 / 0,32).
- **Min-max.** Paling stabil dan salah tandanya paling sedikit, karena dikuasai Isolation Forest. Tapi di provinsi uji setara acak.
- Kestabilan persentil per seed rendah. Itu sebabnya skor dirata-rata 5 seed (Jaccard antar-ulangan 0,69–0,75).
