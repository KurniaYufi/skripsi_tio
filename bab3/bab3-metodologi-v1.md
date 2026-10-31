# BAB 3 METODOLOGI

Bab ini menguraikan metodologi penelitian secara sistematis, meliputi alur kerja, deskripsi tahapan, serta urutan pelaksanaan tugas akhir.

## 3.1 Alur Metodologi Penelitian

Alur metodologi tugas akhir ini ditunjukkan pada Gambar 3.1 dan Gambar 3.2. Diagram dibagi menjadi tiga kolom, yaitu masukan, proses, dan luaran, sehingga hubungan antartahap dapat diikuti dengan jelas. Bagian pertama berisi tahap identifikasi masalah sampai pengembangan model ensemble, sedangkan bagian kedua berisi tahap evaluasi dan interpretasi model sampai penyusunan laporan tugas akhir.

![[Sisipkan Gambar 3.1 di sini: gambar-3-1-metodologi-bagian-1.png]]()

<p align="center">Gambar 3.1 Diagram Metodologi Tugas Akhir Bagian 1</p>

![[Sisipkan Gambar 3.2 di sini: gambar-3-2-metodologi-bagian-2-v3.png]]()

<p align="center">Gambar 3.2 Diagram Metodologi Tugas Akhir Bagian 2</p>

## 3.2 Uraian Alur Penelitian

Penjelasan dari diagram pada Gambar 3.1 dan Gambar 3.2, tentang metodologi penelitian tugas akhir adalah sebagai berikut:

### 3.2.1 Identifikasi dan Perumusan Masalah

Tugas akhir ini berawal dari besarnya anggaran pengadaan barang/jasa pemerintah. Nilai RUP secara nasional mencapai Rp859,27 triliun per 8 Juni 2026 (LKPP, 2026), sedangkan belanja barang dan jasa pemerintah daerah pada tahun 2025 mencapai Rp418,76 triliun (DJPK, 2026). Dengan nilai sebesar itu, pengadaan menjadi sektor yang rawan penyimpangan, misalnya melalui penggelembungan anggaran dan pengadaan fiktif (Adhi et al., 2025). Pada Pemerintah Provinsi Kalimantan Timur, KPK (2026) juga mengidentifikasi pola pemecahan paket dengan nilai mendekati ambang pengadaan langsung serta penyedia yang menangani banyak paket secara bersamaan.

Di sisi lain, pengawasan yang mengandalkan audit manual sulit mengimbangi volume dan kompleksitas data pengadaan (Muñoz-Cancino & Ríos, 2025). Penelitian deteksi anomali pada belanja dan pengadaan pemerintah Indonesia masih menggunakan satu model dan belum menjelaskan alasan suatu data dianggap anomali (Ambarsari et al., 2025; Zulfikar et al., 2023). Selain itu, dari 93 penelitian deteksi penyimpangan pengadaan yang ditelaah, hanya dua yang benar-benar diterapkan dalam sistem yang dipakai lembaga pengawas (Schneider dos Santos et al., 2025).

Berdasarkan kondisi tersebut, permasalahan yang diangkat adalah bagaimana membantu pengawas menentukan paket pengadaan bersumber APBD pemerintah provinsi yang perlu ditelusuri lebih dahulu, sejak tahap perencanaan hingga pelaksanaan. Masukan dari tahap ini adalah kondisi dan permasalahan pengawasan pengadaan, sedangkan luarannya adalah latar belakang, rumusan masalah, batasan masalah, tujuan, dan manfaat tugas akhir yang diuraikan pada Bab 1.

### 3.2.2 Studi Literatur

