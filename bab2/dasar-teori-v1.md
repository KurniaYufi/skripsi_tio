# 2.2 Dasar Teori (Draf v1)

> Format mengikuti proposal Nadia Ayula: paragraf pengantar, lalu subbab 2.2.x berisi pengertian bersitasi dan penerapannya dalam tugas akhir ini. Semua rujukan berupa jurnal open access di library atau sumber resmi yang gratis diakses.

---

Bagian dasar teori membahas konsep-konsep utama yang menjadi landasan tugas akhir ini. Teori yang digunakan mencakup pengadaan barang/jasa pemerintah, Rencana Umum Pengadaan (RUP) dan realisasi pengadaan, red flag pengadaan, machine learning dan unsupervised learning, deteksi anomali, Isolation Forest, Local Outlier Factor (LOF), Autoencoder, ensemble deteksi anomali, SHAP, metrik evaluasi, serta dashboard dan peta choropleth. Teori-teori tersebut digunakan untuk mendukung pengembangan model deteksi anomali anggaran pengadaan barang/jasa bersumber APBD pemerintah provinsi beserta penyajian hasilnya.

## 2.2.1 Pengadaan Barang/Jasa Pemerintah

Pengadaan barang/jasa pemerintah adalah kegiatan pengadaan oleh kementerian, lembaga, atau perangkat daerah yang dibiayai APBN atau APBD, mulai dari identifikasi kebutuhan sampai serah terima hasil pekerjaan (Peraturan Presiden Nomor 46 Tahun 2025, 2025). Objek pengadaan mencakup barang, pekerjaan konstruksi, jasa konsultansi, dan jasa lainnya (Kusumadewi et al., 2022). Proses pengadaan terdiri atas tiga tahap utama, yaitu persiapan, pemilihan, dan pelaksanaan (Kusumadewi et al., 2022). Tahap persiapan meliputi penyusunan rencana umum pengadaan, rencana pelaksanaan pengadaan, dan rencana pemilihan penyedia. Tahap pemilihan meliputi pengumuman, evaluasi penawaran, hingga penetapan pemenang. Tahap pelaksanaan meliputi penandatanganan kontrak, pelaksanaan pekerjaan, dan serah terima hasil pekerjaan (Kusumadewi et al., 2022).

Dalam tugas akhir ini, pengadaan yang dianalisis adalah pengadaan barang/jasa pemerintah provinsi yang bersumber dari APBD. Tahapan pengadaan tersebut menjadi dasar pembagian analisis menjadi dua jalur, yaitu jalur perencanaan yang mewakili tahap persiapan dan jalur pelaksanaan yang mewakili tahap setelah paket berjalan.

## 2.2.2 Rencana Umum Pengadaan dan Realisasi Pengadaan

Rencana Umum Pengadaan (RUP) adalah daftar rencana pengadaan barang/jasa yang akan dilaksanakan oleh kementerian, lembaga, atau perangkat daerah (Peraturan Presiden Nomor 46 Tahun 2025, 2025). RUP diumumkan melalui Sistem Informasi Rencana Umum Pengadaan (SiRUP) agar rencana pengadaan dapat diketahui oleh publik (LKPP, 2025a). Selain melalui SiRUP, data pengadaan juga tersedia secara terbuka melalui Data INAPROC (LKPP, 2025b).

Dalam tugas akhir ini, data RUP digunakan untuk menilai seluruh paket pada jalur perencanaan, karena data ini tersedia sebelum pengadaan dilaksanakan. Data realisasi digunakan pada jalur pelaksanaan dengan memasangkan setiap paket RUP dengan data realisasinya berdasarkan kode RUP. Dengan cara ini, paket dapat dinilai sejak tahap perencanaan dan dinilai kembali setelah pengadaan berjalan.

## 2.2.3 Red Flag Pengadaan

