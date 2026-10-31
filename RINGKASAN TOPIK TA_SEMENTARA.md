# Ringkasan Inti TA: Deteksi Anomali Pengadaan Pemerintah Daerah

Dokumen ini merangkum keputusan dan rencana yang berlaku saat ini. Bagian "Belum diputuskan" sengaja dipisah supaya tidak tercampur dengan hal yang sudah final.

## 1. Topik

Deteksi anomali pada data Rencana Umum Pengadaan (RUP) dan Realisasi pengadaan pemerintah daerah bersumber APBD, memakai unsupervised learning dan explainable AI, dengan keluaran berupa daftar prioritas paket dan dashboard.

Judul kerja (belum final): *Deteksi Anomali pada Rencana Umum Pengadaan Barang/Jasa Pemerintah Daerah (SIRUP) Menggunakan Unsupervised Learning dan Explainable AI*

Posisi hasil: alat triase untuk menentukan paket mana yang ditelusuri lebih dulu, bukan alat pembuktian pelanggaran.

## 2. Prinsip yang dijaga

- Anomali bukan fraud. Skor tinggi berarti pola menyimpang secara statistik dan layak ditelusuri, bukan bukti pelanggaran.
- Tidak ada ground truth, jadi tidak memakai akurasi, F1, atau AUC klasik sebagai evaluasi utama.
- Hasil yang masih berupa rencana ditulis sebagai "akan diuji", bukan sebagai hasil.
- Klaim kebaruan hanya dibuat sebatas penelusuran literatur yang cakupannya jelas. Hindari kalimat "belum pernah diteliti".

## 3. Definisi operasional anomali

Paket pengadaan (atau kelompok paket) yang polanya menyimpang signifikan dari paket pembanding, dinilai dari kombinasi banyak fitur sekaligus, bukan dari satu aturan tunggal.

Dua tahap:
- **Anomali perencanaan:** dinilai dari data RUP saja, dibandingkan dengan paket sejenis.
- **Anomali pelaksanaan:** dinilai dari pasangan RUP dan Realisasi, yaitu penyimpangan realisasi terhadap rencana.

Tiga tipe penyimpangan:
- **Point:** satu paket menyimpang dari keseluruhan data.
- **Contextual:** wajar secara umum, tetapi aneh dibanding kelompoknya (kategori atau satker).
- **Collective:** sekumpulan paket yang bersama-sama membentuk pola tidak lazim.

Daftar indikator (rasio realisasi, pagu terhadap kategori, metode non-tender, vendor berulang, dan seterusnya) adalah dasar penyusunan fitur. Definisi anomali tetap satu: skor gabungan model atas semua fitur tersebut.

## 4. Data

**Sumber:** data.inaproc.id/rup dan data.inaproc.id/realisasi (ekspor CSV per instansi, tahun anggaran, dan sumber dana). Kunci gabung: `kode_rup`.

**Kolom RUP:** nama_instansi, nama_satuan_kerja, tahun_anggaran, cara_pengadaan, metode_pengadaan, jenis_pengadaan, nama_paket, kode_rup, sumber_dana, produk_dalam_negeri, total_nilai.

**Kolom Realisasi:** tambahan kode_paket, sumber_transaksi, nama_penyedia, status_paket, tahapan_pengadaan, nilai_pdn, nilai_umk.

**Keterbatasan data yang harus ditangani:**
- RUP tidak memuat vendor, dan ekspor bulk tidak memuat tanggal atau bulan.
- Nilai "-" pada metode dan jenis pengadaan menyamar sebagai kosong (berasal dari paket Swakelola). Harus dinormalisasi.
- Satu `kode_rup` bisa memiliki banyak baris Realisasi, jadi harus diagregasi sebelum digabung.
- Kolom `total_nilai` bermakna beda di dua file (pagu di RUP, nilai realisasi di Realisasi). Rename sebelum gabung.
- File RUP dan Realisasi harus bertahun anggaran sama, kalau tidak hampir tidak ada `kode_rup` yang cocok.
- Arti `total_nilai` pada Realisasi (nilai kontrak atau nilai pembayaran) perlu dipastikan dari dokumentasi portal.
- Halaman detail per paket di SIRUP memuat jadwal dan uraian yang tidak ada di ekspor bulk. Hanya realistis untuk paket top-N, bukan untuk seluruh data.

