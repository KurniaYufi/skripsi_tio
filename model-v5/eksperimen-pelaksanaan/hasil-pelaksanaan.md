# Eksplorasi jalur pelaksanaan (29 Oktober 2026)

Permintaan Tio: jalur pelaksanaan "di-explore supaya hasilnya lebih bagus". Dasarnya model v5 setelah kategori Terintegrasi dan Tender Cepat dipisah. Kode: `../x5_pelaksanaan.py` dan `../x6_banding_pelaksanaan.py`. Angka lengkap: `banding.csv`.

## Varian yang dicoba

| Kode | Perubahan |
|---|---|
| Q | penskalaan quantile (seperti perencanaan) |
| S | rasio pagu sejenis dan rasio pagu satker satu arah (seperti perencanaan) |
| K | fitur ringkas: pdn/umk dari RUP dan sumber transaksi dibuang |
| QS, QSK | gabungan |
| L50 | LOF memakai 50 tetangga |
| P | tambah fitur penyedia (jumlah paket dan jumlah satker yang dilayani). Dinilai dengan RF1–RF4 saja, karena fitur ini dekat dengan RF5/RF6 |
| W… | bobot ensemble IF-LOF-AE, misalnya W121 = LOF dihitung 2 kali |

Aturan pilih ditulis **sebelum** melihat hasil:
- Varian dipilih berdasarkan 5% teratas di provinsi pilih.
- Syaratnya, paket kecil di 200 teratas tidak naik lebih dari 10 poin.
- Provinsi uji hanya dilaporkan, tidak dipakai untuk memilih.

## Hasil (5% teratas yang punya red flag)

| Varian | Provinsi pilih | Provinsi uji | Uji, RF1–RF4 saja | Pagu < Rp10 jt di 200 teratas |
|---|---|---|---|---|
| Acuan (acak) | 26,8% | 25,6% | 20,1% | – |
| **v5 sekarang** | 32,1% | 27,3% | 18,6% | 12% |
| S | 34,5% | **29,3%** | 21,4% | 9% |
| K (tidak lolos syarat) | 33,3% | 29,3% | 21,6% | 23,5% |
| L50 | 29,2% | **30,9%** | 22,7% | 7,5% |
| QSK (dipilih aturan) | **37,0%** | 27,0% | 18,6% | 22% |
| P | 32,3% | 26,4% | 17,3% | 17,5% |
| Q | 28,5% | 22,9% | 15,5% | 19,5% |
| W121 / W122 / W011 | 31–33% | 28,0–28,2% | 19,1–19,6% | 12–15% |

## Kesimpulan

1. **Tidak ada varian yang jelas lebih bagus.**
   - Aturan memilih QSK karena paling tinggi di provinsi pilih (37,0%). Tetapi di provinsi uji hasilnya sama saja dengan v5 (27,0% vs 27,3%). Artinya kenaikan QSK hanya kebetulan cocok dengan provinsi pilih.
   - S dan L50 naik 2–3,5 poin di provinsi uji. Selisih ini masih sekitar 2 kali galat acak, dan arahnya tidak sama di provinsi pilih (L50 justru turun).
2. **Fitur penyedia (P) dan bobot ensemble (W) tidak membantu.**
3. **Penyebab utamanya bukan pengaturan model.**
   - Kalau hanya dihitung dengan RF1–RF4, model pelaksanaan di provinsi uji berada **di bawah acak** (18,6% vs 20,1%).
   - RF1–RF4 adalah pola tahap perencanaan: pengadaan langsung dekat ambang, pemecahan paket, dan penunjukan langsung. Fitur pelaksanaan justru berfokus pada realisasi (realisasi dibanding pagu, PDN/UMK, sumber transaksi). Model pelaksanaan dan red flag-nya mengukur hal yang berbeda.
   - Sinyal yang ada di pelaksanaan hampir seluruhnya berasal dari RF5/RF6 (penyedia).
