# 2.1 Hasil Penelitian Terdahulu (Draf v3)

> Revisi dari v2 (v2 tetap disimpan sebagai cadangan). Perubahan: bagian Ringkasan dan Keterkaitan dijabarkan lebih panjang berdasarkan isi lengkap tiap paper; format tetap mengikuti proposal Nadia Ayula.

---

Pada bagian ini disajikan sepuluh penelitian terdahulu yang relevan dengan topik tugas akhir. Penelitian tersebut mencakup pemetaan penelitian deteksi penyimpangan pengadaan, penerapan deteksi anomali pada data belanja dan pengadaan pemerintah, penggabungan beberapa metode deteksi anomali, penggunaan explainable AI, serta pengembangan alat bantu bagi pengawas. Setiap penelitian dirangkum berdasarkan jurnal, judul, peneliti, publisher, tahun, ringkasan, dan keterkaitannya dengan tugas akhir ini.

**Tabel 2.1 Keterkaitan Penelitian 1**

| | |
|---|---|
| Jurnal | EPJ Data Science |
| Judul | Detection of Fraud in Public Procurement Using Data-Driven Methods: A Systematic Mapping Study |
| Peneliti | Everton Schneider dos Santos, Matheus Machado dos Santos, Márcio Castro, Jônata Tyska Carvalho |
| Publisher | SpringerOpen |
| Tahun | 2025 |
| Ringkasan | Penelitian ini memetakan perkembangan penelitian deteksi penyimpangan pada pengadaan publik yang menggunakan pendekatan berbasis data. Dari lebih dari 6.000 artikel yang disaring, 93 penelitian yang terbit pada periode 2020–2024 dipilih untuk dianalisis. Hasilnya menunjukkan bahwa sebagian besar penelitian menggunakan machine learning, terutama untuk mendeteksi persekongkolan antarpenyedia, sedangkan analisis statistik lebih banyak dipakai untuk mendeteksi favoritisme. Sebanyak 31 penelitian tidak menggunakan variabel target sama sekali dan memilih pendekatan unsupervised seperti deteksi anomali, klasterisasi, dan analisis jaringan, karena data kasus yang sudah terbukti jarang tersedia. Penelitian ini juga menemukan dua kesenjangan utama. Pertama, hanya dua dari 93 penelitian yang benar-benar diterapkan dalam sistem yang dipakai lembaga pengawas. Kedua, dataset pengadaan yang tersedia untuk publik masih terbatas sehingga hasil penelitian sulit direplikasi. |
| Keterkaitan | Penelitian ini menjadi landasan umum bahwa machine learning relevan untuk mendeteksi penyimpangan dalam pengadaan publik. Temuan bahwa banyak penelitian memilih pendekatan unsupervised karena tidak tersedianya label mendukung pemilihan pendekatan unsupervised pada tugas akhir ini, karena data RUP dan realisasi juga tidak memiliki label anomali. Temuan bahwa hasil penelitian jarang sampai ke tangan pengawas mendukung pengembangan dashboard sebagai bagian dari tugas akhir ini. Selain itu, tugas akhir ini memanfaatkan data pengadaan yang tersedia secara terbuka melalui Data INAPROC, sehingga ikut menjawab kesenjangan terkait ketersediaan data publik. |

**Tabel 2.2 Keterkaitan Penelitian 2**