**Cara akses:** scraping browser (Playwright) sebagai jalur utama, belum tervalidasi ke situs asli. API resmi INAPROC (role API Integrator, surat permohonan ke LKPP, IP publik statis) berat bagi individu, dijadikan opsi jangka panjang.

## 5. Pipeline

```
Data RUP + Realisasi
  -> Pembersihan ("-" -> NaN, agregasi Realisasi per kode_rup, gabung via kode_rup)
  -> Kemiripan nama paket (TF-IDF, dalam satu satker)
  -> Pecah dua jalur: Perencanaan (seluruh RUP) dan Pelaksanaan (paket yang cocok RUP+Realisasi)
  -> Rekayasa fitur per jalur
  -> Ensemble tiga model -> skor gabungan -> ranking
  -> SHAP untuk paket teratas
  -> Validasi tanpa label
  -> Ranking, agregasi per wilayah, dashboard
```

### 5.1 Fitur jalur Perencanaan
- `log_pagu`
- `non_tender` (Penunjukan Langsung, Pengadaan Langsung, Dikecualikan)
- `log_rasio_pagu_kategori` (pagu dibagi median kategori sejenis, dalam bentuk log, dua arah)
- `proporsi_non_tender_satker` (dihitung hanya dari paket cara Penyedia)
- `log_jumlah_paket_satker`
- `pagu_placeholder_suspect` (pagu <= Rp1.000, bukan Dikecualikan, nama paket tidak bertanda sisa/desimal/pembulatan)
- `max_similaritas`, `log_jumlah_mirip` (dari TF-IDF)

### 5.2 Fitur jalur Pelaksanaan
- `log_rasio_realisasi` (realisasi dibagi pagu, bentuk log supaya 10x lebih besar dan 10x lebih kecil setara)
- `log_gap_rp`, `log_pagu`, `non_tender`
- `bayar_luar_sistem` (status PAYMENT OUTSIDE SYSTEM)
- `freq_vendor_satker`, `log_jumlah_transaksi`
- `max_similaritas`, `log_jumlah_mirip`

### 5.3 Model
- Isolation Forest, Local Outlier Factor, dan Autoencoder (pendekatan `MLPRegressor` yang merekonstruksi inputnya sendiri).
- LOF dilatih hanya pada baris fitur yang unik, karena baris kembar membuat skor LOF tidak valid.
- Skor tiap model dinormalisasi memakai peringkat persentil dari data latih (konstanta tetap, bukan dihitung ulang per batch), lalu dirata-rata menjadi skor gabungan.
- Tiga model dipakai karena prinsipnya berbeda (isolasi, kepadatan lokal, galat rekonstruksi), bukan karena ketiganya diharapkan selalu sepakat.

### 5.4 Explainable AI
- SHAP (PermutationExplainer) pada fungsi skor ensemble, dijalankan hanya untuk paket teratas.
- Keluaran per paket: kontribusi tiap fitur beserta arah pengaruhnya.

### 5.5 Rencana evaluasi (tanpa ground truth)
1. Kesepakatan antar model (korelasi peringkat dan irisan top-K).
2. Stabilitas peringkat terhadap pengambilan sampel ulang.
3. Precision@K dan lift terhadap red flag rasio, selalu dibandingkan dengan base rate. Catatan: validasi ini melingkar sebagian karena rasio juga menjadi fitur.
4. Pembanding sederhana (misalnya peringkat berdasarkan pagu saja). ML harus terbukti menambah nilai di atas pembanding ini.
5. Sensitivitas terhadap definisi "kategori sejenis" dan pembersihan paket sisa pembulatan.
6. Red flag independen: Realisasi tanpa pasangan RUP, dilaporkan sebagai daftar terpisah, bukan bagian dari precision@K.
7. Uji prediktif: apakah skor Perencanaan berkaitan dengan penyimpangan yang baru terlihat pada Pelaksanaan. Ini hipotesis yang diuji, bukan asumsi.
8. Telaah kualitatif atas sampel hasil teratas.

