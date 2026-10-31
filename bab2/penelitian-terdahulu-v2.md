# 2.1 Hasil Penelitian Terdahulu (Draf v2)

> Mengikuti format proposal Nadia Ayula: paragraf pengantar, tabel "Keterkaitan Penelitian" per studi (Jurnal, Judul, Peneliti, Publisher, Tahun, Ringkasan, Keterkaitan), lalu 2.1.1 Sintesis Penelitian Terdahulu (paragraf temuan, tabel Aspek–Temuan–Implikasi, paragraf celah). Draf v1 tetap disimpan sebagai cadangan.

---

Pada bagian ini disajikan sepuluh penelitian terdahulu yang relevan dengan topik tugas akhir, mencakup pemetaan penelitian deteksi penyimpangan pengadaan, penerapan deteksi anomali pada data belanja dan pengadaan pemerintah, penggabungan beberapa metode deteksi anomali, serta penggunaan explainable AI dan alat bantu bagi pengawas. Setiap penelitian dirangkum berdasarkan jurnal, judul, peneliti, tahun, ringkasan, dan keterkaitannya dengan tugas akhir ini.

**Tabel 2.1 Keterkaitan Penelitian 1**

| | |
|---|---|
| Jurnal | EPJ Data Science |
| Judul | Detection of Fraud in Public Procurement Using Data-Driven Methods: A Systematic Mapping Study |
| Peneliti | Everton Schneider dos Santos, Matheus Machado dos Santos, Márcio Castro, Jônata Tyska Carvalho |
| Publisher | SpringerOpen |
| Tahun | 2025 |
| Ringkasan | Penelitian ini memetakan 93 studi tentang deteksi penyimpangan pada pengadaan publik berbasis data. Hasilnya menunjukkan bahwa sebagian besar studi menggunakan machine learning, sedangkan hanya dua studi yang benar-benar diterapkan dalam sistem yang dipakai lembaga pengawas. |
| Keterkaitan | Penelitian ini menjadi landasan umum bahwa machine learning relevan untuk deteksi penyimpangan pengadaan. Temuan bahwa hasil penelitian jarang sampai ke pengguna mendukung pengembangan dashboard pada tugas akhir ini. |

**Tabel 2.2 Keterkaitan Penelitian 2**

| | |
|---|---|
| Jurnal | Jurnal Manajemen Perbendaharaan |
| Judul | Deteksi Anomali Menggunakan Isolation Forest Belanja Barang Persediaan Konsumsi pada Satuan Kerja Kepolisian Republik Indonesia |
| Peneliti | Ahmad Zulfikar, Farhan Ariq Rahmani, Nurul Azizah |
| Publisher | Direktorat Jenderal Perbendaharaan, Kementerian Keuangan |
| Tahun | 2023 |
| Ringkasan | Penelitian ini menerapkan Isolation Forest pada realisasi belanja barang persediaan konsumsi (akun 521811) satuan kerja Polri tahun 2019–2021. Model paling optimal diperoleh pada parameter contamination 0,3%, dan hasilnya diusulkan menjadi fitur tambahan pada aplikasi SAKTI. |
| Keterkaitan | Penelitian ini menjadi acuan penerapan Isolation Forest pada data belanja pemerintah Indonesia. Perbedaannya, penelitian ini hanya memakai satu model, menilai belanja yang sudah terealisasi, dan belum menyertakan penjelasan hasil. |

**Tabel 2.3 Keterkaitan Penelitian 3**

| | |
|---|---|
| Jurnal | Bulletin of Informatics and Data Science |
| Judul | Hybrid Chaos-Isolation Forest Framework for Anomaly Detection in Indonesia's Public Procurement |
| Peneliti | E. W. Ambarsari, Desyanti, D. Fathudin |
| Publisher | [CEK: nama penerbit] |
| Tahun | 2025 |
| Ringkasan | Penelitian ini menggabungkan pendekatan chaos dengan Isolation Forest untuk mendeteksi anomali pada data tender pengadaan publik Indonesia berformat Open Contracting Data Standard (OCDS). Analisis dilakukan pada agregat bulanan. |
| Keterkaitan | Penelitian ini menunjukkan bahwa data pengadaan terbuka di Indonesia dapat dipakai untuk deteksi anomali. Perbedaannya, analisis pada agregat bulanan belum menghasilkan prioritas per paket, dan penelitian ini belum menyertakan penjelasan hasil. |

**Tabel 2.4 Keterkaitan Penelitian 4**

| | |
|---|---|
| Jurnal | Procedia Computer Science |
| Judul | Data-Driven Transparency: Machine Learning and Social Network Analysis for Corruption Detection in Public Procurement |
| Peneliti | Ricardo Muñoz-Cancino, Sebastián A. Ríos |
| Publisher | Elsevier |
| Tahun | 2025 |
| Ringkasan | Penelitian ini membentuk fitur jaringan penyedia dengan Social Network Analysis pada data pengadaan publik Chile (ChileCompra), lalu menerapkan dua model Isolation Forest pada tingkat penyedia dan tingkat kelompok penyedia. SHAP digunakan untuk menunjukkan fitur yang paling memengaruhi hasil, seperti umur perusahaan dan keterhubungan antarpenyedia. |
| Keterkaitan | Penelitian ini mendukung penggunaan Isolation Forest dan SHAP pada data pengadaan pemerintah. Perbedaannya, unit analisisnya adalah penyedia, bukan paket, dan hanya memakai satu jenis model. |