| | |
|---|---|
| Jurnal | Jurnal Manajemen Perbendaharaan |
| Judul | Deteksi Anomali Menggunakan Isolation Forest Belanja Barang Persediaan Konsumsi pada Satuan Kerja Kepolisian Republik Indonesia |
| Peneliti | Ahmad Zulfikar, Farhan Ariq Rahmani, Nurul Azizah |
| Publisher | Direktorat Jenderal Perbendaharaan, Kementerian Keuangan |
| Tahun | 2023 |
| Ringkasan | Penelitian ini mendeteksi anomali pada belanja barang persediaan konsumsi (akun 521811) di seluruh satuan kerja Polri, karena akun tersebut memiliki nilai realisasi terbesar dibandingkan bagian anggaran lain sehingga dinilai paling berisiko. Data yang digunakan adalah realisasi belanja bulanan tahun 2019–2021 yang bersumber dari Direktorat Jenderal Perbendaharaan. Sebelum dimodelkan, data dibersihkan dari nilai realisasi negatif, lalu nilai rupiah diubah menjadi persentase terhadap total pagu belanja barang agar satuan kerja dengan pagu berbeda dapat dibandingkan. Model Isolation Forest kemudian dilatih menggunakan dua fitur, yaitu bulan dan persentase realisasi. Nilai parameter contamination ditentukan dengan cara coba-coba: nilai 0,5% menandai 165 data, nilai 0,1% menandai 33 data, dan nilai 0,3% dipilih sebagai yang paling optimal berdasarkan pengamatan visual. Penulis mengusulkan model ini menjadi fitur tambahan pada aplikasi SAKTI, dan mengakui bahwa data yang dipakai masih berupa total bulanan, bukan data per transaksi. |
| Keterkaitan | Penelitian ini menjadi acuan penerapan Isolation Forest pada data belanja pemerintah Indonesia, termasuk cara menyetarakan nilai antarsatuan kerja menggunakan rasio terhadap pagu. Cara ini relevan untuk tugas akhir ini yang juga membandingkan paket dari provinsi dengan besaran anggaran yang berbeda. Namun, terdapat beberapa perbedaan. Penelitian ini hanya memakai satu model dan dua fitur, menilai belanja yang sudah terealisasi, menganalisis data agregat bulanan, serta belum menyertakan penjelasan mengapa suatu data ditandai sebagai anomali. Tugas akhir ini mengembangkannya dengan menggabungkan tiga model, menilai paket sejak tahap RUP, dan menambahkan penjelasan SHAP pada setiap paket yang diprioritaskan. |

**Tabel 2.3 Keterkaitan Penelitian 3**

| | |
|---|---|
| Jurnal | Bulletin of Informatics and Data Science |
| Judul | Hybrid Chaos-Isolation Forest Framework for Anomaly Detection in Indonesia's Public Procurement |
| Peneliti | Erlin Windia Ambarsari, Desyanti, Dedin Fathudin |
| Publisher | Asosiasi Peneliti Data Science Indonesia |
| Tahun | 2025 |
| Ringkasan | Penelitian ini berangkat dari kondisi bahwa alat pengawasan pengadaan yang ada masih bersifat deskriptif dan melihat ke belakang, sehingga diusulkan sistem peringatan dini berbasis deteksi anomali tanpa label. Data yang digunakan adalah data tender LPSE dalam format Open Contracting Data Standard (OCDS) yang dipublikasikan Indonesia Corruption Watch, sebanyak 447.878 data pada periode 2019–2024. Data tersebut diringkas menjadi 71 data bulanan, sehingga unit analisisnya adalah bulan, bukan paket tender. Fitur yang digunakan terdiri atas fitur statistik, seperti total nilai dan jumlah tender, serta fitur chaos, seperti entropi dan volatilitas nilai pengadaan. Isolation Forest dengan fitur gabungan tersebut kemudian dibandingkan dengan Isolation Forest yang hanya memakai fitur statistik. Hasilnya, 5 dari 71 bulan ditandai sebagai anomali dan sebagian besar berada di sekitar akhir tahun anggaran (Oktober–Januari). Penulis menegaskan bahwa hasil tersebut bukan bukti korupsi, melainkan pola yang perlu diperhatikan oleh LKPP dan pengawas. |
| Keterkaitan | Penelitian ini menunjukkan bahwa data pengadaan terbuka di Indonesia dapat dimanfaatkan untuk deteksi anomali tanpa label, dan cara penulis memosisikan hasil anomali sebagai sinyal, bukan bukti pelanggaran, sejalan dengan tugas akhir ini. Namun, karena data diringkas menjadi data bulanan, penelitian ini hanya dapat menunjukkan bulan yang tidak wajar dan belum dapat menunjukkan paket mana yang perlu diperiksa. Penulis sendiri menyebutkan bahwa analisis per tender menjadi pekerjaan lanjutan. Penelitian ini juga hanya memakai satu jenis model, menggunakan data tahap tender, dan belum menyertakan penjelasan hasil. Tugas akhir ini mengisi kekurangan tersebut dengan menilai setiap paket sejak tahap RUP, menggabungkan tiga model, dan menjelaskan hasil setiap paket menggunakan SHAP. |