Pada tahap ini, penulis menyusun dasar teori dan meninjau penelitian terdahulu dari berbagai sumber ilmiah, seperti jurnal, prosiding, peraturan, dan publikasi resmi lembaga pemerintah, untuk mengetahui kelebihan dan kesenjangan penelitian yang dapat diisi oleh tugas akhir ini. Tinjauan penelitian terdahulu berfokus pada penerapan machine learning pada pengadaan publik, deteksi anomali belanja pemerintah Indonesia, ensemble deteksi anomali, dan penerapan SHAP pada deteksi anomali. Dasar teori yang dikaji meliputi pengadaan barang/jasa pemerintah, RUP dan realisasi pengadaan, red flag pengadaan, machine learning dan unsupervised learning, deteksi anomali, Isolation Forest, Local Outlier Factor (LOF), Autoencoder, ensemble deteksi anomali, SHAP, metrik evaluasi, serta dashboard dan peta choropleth. Luaran tahap ini adalah tinjauan pustaka pada Bab 2 yang menjadi dasar pemilihan metode dan rancangan evaluasi.

### 3.2.3 Pengumpulan dan Penyiapan Data

Tahap ini mengubah data mentah dari portal Data INAPROC menjadi dataset yang siap digunakan oleh model. Tahap ini terdiri atas empat proses, yaitu pengumpulan data, pra-pemrosesan data, pembentukan dataset per jalur, dan rekayasa fitur.

#### 3.2.3.1 Pengumpulan Data

Data yang digunakan adalah data RUP dan data realisasi pengadaan yang diambil dari portal Data INAPROC (data.inaproc.id), yaitu portal yang menyediakan data pengadaan secara terbuka (LKPP, 2025b). Data diambil untuk tahun anggaran 2025–2026. Data RUP berisi rencana paket yang diumumkan sebelum pengadaan dilaksanakan, sedangkan data realisasi berisi catatan paket yang sudah berjalan. Kolom yang tersedia pada kedua data ditunjukkan pada Tabel 3.1.

<p align="center">Tabel 3.1 Kolom Data RUP dan Data Realisasi</p>

| Kolom | Data | Keterangan |

|---|---|---|

| nama_instansi | RUP, realisasi | Nama instansi pemilik paket, misalnya pemerintah provinsi |

| nama_satuan_kerja | RUP, realisasi | Nama satuan kerja atau perangkat daerah yang melaksanakan paket |

| tahun_anggaran | RUP, realisasi | Tahun anggaran paket |

| kode_rup | RUP, realisasi | Kode unik paket pada RUP, digunakan untuk memasangkan kedua data |

| cara_pengadaan | RUP | Cara pengadaan, yaitu melalui penyedia atau swakelola |

| metode_pengadaan | RUP, realisasi | Metode pemilihan penyedia, misalnya tender atau pengadaan langsung |

| jenis_pengadaan | RUP, realisasi | Jenis barang/jasa, misalnya barang, pekerjaan konstruksi, jasa konsultansi, atau jasa lainnya |

| nama_paket | RUP, realisasi | Nama paket pengadaan |

| sumber_dana | RUP, realisasi | Sumber dana paket, misalnya APBD |

| produk_dalam_negeri | RUP | Keterangan penggunaan produk dalam negeri |

| total_nilai | RUP, realisasi | Pagu paket pada data RUP dan nilai realisasi pada data realisasi |

| kode_paket | Realisasi | Kode paket pada sistem pelaksanaan pengadaan |

| sumber_transaksi | Realisasi | Asal pencatatan transaksi pengadaan |

| nama_penyedia | Realisasi | Nama penyedia yang melaksanakan paket |

| status_paket | Realisasi | Status paket saat data diambil |

| tahapan_pengadaan | Realisasi | Tahapan pengadaan yang sedang atau sudah dilalui paket |

| nilai_pdn | Realisasi | Nilai produk dalam negeri pada paket |

| nilai_umk | Realisasi | Nilai paket yang dikerjakan oleh usaha mikro dan kecil |

Berdasarkan Tabel 3.1, kedua data memiliki kolom kode_rup yang sama sehingga dapat dipasangkan. Kolom total_nilai memiliki arti yang berbeda pada kedua data, yaitu pagu pada data RUP dan nilai realisasi pada data realisasi. Contoh tampilan data RUP dan data realisasi pada portal Data INAPROC ditunjukkan pada Gambar 3.3 dan Gambar 3.4.

