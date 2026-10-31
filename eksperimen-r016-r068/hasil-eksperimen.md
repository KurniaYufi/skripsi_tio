# Eksperimen: R016 dan R068 dijadikan red flag, fiturnya dibuang dari model

Tanggal: 29 Oktober 2026. Model v4 dan dashboard **tidak diubah**. Kode: `e1_latih.py` (latih), `e2_banding.py` (banding). Angka lengkap: `hasil_banding.csv`.

## Apa yang diuji

| Eksperimen | Fitur yang dibuang | Red flag baru |
|---|---|---|
| A (R016) | Pagu dibanding paket sejenis | **RF7**: pagu ≥ T kali median paket sejenis. OCP tidak memberi angka, jadi diuji T = 3, 5, 10 |
| B (R068) | Rasio realisasi, selisih realisasi, selisih rasio dengan paket sejenis | **RF8**: realisasi > pagu |

Pengaturan lain sama dengan v4 (5 seed, ambang, provinsi pilih/uji).

## Hasil eksperimen A (R016)

**RF7 terlalu umum untuk disebut red flag.** Paket yang kena: 30% (3 kali), 22% (5 kali), 14% (10 kali). Sebagai pembanding, red flag lama hanya 16%.

Jalur perencanaan, dinilai dengan red flag lama:

| | v4 | Eksperimen A | Acuan (semua paket) |
|---|---|---|---|
| 200 teratas ber-red flag | 38,5% | 29,5% | 15,8% |
| 200 teratas, tanpa penunjukan langsung | 25,0% | **11,0%** | 14,6% |
| 5% teratas | 38,2% | 35,6% | 15,8% |
| 5% teratas, provinsi uji | 34,2% | 35,6% | 13,8% |

- Tanpa fitur ini, 200 teratas yang punya red flag selain penunjukan langsung turun ke 11%. Angka itu **di bawah rata-rata semua paket**.
- Model tanpa fitur juga tidak bisa menemukan paket RF7. Untuk RF7 10 kali, 200 teratas hanya 8,5% ber-RF7, padahal rata-ratanya 13,8%.
- Daftar 200 teratas berubah jauh: hanya 20% yang sama dengan v4.
- Di jalur pelaksanaan, model tanpa fitur ini masih menemukan RF7, karena nilai pagu dan porsi pagu satker ikut membawa informasi yang sama. Jadi evaluasinya tetap berputar.

**Kesimpulan A:** R016 lebih baik tetap jadi fitur, seperti di v4.

## Hasil eksperimen B (R068)

**RF8 jarang dan sebagian besar diduga masalah pencatatan.**
- Hanya 2.223 paket (2,1%) yang realisasinya melebihi pagu.
- Dari jumlah itu, 934 paket (42%) realisasinya hampir tepat 2 kali pagu.
- Paket seperti ini hampir selalu punya dua catatan realisasi untuk satu kode RUP, dan 79% nilainya sama persis. Sumbernya sering berbeda, yaitu "Non Tender" dan "Pencatatan Non Tender". Contohnya "Pembayaran Gaji PPSU" Kelurahan Pekayon, Rp4,79 M tercatat dua kali.
- Ini **diduga tercatat ganda**. Dugaan ini belum dipastikan: bisa juga memang ada dua kontrak bernilai sama.

Jalur pelaksanaan, dinilai dengan red flag lama:

| | v4 | Eksperimen B | Acuan |
|---|---|---|---|
| 200 teratas | 48,0% | 44,5% | 24,7% |
| 5% teratas | 29,2% | 31,0% | 24,7% |
| 5% teratas, provinsi uji | 25,3% | **29,4%** | 24,7% |

- Tanpa fitur realisasi, hasil terhadap red flag lama **tidak memburuk**. Hasilnya malah sedikit lebih baik di 5% teratas dan di provinsi uji.
- Model tanpa fitur hampir tidak menemukan RF8: 3,5% di 200 teratas, sedangkan rata-ratanya 2,1%. Jadi RF8 sebagai red flag evaluasi tidak menambah apa-apa, karena isinya hanya aturan satu kolom.

## Temuan sampingan yang penting untuk v4

**16% dari 200 teratas pelaksanaan v4 (32 paket) punya realisasi hampir tepat 2 kali pagu.** Di semua paket, angkanya hanya 0,9%. Artinya fitur rasio realisasi ikut mengangkat paket yang diduga tercatat ganda. Hal ini lebih ke masalah data daripada pola pengadaan yang tidak lazim.

## Pilihan untuk jalur pelaksanaan

1. **Bersihkan catatan ganda dulu (disarankan).** Dua catatan realisasi dengan kode RUP dan nilai yang sama dihitung satu kali, lalu model pelaksanaan dilatih ulang. Fitur realisasi tetap dipakai, sesuai rumusan masalah yang memasangkan RUP dengan realisasi.
2. **Pakai versi eksperimen B.** Fitur realisasi dibuang. Angkanya sedikit lebih baik di 5% teratas, tetapi makna "pasangan RUP + realisasi" jadi lemah.
3. **Tetap v4,** dan catatan ganda ditulis sebagai batasan.

Untuk R016 dan R068, tidak ada yang dijadikan red flag baru.