**Tabel 2.4 Keterkaitan Penelitian 4**

| | |
|---|---|
| Jurnal | Procedia Computer Science |
| Judul | Data-Driven Transparency: Machine Learning and Social Network Analysis for Corruption Detection in Public Procurement |
| Peneliti | Ricardo Muñoz-Cancino, Sebastián A. Ríos |
| Publisher | Elsevier |
| Tahun | 2025 |
| Ringkasan | Penelitian ini mengusulkan metode untuk menemukan pola penyedia yang tidak wajar pada pengadaan publik Chile dengan menggabungkan machine learning dan Social Network Analysis. Data diambil dari platform ChileCompra tahun 2023, lalu dibentuk jaringan penyedia yang saling terhubung jika mengikuti tender yang sama. Jaringan yang terbentuk terdiri atas 42.282 penyedia dan 836.426 hubungan. Dari jaringan tersebut dihitung ukuran-ukuran jaringan, seperti tingkat keterhubungan dan posisi sentral penyedia, yang kemudian digabung dengan data keuangan penyedia, seperti umur perusahaan dan total nilai kontrak. Dua model Isolation Forest dilatih dengan contamination 5%, yaitu pada tingkat penyedia dan tingkat kelompok penyedia. SHAP digunakan untuk menjelaskan fitur yang paling memengaruhi hasil, misalnya penyedia yang sangat sentral dalam jaringan dan perusahaan yang sangat baru lebih mungkin ditandai tidak wajar. Penulis menyarankan validasi hasil bersama pengawas dan penambahan data, seperti riwayat sanksi penyedia, pada penelitian selanjutnya. |
| Keterkaitan | Penelitian ini mendukung penggunaan Isolation Forest pada data pengadaan pemerintah tanpa label, serta penggunaan SHAP untuk menjelaskan hasil deteksi kepada pengawas. Cara penelitian ini menyajikan penjelasan SHAP, baik secara keseluruhan maupun per fitur, dapat menjadi acuan penyajian penjelasan pada tugas akhir ini. Perbedaannya, unit analisis penelitian ini adalah penyedia dan kelompok penyedia, sedangkan tugas akhir ini menilai paket pengadaan. Penelitian ini juga hanya memakai satu jenis model dan belum dilengkapi alat bantu yang dapat langsung digunakan pengawas, sedangkan tugas akhir ini menggabungkan tiga model dan menyajikan hasilnya dalam dashboard. |

**Tabel 2.5 Keterkaitan Penelitian 5**

| | |
|---|---|
| Jurnal | Information |
| Judul | Applied Machine Learning to Anomaly Detection in Enterprise Purchase Processes: A Hybrid Approach Using Clustering and Isolation Forest |
| Peneliti | Antonio Herreros-Martínez, Rafael Magdalena-Benedicto, Joan Vila-Francés, Antonio José Serrano-López, Sonia Pérez-Díaz, José Javier Martínez-Herráiz |
| Publisher | MDPI |
| Tahun | 2025 |
| Ringkasan | Penelitian ini berangkat dari praktik audit internal yang masih mengandalkan sampel, sehingga transaksi yang tidak wajar dapat terlewat karena tidak masuk sampel. Data yang digunakan adalah 65.712 transaksi pembelian dengan 17 kolom dari dua perusahaan dalam satu grup multinasional pada tahun 2021. Analisis dilakukan dalam dua tahap, yaitu analisis satu variabel menggunakan z-Score dan DBSCAN, serta analisis banyak variabel menggunakan k-Means dan Isolation Forest. Pada Isolation Forest, transaksi yang ditandai dibatasi pada 1% skor tertinggi dengan jumlah maksimal 500 transaksi agar tetap dapat diperiksa oleh auditor. Hasil dari setiap metode kemudian digabungkan dalam ensemble prioritisation, yaitu transaksi diurutkan berdasarkan berapa banyak metode yang menandainya. SHAP digunakan untuk menjelaskan alasan suatu transaksi ditandai, baik per transaksi maupun secara keseluruhan. Hasil validasi menunjukkan bahwa 78–91% transaksi yang ditandai dikonfirmasi relevan oleh auditor. |
| Keterkaitan | Penelitian ini menjadi acuan utama dalam menggabungkan beberapa metode deteksi anomali untuk menyusun prioritas pemeriksaan. Cara penggabungan berdasarkan jumlah metode yang menandai suatu data relevan dengan rencana tugas akhir ini untuk memberi perhatian lebih pada paket yang ditandai oleh lebih dari satu model. Pembatasan jumlah data yang ditandai agar tetap dapat diperiksa juga sejalan dengan pemeringkatan paket pada tugas akhir ini. Perbedaannya, penelitian ini diterapkan pada transaksi pembelian perusahaan, bukan pengadaan pemerintah, dan metode yang digabungkan berbeda. Tugas akhir ini menerapkan gagasan serupa pada paket pengadaan APBD pemerintah provinsi dengan Isolation Forest, LOF, dan Autoencoder. |