### 5.6 Keluaran dan dashboard
- Ranking per paket untuk tiap jalur.
- Agregasi per wilayah memakai rate (proporsi paket anomali atau rata-rata skor), bukan hitungan mentah, supaya daerah besar tidak otomatis tampak paling merah.
- Drill-down: klik wilayah, lihat paket paling anomali beserta penjelasan SHAP.
- Peta Indonesia berwarna per kabupaten/kota (butuh file batas wilayah GeoJSON).
- Dashboard memiliki pengguna dan tujuan: pengawas yang menentukan urutan penelusuran.

## 6. Rumusan masalah dan tujuan (draf)

| Rumusan masalah | Tujuan |
|---|---|
| Bagaimana mendeteksi anomali pada data RUP dan Realisasi tanpa label? | Mengembangkan dan membandingkan model unsupervised pada data tersebut |
| Bagaimana faktor penyebab suatu paket ditandai dapat dijelaskan? | Menerapkan SHAP untuk penjelasan per paket |
| Bagaimana hasil dievaluasi tanpa ground truth? | Merancang dan menerapkan skema evaluasi tanpa label |

## 7. Belum diputuskan

- **Cakupan wilayah dan tahun:** satu daerah, beberapa daerah sampel, atau nasional. Skala nasional memerlukan pengumpulan data yang belum terbukti layak.
- **Fitur tingkat kelompok:** misalnya jumlah paket berpagu identik dalam satu satker, untuk menangkap anomali collective. Belum ditambahkan ke pipeline.
- **Fitur graf (vendor dan instansi):** opsional, hanya relevan bila cakupan lintas instansi cukup luas.
- **Peran TF-IDF:** saat ini dipakai sebagai fitur, tetapi nama paket banyak berbentuk templat sehingga kemiripan tinggi belum tentu pemecahan paket. Perlu diputuskan tetap sebagai fitur atau pembanding.
- **Pelaporan konsensus model:** usulan memakai "ditandai minimal dua model" sebagai pengganti klaim "ketiga model sepakat".
- **Pemisahan populasi:** paket sisa pembulatan dan paket statutori berstatus Dikecualikan (misalnya iuran wajib, pengadaan tanah, tarif listrik) dianalisis terpisah atau tidak.
- **Judul final dan batasan masalah.**

## 8. Ditunda dan di luar target wajib

- **Chatbot (RAG):** pengembangan lanjutan, bukan target Bab 1 sampai 3. Bila dibuat: retrieval terstruktur dari tabel hasil (bukan pencarian kemiripan vektor), LLM hanya merangkai kalimat dari angka yang sudah dihitung, jawaban diverifikasi terhadap angka sumber, dan angka mentah selalu ditampilkan.
- **Graph RAG dan GNN:** tidak dipakai.
- **Analisis berbasis teks lanjutan (embedding IndoBERT):** hanya bila waktu memungkinkan.

## 9. Pertanyaan yang perlu dijawab sebelum menulis Bab 1 sampai 3

1. Apa arti `total_nilai` pada Realisasi di portal?
2. Apakah ekspor RUP memuat semua satker dan status paket?
3. Apakah pola utama bertahan pada 2 sampai 3 daerah lain?
4. Apakah fitur tingkat kelompok akan masuk desain?
5. Klaim "deteksi dini pada tahap RUP" belum boleh dipakai sebelum hipotesis pada poin 5.5 nomor 7 teruji.
