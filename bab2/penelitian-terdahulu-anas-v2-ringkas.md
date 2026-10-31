# BAB 2 TINJAUAN PUSTAKA

## 2.1 Hasil Penelitian Terdahulu

Dalam tugas akhir ini, penelitian-penelitian terdahulu yang relevan digunakan sebagai panduan dan rujukan utama dalam proses penelitian. Berikut merupakan beberapa penelitian terdahulu yang berkaitan dengan topik tugas akhir ini.

### 2.1.1 Deteksi Penyimpangan pada Pengadaan Publik

Penelitian yang dilakukan Schneider dos Santos et al. (2025) memetakan penelitian deteksi penyimpangan pada pengadaan publik dengan menyaring lebih dari 6.000 artikel menjadi 93 penelitian yang terbit pada periode 2020–2024. Hasilnya menunjukkan bahwa sebagian besar penelitian menggunakan machine learning, terutama untuk mendeteksi persekongkolan antarpenyedia, dan 31 penelitian memilih pendekatan unsupervised karena data kasus yang sudah terbukti jarang tersedia. Penelitian ini juga menemukan bahwa hanya dua dari 93 penelitian yang benar-benar diterapkan dalam sistem yang dipakai lembaga pengawas. Selain itu, dataset pengadaan yang terbuka untuk publik masih terbatas sehingga hasil penelitian sulit direplikasi.

Salah satu contoh pendekatan unsupervised adalah penelitian Muñoz-Cancino dan Ríos (2025) yang mencari pola penyedia yang tidak wajar pada data pengadaan ChileCompra tahun 2023. Penyedia dihubungkan dalam jaringan berdasarkan keikutsertaan pada tender yang sama, sehingga terbentuk jaringan berisi 42.282 penyedia dan 836.426 hubungan. Ukuran jaringan dan data keuangan penyedia kemudian digunakan sebagai fitur untuk dua model Isolation Forest dengan nilai contamination 5%, yaitu pada tingkat penyedia dan tingkat kelompok penyedia. Hasil SHAP menunjukkan bahwa penyedia yang sangat sentral dalam jaringan dan perusahaan yang sangat baru lebih mungkin ditandai tidak wajar. Namun, unit analisis penelitian ini adalah penyedia, bukan paket pengadaan.

Dari sisi pemanfaatan hasil oleh pengawas, Salazar et al. (2024) mengembangkan VigIA, yaitu alat bantu bagi lembaga pengawas pengadaan di Kota Bogotá, Kolombia, menggunakan 87.027 kontrak dari data terbuka SECOP II. VigIA terdiri atas model Logistic Regression dan Random Forest untuk memprediksi kontrak yang berisiko mengalami pembengkakan biaya atau keterlambatan, dengan hasil terbaik dari Random Forest (AUC 0,943 dan 0,936), serta indeks risiko yang disusun dari 11 indikator red flag. Indeks tersebut dapat dirata-ratakan per instansi untuk membandingkan risiko antarinstansi. Penelitian ini juga menunjukkan bahwa model yang hanya memakai informasi sebelum kontrak berjalan tetap berguna agar pengawas dapat bertindak lebih awal. Meskipun demikian, model VigIA bersifat supervised sehingga membutuhkan label dari kontrak yang sudah selesai.

Ketiga penelitian tersebut mendukung penggunaan pendekatan unsupervised pada tugas akhir ini, karena data RUP dan realisasi tidak memiliki label anomali. Gagasan VigIA dalam membandingkan risiko antarinstansi dan menilai kontrak sejak tahap awal juga menjadi acuan bagi dashboard tugas akhir ini.

### 2.1.2 Deteksi Anomali pada Data Belanja dan Pengadaan Pemerintah Indonesia

Penelitian yang dilakukan Zulfikar et al. (2023) menerapkan Isolation Forest pada realisasi belanja barang persediaan konsumsi satuan kerja Polri tahun 2019–2021, karena belanja ini memiliki nilai realisasi terbesar sehingga dinilai paling berisiko. Agar satuan kerja dengan pagu berbeda dapat dibandingkan, nilai realisasi diubah menjadi persentase terhadap total pagu belanja barang. Model kemudian dilatih menggunakan dua fitur, yaitu bulan dan persentase realisasi, dengan nilai contamination 0,3% yang dipilih berdasarkan pengamatan visual. Penulis mengusulkan model ini sebagai fitur tambahan pada aplikasi SAKTI, tetapi data yang dipakai masih berupa total bulanan, bukan data per transaksi.