**Tabel 2.6 Keterkaitan Penelitian 6**

| | |
|---|---|
| Jurnal | Data & Policy |
| Judul | VigIA: Prioritizing Public Procurement Oversight with Machine Learning Models and Risk Indices |
| Peneliti | Andrés Salazar, Juan F. Pérez, Jorge Gallego |
| Publisher | Cambridge University Press |
| Tahun | 2024 |
| Ringkasan | Penelitian ini mengembangkan VigIA, alat bantu bagi Veeduría Distrital, lembaga pengawas pengadaan di Kota Bogotá, Kolombia, yang setiap tahun harus mengawasi ratusan ribu kontrak dengan sumber daya terbatas. Data yang digunakan berasal dari data terbuka SECOP II, yaitu 87.027 kontrak dengan 47 variabel yang dikelompokkan berdasarkan tahap sebelum kontrak, penetapan pemenang, dan pelaksanaan. VigIA memiliki dua komponen. Komponen pertama adalah model Logistic Regression dan Random Forest untuk memprediksi kontrak yang berisiko mengalami pembengkakan biaya atau keterlambatan. Random Forest memberikan hasil terbaik dengan AUC 0,943 untuk pembengkakan biaya dan 0,936 untuk keterlambatan. Komponen kedua adalah indeks risiko (IRIC) yang disusun dari 11 indikator red flag dan dapat dirata-ratakan per instansi untuk membandingkan risiko antarinstansi dan antarwilayah. Penelitian ini juga menunjukkan bahwa model yang hanya memakai informasi sebelum kontrak berjalan memiliki kinerja lebih rendah, tetapi tetap berguna agar pengawas dapat bertindak lebih awal. |
| Keterkaitan | Penelitian ini menjadi acuan perancangan dashboard pada tugas akhir ini, karena VigIA dirancang untuk kebutuhan pengawas, mengutamakan hasil yang dapat dijelaskan, dan memanfaatkan data pengadaan terbuka. Gagasan merata-ratakan risiko per instansi untuk membandingkan antarwilayah sejalan dengan penyajian sebaran hasil antarprovinsi pada dashboard tugas akhir ini. Temuan bahwa informasi tahap awal tetap berguna untuk pengawasan dini juga mendukung penilaian paket sejak tahap RUP. Perbedaannya, model VigIA bersifat supervised dan membutuhkan variabel target dari kontrak yang sudah selesai, sedangkan tugas akhir ini menggunakan pendekatan unsupervised karena data RUP dan realisasi tidak memiliki label anomali. |

**Tabel 2.7 Keterkaitan Penelitian 7**