**Tabel 2.5 Keterkaitan Penelitian 5**

| | |
|---|---|
| Jurnal | Information |
| Judul | Applied Machine Learning to Anomaly Detection in Enterprise Purchase Processes: A Hybrid Approach Using Clustering and Isolation Forest |
| Peneliti | Antonio Herreros-Martínez, Rafael Magdalena-Benedicto, Joan Vila-Francés, Antonio José Serrano-López, Sonia Pérez-Díaz, José Javier Martínez-Herráiz |
| Publisher | MDPI |
| Tahun | 2025 |
| Ringkasan | Penelitian ini menerapkan z-Score, DBSCAN, k-Means, dan Isolation Forest pada dua dataset transaksi pembelian perusahaan. Setiap metode menghasilkan daftar transaksi kandidat, lalu hasilnya digabungkan dalam ensemble prioritisation dan dijelaskan menggunakan SHAP untuk membantu auditor internal. |
| Keterkaitan | Penelitian ini menjadi acuan utama penggabungan beberapa metode deteksi anomali untuk menyusun prioritas pemeriksaan beserta penjelasannya. Perbedaannya, penelitian ini diterapkan pada pembelian perusahaan, bukan pengadaan pemerintah. |

**Tabel 2.6 Keterkaitan Penelitian 6**

| | |
|---|---|
| Jurnal | Data & Policy |
| Judul | VigIA: Prioritizing Public Procurement Oversight with Machine Learning Models and Risk Indices |
| Peneliti | Andrés Salazar, Juan F. Pérez, Jorge Gallego |
| Publisher | Cambridge University Press |
| Tahun | 2024 |
| Ringkasan | Penelitian ini mengembangkan VigIA, alat bantu bagi lembaga pengawas pengadaan Kota Bogotá, Kolombia. VigIA terdiri atas model machine learning untuk memprediksi pembengkakan biaya dan keterlambatan kontrak, serta indeks risiko berbasis red flag, dengan memanfaatkan data terbuka SECOP II. |
| Keterkaitan | Penelitian ini menjadi acuan perancangan dashboard yang ditujukan bagi pengawas dan pemanfaatan data pengadaan terbuka. Perbedaannya, modelnya bersifat supervised dan membutuhkan variabel target dari kontrak yang sudah berjalan. |

**Tabel 2.7 Keterkaitan Penelitian 7**

| | |
|---|---|
| Jurnal | International Transactions in Operational Research |
| Judul | Explainable Anomaly Detection for Procurement Fraud Identification—Lessons from Practical Deployments |
| Peneliti | A. Westerski, R. Kanagasabai, E. Shaham, A. Narayanan, J. Wong, M. Singh |
| Publisher | Wiley |
| Tahun | 2021 |
| Ringkasan | Penelitian ini membahas pengalaman penerapan deteksi anomali pada data pengadaan di lingkungan pemerintah. Hasilnya menunjukkan bahwa hasil deteksi lebih mudah ditindaklanjuti oleh pemeriksa jika disertai alasan mengapa suatu transaksi ditandai. |
| Keterkaitan | Penelitian ini menjadi dasar perlunya penjelasan pada setiap paket yang diprioritaskan dalam tugas akhir ini. |

**Tabel 2.8 Keterkaitan Penelitian 8**

| | |
|---|---|
| Jurnal | Advances in Neural Information Processing Systems (NeurIPS) |
| Judul | ADBench: Anomaly Detection Benchmark |
| Peneliti | S. Han, X. Hu, H. Huang, M. Jiang, Y. Zhao |
| Publisher | NeurIPS Foundation |
| Tahun | 2022 |
| Ringkasan | Penelitian ini membandingkan 30 algoritma deteksi anomali pada 57 dataset. Hasilnya menunjukkan bahwa tidak ada satu metode yang selalu unggul pada semua dataset, karena setiap metode peka terhadap jenis anomali yang berbeda. |
| Keterkaitan | Penelitian ini mendukung alasan tugas akhir ini tidak mengandalkan satu model saja, melainkan menggabungkan Isolation Forest, LOF, dan Autoencoder. |

**Tabel 2.9 Keterkaitan Penelitian 9**

| | |
|---|---|
| Jurnal | AI |
| Judul | Less Is More: Principled Diversity in Heterogeneous Anomaly Detection Ensembles |
| Peneliti | T. Krčmar, D. Šabanović, M. Köhler, I. Lukić |
| Publisher | MDPI |
| Tahun | 2026 |
| Ringkasan | Penelitian ini menguji ensemble deteksi anomali yang tersusun dari metode dengan prinsip berbeda. Hasilnya menunjukkan bahwa ensemble memberikan kinerja yang konsisten di peringkat atas dan mengungguli model individual yang lemah, dengan kinerja yang setara dengan model individual terbaik. |
| Keterkaitan | Penelitian ini mendukung penggunaan ensemble dari metode yang berbeda prinsip agar hasil lebih konsisten. Hal ini sejalan dengan pemilihan Isolation Forest (isolasi), LOF (kepadatan lokal), dan Autoencoder (galat rekonstruksi). |

