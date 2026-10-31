# Review Daftar Fitur Lama vs Bab 3 v.1 dan Data 2025

Dicek 2026-10-28 terhadap data_rup_2025.csv dan dara_realisasi_2025.csv (paket penyedia selain "Dikecualikan" = 344.668 paket), Tabel 3.2 dan Tabel 3.3 di tab "Bab 3 v.1", serta teks jurnal di Library.

## 1. Masalah utama: fitur lama tumpang tindih dengan red flag

Tiga fitur lama sama dengan red flag yang dipakai untuk evaluasi:

| Fitur lama | Sama dengan red flag (Tabel 3.3) |
|---|---|
| freq_vendor_satker | Penyedia dengan banyak paket |
| max_similaritas, jumlah_paket_mirip | Pemecahan paket |
| non_tender | Prosedur tidak kompetitif |

Kalau fitur ini masuk model **dan** juga dipakai sebagai acuan Precision@K, evaluasinya berputar: model diberi tahu red flag-nya, lalu dinilai dengan red flag yang sama. Hasil Precision@K akan tinggi bukan karena model bagus. Bab 3.2.3.4 saat ini sudah menulis bahwa red flag tidak dimasukkan sebagai fitur.

## 2. Hasil cek per fitur

| Fitur lama | Cek data 2025 | Cek sumber | Saran |
|---|---|---|---|
| rasio_realisasi | Median 0,985; 9,1% paket tepat 100%; 42,5% paket ≥ 99% | Zulfikar et al. (2023) memakai rasio realisasi terhadap pagu: **benar**. Hasmi et al. (2026) membahas penyerapan per **akun belanja** di laporan realisasi Kota Kendari, bukan per paket, jadi jangan dipakai untuk klaim "realisasi 100% per paket = red flag" (di data, hampir separuh paket ≥ 99%). | **Pakai** sebagai fitur, rujuk Zulfikar saja |
| gap_abs_rp | Bisa dihitung | Turunan data | **Pakai** (sebaiknya dalam bentuk logaritma) |
| log_pagu | Pagu sangat timpang (median Rp15,9 jt, maks Rp2,29 T) | Turunan data | **Pakai** (sudah ada di Tabel 3.2) |
| non_tender | **98,7% paket non-tender** (E-Purchasing 55,4% + Pengadaan Langsung 42,1%). Hampir semua bernilai 1, jadi tidak membedakan paket | Schneider dos Santos et al. (2025): red flag paling umum memang single bid (11 studi) dan restricted procedure (7 studi), **benar**, tapi itu untuk tender, bukan "semua non-tender" | **Buang**. Ganti dengan one-hot metode (sudah di Tabel 3.2); penunjukan langsung tetap jadi red flag |
| freq_vendor_satker | Bisa dihitung (35.331 paket di atas persentil 95) | Schneider dos Santos et al. (2025) menyebut frequent winners sebagai fitur yang **masih perlu divalidasi** penelitian lanjutan, bukan red flag baku | Jadikan **red flag** saja (rujuk KPK 2026), bukan fitur |
| bayar_luar_sistem | Status "PAYMENT OUTSIDE SYSTEM" **hanya muncul di E-Katalog Versi 6.0**, di 37 provinsi (22.531 baris). Ini status bawaan sistem katalog, bukan ciri paket tertentu | Tidak ada rujukan | **Buang** |
| jumlah_transaksi_realisasi | Paket dengan lebih dari satu baris realisasi kebanyakan **E-Katalog** (19.401 dari 22.398). Baris berulang = beberapa pesanan/barang dalam katalog, bukan pembayaran bertahap | Tidak ada rujukan; tafsiran "pembayaran bertahap" tidak cocok dengan data | **Buang** |
| max_similaritas, jumlah_paket_mirip | Perlu untuk mempersempit aturan pemecahan paket (aturan kasar sekarang menandai ±61 ribu paket) | Poster mahasiswa S2 bukan sumber akademik. Potin et al. (2023) tidak ada di Library dan belum dicek aksesnya | Pakai sebagai **cara menghitung red flag pemecahan paket**, bukan fitur; rujuk KPK (2026) |
| rasio_pagu_vs_kategori | Bisa dihitung | Studi Kosta Rika/OECD tidak ada di Library, belum dibaca | **Pakai** (sama dengan "Rasio pagu terhadap paket sejenis" di Tabel 3.2); cukup dijelaskan sebagai pembanding paket sejenis, tanpa sitasi OECD |
| proporsi_non_tender_satker | Ikut masalah non_tender: hampir semua satker mendekati 100% | Turunan non_tender | **Ganti** dengan proporsi pengadaan langsung per satker (bervariasi, ±42% rata-rata) |
| jumlah_paket_satker | Bisa dihitung | Kasus berita (Lampung Utara, Rohil) bukan sumber akademik | **Pakai** (sudah ada di Tabel 3.2) tanpa sitasi berita |
| pagu_placeholder_suspect | 748 paket pagunya ≤ Rp10.000 | Tidak ada rujukan | Pindah ke **pra-pemrosesan** (paket pagu tidak wajar dibuang atau ditandai), bukan fitur |

## 3. Usulan daftar fitur gabungan

**Jalur perencanaan:** log pagu, rasio pagu terhadap paket sejenis, porsi pagu pada satuan kerja, jumlah paket satuan kerja, proporsi pengadaan langsung satuan kerja, metode pengadaan (one-hot), jenis pengadaan (one-hot), produk dalam negeri, status UMK.

**Jalur pelaksanaan:** semua fitur jalur perencanaan + rasio realisasi terhadap pagu, selisih realisasi dan pagu (log), perubahan metode pengadaan, porsi nilai PDN, porsi nilai UMK, sumber transaksi (one-hot).

**Red flag (hanya untuk evaluasi):** nilai mendekati ambang pengadaan langsung, pemecahan paket (dihitung dengan kemiripan nama paket), penyedia dengan banyak paket, penunjukan langsung.

Catatan: one-hot metode masih memuat kategori penunjukan langsung, jadi sedikit beririsan dengan red flag ke-4. Kalau mau benar-benar bersih, kategori metode bisa diringkas tanpa memisahkan penunjukan langsung, atau red flag ke-4 diganti.
