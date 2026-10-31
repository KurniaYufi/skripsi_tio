# 2.1 Penelitian Terdahulu (Draf v1)

> Struktur sementara: tabel per penelitian (judul, penulis/tahun, metode, hasil, keterkaitan dengan penelitian ini), lalu tabel perbandingan dan paragraf posisi penelitian. Akan disesuaikan dengan format proposal Nadia Ayula setelah file-nya tersedia.

---

Bagian ini menguraikan penelitian terdahulu yang menjadi acuan dalam tugas akhir ini. Penelitian yang dipilih membahas deteksi anomali dan pemberian prioritas pemeriksaan pada data pengadaan atau belanja, baik di Indonesia maupun di luar negeri. Setiap penelitian diuraikan metode dan hasilnya, serta keterkaitannya dengan tugas akhir ini.

## 2.1.1 Deteksi Anomali Belanja Persediaan Satuan Kerja Polri

**Tabel 2.1** Penelitian Zulfikar et al. (2023)

| Aspek | Keterangan |
|---|---|
| Judul | Deteksi Anomali Menggunakan Isolation Forest Belanja Barang Persediaan Konsumsi pada Satuan Kerja Kepolisian Republik Indonesia |
| Penulis, Tahun | Zulfikar, Rahmani, & Azizah (2023) |
| Metode | Isolation Forest (unsupervised) |
| Data | Realisasi belanja barang persediaan konsumsi (akun 521811) satuan kerja Polri tahun 2019–2021 |
| Hasil | Model paling optimal diperoleh pada parameter *contamination* 0,3% dan diusulkan menjadi fitur tambahan pada aplikasi SAKTI |
| Keterkaitan | Menjadi acuan penerapan Isolation Forest pada data belanja pemerintah Indonesia. Namun, penelitian ini hanya memakai satu model, menilai belanja yang sudah terealisasi, dan belum menyertakan penjelasan atas hasil deteksi |

## 2.1.2 Deteksi Anomali pada Data Tender Pengadaan Indonesia

**Tabel 2.2** Penelitian Ambarsari et al. (2025)

| Aspek | Keterangan |
|---|---|
| Judul | Hybrid Chaos-Isolation Forest Framework for Anomaly Detection in Indonesia's Public Procurement |
| Penulis, Tahun | Ambarsari, Desyanti, & Fathudin (2025) |
| Metode | Isolation Forest yang dikombinasikan dengan pendekatan *chaos* |
| Data | Data tender pengadaan publik Indonesia dalam format Open Contracting Data Standard (OCDS), dianalisis dalam bentuk agregat bulanan |
| Hasil | Kerangka yang diusulkan mampu menandai periode dengan pola pengadaan yang tidak wajar |
| Keterkaitan | Menunjukkan bahwa data pengadaan terbuka di Indonesia dapat dipakai untuk deteksi anomali. Namun, analisis dilakukan pada agregat bulanan sehingga belum menghasilkan prioritas per paket, hanya memakai satu jenis model, dan belum menyertakan penjelasan |

## 2.1.3 Machine Learning dan Analisis Jaringan untuk Pengadaan Publik Chile

**Tabel 2.3** Penelitian Muñoz-Cancino & Ríos (2025)

| Aspek | Keterangan |
|---|---|
| Judul | Data-Driven Transparency: Machine Learning and Social Network Analysis for Corruption Detection in Public Procurement |
| Penulis, Tahun | Muñoz-Cancino & Ríos (2025) |
| Metode | Social Network Analysis untuk membentuk fitur jaringan penyedia, Isolation Forest pada tingkat penyedia dan tingkat kelompok penyedia, serta SHAP untuk menjelaskan fitur yang berpengaruh |
| Data | Data pengadaan publik Chile (ChileCompra) |
| Hasil | Model mampu menandai penyedia dan struktur jaringan penyedia yang tidak wajar, dan SHAP menunjukkan fitur yang paling memengaruhi hasil, seperti umur perusahaan dan keterhubungan antarpenyedia |
| Keterkaitan | Menjadi acuan penggunaan Isolation Forest dan SHAP pada pengadaan pemerintah. Perbedaannya, unit analisisnya adalah penyedia, bukan paket, dan hanya memakai satu jenis model |

## 2.1.4 Prioritas Pemeriksaan Anomali pada Proses Pembelian Perusahaan

**Tabel 2.4** Penelitian Herreros-Martínez et al. (2025)

| Aspek | Keterangan |
|---|---|
| Judul | Applied Machine Learning to Anomaly Detection in Enterprise Purchase Processes: A Hybrid Approach Using Clustering and Isolation Forest |
| Penulis, Tahun | Herreros-Martínez et al. (2025) |
| Metode | z-Score, DBSCAN, k-Means, dan Isolation Forest yang hasilnya digabungkan dalam *ensemble prioritisation*, serta SHAP untuk penjelasan |
| Data | Dua dataset transaksi pembelian perusahaan |
| Hasil | Setiap metode menghasilkan daftar transaksi kandidat, lalu penggabungannya menghasilkan satu daftar prioritas yang lebih ringkas untuk diperiksa auditor internal |
| Keterkaitan | Menjadi acuan utama penggabungan beberapa metode untuk menyusun prioritas pemeriksaan beserta penjelasannya. Namun, penelitian ini diterapkan pada pembelian perusahaan, bukan pengadaan pemerintah |