| | |
|---|---|
| Jurnal | International Transactions in Operational Research |
| Judul | Explainable Anomaly Detection for Procurement Fraud Identification—Lessons from Practical Deployments |
| Peneliti | Adam Westerski, Rajaraman Kanagasabai, Eran Shaham, Amudha Narayanan, Jiayu Wong, Manjeet Singh |
| Publisher | Wiley |
| Tahun | 2021 |
| Ringkasan | Penelitian ini membahas pengalaman penerapan sistem Procurement Analytics Core Engine (PACE) di unit audit pengadaan A*STAR, Singapura. Data yang dianalisis adalah sekitar 216.000 transaksi pengadaan selama kurang lebih empat tahun tanpa label kasus. Sistem ini menggunakan 48 indikator risiko berbasis statistik yang masing-masing mewakili satu jenis penyimpangan, lalu indikator tersebut digabungkan menjadi satu skor yang dapat diuraikan kembali. Hasilnya disajikan setiap triwulan kepada auditor dalam bentuk daftar transaksi yang diurutkan beserta alasan mengapa setiap transaksi ditandai. Sistem ini mencapai presisi 67,1% dalam mendeteksi transaksi yang mencurigakan. Pelajaran utama dari penelitian ini adalah bahwa penjelasan hasil sangat menentukan apakah sistem diterima oleh auditor, dan pendekatan yang terlalu berbeda dari kebiasaan kerja auditor justru menyulitkan pemahaman dan penggunaan sistem. |
| Keterkaitan | Penelitian ini menjadi dasar perlunya penjelasan pada setiap paket yang diprioritaskan dalam tugas akhir ini, karena terbukti bahwa skor tanpa alasan sulit diterima oleh pemeriksa. Bentuk keluaran berupa daftar yang diurutkan beserta alasannya juga menjadi acuan bagi dashboard tugas akhir ini. Perbedaannya, penelitian ini menggunakan indikator statistik yang disusun berdasarkan pengetahuan auditor, sedangkan tugas akhir ini menggunakan ensemble model machine learning dan SHAP untuk menghasilkan penjelasan. Penelitian ini juga diterapkan pada satu organisasi dan berfokus pada transaksi yang sudah terjadi, sedangkan tugas akhir ini mencakup paket pengadaan APBD seluruh pemerintah provinsi sejak tahap perencanaan. |

**Tabel 2.8 Keterkaitan Penelitian 8**

| | |
|---|---|
| Jurnal | Advances in Neural Information Processing Systems (NeurIPS) |
| Judul | ADBench: Anomaly Detection Benchmark |
| Peneliti | Songqiao Han, Xiyang Hu, Hailiang Huang, Mingqi Jiang, Yue Zhao |
| Publisher | NeurIPS Foundation |
| Tahun | 2022 |
| Ringkasan | Penelitian ini membangun tolok ukur untuk membandingkan metode deteksi anomali secara menyeluruh. Sebanyak 30 algoritma, yang terdiri atas 14 metode unsupervised, 7 semi-supervised, dan 9 supervised, diuji pada 57 dataset dengan total 98.436 percobaan. Hasilnya menunjukkan bahwa tidak ada satu metode unsupervised yang secara statistik lebih unggul dibandingkan metode lainnya, dan Isolation Forest termasuk metode dengan peringkat rata-rata terbaik. Kinerja setiap metode sangat bergantung pada kesesuaian antara asumsi metode tersebut dan jenis anomali dalam data. Sebagai contoh, LOF unggul pada anomali lokal, yaitu data yang menyimpang dari kelompok terdekatnya, sedangkan metode lain lebih unggul pada jenis anomali yang berbeda. Penelitian ini juga menemukan bahwa metode deep learning tidak selalu lebih baik daripada metode yang lebih sederhana. |
| Keterkaitan | Penelitian ini mendukung alasan tugas akhir ini tidak bergantung pada satu model saja. Karena jenis anomali pada data pengadaan APBD tidak diketahui sebelumnya, penggunaan beberapa model dengan asumsi berbeda dapat mengurangi risiko memilih model yang tidak sesuai. Temuan bahwa Isolation Forest termasuk metode terbaik dan LOF unggul pada anomali lokal juga mendukung pemilihan kedua model tersebut. Isolation Forest diharapkan menangkap paket yang menyimpang dari keseluruhan data, sedangkan LOF menangkap paket yang menyimpang dari paket sejenis di sekitarnya. |

**Tabel 2.9 Keterkaitan Penelitian 9**