![[Sisipkan Gambar 3.3 di sini: tangkapan layar data RUP dari data.inaproc.id]]()

<p align="center">Gambar 3.3 Contoh Data RUP pada Portal Data INAPROC (LKPP, 2025b)</p>

![[Sisipkan Gambar 3.4 di sini: tangkapan layar data realisasi dari data.inaproc.id]]()

<p align="center">Gambar 3.4 Contoh Data Realisasi pada Portal Data INAPROC (LKPP, 2025b)</p>

Sesuai batasan masalah, data yang digunakan hanya paket milik pemerintah provinsi yang bersumber dari APBD. Paket milik pemerintah kabupaten/kota dan kementerian/lembaga, serta paket dengan sumber dana selain APBD, tidak digunakan dalam tugas akhir ini.

#### 3.2.3.2 Pra-pemrosesan Data

Pra-pemrosesan dilakukan agar data bersih, konsisten, dan dapat dipasangkan. Pertama, data disaring sehingga hanya berisi paket pemerintah provinsi yang bersumber dari APBD. Kedua, baris yang tercatat lebih dari satu kali dihapus. Ketiga, nilai kosong dan format nilai diseragamkan, misalnya nilai "-" pada paket swakelola diubah menjadi nilai kosong dan nilai rupiah diubah menjadi angka. Keempat, beberapa baris realisasi yang memiliki kode RUP yang sama digabungkan menjadi satu baris dengan menjumlahkan nilai realisasinya, sehingga setiap paket hanya muncul satu kali. Selain itu, kolom total_nilai diberi nama yang berbeda pada kedua data, yaitu pagu dan nilai realisasi, agar tidak tertukar saat data dipasangkan.

#### 3.2.3.3 Pembentukan Dataset per Jalur

Data yang sudah bersih dibagi menjadi dua dataset sesuai jalur analisis. Dataset jalur perencanaan berisi seluruh paket pada data RUP, sehingga setiap paket dapat dinilai sebelum pengadaan dilaksanakan. Dataset jalur pelaksanaan berisi paket yang memiliki pasangan data RUP dan data realisasi, yang dipasangkan berdasarkan kode RUP. Alur penyiapan dataset ditunjukkan pada Gambar 3.5.

![[Sisipkan Gambar 3.5 di sini: gambar-3-5-diagram-alir-penyiapan-dataset.png]]()

<p align="center">Gambar 3.5 Diagram Alir Penyiapan Dataset per Jalur</p>

Pada Gambar 3.5, setiap paket RUP masuk ke dataset jalur perencanaan. Paket yang memiliki pasangan data realisasi juga masuk ke dataset jalur pelaksanaan, sedangkan paket yang belum memiliki data realisasi hanya dinilai pada jalur perencanaan. Dengan cara ini, satu paket dapat dinilai dari sisi rencana maupun dari sisi pelaksanaannya.

#### 3.2.3.4 Rekayasa Fitur

Rekayasa fitur dilakukan untuk mengubah kolom data paket menjadi angka yang menggambarkan karakteristik paket, karena model hanya dapat mengolah data numerik. Kolom kategori, seperti metode pengadaan dan jenis pengadaan, diubah menjadi angka menggunakan one-hot encoding. Nilai pagu diubah dengan transformasi logaritma karena nilai pagu antarpaket dapat berbeda sangat jauh. Selain itu, nilai paket dibandingkan dengan nilai paket sejenis agar paket dengan jenis dan metode pengadaan yang berbeda tetap dapat dinilai secara setara. Cara serupa digunakan oleh Zulfikar et al. (2023), yang mengubah nilai realisasi menjadi persentase terhadap pagu agar satuan kerja dengan pagu berbeda dapat dibandingkan. Rancangan awal fitur untuk setiap jalur ditunjukkan pada Tabel 3.2.

<p align="center">Tabel 3.2 Rancangan Awal Fitur</p>

| Fitur | Jalur | Keterangan |

|---|---|---|

| Nilai pagu | Perencanaan, pelaksanaan | Logaritma dari pagu paket |