Pada data pengadaan, Ambarsari et al. (2025) mengusulkan sistem peringatan dini karena alat pengawasan pengadaan yang ada masih bersifat deskriptif dan melihat ke belakang. Data yang digunakan adalah 447.878 data tender LPSE periode 2019–2024 yang dipublikasikan Indonesia Corruption Watch. Data tersebut diringkas menjadi 71 data bulanan, lalu dianalisis dengan Isolation Forest menggunakan fitur statistik dan fitur chaos, seperti entropi dan volatilitas nilai pengadaan. Hasilnya, 5 dari 71 bulan ditandai sebagai anomali dan sebagian besar berada di sekitar akhir tahun anggaran (Oktober–Januari). Penulis menegaskan bahwa hasil tersebut bukan bukti korupsi dan menyebutkan analisis per tender sebagai pekerjaan lanjutan.

Kedua penelitian tersebut menunjukkan bahwa Isolation Forest dapat diterapkan pada data belanja dan pengadaan pemerintah Indonesia. Namun, keduanya masih menganalisis data agregat bulanan dengan satu jenis model dan belum menjelaskan alasan suatu data ditandai sebagai anomali.

### 2.1.3 Ensemble Deteksi Anomali

Penelitian yang dilakukan Han et al. (2022) membangun ADBench untuk membandingkan 30 algoritma deteksi anomali, yang terdiri atas 14 metode unsupervised, 7 semi-supervised, dan 9 supervised, pada 57 dataset dengan total 98.436 percobaan. Hasilnya menunjukkan bahwa tidak ada satu metode unsupervised yang selalu unggul, karena kinerja setiap metode bergantung pada kesesuaian asumsinya dengan jenis anomali dalam data. Isolation Forest termasuk metode dengan peringkat rata-rata terbaik, sedangkan LOF unggul pada anomali lokal, yaitu data yang menyimpang dari kelompok terdekatnya. Penelitian ini juga menemukan bahwa metode deep learning tidak selalu lebih baik daripada metode yang lebih sederhana.

Krčmar et al. (2026) kemudian menguji apakah keberagaman metode dalam ensemble lebih penting daripada jumlah metode yang digabungkan, menggunakan 11 metode pada 22 dataset. Skor setiap metode dinormalisasi, lalu digabungkan dengan bobot lebih besar bagi metode yang hasilnya tidak terlalu mirip dengan metode lain. Hasilnya, ensemble berisi empat metode yang beragam sedikit lebih baik dibandingkan ensemble berisi seluruh 11 metode, dengan waktu komputasi jauh lebih kecil. Ensemble juga mengungguli metode yang lemah dan setara dengan Isolation Forest sebagai metode individual terbaik.

Penggabungan metode juga digunakan untuk menyusun prioritas pemeriksaan. Herreros-Martínez et al. (2025) berangkat dari praktik audit internal yang masih mengandalkan sampel, sehingga transaksi yang tidak wajar dapat terlewat. Penelitian ini menganalisis 65.712 transaksi pembelian dari dua perusahaan menggunakan z-Score, DBSCAN, k-Means, dan Isolation Forest, lalu mengurutkan transaksi berdasarkan jumlah metode yang menandainya. Jumlah transaksi yang ditandai juga dibatasi, misalnya 1% skor tertinggi dengan maksimal 500 transaksi pada Isolation Forest, agar tetap dapat diperiksa oleh auditor. SHAP digunakan untuk menjelaskan alasan suatu transaksi ditandai, dan 78–91% transaksi yang ditandai dikonfirmasi relevan oleh auditor. Namun, penelitian ini diterapkan pada transaksi perusahaan, bukan pengadaan pemerintah.

Pada data belanja publik, Schiavon et al. (2026) mendeteksi anomali pada pengeluaran kuota kegiatan anggota parlemen Brasil (CEAP) tahun 2019–2023 yang terbagi dalam empat dataset tanpa label dengan total lebih dari 455.000 data. Ensemble yang digunakan menggabungkan Isolation Forest, KNN, LOF, GMM, dan One-Class SVM, dan suatu data baru ditandai jika semua metode sepakat. Ensemble ini mencapai presisi rata-rata 40,3%, lebih tinggi daripada metode individual terbaik (29,0%), meskipun recall-nya lebih rendah (19,6%). Pada data asli, jumlah data yang ditandai berkurang sekitar 92–99% dibandingkan KNN, dan seluruh 24 anggota parlemen yang sebelumnya disorot lembaga pemantau independen pada data bahan bakar ikut ditandai. Namun, penelitian ini belum menyertakan penjelasan hasil seperti SHAP.

