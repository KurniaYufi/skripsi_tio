# Eksperimen fitur "pagu dibanding paket bernama sama di satker yang sama" (29 Oktober 2026)

Fitur: log10(pagu / median pagu paket **lain** dengan nama sama di satker yang sama), satu arah. Nama disamakan dulu: huruf kecil, angka dan tanda baca dibuang. Ada 127 ribu paket yang punya kembaran nama di satkernya.

Dua varian diuji:
- **M2**: cukup 1 paket lain sebagai pembanding.
- **M3**: minimal 2 paket lain sebagai pembanding, seperti contoh paket A, B, C.

Model dasarnya v5 (yang ada di dashboard sekarang). Kode: `../x3_nama_satker.py` dan `../x4_banding_nama_satker.py`. Angka lengkap: `banding.csv`.

Yang disebut **pola A-B-C** di bawah: paket yang pagunya ≥ 10 kali paket lain bernama sama di satkernya, dengan minimal 2 paket lain. Ada 4.724 paket seperti ini di jalur perencanaan.

## Hasil

| Perencanaan | v5 | M2 | M3 |
|---|---|---|---|
| Pola A-B-C yang masuk 5% teratas (acak = 5%) | 4% | 26,5% | **38,8%** |
| Pola A-B-C di 200 teratas | 2 | 30 | 47 |
| 5% teratas ber-red flag | **41,7%** | 37,4% | 36,3% |
| 5% teratas, provinsi uji (acuan 13,8%) | **39,9%** | 25,1% | 28,9% |
| 200 teratas ber-red flag | 33,5% | 33% | 33% |
| 200 teratas tanpa penunjukan langsung | 15% | 23% | 19,5% |
| Pagu < Rp10 jt di 200 teratas | 19% | 8% | 9,5% |

| Pelaksanaan | v5 | M2 | M3 |
|---|---|---|---|
| Pola A-B-C yang masuk 5% teratas | 9% | 26% | 26% |
| 5% teratas ber-red flag | **31,2%** | 28,4% | 29,0% |
| 5% teratas, provinsi uji (acuan 25,6%) | **27,7%** | 26,8% | 27,0% |
| 200 teratas ber-red flag | 40% | 35% | 42,5% |

Contoh di jalur perencanaan (M3):
- "Bahan Cetak" Dinas Pendidikan Rp20 M naik dari peringkat 24.076 ke **23**.
- "Makan Minum Rapat" Setwan DPRD Rp25,7 M naik dari peringkat 26.162 ke **70**.

## Kesimpulan

- **Fitur ini berhasil menangkap pola A-B-C.** Wajar, karena polanya sekarang ada di fitur. Jadi angka ini hanya pengecekan kewajaran, bukan bukti validitas.
- **Kesesuaian dengan red flag yang independen turun**, terutama di provinsi uji (perencanaan 39,9% → 28,9%). Paket pola A-B-C menggeser paket lain yang punya red flag pengadaan.
- Ini tidak berarti pola A-B-C tidak penting. Pola ini memang jenis keanehan lain yang tidak ada di daftar red flag. Tetapi kalau fitur ini dimasukkan, bukti utama skripsi (Precision@K) jadi lebih lemah.

## Pilihan

1. **Jadikan penanda terpisah di dashboard dan naskah (disarankan).** Model tetap v5. Paket pola A-B-C diberi penanda "Pagu jauh di atas paket bernama sama di satkernya" di samping red flag, lengkap dengan daftar paket pembandingnya. Penanda ini tidak ikut skor maupun Precision@K.
2. **Masukkan ke model (M3).** Pola A-B-C tertangkap oleh skor, tetapi Precision@K turun dan harus dijelaskan.
3. Tidak dipakai.
