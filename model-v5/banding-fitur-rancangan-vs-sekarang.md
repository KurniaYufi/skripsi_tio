# Fitur rancangan awal Tio vs fitur model sekarang (30 Oktober 2026)

**Ringkasnya:** dari 11 fitur rancangan awal, nasibnya:
- **4 tetap dipakai** sebagai fitur, sebagian dengan perbaikan;
- **3 dipindah menjadi red flag atau alat hitung red flag**;
- **1 dipindah ke pra-pemrosesan**;
- **3 dibuang** karena ternyata bukan tanda anomali di data ini.

Ada juga **2 fitur baru** yang tidak ada di rancangan.

## Jalur pelaksanaan (dulu "jalur eksekusi")

| Fitur rancangan | Status sekarang | Alasan |
|---|---|---|
| rasio_realisasi | **Dipakai** ("realisasi dibanding pagu", maksimal 5 kali, dua arah) | Sesuai rancangan |
| gap_abs_rp | **Dipakai** ("besar selisih realisasi", skala log) | Sesuai rancangan |
| log_pagu | **Dipakai** | Uji tanpa log_pagu membuat hasil setara acak di kedua jalur. Ada efek sampingnya: peringkat atas jadi banyak berisi paket besar (lihat catatan 2) |
| non_tender | **Tidak jadi fitur; menjadi red flag** (RF1–RF4) | (1) 98,7% paket non-tender, jadi kolomnya hampir seragam dan model malah menganggap paket Tender yang "aneh". (2) Metode adalah dasar RF1–RF4. Kalau metode jadi fitur, Precision@K "menyontek" (temuan model v1: tanpa RF4, P@K perencanaan di bawah acak) |
| freq_vendor_satker | **Tidak jadi fitur; menjadi RF5** (penyedia dominan, OCP R040: satu penyedia > 40% nilai realisasi satker) | Supaya evaluasi tidak berputar. Definisinya diganti mengikuti OCP agar ada rujukan |
| bayar_luar_sistem | **Dibuang** | "PAYMENT OUTSIDE SYSTEM" ternyata status bawaan E-Katalog versi 6 di 37 provinsi, bukan kejadian khusus. Temuan di DKI Jakarta tidak berlaku umum |
| jumlah_transaksi_realisasi | **Dibuang** | Baris realisasi berulang hampir semuanya pesanan e-katalog berisi beberapa barang, bukan pembayaran bertahap. Catatan ganda yang sebenarnya sudah dibersihkan di pra-pemrosesan (aturan B3) |
| max_similaritas, jumlah_paket_mirip (TF-IDF) | **Tidak jadi fitur; menjadi alat hitung RF3** (pemecahan paket) | Kemiripan nama adalah inti pola pemecahan paket, jadi lebih tepat dipakai menilai model daripada menjadi masukan model |

## Jalur perencanaan

| Fitur rancangan | Status sekarang | Alasan |
|---|---|---|
| log_pagu | **Dipakai** | Sama seperti di atas |
| non_tender | **Tidak jadi fitur; menjadi red flag** | Sama seperti di atas |
| rasio_pagu_vs_kategori | **Dipakai, diperbaiki**: "pagu dibanding paket sejenis" | (1) Pembandingnya median, bukan rata-rata, karena rata-rata mudah terseret paket raksasa. (2) Kategorinya jenis **dan** metode. (3) Satu arah: hanya pagu yang lebih besar yang dianggap aneh. Lihat juga catatan 1 soal RF2 |
| proporsi_non_tender_satker | **Dibuang** | Bocor ke RF1/RF3, dan hampir kembar dengan porsi e-purchasing satker (korelasi −0,98) |
| jumlah_paket_satker | **Dibuang**, diganti "pagu dibanding paket di satker" | Satker yang hanya punya 1–4 paket otomatis dianggap aneh: 58% dari 50 paket teratas perencanaan berasal dari satker kecil |
| pagu_placeholder_suspect | **Dipindah ke pra-pemrosesan** | Pagu ≤ Rp10 ribu dibuang (748 paket), dan di jalur perencanaan pagu < Rp1 jt tidak dinilai. Lebih tepat dibersihkan daripada dinilai sebagai anomali |
| max_similaritas, jumlah_paket_mirip | **Alat hitung RF3** | Sama seperti di atas |

## Fitur baru yang tidak ada di rancangan

| Fitur | Jalur | Asal |
|---|---|---|
| Pagu dibanding paket di satker (jenis sama, minimal 4 paket) | keduanya | Pengganti jumlah_paket_satker: konteks satker tetap ada tanpa menghukum satker kecil |
| Pagu dibanding paket bernama sama di satker (pola A-B-C) | perencanaan | Usulan Tio |

## Catatan

1. **Tumpang tindih dengan RF2.** "Pagu dibanding paket sejenis" hampir sama dengan RF2 (PL lewat ambang). PL Rp350 jt pasti jauh di atas median PL, jadi fitur ini otomatis tinggi untuk paket ber-RF2. Karena itu Precision@K dilaporkan dengan dan tanpa RF2.
2. **log_pagu dan paket besar.** 200 teratas perencanaan didominasi paket di atas Rp1 M (69%). Ini konsekuensi log_pagu: besar pagu ikut dihitung, bukan hanya rasionya.
3. **Sumber yang perlu hati-hati** (dari pengecekan 28 Oktober):
   - **Hasmi dkk. (2026)** membahas penyerapan per **akun**, bukan per paket. Jangan dipakai sebagai dasar rasio realisasi per paket; pakai Zulfikar dkk. (2023).
   - **Studi Kosta Rika/OECD dan Potin dkk. (2023)** tidak ada di Library. Jangan dikutip.
   - **Poster mahasiswa S2 dan berita kasus** (Lampung Utara, Rohil) bukan sumber akademik.
   - **Schneider dos Santos dkk. (2025)**: "frequent winner" masih disebut perlu divalidasi. Untuk RF5 lebih aman merujuk OCP (2024) R040.
   - Kata "kecurangan" di kolom alasan sebaiknya diganti "penyimpangan" atau "ketidaklaziman".