Red flag adalah tanda peringatan dini yang menunjukkan adanya risiko ketidakwajaran dalam proses pengadaan (Salazar et al., 2024). Salazar et al. (2024) menyusun 11 red flag yang dikelompokkan ke dalam tiga dimensi, yaitu kurangnya persaingan, kurangnya transparansi, dan ketidakwajaran dalam proses pengadaan. Contoh red flag tersebut antara lain hanya ada satu penawar, penyedia yang terlalu sering menang, penunjukan langsung, serta masa pengumuman yang terlalu pendek atau terlalu panjang (Salazar et al., 2024). Di Indonesia, Komisi Pemberantasan Korupsi (KPK, 2026) mencontohkan pola pemecahan paket dengan nilai mendekati ambang pengadaan langsung serta penyedia yang menangani banyak paket secara bersamaan sebagai pola yang perlu diklarifikasi. Ambang pengadaan langsung sendiri ditetapkan paling banyak Rp200 juta untuk barang/jasa lainnya, Rp400 juta untuk pekerjaan konstruksi, dan Rp100 juta untuk jasa konsultansi (Peraturan Presiden Nomor 46 Tahun 2025, 2025).

Dalam tugas akhir ini, red flag tidak digunakan sebagai label kebenaran, karena keberadaan red flag belum tentu berarti terjadi pelanggaran. Red flag digunakan sebagai acuan pembanding untuk melihat apakah paket yang mendapat skor anomali tinggi juga memiliki tanda-tanda risiko yang dikenal dalam pengadaan.

## 2.2.4 Machine Learning dan Unsupervised Learning

Machine learning merupakan pendekatan yang memungkinkan komputer mempelajari pola dari data, dan sebagian besar penelitian deteksi penyimpangan pengadaan saat ini menggunakan pendekatan tersebut (Schneider dos Santos et al., 2025). Berdasarkan ketersediaan label, metode machine learning untuk deteksi anomali dapat dibagi menjadi supervised, semi-supervised, dan unsupervised (Han et al., 2022). Metode supervised membutuhkan label lengkap yang jarang tersedia, sedangkan metode unsupervised tidak membutuhkan label dan bekerja berdasarkan asumsi tertentu tentang sebaran data, misalnya anomali berada pada daerah yang jarang berisi data (Han et al., 2022).

Tugas akhir ini menggunakan unsupervised learning karena data RUP dan realisasi tidak memiliki label paket yang terbukti bermasalah. Penelitian anomali pengadaan juga umumnya bergantung pada data yang tidak berlabel (Schneider dos Santos et al., 2025).

## 2.2.5 Deteksi Anomali

Deteksi anomali, yang juga dikenal sebagai deteksi outlier, adalah proses menemukan data yang menyimpang secara signifikan dari sebagian besar data lainnya (Han et al., 2022). Han et al. (2022) membagi anomali menjadi empat jenis. Anomali lokal adalah data yang menyimpang dari data di sekitarnya, anomali global adalah data yang sangat berbeda dari keseluruhan data, anomali dependensi adalah data yang tidak mengikuti pola hubungan antarfitur pada data normal, dan anomali berkelompok adalah sekumpulan anomali yang memiliki karakteristik serupa. Kinerja suatu metode sangat bergantung pada kesesuaian antara asumsi metode tersebut dan jenis anomali dalam data, sehingga tidak ada satu metode yang unggul untuk semua jenis anomali (Han et al., 2022).

Dalam tugas akhir ini, anomali diartikan sebagai paket pengadaan yang karakteristiknya tidak lazim dibandingkan paket lain, misalnya dari sisi pagu, metode pemilihan, jenis pengadaan, waktu, atau selisih antara rencana dan realisasi. Anomali menunjukkan ketidaklaziman statistik dan bukan bukti pelanggaran, sehingga hasilnya digunakan sebagai prioritas penelusuran.

## 2.2.6 Isolation Forest

Isolation Forest adalah metode deteksi anomali unsupervised berbasis kumpulan pohon yang memisahkan data melalui pembagian acak secara berulang (Ambarsari et al., 2025). Metode ini didasarkan pada gagasan bahwa anomali lebih mudah dipisahkan, sehingga anomali cenderung terisolasi lebih dekat ke akar pohon isolasi (isolation tree), sedangkan data normal terisolasi lebih dalam (Herreros-Martínez et al., 2025). Skor anomali Isolation Forest dihitung dengan persamaan berikut (Ambarsari et al., 2025).