Keempat penelitian tersebut menunjukkan bahwa penggabungan metode dengan prinsip berbeda membuat hasil deteksi lebih konsisten dan mempersempit jumlah data yang perlu diperiksa. Hal ini mendukung pemilihan Isolation Forest, LOF, dan Autoencoder pada tugas akhir ini, yang masing-masing mendeteksi anomali berdasarkan isolasi, kepadatan lokal, dan galat rekonstruksi.

### 2.1.4 Penjelasan Hasil Deteksi Anomali Menggunakan SHAP

Hasil deteksi anomali perlu disertai penjelasan agar pemeriksa mengetahui alasan suatu data ditandai. SHAP telah digunakan untuk menjelaskan hasil Isolation Forest (Muñoz-Cancino & Ríos, 2025) dan hasil penggabungan beberapa metode (Herreros-Martínez et al., 2025). Untuk model Autoencoder, Roshan dan Zafar (2021) menggunakan Kernel SHAP untuk menghitung kontribusi setiap fitur terhadap galat rekonstruksi pada data lalu lintas jaringan komputer CICIDS2017. Berdasarkan hasil SHAP, dipilih 30 fitur terpenting dari 78 fitur untuk melatih ulang model, sehingga AUC meningkat dari 0,819 menjadi 0,969 dan F-score dari 0,71 menjadi 0,90. Penelitian ini juga mencatat bahwa Kernel SHAP membutuhkan waktu komputasi yang besar dan hasilnya bergantung pada pemilihan data latar (background data).

Temuan ini mendukung penggunaan SHAP untuk menjelaskan alasan setiap paket diprioritaskan pada tugas akhir ini, termasuk pada komponen Autoencoder. Karena waktu komputasinya besar, penjelasan dapat difokuskan pada paket berperingkat atas.

### 2.1.5 Kesenjangan Penelitian Terdahulu

Penelitian-penelitian terdahulu yang telah diuraikan menjadi rujukan utama dan kerangka pemikiran dalam tugas akhir ini. Ringkasan dataset, metode, dan hasil dari setiap penelitian tersebut disajikan pada Tabel 2.1.

**Tabel 2.1 Kesenjangan Penelitian Terdahulu**

| Judul Penelitian | Dataset | Metode | Hasil |

|---|---|---|---|

| Detection of Fraud in Public Procurement Using Data-Driven Methods: A Systematic Mapping Study (Schneider dos Santos et al., 2025) | 93 penelitian periode 2020–2024 yang disaring dari lebih dari 6.000 artikel | Systematic mapping study | Sebagian besar penelitian memakai machine learning dan 31 penelitian memakai pendekatan unsupervised. Hanya 2 dari 93 penelitian yang diterapkan di lembaga pengawas, dan dataset pengadaan terbuka masih terbatas. |

| Data-Driven Transparency: Machine Learning and Social Network Analysis for Corruption Detection in Public Procurement (Muñoz-Cancino & Ríos, 2025) | Data ChileCompra tahun 2023, jaringan 42.282 penyedia dan 836.426 hubungan | Social Network Analysis, Isolation Forest (contamination 5%), SHAP | Penyedia yang sangat sentral dalam jaringan dan perusahaan yang sangat baru lebih mungkin ditandai tidak wajar. Unit analisis berupa penyedia, bukan paket. |

| VigIA: Prioritizing Public Procurement Oversight with Machine Learning Models and Risk Indices (Salazar et al., 2024) | 87.027 kontrak SECOP II dengan 47 variabel | Logistic Regression, Random Forest, indeks risiko IRIC (11 red flag) | Random Forest mencapai AUC 0,943 (pembengkakan biaya) dan 0,936 (keterlambatan). Model bersifat supervised dan membutuhkan label dari kontrak yang sudah selesai. |

