# Draf Keterangan Tiap Proses (Uraian Alur Metodologi)

> Draf pendamping Gambar 3.1 dan Gambar 3.2 (bab3/gambar/gambar-3-1-metodologi-bagian-1.png dan bab3/gambar/gambar-3-2-metodologi-bagian-2.png). Format mengikuti TA Anas Ghifari: gambar hanya berisi nama proses, sedangkan rincian metode dan keterangan ditulis di subbab berikut. Hal yang belum diputuskan ditandai [BELUM FINAL].

## 3.1 Alur Metodologi Penelitian

Alur metodologi tugas akhir ditunjukkan pada Gambar 3.1 dan Gambar 3.2. Setiap tahap memiliki masukan, proses, dan luaran yang menjadi dasar tahap berikutnya.

[Gambar 3.1 Diagram Metodologi Tugas Akhir Bagian 1]

[Gambar 3.2 Diagram Metodologi Tugas Akhir Bagian 2]

## 3.2 Uraian Alur Penelitian

Penjelasan setiap proses pada Gambar 3.1 dan Gambar 3.2 adalah sebagai berikut.

### 3.2.1 Identifikasi dan Perumusan Masalah

Tahap ini menentukan fokus tugas akhir, yaitu besarnya anggaran pengadaan barang/jasa bersumber APBD pemerintah provinsi dan terbatasnya kemampuan pengawas untuk memeriksa seluruh paket. Hasil tahap ini berupa rumusan masalah, tujuan, batasan masalah, dan manfaat tugas akhir.

### 3.2.2 Studi Literatur

Studi literatur dilakukan untuk memperoleh dasar teori dan penelitian terdahulu yang relevan. Literatur yang dikaji mencakup pengadaan barang/jasa pemerintah, RUP dan realisasi pengadaan, red flag pengadaan, unsupervised learning, deteksi anomali, Isolation Forest, Local Outlier Factor (LOF), Autoencoder, ensemble, SHAP, Large Language Model (LLM), metrik evaluasi, serta dashboard dan peta choropleth. Hasil tahap ini digunakan untuk menentukan metode dan rancangan evaluasi.

### 3.2.3 Pengumpulan dan Penyiapan Data

Tahap ini menyiapkan data mentah menjadi dataset yang siap digunakan oleh model.

#### 3.2.3.1 Pengumpulan Data

Data yang dikumpulkan adalah data Rencana Umum Pengadaan (RUP) dan data realisasi pengadaan dari portal Data INAPROC (data.inaproc.id). Data yang diambil adalah paket pengadaan pemerintah provinsi di seluruh Indonesia yang bersumber dari APBD pada tahun anggaran 2025–2026. Data RUP berisi informasi rencana paket, seperti satuan kerja, cara dan metode pengadaan, jenis pengadaan, nama paket, dan pagu. Data realisasi berisi informasi pelaksanaan paket, seperti nilai realisasi, nama penyedia, dan status paket.

#### 3.2.3.2 Pra-pemrosesan Data

Pra-pemrosesan dilakukan agar data bersih dan konsisten. Langkah yang dilakukan meliputi penyeragaman nilai kosong (misalnya nilai "-" pada paket swakelola), penggabungan beberapa baris realisasi yang memiliki kode RUP yang sama, serta penyesuaian nama kolom nilai, karena kolom nilai pada data RUP berarti pagu, sedangkan pada data realisasi berarti nilai realisasi.

#### 3.2.3.3 Pembentukan Dataset per Jalur

Data dibagi menjadi dua jalur. Jalur perencanaan berisi seluruh paket pada data RUP. Jalur pelaksanaan berisi paket yang memiliki pasangan data RUP dan realisasi, yang dipasangkan berdasarkan kode RUP.

#### 3.2.3.4 Rekayasa Fitur

Rekayasa fitur dilakukan untuk mengubah data paket menjadi angka yang menggambarkan karakteristik paket. Fitur jalur perencanaan antara lain pagu, metode pengadaan non-tender, dan perbandingan pagu dengan paket sejenis. Fitur jalur pelaksanaan antara lain perbandingan nilai realisasi dengan pagu, selisih nilai realisasi dan pagu, serta frekuensi penyedia pada satuan kerja yang sama. Luaran tahap ini adalah dataset fitur untuk jalur perencanaan dan jalur pelaksanaan. [BELUM FINAL: daftar fitur akhir]

### 3.2.4 Pengembangan Model Ensemble

Tahap ini menghasilkan skor anomali dan peringkat prioritas setiap paket. Seluruh proses dijalankan terpisah untuk jalur perencanaan dan jalur pelaksanaan.

#### 3.2.4.1 Pelatihan Model Individual

Tiga model unsupervised dilatih menggunakan data seluruh provinsi sekaligus, yaitu Isolation Forest, LOF, dan Autoencoder. Ketiga model menilai ketidaklaziman dengan cara yang berbeda: Isolation Forest melalui kemudahan suatu paket dipisahkan, LOF melalui kepadatan data di sekitar paket, dan Autoencoder melalui besarnya galat rekonstruksi. Setiap model menghasilkan skor anomali untuk setiap paket.

#### 3.2.4.2 Normalisasi Skor

Skor dari ketiga model memiliki skala yang berbeda, sehingga perlu disamakan terlebih dahulu. Normalisasi min-max digunakan untuk mengubah skor setiap model ke rentang 0 sampai 1.

#### 3.2.4.3 Penggabungan Skor

Skor yang sudah dinormalisasi digabungkan dengan menghitung rata-ratanya. Hasilnya adalah skor ensemble untuk setiap paket.