s(x, n) = 2^(−E(h(x)) / c(n))    (2.1)

c(n) = 2H(n − 1) − 2(n − 1)/n    (2.2)

Pada persamaan tersebut, E(h(x)) adalah rata-rata panjang lintasan (path length) yang dibutuhkan untuk mengisolasi data x pada seluruh pohon, sedangkan c(n) adalah rata-rata panjang lintasan untuk n data yang digunakan sebagai pembanding (Ambarsari et al., 2025). Semakin pendek rata-rata panjang lintasan suatu data, semakin besar skor anomalinya. Isolation Forest juga efisien karena memiliki kompleksitas komputasi O(n log n) (Krčmar et al., 2026).

Dalam tugas akhir ini, Isolation Forest digunakan untuk menangkap paket yang menyimpang dari keseluruhan data, misalnya paket dengan kombinasi nilai pagu dan karakteristik yang jarang muncul.

## 2.2.7 Local Outlier Factor (LOF)

Local Outlier Factor (LOF) adalah metode deteksi anomali yang menilai ketidaklaziman suatu data berdasarkan perbedaan kepadatan lokal data tersebut dibandingkan dengan tetangga-tetangga terdekatnya (Krčmar et al., 2026). Data yang berada di daerah dengan kepadatan jauh lebih rendah daripada tetangganya akan memperoleh skor anomali yang lebih tinggi. LOF unggul dalam menemukan anomali lokal, tetapi kurang baik untuk anomali berkelompok (Han et al., 2022).

Dalam tugas akhir ini, LOF digunakan untuk menangkap paket yang tidak lazim dibandingkan paket sejenis di sekitarnya, meskipun nilainya tidak terlihat ekstrem jika dibandingkan dengan seluruh data.

## 2.2.8 Autoencoder

Autoencoder adalah jaringan saraf tiruan unsupervised yang dilatih untuk menyalin masukannya menjadi keluaran (Roshan & Zafar, 2021). Autoencoder terdiri atas dua bagian, yaitu encoder yang memadatkan data menjadi representasi yang lebih kecil pada lapisan tengah (bottleneck) dan decoder yang menyusun kembali data dari representasi tersebut (Roshan & Zafar, 2021). Ketika dilatih pada data yang sebagian besar normal, Autoencoder dapat menyusun kembali data normal dengan galat kecil, sedangkan data yang tidak lazim akan menghasilkan galat rekonstruksi yang besar (Roshan & Zafar, 2021). Galat rekonstruksi umumnya dihitung menggunakan Mean Squared Error (MSE) sebagai berikut (Roshan & Zafar, 2021).

MSE = Σᵢ₌₁ᴺ (x̂ᵢ − xᵢ)²    (2.3)

Pada persamaan tersebut, xᵢ adalah nilai fitur ke-i pada data asli, x̂ᵢ adalah nilai hasil rekonstruksi, dan N adalah jumlah fitur.

Dalam tugas akhir ini, Autoencoder digunakan untuk menangkap paket yang pola hubungan antarfiturnya tidak sesuai dengan pola umum paket lain. Galat rekonstruksi setiap paket digunakan sebagai skor anomali dari Autoencoder.

## 2.2.9 Ensemble Deteksi Anomali

Ensemble deteksi anomali adalah penggabungan beberapa detektor untuk menghasilkan satu keputusan atau skor akhir. Ensemble yang terdiri atas detektor dengan asumsi berbeda dapat saling melengkapi dan lebih tahan terhadap perbedaan karakteristik data, karena tidak ada satu detektor yang selalu unggul (Krčmar et al., 2026). Skor dari setiap detektor memiliki skala yang berbeda, sehingga perlu dinormalisasi terlebih dahulu ke rentang 0 sampai 1 menggunakan normalisasi min-max sebelum digabungkan, misalnya dengan menghitung rata-ratanya (Krčmar et al., 2026). Penggabungan juga dapat dilakukan melalui pemungutan suara (voting), yaitu suatu data ditandai jika sebagian atau seluruh detektor sepakat (Schiavon et al., 2026).