## 2.1.5 VigIA: Alat Bantu Prioritas Pengawasan Pengadaan

**Tabel 2.5** Penelitian Salazar et al. (2024)

| Aspek | Keterangan |
|---|---|
| Judul | VigIA: Prioritizing Public Procurement Oversight with Machine Learning Models and Risk Indices |
| Penulis, Tahun | Salazar, Pérez, & Gallego (2024) |
| Metode | Model machine learning supervised untuk memprediksi pembengkakan biaya dan keterlambatan kontrak, serta indeks risiko berbasis red flag |
| Data | Data terbuka pengadaan Kota Bogotá, Kolombia (SECOP II) |
| Hasil | VigIA diserahkan kepada lembaga pengawas untuk membantu memprioritaskan pemeriksaan dan alokasi sumber daya, dengan memperhatikan kemudahan penggunaan dan penjelasan hasil |
| Keterkaitan | Menjadi acuan perancangan dashboard yang ditujukan bagi pengawas. Namun, modelnya bersifat supervised dan membutuhkan variabel target dari kontrak yang sudah berjalan |

## 2.1.6 Deteksi Anomali yang Dapat Dijelaskan pada Pengadaan

**Tabel 2.6** Penelitian Westerski et al. (2021)

| Aspek | Keterangan |
|---|---|
| Judul | Explainable Anomaly Detection for Procurement Fraud Identification—Lessons from Practical Deployments |
| Penulis, Tahun | Westerski et al. (2021) |
| Metode | Deteksi anomali pada data pengadaan yang dilengkapi penjelasan hasil |
| Data | Data pengadaan pada penerapan nyata di lingkungan pemerintah |
| Hasil | Hasil deteksi lebih mudah ditindaklanjuti oleh pemeriksa jika disertai alasan mengapa suatu transaksi ditandai |
| Keterkaitan | Menjadi dasar perlunya penjelasan pada setiap paket yang diprioritaskan. Penelitian ini belum menggabungkan beberapa model dan tidak berfokus pada data perencanaan |

---

## 2.1.7 Perbandingan dan Posisi Penelitian

**Tabel 2.7** Perbandingan penelitian terdahulu dengan tugas akhir ini

| Penelitian | Pengadaan pemerintah | Data Indonesia | Unit paket/transaksi | Menilai tahap perencanaan (RUP) | Lebih dari satu model | Penjelasan (XAI) | Dashboard/alat bantu |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Zulfikar et al. (2023) | ✓ | ✓ | – | – | – | – | – |
| Ambarsari et al. (2025) | ✓ | ✓ | – | – | – | – | – |
| Muñoz-Cancino & Ríos (2025) | ✓ | – | – | – | – | ✓ | – |
| Herreros-Martínez et al. (2025) | – | – | ✓ | – | ✓ | ✓ | – |
| Salazar et al. (2024) | ✓ | – | ✓ | – | ✓ | ✓ | ✓ |
| Westerski et al. (2021) | ✓ | – | ✓ | – | – | ✓ | ✓ |
| **Tugas akhir ini** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Berdasarkan Tabel 2.7, penelitian di Indonesia sudah menerapkan Isolation Forest pada data belanja dan tender pemerintah, tetapi masih memakai satu model dan belum menyertakan penjelasan. Penelitian di luar negeri sudah menggabungkan beberapa metode, memakai SHAP, dan mengembangkan alat bantu bagi pengawas, tetapi diterapkan pada konteks yang berbeda. Selain itu, belum ada penelitian yang dibahas yang menilai paket sejak tahap perencanaan. Tugas akhir ini mengisi celah tersebut dengan menerapkan ensemble Isolation Forest, LOF, dan Autoencoder pada data RUP serta pasangan RUP dan realisasi pengadaan APBD pemerintah provinsi, lalu menjelaskan hasilnya dengan SHAP dan menyajikannya dalam dashboard.

---

## Catatan untuk Tio (di luar naskah)

- File "Proposal TA Nadia Ayula" tidak ada di folder project maupun di Google Drive yang bisa saya akses, jadi struktur di atas memakai format umum (tabel per penelitian + tabel perbandingan). Kalau file-nya diunggah, formatnya akan saya samakan.
- Isi Zulfikar, Muñoz-Cancino, Herreros-Martínez, dan VigIA sudah saya cek ulang ke PDF di library. Ambarsari dan Westerski tidak ada PDF-nya di library, jadi isinya berdasarkan abstrak yang dicek sebelumnya. Baris "Hasil" keduanya sebaiknya dicek ke paper aslinya.
- Tanda ✓ untuk Salazar pada kolom "Lebih dari satu model" artinya VigIA memakai beberapa model dan indeks risiko, bukan ensemble deteksi anomali. Tanda ✓ untuk Westerski pada kolom "Dashboard/alat bantu" mengacu pada penerapan nyatanya di lembaga.
- Semua referensi sudah ada di Daftar Pustaka Bab 1 v4.