**Tabel 2.10 Keterkaitan Penelitian 10**

| | |
|---|---|
| Jurnal | Expert Systems with Applications |
| Judul | Explaining Anomalies Detected by Autoencoders Using Shapley Additive Explanations |
| Peneliti | L. Antwarg, R. M. Miller, B. Shapira, L. Rokach |
| Publisher | Elsevier |
| Tahun | 2021 |
| Ringkasan | Penelitian ini mengembangkan cara menjelaskan anomali yang ditemukan oleh Autoencoder menggunakan SHAP, sehingga dapat diketahui fitur yang paling memengaruhi tingginya galat rekonstruksi. |
| Keterkaitan | Penelitian ini mendukung penggunaan SHAP pada tugas akhir ini, termasuk untuk komponen Autoencoder dalam ensemble. |

---

## 2.1.1 Sintesis Penelitian Terdahulu

Berdasarkan penelitian terdahulu, terdapat beberapa temuan penting yang menjadi dasar tugas akhir ini. Pertama, machine learning telah banyak digunakan untuk mendeteksi penyimpangan pengadaan, dan pendekatan unsupervised seperti Isolation Forest sudah diterapkan pada data belanja dan pengadaan pemerintah di Indonesia. Kedua, tidak ada satu metode deteksi anomali yang selalu unggul, sehingga penggabungan beberapa metode dengan prinsip berbeda memberikan hasil yang lebih konsisten. Ketiga, hasil deteksi lebih mudah ditindaklanjuti jika disertai penjelasan, dan SHAP dapat digunakan termasuk pada Autoencoder. Keempat, hasil penelitian perlu disajikan dalam alat bantu yang mudah digunakan oleh pengawas.

**Tabel 2.11 Sintesis Penelitian Terdahulu**

| Aspek | Temuan Utama | Implikasi terhadap Tugas Akhir Ini |
|---|---|---|
| Data dan tahap pengadaan | Penelitian di Indonesia menilai data yang sudah berjalan, yaitu realisasi belanja dan tender, sehingga paket yang masih berupa RUP belum dinilai. | Tugas akhir ini menilai paket melalui dua jalur, yaitu jalur perencanaan (data RUP) dan jalur pelaksanaan (pasangan RUP dan realisasi). |
| Pemilihan model | Isolation Forest paling sering dipakai, tetapi tidak ada satu metode yang selalu unggul pada semua data. | Tugas akhir ini membandingkan Isolation Forest, LOF, dan Autoencoder sebagai model individual. |
| Penggabungan model | Penggabungan metode dengan prinsip berbeda memberikan hasil yang lebih konsisten dan dapat dipakai untuk menyusun prioritas pemeriksaan. | Tugas akhir ini menggabungkan ketiga model dalam ensemble untuk menghasilkan peringkat paket. |
| Interpretasi model | SHAP digunakan untuk menjelaskan fitur yang memengaruhi hasil deteksi, termasuk pada Autoencoder. | Tugas akhir ini menggunakan SHAP untuk menjelaskan paket yang diprioritaskan. |
| Penyajian hasil | Hasil penelitian jarang diterapkan dalam sistem yang dipakai pengawas, sedangkan alat bantu seperti VigIA terbukti membantu menentukan prioritas pemeriksaan. | Tugas akhir ini menyajikan hasil dalam dashboard berisi sebaran antarprovinsi dan rincian paket beserta penjelasannya. |

Dengan demikian, celah yang diambil dalam tugas akhir ini adalah pengembangan deteksi anomali berbasis ensemble Isolation Forest, LOF, dan Autoencoder pada data RUP serta pasangan RUP dan realisasi pengadaan APBD pemerintah provinsi, yang dilengkapi penjelasan SHAP dan disajikan dalam dashboard untuk membantu pengawas menentukan paket yang perlu ditelusuri lebih lanjut.

---

## Catatan untuk Tio (di luar naskah)

- Ayula memakai 12 penelitian. Di sini ada 10: enam penelitian inti dari v1 ditambah empat penelitian pendukung metode (Schneider dos Santos, Han, Krčmar, Antwarg) yang sudah ada di Daftar Pustaka Bab 1.
- Isi Zulfikar, Muñoz-Cancino, Herreros-Martínez, VigIA, dan Schneider dos Santos sudah dicek ke PDF di library. Ambarsari, Westerski, Han, Krčmar, dan Antwarg tidak ada PDF-nya di library, jadi isinya berdasarkan abstrak. Sebaiknya angka dan klaimnya dicek ulang ke paper aslinya.
- Nama penerbit Ambarsari dan nama lengkap peneliti yang masih berupa inisial perlu dilengkapi.