s̃ₘ(x) = (sₘ(x) − min(sₘ)) / (max(sₘ) − min(sₘ))    (2.4)

S(x) = (1/M) Σₘ₌₁ᴹ s̃ₘ(x)    (2.5)

Pada persamaan tersebut, sₘ(x) adalah skor anomali data x dari detektor ke-m, s̃ₘ(x) adalah skor setelah normalisasi, M adalah jumlah detektor, dan S(x) adalah skor gabungan.

Dalam tugas akhir ini, ensemble disusun dari Isolation Forest, LOF, dan Autoencoder yang masing-masing mewakili prinsip isolasi, kepadatan lokal, dan galat rekonstruksi. Skor ketiga model dinormalisasi lalu digabungkan menjadi skor prioritas, sehingga paket dengan skor tertinggi menjadi prioritas penelusuran.

## 2.2.10 SHAP dan Interpretasi Model

SHapley Additive exPlanations (SHAP) adalah metode Explainable AI yang menjelaskan kontribusi setiap fitur terhadap keluaran model berdasarkan konsep nilai Shapley dari teori permainan koalisi (Roshan & Zafar, 2021). SHAP bersifat model-agnostic, artinya dapat digunakan untuk menjelaskan model yang kompleks seperti metode ensemble dan jaringan saraf tiruan (Roshan & Zafar, 2021). Penjelasan SHAP dinyatakan sebagai penjumlahan kontribusi setiap fitur sebagai berikut (Roshan & Zafar, 2021).

g(z′) = φ₀ + Σᵢ₌₁ᴹ φᵢ z′ᵢ    (2.6)

Pada persamaan tersebut, g adalah model penjelas, φ₀ adalah nilai dasar, φᵢ adalah kontribusi fitur ke-i, dan M adalah jumlah fitur. Kernel SHAP dapat digunakan untuk menghitung kontribusi setiap fitur terhadap galat rekonstruksi Autoencoder, baik untuk satu data maupun untuk keseluruhan model (Roshan & Zafar, 2021). Hasil SHAP dapat disajikan dalam bentuk summary plot yang mengurutkan fitur berdasarkan pengaruhnya dan dependence plot yang menunjukkan pengaruh nilai suatu fitur terhadap hasil model (Muñoz-Cancino & Ríos, 2025). Penjelasan SHAP juga telah digunakan untuk membantu auditor meninjau transaksi yang diprioritaskan (Herreros-Martínez et al., 2025).

Dalam tugas akhir ini, SHAP digunakan setelah skor gabungan diperoleh untuk menjelaskan fitur yang paling memengaruhi skor paket berperingkat atas. Penjelasan ini membantu pengguna memahami alasan suatu paket diprioritaskan.

## 2.2.11 Metrik Evaluasi

Metrik evaluasi digunakan untuk menilai kinerja model. Pada model yang menghasilkan keputusan positif atau negatif, hasil prediksi dapat dikelompokkan menjadi true positive (TP), true negative (TN), false positive (FP), dan false negative (FN) (Roshan & Zafar, 2021). Precision adalah perbandingan antara jumlah data yang benar ditandai positif dengan seluruh data yang ditandai positif (Roshan & Zafar, 2021). Pada data belanja publik tanpa label, precision dapat digunakan untuk memilih kombinasi ensemble, sedangkan hasil pada data asli dinilai dengan membandingkan data yang ditandai dengan acuan di luar data (Schiavon et al., 2026).

Precision = TP / (TP + FP)    (2.7)

Precision@K = (jumlah paket ber-red flag pada K paket teratas) / K    (2.8)

Karena tugas akhir ini tidak memiliki label anomali, precision dihitung pada K paket dengan skor tertinggi (Precision@K), dengan red flag sebagai acuan pembanding. Metrik yang digunakan beserta fungsinya disajikan pada Tabel 2.12.

**Tabel 2.12 Metrik Evaluasi Model**

