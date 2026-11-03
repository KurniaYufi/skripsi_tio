# Ringkasan Fitur, Red Flag, dan Cara Mendapatkannya (model-v5, versi 31 Oktober 2026)

Disusun 3 November 2026 dari kode model-v5 (s1_data.py, s2_model.py, x3_nama_satker.py, tambahan_sebelah.py). Disalin juga ke tab "Ringkasan Fitur dan Red Flag" di Google Doc SKRIPSI TIO.

## 1. Sumber data dan kolom yang dipakai

Data berasal dari portal Data INAPROC (data.inaproc.id), tahun anggaran 2025, 38 pemerintah provinsi.

| Data | Kolom yang dipakai | Kegunaan |
|---|---|---|
| RUP | kode_rup, nama_instansi, nama_satuan_kerja, nama_paket, cara_pengadaan, metode_pengadaan, jenis_pengadaan, total_nilai (pagu), produk_dalam_negeri, status_umk | Lingkup data, fitur pagu, red flag RF1-RF4, R013, E4, E5 |
| Realisasi | kode_rup, kode_paket, nama_instansi, total_nilai (nilai realisasi), nilai_pdn, nilai_umk, nama_penyedia, metode_pengadaan, sumber_transaksi, tahapan_pengadaan | Fitur realisasi dan penyedia, red flag RF5, RF6, E3-E6 |

RUP dan realisasi digabung melalui kode_rup. Satu kode_rup bisa punya beberapa baris realisasi, sehingga realisasi dijumlahkan per kode_rup.

## 2. Pembersihan data dan lingkup

| Langkah | Aturan |
|---|---|
| Lingkup paket | Hanya cara pengadaan Penyedia. Swakelola, metode "Dikecualikan", dan isian "-" dibuang |
| A2 | Pagu <= Rp10.000 dibuang |
| Jalur perencanaan | Semua paket RUP dalam lingkup dengan pagu >= Rp1 juta (303.930 paket) |
| B1 | Baris realisasi bernilai 0 atau minus dibuang |
| B2 | Baris realisasi yang provinsinya berbeda dengan RUP-nya dibuang |
| Serah terima | Jalur pelaksanaan hanya memakai paket yang semua baris realisasinya berstatus "Serah Terima" |
| B3 | Catatan ganda: baris bernilai sama dalam satu kode_rup dihitung sekali, jika totalnya melebihi pagu dan setelah digabung tidak lagi melebihi pagu |
| B4 | Nilai PDN/UMK 1-100 dibaca sebagai persen |
| B5 | Paket dengan realisasi < 1% atau > 9,5 kali pagu tidak dinilai |
| B6 | Paket Tender dengan lebih dari satu penyedia untuk satu kode paket tidak dinilai |
| C1 | Nama penyedia dirapikan ("A, A" menjadi "A"); bentuk usaha (PT, CV, UD, dll.) diabaikan saat mencocokkan penyedia |
| C2 | Penyedia yang berupa unit pemerintah (dinas, kelurahan, dll.) dianggap tidak diketahui ("-") |
| Jalur pelaksanaan | Paket hasil langkah di atas (105.499 paket) |

## 3. Fitur yang dilatih di model

Semua fitur berupa angka. Kolom kategori (metode, jenis, sumber transaksi, PDN/UMK) tidak dipakai sebagai fitur.

| Fitur | Jalur | Arti | Cara menghitung |
|---|---|---|---|
| log_pagu | Perencanaan, pelaksanaan | Besar pagu | log10(pagu) |
| log_rasio_pagu_sejenis | Perencanaan, pelaksanaan | Pagu dibanding paket sejenis | log10(pagu / median pagu paket nasional dengan jenis dan metode yang sama) |
| log_rasio_pagu_satker | Perencanaan, pelaksanaan | Pagu dibanding paket lain di satker yang sama | log10(pagu / median pagu paket satker dengan jenis yang sama). Bernilai 0 jika kelompok satker-jenis kurang dari 4 paket |
| log_rasio_pagu_nama_satker | Perencanaan | Pagu dibanding paket bernama sama di satker yang sama (pola A-B-C) | log10(pagu / median pagu paket lain bernama sama di satker). Nama dibandingkan setelah angka dan tanda baca dihapus. Bernilai 0 jika paket lain bernama sama kurang dari 2, atau nama itu dipakai lebih dari 50 satker se-nasional |
| rasio_realisasi | Pelaksanaan | Realisasi dibanding pagu | total realisasi / pagu, dipotong maksimal 5 |
| log_selisih_realisasi | Pelaksanaan | Besar selisih realisasi dan pagu | log10(1 + abs(realisasi - pagu)) |
| log_rasio_kebiasaan_penyedia | Pelaksanaan | Nilai paket dibanding kebiasaan penyedianya | log10(realisasi) - median log10(realisasi) semua paket penyedia itu. Bernilai 0 jika penyedia kosong atau punya kurang dari 3 paket |