| Rasio pagu terhadap paket sejenis | Perencanaan, pelaksanaan | Pagu paket dibagi median pagu paket dengan jenis dan metode pengadaan yang sama |

| Porsi pagu pada satuan kerja | Perencanaan, pelaksanaan | Pagu paket dibagi total pagu satuan kerja pada tahun yang sama |

| Jumlah paket satuan kerja | Perencanaan, pelaksanaan | Jumlah paket yang direncanakan satuan kerja pada tahun yang sama |

| Metode pengadaan | Perencanaan, pelaksanaan | Hasil one-hot encoding metode pengadaan |

| Jenis pengadaan | Perencanaan, pelaksanaan | Hasil one-hot encoding jenis pengadaan |

| Cara pengadaan | Perencanaan, pelaksanaan | Bernilai 1 untuk penyedia dan 0 untuk swakelola |

| Produk dalam negeri | Perencanaan, pelaksanaan | Bernilai 1 jika paket menggunakan produk dalam negeri |

| Rasio realisasi terhadap pagu | Pelaksanaan | Nilai realisasi dibagi pagu paket |

| Perubahan metode pengadaan | Pelaksanaan | Bernilai 1 jika metode pada data realisasi berbeda dengan data RUP |

| Porsi nilai PDN | Pelaksanaan | Nilai produk dalam negeri dibagi nilai realisasi |

| Porsi nilai UMK | Pelaksanaan | Nilai usaha mikro dan kecil dibagi nilai realisasi |

| Sumber transaksi | Pelaksanaan | Hasil one-hot encoding sumber transaksi |

Fitur pada Tabel 3.2 masih dapat berubah setelah data dieksplorasi, misalnya jika suatu kolom banyak bernilai kosong. Indikator red flag yang digunakan pada tahap evaluasi tidak dimasukkan secara langsung sebagai fitur, agar evaluasi tidak hanya mengukur kembali informasi yang sudah diberikan kepada model. Luaran tahap ini adalah dataset fitur jalur perencanaan dan jalur pelaksanaan.

### 3.2.4 Pengembangan Model Ensemble

Tahap ini menghasilkan skor anomali dan peringkat prioritas setiap paket. Model dilatih menggunakan data seluruh provinsi sekaligus agar setiap paket dibandingkan dengan paket lain secara nasional, kemudian hasilnya diringkas per provinsi pada tahap pengembangan dashboard. Seluruh proses dijalankan secara terpisah untuk jalur perencanaan dan jalur pelaksanaan. Alur pengembangan model ensemble ditunjukkan pada Gambar 3.6.

![[Sisipkan Gambar 3.6 di sini: gambar-3-6-diagram-alir-model-ensemble.png]]()

<p align="center">Gambar 3.6 Diagram Alir Pengembangan Model Ensemble</p>

Pada Gambar 3.6, dataset fitur distandardisasi lalu digunakan untuk melatih tiga model secara terpisah. Skor dari ketiga model dinormalisasi dan dirata-ratakan menjadi skor ensemble, lalu paket diurutkan berdasarkan skor tersebut. Rincian setiap proses diuraikan sebagai berikut.

#### 3.2.4.1 Pelatihan Model Individual

Tiga model unsupervised dilatih menggunakan dataset fitur, yaitu Isolation Forest, LOF, dan Autoencoder. Ketiga model dipilih karena menilai ketidaklaziman dengan prinsip yang berbeda, yaitu isolasi observasi, kepadatan lokal, dan galat rekonstruksi (Han et al., 2022; Roshan & Zafar, 2021). Isolation Forest menilai seberapa mudah suatu paket dipisahkan dari paket lain, LOF menilai kepadatan data di sekitar paket dibandingkan dengan tetangganya, dan Autoencoder menilai besarnya galat saat paket disusun ulang. Sebelum pelatihan, fitur distandardisasi agar setiap fitur memiliki skala yang sama, karena perhitungan jarak pada LOF dan galat rekonstruksi pada Autoencoder dipengaruhi oleh skala fitur. Parameter awal setiap model, seperti jumlah pohon pada Isolation Forest, jumlah tetangga k pada LOF, dan ukuran lapisan bottleneck pada Autoencoder, ditentukan dari nilai yang umum digunakan, lalu disesuaikan berdasarkan hasil percobaan. Setiap model menghasilkan satu skor anomali untuk setiap paket, dengan nilai yang lebih tinggi menunjukkan paket yang lebih tidak lazim.