| Metrik | Fungsi |
|---|---|
| Precision@K | Mengukur proporsi paket ber-red flag di antara K paket dengan skor anomali tertinggi. |
| Perbandingan dengan model individual | Melihat apakah ensemble menghasilkan Precision@K yang setara atau lebih baik daripada Isolation Forest, LOF, dan Autoencoder secara terpisah. |
| Perbandingan dengan peringkat berdasarkan pagu | Melihat apakah ensemble memberi informasi tambahan dibandingkan sekadar mengurutkan paket dari pagu terbesar. |
| Stabilitas peringkat | Melihat apakah paket berperingkat atas tetap konsisten ketika model dijalankan ulang atau datanya sedikit diubah. |

## 2.2.12 Dashboard dan Peta Choropleth

Dashboard adalah layanan berbasis web yang memudahkan visualisasi data spasial maupun nonspasial secara interaktif (Adams et al., 2023). Salah satu bentuk visualisasi spasial pada dashboard adalah peta choropleth, yaitu peta tematik yang menggunakan intensitas warna untuk mewakili nilai data pada setiap wilayah (Adams et al., 2023). Peta choropleth sebaiknya menggunakan nilai relatif, seperti rasio atau proporsi, bukan nilai absolut, karena peta dengan nilai absolut dapat menyesatkan pembaca tentang tingkat keparahan suatu kondisi (Adams et al., 2023). Alat bantu berbasis data yang dirancang bagi lembaga pengawas dapat membantu menentukan prioritas pemeriksaan pengadaan (Salazar et al., 2024), tetapi hanya sedikit penelitian deteksi penyimpangan pengadaan yang benar-benar diterapkan dalam sistem yang digunakan pengawas (Schneider dos Santos et al., 2025).

Dalam tugas akhir ini, dashboard digunakan untuk menyajikan sebaran paket anomali antarprovinsi, peringkat paket, dan penjelasan SHAP untuk setiap paket. Peta choropleth menggunakan proporsi paket anomali di setiap provinsi agar provinsi dengan jumlah paket yang besar tidak otomatis terlihat paling berisiko.

---

## Referensi baru untuk Daftar Pustaka

Adams, A. M., Chen, X., Li, W., & Zhang, C. (2023). Normalizing the pandemic: Exploring the cartographic issues in state government COVID-19 dashboards. *Journal of Maps, 19*(1), 1–9. https://doi.org/10.1080/17445647.2023.2235385

Peraturan Presiden Nomor 46 Tahun 2025 tentang Perubahan Kedua atas Peraturan Presiden Nomor 16 Tahun 2018 tentang Pengadaan Barang/Jasa Pemerintah. (2025). https://peraturan.bpk.go.id/Details/318647

---

## Catatan untuk Tio (di luar naskah)

- Dua sumber baru, keduanya gratis: Adams et al. (2023), Journal of Maps (open access, https://doi.org/10.1080/17445647.2023.2235385), dan Perpres 46/2025 (https://peraturan.bpk.go.id/Details/318647). Sisanya sudah ada di library.
- Rumus 2.1–2.6 diambil dari Ambarsari et al. (2025), Krčmar et al. (2026), dan Roshan & Zafar (2021). Rumus 2.8 (Precision@K) adalah turunan dari rumus precision yang disesuaikan dengan rancangan evaluasi tugas akhir ini.
- Isi Tabel 2.12 mengikuti rencana evaluasi di Bab 1 (Precision@K terhadap red flag, perbandingan dengan model individual dan peringkat pagu, serta stabilitas peringkat). Rinciannya nanti dibahas di Bab 3.
- Sumber asli metode (Liu et al., 2008 untuk Isolation Forest; Breunig et al., 2000 untuk LOF; Lundberg & Lee, 2017 untuk SHAP) sengaja tidak dipakai karena lebih dari 5 tahun. Kalau dosen membolehkan, Lundberg & Lee (2017) bisa ditambahkan karena gratis di NeurIPS.
- Gambar belum ada. Kalau mau seperti Ayula, bisa ditambahkan misalnya ilustrasi arsitektur Autoencoder (Roshan & Zafar, 2021, Gambar 1) dan alur ensemble.