#### 3.2.4.4 Pemeringkatan Paket

Paket diurutkan berdasarkan skor ensemble dari yang tertinggi. Paket dengan skor tertinggi menjadi prioritas penelusuran. Luaran tahap ini adalah skor anomali dan peringkat paket.

### 3.2.5 Evaluasi dan Interpretasi Model

Tahap ini menilai kinerja model dan menjelaskan alasan suatu paket mendapat skor tinggi, baik dalam bentuk kontribusi fitur maupun kalimat penjelasan.

#### 3.2.5.1 Evaluasi Model

Karena tidak tersedia label anomali, evaluasi dilakukan dengan Precision@K, yaitu proporsi paket yang memiliki red flag di antara K paket dengan skor tertinggi. Red flag yang digunakan antara lain nilai paket yang mendekati batas pengadaan langsung dan penyedia yang menangani banyak paket. Red flag digunakan sebagai pembanding, bukan sebagai label kebenaran. Hasil ensemble dibandingkan dengan Isolation Forest, LOF, dan Autoencoder secara terpisah serta dengan peringkat berdasarkan pagu. Stabilitas peringkat juga diperiksa dengan menjalankan ulang model. [BELUM FINAL: daftar red flag dan nilai K]

#### 3.2.5.2 Interpretasi Hasil Model

Interpretasi dilakukan menggunakan SHAP pada paket dengan skor tertinggi. SHAP menunjukkan fitur yang paling memengaruhi skor suatu paket beserta arah pengaruhnya, sehingga pengguna dapat memahami alasan paket tersebut diprioritaskan.

#### 3.2.5.3 Penyusunan Kalimat Penjelasan

Hasil SHAP berupa angka kontribusi fitur diubah menjadi kalimat penjelasan menggunakan Large Language Model (LLM) agar lebih mudah dipahami oleh pengawas. LLM tidak menghitung ulang SHAP dan tidak menambahkan alasan sendiri. Masukan yang diberikan kepada LLM hanya berupa beberapa fitur dengan kontribusi terbesar beserta nilainya, misalnya pagu paket dibandingkan dengan median paket sejenis. Instruksi (prompt) kepada LLM dibuat tetap untuk semua paket dan membatasi pilihan kata agar kalimat hanya menyebut ketidaklaziman, misalnya "tidak lazim" atau "berbeda dari paket sejenis", tanpa menyimpulkan adanya pelanggaran. Kalimat dibuat satu kali untuk paket berperingkat atas lalu disimpan, sehingga hasilnya konsisten dan dapat diperiksa. [BELUM FINAL: model LLM yang digunakan dan jumlah fitur yang dijelaskan]

#### 3.2.5.4 Verifikasi Kalimat Penjelasan

Kalimat yang dihasilkan LLM diperiksa agar sesuai dengan hasil SHAP. Pemeriksaan dilakukan dengan mencocokkan nama fitur dan angka yang disebut dalam kalimat dengan nilai aslinya. Kalimat yang tidak sesuai dibuat ulang. Selain itu, kalimat dibandingkan dengan kalimat templat tanpa LLM, misalnya "Pagu paket ini 8 kali lebih besar dari median paket sejenis", untuk melihat nilai tambah penggunaan LLM.

#### 3.2.5.5 Telaah Sampel Paket Prioritas

Sejumlah paket berperingkat atas ditelaah untuk memeriksa apakah ketidaklaziman yang ditunjukkan model, penjelasan SHAP, dan kalimat penjelasan masuk akal jika dilihat dari data paket. Luaran tahap ini adalah hasil evaluasi dan kalimat penjelasan untuk setiap paket berperingkat atas.

### 3.2.6 Pengembangan Dashboard

Tahap ini menyajikan hasil model dalam bentuk yang mudah digunakan oleh pengawas.

#### 3.2.6.1 Agregasi Hasil per Provinsi

Hasil per paket diringkas untuk setiap provinsi dalam bentuk proporsi paket anomali, yaitu jumlah paket yang melewati batas skor tertentu dibagi jumlah seluruh paket di provinsi tersebut. Proporsi digunakan agar provinsi dengan jumlah paket yang besar tidak otomatis terlihat paling tinggi. [BELUM FINAL: batas skor paket anomali]

#### 3.2.6.2 Perancangan Dashboard

Perancangan dilakukan dengan menyusun sketsa tampilan dashboard. Dashboard dirancang memuat peta choropleth 38 provinsi, pilihan tampilan jalur perencanaan dan jalur pelaksanaan, daftar peringkat paket, serta rincian paket beserta kalimat penjelasan dan grafik kontribusi fitur dari SHAP.

#### 3.2.6.3 Implementasi Dashboard

Rancangan dashboard diimplementasikan menjadi aplikasi berbasis web yang menampilkan hasil model. Luaran tahap ini adalah dashboard pemeringkatan paket dan sebaran anomali antarprovinsi.

### 3.2.7 Analisis Hasil dan Pembahasan

Hasil evaluasi, penjelasan SHAP, kalimat penjelasan, dan sebaran antarprovinsi dianalisis untuk menjawab rumusan masalah. Pembahasan juga mencakup keterbatasan hasil, karena skor anomali menunjukkan ketidaklaziman statistik dan bukan bukti pelanggaran.

### 3.2.8 Penyusunan Laporan Tugas Akhir

Seluruh proses dan hasil tugas akhir disusun menjadi laporan tugas akhir, mulai dari pendahuluan, tinjauan pustaka, metodologi, hasil dan pembahasan, hingga kesimpulan dan saran.