#### 3.2.4.2 Normalisasi Skor

Skor dari ketiga model memiliki skala yang berbeda, sehingga tidak dapat langsung digabungkan. Oleh karena itu, skor setiap model diubah ke rentang 0 sampai 1 menggunakan normalisasi min-max sesuai Persamaan 2.9 (Krčmar et al., 2026). Paket dengan skor tertinggi pada suatu model bernilai 1, sedangkan paket dengan skor terendah bernilai 0.

#### 3.2.4.3 Penggabungan Skor

Skor yang sudah dinormalisasi digabungkan dengan menghitung rata-ratanya sesuai Persamaan 2.10 (Krčmar et al., 2026). Setiap model diberi bobot yang sama, sehingga skor ensemble tidak bergantung pada satu model saja. Hasil proses ini adalah skor ensemble untuk setiap paket.

#### 3.2.4.4 Pemeringkatan Paket

Paket diurutkan berdasarkan skor ensemble dari yang tertinggi ke yang terendah. Paket pada urutan teratas menjadi prioritas penelusuran bagi pengawas. Selain peringkat ensemble, peringkat dari setiap model individual juga disimpan untuk digunakan pada tahap evaluasi. Luaran tahap ini adalah skor anomali dan peringkat paket untuk jalur perencanaan dan jalur pelaksanaan.

### 3.2.5 Evaluasi dan Interpretasi Model

Tahap ini menilai kinerja model dan menjelaskan alasan suatu paket mendapat skor tinggi. Karena tidak tersedia label anomali yang terverifikasi, evaluasi dilakukan melalui perbandingan dengan model individual menggunakan Precision@K terhadap indikator red flag pengadaan, serta penelaahan jumlah indikator red flag yang dipenuhi oleh paket dengan peringkat anomali tertinggi. Setelah itu, SHAP digunakan untuk menjelaskan kontribusi fitur terhadap skor paket berperingkat atas. Alur evaluasi dan interpretasi model ditunjukkan pada Gambar 3.7.

![[Sisipkan Gambar 3.7 di sini: gambar-3-7-diagram-alir-evaluasi-model.png]]()

<p align="center">Gambar 3.7 Diagram Alir Evaluasi dan Interpretasi Model</p>

Pada Gambar 3.7, Precision@K dihitung berulang untuk setiap model dan setiap nilai K. Setelah semua hasil diperoleh, Precision@K ensemble dibandingkan dengan model individual, lalu paket berperingkat atas ditelaah berdasarkan jumlah red flag dan dijelaskan menggunakan SHAP.

#### 3.2.5.1 Penyusunan Indikator Red Flag

Indikator red flag disusun sebagai acuan pembanding, bukan sebagai label kebenaran, karena keberadaan red flag tidak sama dengan bukti pelanggaran (Decarolis & Giorgiantonio, 2022). Indikator dipilih dari pola yang dikenal dalam pengadaan dan dapat dihitung dari kolom data yang tersedia. Rancangan indikator red flag ditunjukkan pada Tabel 3.3.

<p align="center">Tabel 3.3 Rancangan Indikator Red Flag</p>

| Indikator | Aturan Penandaan | Jalur | Sumber |

|---|---|---|---|

| Nilai mendekati ambang pengadaan langsung | Paket dengan metode pengadaan langsung yang pagunya paling sedikit 90% dari ambang pengadaan langsung sesuai jenis pengadaan pada Subbab 2.2.3 | Perencanaan, pelaksanaan | KPK (2026); Peraturan Presiden Nomor 46 Tahun 2025 (2025) |

