# Eksperimen satker kecil (29 Oktober 2026)

**Masalah:** satker dengan kurang dari 10 paket hanya 0,4% dari seluruh paket perencanaan, tetapi mengisi 58% dari 50 teratas dan 24% dari 200 teratas v5. Penyebabnya dua fitur:
- "porsi pagu di satker" bernilai 100% kalau satker hanya punya 1 paket;
- "jumlah paket satker" bernilai 1.

Kedua nilai itu terlihat ekstrem, padahal memang begitu bentuk satker kecil.

Kode: `../x1_satker_kecil.py` (latih), `../x2_banding_satker_kecil.py` (banding). Angka lengkap: `banding.csv`. Model v5 dan dashboard tidak diubah.

## Varian yang diuji

| Varian | Isi |
|---|---|
| N3 / N5 / N10 | Untuk satker dengan paket kurang dari 3/5/10, porsi pagu disamakan dengan median, dan jumlah paket satker dibuat satu arah |
| N5-tanpaJ | Sama dengan N5, tetapi jumlah paket tidak diubah |
| D | Porsi pagu satker dan jumlah paket satker dibuang |
| **R** | Porsi pagu satker diganti **"pagu dibanding rata-rata pagu paket di satkernya"** (satu arah). Satker yang punya 1 paket nilainya wajar (= 1 kali rata-rata). Jumlah paket satker dibuang |
| X5 | Satker dengan kurang dari 5 paket tidak ikut dinilai |

## Hasil jalur perencanaan (red flag v5)

| | v5 | **R** | N5-tanpaJ | D | N10 |
|---|---|---|---|---|---|
| Satker < 10 paket di 50 teratas | 58% | **10%** | 50% | 2% | 28% |
| Satker < 10 paket di 200 teratas | 24% | **3%** | 28,5% | 2,5% | 11% |
| 200 teratas ber-red flag (acuan 15,8%) | 38,5% | 33,5% | 42% | 14% | 24,5% |
| 5% teratas ber-red flag | 38,2% | **41,7%** | 37,8% | 40,6% | 34,8% |
| 5% teratas, provinsi pilih (acuan 17,9%) | 41,0% | **47,4%** | 41,7% | 43,3% | 38,3% |
| 5% teratas, **provinsi uji** (acuan 13,8%) | 34,2% | **39,9%** | 34,0% | 33,9% | 28,1% |
| 5% teratas tanpa penunjukan langsung | 35,3% | **39,0%** | 34,7% | 36,5% | 31,7% |
| Pagu < Rp10 jt di 200 teratas | 13% | 19% | 11% | 46% | 14% |

## Hasil jalur pelaksanaan

| | v5 | **R** | N10 |
|---|---|---|---|
| Satker < 10 paket di 200 teratas | 10% | **0,5%** | 0% |
| 200 teratas ber-red flag (acuan 26,3%) | 50% | 40% | 42,5% |
| 5% teratas | 29,9% | **31,2%** | 30,7% |
| 5% teratas, provinsi uji (acuan 25,6%) | 26,4% | **27,7%** | 27,1% |

## Kesimpulan

- **N3/N5/N10 tidak berhasil.** Jumlah paket satker yang dibuat satu arah membuat satker kecil terlihat "normal", sehingga porsi pagunya yang besar malah makin terlihat aneh.
- **Aturan pilih yang saya tetapkan di awal memilih D, tetapi D jelek.** 200 teratasnya di bawah acuan, dan 46% berisi paket < Rp10 jt. Aturan itu terlalu sempit karena hanya melihat porsi satker kecil, jadi pilihan akhirnya tidak mengikuti aturan tersebut. Ini perlu ditulis jujur.
- **R paling seimbang:**
  - masalah satker kecil hilang (58% → 10% di 50 teratas);
  - 5% teratas naik, termasuk di provinsi uji yang tidak dipakai saat memilih (34,2% → 39,9% di perencanaan);
  - definisinya sama untuk kedua jalur.
- **Harga yang dibayar R:** 200 teratas yang ber-red flag turun (perencanaan 38,5% → 33,5%, pelaksanaan 50% → 40%), meskipun masih 2,1 dan 1,5 kali acuan.
- Satker 1 paket masih bisa muncul kalau memang ada alasannya. Contohnya RSUD Tanah Abang, pengadaan langsung Rp16,9 M, yang punya red flag RF2. Paket ini muncul karena nilainya, bukan karena ukuran satkernya.
