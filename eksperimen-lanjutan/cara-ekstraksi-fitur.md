# Cara ekstraksi fitur (model v5 sekarang)

Sumber kode: /mnt/project-files/model-v5/s1_data.py, s2_model.py (fungsi `fitur`), x3_nama_satker.py.

## Urutan lengkap

1. Tentukan red flag (dari Perpres dan OCP), sebelum melihat model.
2. Kumpulkan data RUP dan realisasi.
3. Pra-pemrosesan: hanya paket penyedia, buang "Dikecualikan", buang pagu ≤ Rp10 rb, gabungkan realisasi per paket, buang rasio realisasi yang tidak masuk akal.
4. Ekstraksi fitur, dan hitung red flag. Red flag disimpan **terpisah** dan tidak masuk model.
5. Latih model (IF, LOF, Autoencoder; 5 seed).
6. Evaluasi (Precision@K memakai red flag), lalu SHAP dan dashboard.

## Ide dasarnya

Model tidak diberi kolom mentah. Model diberi **angka yang menjawab "seberapa besar paket ini dibanding paket yang mirip?"**. Paket Rp5 M itu wajar untuk konstruksi jalan, tetapi aneh untuk ATK. Karena itu sebagian besar fitur berupa **rasio pagu terhadap median pembanding**.

Semua rasio dihitung dalam log10, jadi 1 artinya 10 kali lipat dan 2 artinya 100 kali lipat. Rasio juga dibuat **satu arah**: kalau pagu lebih kecil dari pembanding, nilainya dibuat 0. Paket yang lebih murah tidak dianggap aneh.

## Fitur jalur perencanaan (data RUP)

| Fitur | Cara hitung | Arti |
|---|---|---|
| log_pagu | log10(pagu) | besar paket secara mutlak |
| log_rasio_pagu_sejenis | log10(pagu ÷ median pagu semua paket dengan **jenis + metode** sama, nasional) | lebih mahal dari paket sejenis? |
| log_rasio_pagu_satker | log10(pagu ÷ median pagu paket di **satker yang sama dengan jenis yang sama**). Kalau kelompoknya kurang dari 4 paket, nilainya 0 | lebih mahal dari kebiasaan satkernya? |
| log_rasio_pagu_nama_satker | log10(pagu ÷ median pagu paket **lain dengan nama sama** di satker yang sama). Hanya dihitung kalau ada ≥ 2 paket lain dan nama itu spesifik (dipakai ≤ 50 satker). Kalau tidak, nilainya 0 | barang yang sama di satker yang sama, tapi pagunya jauh lebih besar? |

## Fitur jalur pelaksanaan (RUP + realisasi)

Fitur ini terdiri dari tiga fitur pertama di atas (tanpa fitur nama), ditambah:

| Fitur | Cara hitung | Arti |
|---|---|---|
| rasio_realisasi | realisasi ÷ pagu (dipotong maksimal 5) | realisasi jauh di bawah atau di atas pagu |
| log_selisih_realisasi | log10(1 + \|realisasi − pagu\|) | besar selisih dalam rupiah |

## Contoh (angka ilustrasi)

Paket "Pengadaan Laptop", PL, Barang, pagu Rp180 jt.
- Median PL Barang nasional = Rp18 jt → rasio sejenis = log10(10) = **1,0**.
- Median paket Barang di satkernya = Rp36 jt → rasio satker = log10(5) = **0,7**.
- Dua paket lain "Pengadaan Laptop" di satker yang sama: Rp45 jt dan Rp45 jt → rasio nama = log10(4) = **0,6**.
- log_pagu = log10(180.000.000) = **8,26**.

Keempat angka ini masuk ke model setelah diskalakan (standardisasi).

## Langkah terakhir sebelum latih

- **Standardisasi:** setiap fitur dikurangi rata-ratanya lalu dibagi simpangan bakunya, supaya skalanya setara. Fitur nama memakai simpangan baku fitur sejenis.
- **Dibuang dari fitur** karena sama dengan red flag (supaya evaluasi tidak menyontek):
  - metode (sama dengan RF4 Penunjukan Langsung);
  - kemiripan nama untuk pemecahan paket (sama dengan RF3);
  - frekuensi penyedia (sama dengan RF5/RF6).
- Dibuang juga karena justru membuat kategori jarang dianggap aneh: one-hot jenis/sumber, PDN/UMK biner, profil metode satker.