| Pemecahan paket | Satuan kerja memiliki beberapa paket pengadaan langsung dengan jenis pengadaan sama dan nama paket mirip pada tahun yang sama, yang jika dijumlahkan melebihi ambang pengadaan langsung | Perencanaan, pelaksanaan | KPK (2026) |

| Penyedia dengan banyak paket | Penyedia menangani paket pada satuan kerja yang sama dalam satu tahun anggaran dengan jumlah di atas persentil ke-95 seluruh penyedia | Pelaksanaan | KPK (2026) |

| Prosedur tidak kompetitif | Paket menggunakan metode penunjukan langsung | Perencanaan, pelaksanaan | Decarolis dan Giorgiantonio (2022) |

Suatu paket dianggap ber-red flag jika memenuhi paling sedikit satu indikator pada Tabel 3.3. Jumlah indikator yang dipenuhi setiap paket juga dicatat untuk digunakan pada penelaahan jumlah red flag. Daftar indikator ini masih dapat disesuaikan setelah data dieksplorasi.

#### 3.2.5.2 Perhitungan Precision@K

Precision@K dihitung sebagai proporsi paket ber-red flag di antara K paket dengan skor tertinggi sesuai Persamaan 2.14. Perhitungan dilakukan pada beberapa nilai K, yaitu 50, 100, dan 200 paket, agar hasil tidak bergantung pada satu nilai K saja. Nilai K dibatasi pada jumlah paket yang masih wajar untuk diperiksa oleh pengawas. Pembatasan serupa dilakukan oleh Herreros-Martínez et al. (2025), yang membatasi jumlah transaksi yang ditandai agar tetap dapat diperiksa oleh auditor. Perhitungan dilakukan terpisah untuk jalur perencanaan dan jalur pelaksanaan.

#### 3.2.5.3 Perbandingan dengan Model Individual

Precision@K ensemble dibandingkan dengan Precision@K Isolation Forest, LOF, dan Autoencoder secara terpisah pada nilai K yang sama. Perbandingan ini dilakukan untuk melihat apakah penggabungan ketiga model memberikan hasil yang lebih konsisten daripada setiap model individual. Hal ini diperlukan karena tidak ada satu metode unsupervised yang selalu unggul pada semua data (Han et al., 2022), sedangkan ensemble berisi metode yang beragam dapat memberikan kinerja yang setara dengan metode individual terbaik (Krčmar et al., 2026). Hasil perbandingan disajikan dalam bentuk tabel dan grafik untuk setiap jalur.

#### 3.2.5.4 Penelaahan Jumlah Red Flag

Precision@K hanya melihat ada atau tidaknya red flag pada suatu paket. Oleh karena itu, paket dengan peringkat anomali tertinggi juga ditelaah berdasarkan jumlah indikator red flag yang dipenuhinya. Penelaahan dilakukan dengan menghitung sebaran jumlah indikator pada K paket teratas hasil ensemble, lalu membandingkannya dengan sebaran pada seluruh paket. Jika paket berperingkat atas cenderung memenuhi lebih banyak indikator, skor ensemble dinilai searah dengan tanda risiko yang dikenal dalam pengadaan.

#### 3.2.5.5 Interpretasi dengan SHAP

SHAP digunakan untuk menjelaskan kontribusi setiap fitur terhadap skor ensemble pada paket berperingkat atas. Karena skor ensemble berasal dari gabungan tiga model, penjelasan dihitung menggunakan Kernel SHAP yang bersifat model-agnostic (Roshan & Zafar, 2021). Kernel SHAP membutuhkan waktu komputasi yang besar dan hasilnya bergantung pada pemilihan data latar (Roshan & Zafar, 2021). Oleh karena itu, SHAP hanya dihitung untuk 200 paket teratas pada setiap jalur, dengan data latar berupa sampel paket yang mewakili dataset. Hasil SHAP disajikan dalam dua bentuk, yaitu grafik kontribusi fitur untuk setiap paket seperti pada Gambar 2.6 dan summary plot untuk melihat fitur yang paling berpengaruh secara keseluruhan (Muñoz-Cancino & Ríos, 2025). Luaran tahap ini adalah hasil evaluasi dan kontribusi fitur untuk setiap paket berperingkat atas.