Jalur perencanaan memakai 4 fitur, jalur pelaksanaan memakai 6 fitur.

Perlakuan sebelum masuk model:
- Satu arah: log_rasio_pagu_sejenis, log_rasio_pagu_satker, dan log_rasio_pagu_nama_satker dipotong di 0, sehingga hanya pagu yang lebih besar dari pembandingnya yang menaikkan skor.
- Semua fitur distandardisasi (z-score). Khusus log_rasio_pagu_nama_satker dibagi simpangan baku log_rasio_pagu_sejenis, karena fitur ini hampir selalu bernilai 0.

## 4. Red flag (hanya untuk evaluasi, tidak masuk model)

Batas pengadaan langsung (Perpres 46/2025 Pasal 38 ayat (3) dan Pasal 41 ayat (3)): Barang dan Jasa Lainnya Rp200 juta, Pekerjaan Konstruksi Rp400 juta, Jasa Konsultansi Rp100 juta.

| Kode | Nama | Jalur | Aturan | Kolom sumber | Rujukan |
|---|---|---|---|---|---|
| RF1 | PL mendekati ambang | Perencanaan, pelaksanaan | Metode Pengadaan Langsung dan pagu 90-100% batas PL. Untuk konstruksi juga pagu Rp180-200 juta (batas lama) | metode_pengadaan, jenis_pengadaan, total_nilai (RUP) | KPK (2026); OCP R002 |
| RF3 | Pemecahan paket | Perencanaan, pelaksanaan | Paket PL dengan pagu di bawah batas, dalam satker dan jenis yang sama, nama paketnya mirip (TF-IDF >= 0,8). Jika ada >= 2 paket mirip dan jumlah pagunya melebihi batas PL, semua paket itu ditandai | nama_paket, nama_satuan_kerja, jenis_pengadaan, metode_pengadaan, total_nilai (RUP) | KPK (2026); OCP R011; Perpres Pasal 20 ayat (2) huruf d |
| RF4 | Penunjukan langsung | Perencanaan, pelaksanaan | Metode = Penunjukan Langsung | metode_pengadaan (RUP) | OCP R010; Salazar et al. (2024) |
| R013 | Satker non-kompetitif | Perencanaan | Satker dengan >= 5 paket yang SEMUA paketnya Pengadaan Langsung atau Penunjukan Langsung; semua paket satker itu ditandai | nama_satuan_kerja, metode_pengadaan (RUP) | OCP R013 (diadaptasi) |
| RF5 | Penyedia dominan | Pelaksanaan | Satu penyedia menerima > 40% nilai realisasi satker yang punya >= 5 paket berpenyedia | nama_penyedia, total_nilai (realisasi), nama_satuan_kerja | OCP R040 |
| RF6 | Penyedia serba-ada | Pelaksanaan | Penyedia menang di >= 3 jenis pengadaan berbeda | nama_penyedia (realisasi), jenis_pengadaan (RUP) | OCP R048; Salazar et al. (2024) |
| E3 | Metode berubah | Pelaksanaan | Metode di realisasi berbeda dengan metode di RUP | metode_pengadaan (RUP dan realisasi) | Perpres Pasal 18-19, 22; OCP R012 |
| E4 | PDN kurang | Pelaksanaan | RUP menyatakan PDN, tetapi porsi nilai PDN di realisasi < 50% | produk_dalam_negeri (RUP), nilai_pdn, total_nilai (realisasi) | Perpres Pasal 66 |
| E5 | UMK kurang | Pelaksanaan | RUP dicadangkan untuk UMK, tetapi porsi nilai UMK di realisasi < 50% | status_umk (RUP), nilai_umk, total_nilai (realisasi) | Perpres Pasal 65 |
| E6 | Penyedia menguasai satker | Pelaksanaan | Di satker dengan >= 5 paket non-katalog berpenyedia, penyedia utama memegang >= 50% paket non-katalog; paket dari penyedia itu ditandai | nama_penyedia, sumber_transaksi (realisasi), nama_satuan_kerja | Perpres Pasal 7 ayat (1); OCP R040 |

Red flag yang dihitung tetapi tidak dipakai untuk evaluasi:
- RF2, PL melewati ambang (metode PL dan pagu di atas batas PL). Dihapus 31 Oktober 2026 karena bocor ke fitur log_rasio_pagu_sejenis. Disarankan tetap ditampilkan sebagai penanda kepatuhan terpisah di dashboard.

## 5. Ringkasan model

- Ensemble Isolation Forest, LOF, dan Autoencoder, dilatih terpisah untuk tiap jalur.
- Skor tiap model diubah menjadi peringkat persentil, dirata-rata antar 5 seed (42, 1, 2, 3, 4), lalu dirata-rata antar 3 model.
- Paket anomali = 5% skor ensemble tertinggi di tiap jalur.
- SHAP (Kernel SHAP) untuk 200 paket teratas di tiap jalur.