| Deteksi Anomali Menggunakan Isolation Forest Belanja Barang Persediaan Konsumsi pada Satuan Kerja Kepolisian Republik Indonesia (Zulfikar et al., 2023) | Realisasi belanja bulanan satuan kerja Polri tahun 2019–2021 | Isolation Forest dengan 2 fitur (bulan dan persentase realisasi terhadap pagu) | Contamination 0,3% dipilih sebagai nilai paling optimal berdasarkan pengamatan visual. Data masih berupa total bulanan dan belum disertai penjelasan hasil. |

| Hybrid Chaos-Isolation Forest Framework for Anomaly Detection in Indonesia's Public Procurement (Ambarsari et al., 2025) | 447.878 data tender LPSE (OCDS) periode 2019–2024, diringkas menjadi 71 data bulanan | Isolation Forest dengan fitur statistik dan fitur chaos | 5 dari 71 bulan ditandai anomali, sebagian besar pada Oktober–Januari. Belum menunjukkan paket yang perlu diperiksa. |

| ADBench: Anomaly Detection Benchmark (Han et al., 2022) | 57 dataset dengan total 98.436 percobaan | 30 algoritma (14 unsupervised, 7 semi-supervised, 9 supervised) | Tidak ada satu metode unsupervised yang selalu unggul. Isolation Forest termasuk peringkat terbaik dan LOF unggul pada anomali lokal. |

| Less Is More: Principled Diversity in Heterogeneous Anomaly Detection Ensembles (Krčmar et al., 2026) | 22 dataset uji berlabel | Ensemble 11 metode dengan normalisasi skor dan pembobotan keberagaman | Ensemble 4 metode yang beragam sedikit lebih baik daripada ensemble 11 metode dengan komputasi lebih kecil, serta setara dengan Isolation Forest. |

| Applied Machine Learning to Anomaly Detection in Enterprise Purchase Processes: A Hybrid Approach Using Clustering and Isolation Forest (Herreros-Martínez et al., 2025) | 65.712 transaksi pembelian dari dua perusahaan tahun 2021 | z-Score, DBSCAN, k-Means, Isolation Forest, ensemble prioritisation, SHAP | 78–91% transaksi yang ditandai dikonfirmasi relevan oleh auditor. Diterapkan pada perusahaan, bukan pengadaan pemerintah. |

| Ensemble-Based Anomaly Detection in Brazilian Parliamentary Expenses Using Unlabeled Public Data (Schiavon et al., 2026) | Pengeluaran CEAP tahun 2019–2023 dalam 4 dataset tanpa label (lebih dari 455.000 data) | Ensemble konsensus Isolation Forest, KNN, LOF, GMM, dan One-Class SVM | Presisi rata-rata 40,3%, lebih tinggi daripada GMM (29,0%), dengan recall 19,6%. Jumlah data yang ditandai berkurang 92–99%, tetapi belum disertai penjelasan hasil. |

| Utilizing XAI Technique to Improve Autoencoder Based Model for Computer Network Anomaly Detection with Shapley Additive Explanation (SHAP) (Roshan & Zafar, 2021) | Dataset CICIDS2017 (150.000 data normal untuk pelatihan, 137.718 data uji) | Autoencoder dan Kernel SHAP | Pemilihan 30 fitur berdasarkan SHAP meningkatkan AUC dari 0,819 menjadi 0,969 dan F-score dari 0,71 menjadi 0,90. Kernel SHAP membutuhkan komputasi besar. |

Berdasarkan Tabel 2.1, penelitian terdahulu menunjukkan bahwa deteksi anomali tanpa label dapat diterapkan pada data belanja dan pengadaan pemerintah, penggabungan metode yang beragam membuat hasil lebih konsisten, dan SHAP dapat menjelaskan alasan suatu data ditandai. Namun, penelitian di Indonesia masih menganalisis data agregat bulanan dengan satu jenis model, belum menilai paket sejak tahap perencanaan (RUP), dan belum menyertakan penjelasan hasil. Selain itu, hasil penelitian masih jarang disajikan dalam alat yang dapat langsung digunakan pengawas. Oleh karena itu, tugas akhir ini mengembangkan deteksi anomali berbasis ensemble Isolation Forest, LOF, dan Autoencoder pada data RUP serta pasangan RUP dan realisasi pengadaan APBD pemerintah provinsi, yang dilengkapi penjelasan SHAP dan disajikan dalam dashboard untuk membantu pengawas menentukan paket yang perlu ditelusuri lebih lanjut.