### 3.2.6 Pengembangan Dashboard

Tahap ini menyajikan hasil model dalam bentuk yang mudah digunakan oleh pengawas. Dashboard dikembangkan melalui tiga proses, yaitu agregasi hasil per provinsi, perancangan dashboard, dan implementasi dashboard.

#### 3.2.6.1 Agregasi Hasil per Provinsi

Hasil per paket diringkas untuk setiap provinsi dalam bentuk proporsi paket anomali, yaitu jumlah paket anomali di suatu provinsi dibagi jumlah seluruh paket di provinsi tersebut. Paket anomali ditetapkan sebagai paket yang masuk dalam 5% skor ensemble tertinggi secara nasional pada setiap jalur. Proporsi digunakan sebagai pengganti jumlah paket karena peta yang menggunakan nilai absolut dapat menyesatkan pembaca (Adams et al., 2023). Dengan cara ini, provinsi dengan jumlah paket yang besar tidak otomatis terlihat paling tinggi.

#### 3.2.6.2 Perancangan Dashboard

Perancangan dilakukan dengan menyusun rancangan tampilan dashboard sebelum diimplementasikan. Dashboard dirancang memuat empat komponen utama. Pertama, peta choropleth 38 provinsi yang warnanya menunjukkan proporsi paket anomali. Kedua, pilihan tampilan jalur perencanaan dan jalur pelaksanaan. Ketiga, daftar peringkat paket yang dapat disaring berdasarkan provinsi. Keempat, rincian paket yang memuat data paket, skor anomali, dan grafik kontribusi fitur dari SHAP.

#### 3.2.6.3 Implementasi Dashboard

Rancangan dashboard diimplementasikan menjadi aplikasi berbasis web yang menampilkan hasil model yang sudah disimpan. Dashboard tidak dirancang sebagai sistem pemantauan real-time, sehingga data diperbarui dengan menjalankan ulang proses pemodelan. Setelah diimplementasikan, setiap komponen dashboard diuji untuk memastikan peta, pilihan jalur, daftar peringkat, dan rincian paket menampilkan data yang sesuai dengan hasil model. Luaran tahap ini adalah dashboard pemeringkatan paket dan sebaran anomali antarprovinsi.

### 3.2.7 Analisis Hasil dan Pembahasan

Pada tahap ini, hasil evaluasi, penjelasan SHAP, dan sebaran antarprovinsi dianalisis untuk menjawab rumusan masalah. Analisis mencakup perbandingan kinerja ensemble dengan model individual, fitur yang paling sering memengaruhi skor paket berperingkat atas, serta provinsi dengan proporsi paket anomali yang tinggi pada setiap jalur. Pembahasan juga mencakup keterbatasan hasil, karena skor anomali hanya menunjukkan ketidaklaziman berdasarkan data dan bukan bukti pelanggaran. Luaran tahap ini adalah hasil analisis dan pembahasan yang menjadi dasar penarikan kesimpulan dan saran.

### 3.2.8 Penyusunan Laporan Tugas Akhir

Tahap penyusunan buku tugas akhir dilakukan untuk mendokumentasikan seluruh hal yang dilakukan pada tugas akhir ini. Penyusunan buku tugas akhir mengikuti format dan ketentuan penulisan berdasarkan pedoman penyusunan tugas akhir program sarjana (S1) Institut Teknologi Sepuluh Nopember (ITS). Masukan dari tahap ini adalah seluruh hal yang telah dilakukan selama pengerjaan tugas akhir, terutama model ensemble deteksi anomali, penjelasan SHAP, dan dashboard. Luaran dari tahap ini adalah buku tugas akhir yang mencakup bab pendahuluan, tinjauan pustaka, metodologi, hasil dan pembahasan, hingga kesimpulan dan saran.