| | |
|---|---|
| Jurnal | AI |
| Judul | Less Is More: Principled Diversity in Heterogeneous Anomaly Detection Ensembles |
| Peneliti | Tea Krčmar, Dina Šabanović, Mirko Köhler, Ivica Lukić |
| Publisher | MDPI |
| Tahun | 2026 |
| Ringkasan | Penelitian ini menguji apakah keberagaman metode dalam ensemble lebih penting daripada jumlah metode yang digabungkan. Sebanyak 11 metode deteksi anomali, di antaranya Isolation Forest, LOF, KNN, dan Variational Autoencoder, diuji pada 22 dataset. Skor setiap metode dinormalisasi, lalu digabungkan dengan pembobotan yang memberi bobot lebih besar pada metode yang hasilnya tidak terlalu mirip dengan metode lain. Seluruh kemungkinan kombinasi metode diuji untuk mencari susunan ensemble terbaik. Hasilnya, ensemble berisi empat metode yang beragam memberikan hasil sedikit lebih baik dibandingkan ensemble berisi seluruh 11 metode, dengan waktu komputasi jauh lebih kecil. Ensemble juga mengungguli metode-metode yang lemah, sedangkan kinerjanya setara dengan Isolation Forest sebagai metode individual terbaik. |
| Keterkaitan | Penelitian ini mendukung penyusunan ensemble dari metode yang berbeda prinsip, yaitu Isolation Forest (isolasi), LOF (kepadatan lokal), dan Autoencoder (galat rekonstruksi), dibandingkan menggabungkan banyak metode yang serupa. Hasil bahwa ensemble setara dengan metode terbaik dan lebih baik daripada metode yang lemah relevan untuk kondisi tanpa label, karena pada data RUP dan realisasi tidak dapat diketahui sejak awal metode mana yang terbaik. Dengan ensemble, hasil tidak bergantung pada satu metode yang mungkin kurang sesuai. Penelitian ini juga menjadi acuan teknis normalisasi skor sebelum penggabungan. Perbedaannya, penelitian ini menggunakan dataset uji umum yang memiliki label, sedangkan tugas akhir ini menerapkan ensemble pada data pengadaan tanpa label. |

**Tabel 2.10 Keterkaitan Penelitian 10**

| | |
|---|---|
| Jurnal | Expert Systems with Applications |
| Judul | Explaining Anomalies Detected by Autoencoders Using Shapley Additive Explanations |
| Peneliti | Liat Antwarg, Ronnie Mindlin Miller, Bracha Shapira, Lior Rokach |
| Publisher | Elsevier |
| Tahun | 2021 |
| Ringkasan | Penelitian ini mengembangkan cara menjelaskan anomali yang ditemukan oleh Autoencoder menggunakan Kernel SHAP. Langkahnya dimulai dengan memilih fitur yang memiliki galat rekonstruksi terbesar, lalu SHAP digunakan untuk menunjukkan fitur lain yang menyebabkan galat tersebut. Hasilnya dipisahkan menjadi fitur yang memperkuat dan fitur yang melemahkan anomali. Metode ini diuji pada beberapa dataset, termasuk 15.000 klaim garansi produsen mobil dan 284.807 transaksi kartu kredit. Hasil wawancara dengan empat pakar menunjukkan bahwa satu sampai tiga fitur teratas sudah cukup menjelaskan anomali pada lebih dari 85% klaim. Penjelasan dari SHAP juga lebih stabil dan lebih tepat dibandingkan metode penjelasan lain, yaitu LIME. |
| Keterkaitan | Penelitian ini mendukung penggunaan SHAP pada tugas akhir ini, khususnya untuk komponen Autoencoder yang tidak dapat dijelaskan secara langsung seperti model berbasis pohon. Temuan bahwa beberapa fitur teratas sudah cukup menjelaskan anomali mendukung rencana penyajian penjelasan yang ringkas pada dashboard, misalnya tiga fitur dengan kontribusi terbesar untuk setiap paket. Perbedaannya, penelitian ini menjelaskan satu model Autoencoder, sedangkan tugas akhir ini menjelaskan skor gabungan dari ensemble. Penelitian ini juga tidak membahas data pengadaan pemerintah. |

---

## 2.1.1 Sintesis Penelitian Terdahulu

Berdasarkan penelitian terdahulu, terdapat beberapa temuan penting yang menjadi dasar tugas akhir ini. Pertama, machine learning telah banyak digunakan untuk mendeteksi penyimpangan dalam pengadaan, dan pendekatan unsupervised banyak dipilih karena data kasus yang sudah terbukti jarang tersedia. Di Indonesia, Isolation Forest sudah diterapkan pada data realisasi belanja dan data tender, tetapi masih pada data agregat bulanan. Kedua, tidak ada satu metode deteksi anomali yang selalu unggul, sehingga penggabungan metode dengan prinsip berbeda membuat hasil tidak bergantung pada satu metode yang mungkin kurang sesuai. Ketiga, hasil deteksi lebih mudah diterima dan ditindaklanjuti oleh pemeriksa jika disertai penjelasan, dan SHAP dapat digunakan untuk berbagai model, termasuk Autoencoder. Keempat, hasil penelitian masih jarang diterapkan dalam alat yang dipakai pengawas, padahal alat bantu yang dirancang untuk pengawas terbukti membantu menentukan prioritas pemeriksaan.

**Tabel 2.11 Sintesis Penelitian Terdahulu**

| Aspek | Temuan Utama | Implikasi terhadap Tugas Akhir Ini |
|---|---|---|
| Data dan tahap pengadaan | Penelitian di Indonesia menganalisis data realisasi belanja dan data tender dalam bentuk agregat bulanan, sehingga belum menilai paket satu per satu dan belum mencakup paket yang masih berupa RUP. | Tugas akhir ini menilai setiap paket melalui dua jalur, yaitu jalur perencanaan (data RUP) dan jalur pelaksanaan (pasangan RUP dan realisasi). |
| Pemilihan model | Tidak ada satu metode unsupervised yang selalu unggul. Isolation Forest termasuk metode terbaik secara umum, sedangkan LOF unggul pada anomali lokal. | Tugas akhir ini menggunakan Isolation Forest, LOF, dan Autoencoder yang memiliki prinsip berbeda, lalu membandingkan kinerja masing-masing. |
| Penggabungan model | Ensemble dari metode yang beragam setara dengan metode terbaik dan lebih baik daripada metode yang lemah, serta dapat digunakan untuk menyusun prioritas pemeriksaan. | Tugas akhir ini menggabungkan ketiga model dalam ensemble untuk menghasilkan peringkat paket. |
| Interpretasi model | Penjelasan hasil menentukan diterimanya sistem oleh pemeriksa, dan SHAP dapat menjelaskan hasil Isolation Forest maupun Autoencoder. | Tugas akhir ini menggunakan SHAP untuk menjelaskan fitur yang paling memengaruhi skor paket yang diprioritaskan. |
| Penyajian hasil | Hanya sedikit penelitian yang diterapkan dalam alat yang dipakai pengawas, sedangkan alat seperti VigIA dan PACE membantu menentukan prioritas pemeriksaan. | Tugas akhir ini menyajikan hasil dalam dashboard berisi sebaran antarprovinsi, peringkat paket, dan penjelasannya. |

Dengan demikian, celah yang diambil dalam tugas akhir ini adalah pengembangan deteksi anomali berbasis ensemble Isolation Forest, LOF, dan Autoencoder pada data RUP serta pasangan RUP dan realisasi pengadaan APBD pemerintah provinsi, yang menilai setiap paket sejak tahap perencanaan, dilengkapi penjelasan SHAP, dan disajikan dalam dashboard untuk membantu pengawas menentukan paket yang perlu ditelusuri lebih lanjut.

---

## Catatan untuk Tio (di luar naskah)

- Semua angka di tabel sudah dicek ke paper aslinya: lima paper dari PDF di library, Ambarsari, ADBench, Krčmar, dan Antwarg dari teks lengkap di web. Westerski hanya bisa dibaca bagian abstrak dan pendahuluannya, jadi angka 216.000 transaksi, 48 indikator, dan presisi 67,1% sebaiknya dicek ulang ke paper lengkapnya.
- Temuan penting dari Krčmar: ensemble tidak lebih akurat dari metode terbaik (setara dengan Isolation Forest), tetapi lebih aman karena tidak bergantung pada satu metode. Kalimat Bab 1 "ensemble memberikan hasil yang lebih konsisten" masih bisa dipakai, asal jangan diubah menjadi "lebih akurat".
- Kalimat tentang "tiga fitur dengan kontribusi terbesar" di Tabel 2.10 adalah usulan rancangan, silakan disesuaikan dengan rencana dashboard-mu.
- Publisher Ambarsari sudah dilengkapi (Asosiasi Peneliti Data Science Indonesia), begitu juga nama lengkap seluruh peneliti.
