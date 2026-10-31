# 1.1 Latar Belakang (Draf v2)

> Draf sementara, disusun ulang mengikuti struktur Introduction (umum → riset sebelumnya → spesifik → kontribusi → metode) dan alur bertingkat dari dosen. Penanda `[PERLU ...]` menunjukkan bagian yang masih perlu dilengkapi sebelum final. Catatan untuk Tio ada di bagian paling bawah, di luar naskah.

---

**[Informasi umum → permasalahan umum]**

Pengadaan barang/jasa pemerintah merupakan instrumen utama untuk memenuhi kebutuhan barang, pekerjaan konstruksi, dan jasa dalam pelaksanaan program pemerintahan. Berdasarkan data Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah (LKPP), nilai Rencana Umum Pengadaan (RUP) mencapai Rp859,27 triliun dari total belanja barang/jasa sebesar Rp929,01 triliun per 8 Juni 2026 (LKPP, 2026). Pada tingkat daerah, data Direktorat Jenderal Perimbangan Keuangan menunjukkan bahwa total belanja daerah tahun 2025 pada 546 pemerintah daerah mencapai Rp1.414,62 triliun, dengan alokasi belanja barang dan jasa sebesar Rp418,76 triliun (DJPK, 2026). Pelaksanaan pengadaan tersebut berlangsung melalui tahapan persiapan, pemilihan, dan pelaksanaan kontrak, sehingga kualitas pengadaan sangat ditentukan sejak tahap perencanaan (Kusumadewi et al., 2022).

Besarnya nilai anggaran tersebut juga menjadikan pengadaan sebagai sektor yang rawan penyimpangan. Kajian terhadap kasus korupsi pengadaan di Indonesia menunjukkan pola berulang berupa penggelembungan anggaran, pengadaan fiktif, dan nepotisme dalam pemberian kontrak (Adhi et al., 2025), yang berakar pada lemahnya aturan dan maladministrasi dalam proses pengadaan (Putri et al., 2024). Pada pemerintah daerah, Komisi Pemberantasan Korupsi (KPK) mengidentifikasi pola pemecahan paket dengan nilai mendekati ambang pengadaan langsung serta penyedia yang menangani banyak paket konstruksi secara bersamaan di Pemerintah Provinsi Kalimantan Timur, dan menegaskan bahwa pola tersebut memerlukan klarifikasi lebih lanjut (KPK, 2026). Analisis terhadap realisasi belanja daerah juga menemukan bahwa tingkat penyerapan yang tampak wajar secara agregat dapat menyembunyikan ketidaksesuaian pada kategori belanja tertentu (Hasmi et al., 2026). Di sisi lain, mekanisme pengawasan yang mengandalkan audit manual sulit mengimbangi volume dan kompleksitas data pengadaan (Muñoz-Cancino & Ríos, 2025). Kondisi ini menunjukkan perlunya cara yang dapat membantu pengawas menentukan paket mana yang perlu ditelusuri lebih dahulu.

**[Riset sebelumnya → solusi umum: machine learning]**

Penelitian mengenai deteksi kecurangan pengadaan berbasis data telah berkembang luas. Telaah sistematis terhadap 93 studi menunjukkan bahwa sebagian besar penelitian menggunakan model machine learning untuk mendeteksi indikasi kolusi pada pengadaan publik (Schneider dos Santos et al., 2025). Tinjauan lain juga mencatat pemanfaatan machine learning, jaringan saraf tiruan, pemrosesan bahasa alami, dan analisis jaringan untuk mendeteksi kecurangan pada organisasi publik (Nai et al., 2022). Namun, sebagian besar data pengadaan tidak memiliki label kasus yang terverifikasi, sehingga pendekatan unsupervised anomaly detection banyak digunakan untuk menyusun prioritas pemeriksaan, bukan untuk memutuskan pelanggaran (Salazar et al., 2024; Westerski et al., 2021).

**[Riset sebelumnya → Isolation Forest]**

Salah satu metode unsupervised yang banyak diterapkan adalah Isolation Forest. Muñoz-Cancino dan Ríos (2025) menggunakan Isolation Forest untuk mengidentifikasi penyedia dengan pola relasi tidak lazim pada data pengadaan publik Chile. Di Indonesia, Zulfikar et al. (2023) menerapkan Isolation Forest untuk mendeteksi anomali transaksi belanja barang persediaan pada satuan kerja Kepolisian Republik Indonesia, sedangkan Herreros-Martínez et al. (2025) memanfaatkannya untuk memprioritaskan transaksi pembelian yang perlu diaudit. Meskipun demikian, setiap metode deteksi anomali memiliki asumsi tersendiri mengenai bentuk penyimpangan, dan hasil uji pada 57 dataset menunjukkan bahwa tidak ada satu metode yang unggul secara konsisten pada semua tipe anomali dan kondisi data (Han et al., 2022). Isolation Forest cenderung menangkap observasi yang terisolasi secara global, tetapi belum tentu peka terhadap paket yang hanya menyimpang dibanding kelompok sejenisnya.

**[Riset sebelumnya → argumen ensemble]**

Keterbatasan tersebut menjadi lebih penting ketika data tidak memiliki label, karena model terbaik tidak dapat dipilih secara langsung. Studi berskala besar oleh Ma et al. (2023) menunjukkan bahwa strategi pemilihan model tanpa label belum mampu secara andal memilih detektor yang paling sesuai. Penggabungan beberapa detektor menjadi alternatif untuk mengurangi risiko tersebut. Krčmar et al. (2026) menemukan bahwa ensemble heterogen konsisten berada di peringkat teratas pada 22 dataset acuan dan secara signifikan mengungguli detektor individual yang lebih lemah, termasuk LOF dan autoencoder variasional, meskipun hasilnya setara dengan detektor tunggal terbaik. Pada data pembelian, Herreros-Martínez et al. (2025) juga menggabungkan beberapa teknik deteksi anomali ke dalam satu kerangka prioritas agar berbagai jenis anomali dapat tertangkap. Temuan ini menunjukkan bahwa nilai utama ensemble pada data tanpa label adalah kestabilan hasil, yaitu menghindari ketergantungan pada satu model yang kinerjanya tidak dapat diverifikasi.

**[Latar belakang spesifik → permasalahan khusus / research problem]**

Pada konteks Indonesia, data pengadaan tersedia secara terbuka melalui Sistem Informasi Rencana Umum Pengadaan (SiRUP) dan portal Data INAPROC yang memuat informasi RUP, realisasi, dan pembayaran pengadaan (LKPP, 2025a, 2025b). Namun, penelitian deteksi anomali pengadaan di Indonesia yang ditemukan dalam penelusuran ini masih memiliki beberapa keterbatasan jika dikaitkan dengan pengawasan pengadaan APBD pemerintah provinsi. Ambarsari et al. (2025) menerapkan Isolation Forest pada data tender nasional, tetapi analisis dilakukan pada agregat bulanan sehingga belum menghasilkan prioritas pada tingkat paket, dan penulis sendiri menyarankan analisis per tender sebagai pengembangan. Syaifudin et al. (2026) membandingkan model klasifikasi pada transaksi e-procurement, tetapi pendekatan tersebut membutuhkan label anomali yang telah tersedia. Sukawati dan Rojali (2026) mendeteksi kecurangan transaksi belanja pada satu instansi pemerintah dan menyatakan analisis penjelasan seperti SHAP berada di luar cakupan penelitiannya. Selain itu, penelitian-penelitian tersebut menggunakan data tender atau transaksi yang sudah berjalan, sehingga paket yang masih berada pada tahap rencana dan belum memiliki catatan realisasi tidak ikut dinilai. Dengan demikian, sejauh penelusuran yang dilakukan, masih dibutuhkan analisis pada tingkat paket untuk pengadaan bersumber APBD pemerintah provinsi yang mencakup tahap perencanaan hingga pelaksanaan, tidak bergantung pada label, dan disertai penjelasan atas hasilnya.

Kebutuhan penjelasan tersebut juga penting karena skor anomali tanpa alasan sulit ditindaklanjuti oleh pengawas. Westerski et al. (2021) menunjukkan bahwa penjelasan hasil merupakan syarat agar deteksi anomali pengadaan dapat digunakan dalam praktik. SHapley Additive exPlanations (SHAP) telah digunakan untuk menjelaskan fitur yang berkontribusi terhadap anomali yang dideteksi autoencoder (Antwarg et al., 2021) dan untuk membantu auditor menafsirkan prioritas transaksi pembelian (Herreros-Martínez et al., 2025).

**[Kontribusi / usulan → solusi khusus]**

Berdasarkan permasalahan tersebut, tugas akhir ini mengusulkan deteksi anomali anggaran pengadaan barang/jasa bersumber APBD pemerintah provinsi di seluruh Indonesia dengan pendekatan ensemble unsupervised learning dan explainable AI. Analisis dilakukan melalui dua jalur, yaitu jalur perencanaan yang menilai seluruh paket berdasarkan data RUP dan jalur pelaksanaan yang menilai paket dengan pasangan data RUP dan realisasi. Dengan rancangan ini, paket yang belum memiliki catatan realisasi tetap memperoleh penilaian, sedangkan paket yang telah berjalan dapat dinilai dari hubungan antara rencana dan pelaksanaannya.

**[Ringkasan metode]**

Ensemble disusun dari Isolation Forest, Local Outlier Factor (LOF), dan Autoencoder, yang masing-masing menilai ketidaklaziman melalui isolasi observasi, kepadatan lokal, dan galat rekonstruksi. Skor ketiga model digabungkan menjadi skor prioritas, lalu SHAP digunakan untuk menjelaskan kontribusi fitur pada paket dengan skor tertinggi. Karena tidak terdapat label acuan, evaluasi dilakukan melalui perbandingan dengan model individual dan pemeringkatan berdasarkan pagu, pengujian stabilitas peringkat, serta telaah sampel paket prioritas. Hasilnya disajikan dalam dashboard yang memuat sebaran hasil antarprovinsi dan rincian paket beserta penjelasannya.

**[Harapan]**

Hasil tugas akhir ini diharapkan dapat menjadi bahan pendukung bagi pengawas dalam menentukan urutan penelusuran paket pengadaan bersumber APBD, sejak tahap perencanaan hingga pelaksanaan. Skor anomali yang dihasilkan menunjukkan ketidaklaziman statistik dan tetap memerlukan klarifikasi serta verifikasi lebih lanjut.

---

## Daftar Pustaka tambahan / yang dipakai di draf ini

Sumber yang sudah ada di Daftar Pustaka Tio dan tetap dipakai: Antwarg et al. (2021), DJPK (2026), Han et al. (2022), KPK (2026), LKPP (2025a, 2025b, 2026), Salazar et al. (2024), Westerski et al. (2021), Ambarsari et al. (2025).

Sumber baru (semua ≤ 5 tahun):

Adhi, S., Arifin, R., & Sani, T. (2025). From administrative irregularities to criminal acts: Uncovering corruption in state procurement systems. *PAMPAS: Journal of Criminal Law, 6*(2). `[PERLU LENGKAPI: halaman dan DOI dari PDF di library]`

Hasmi, M., Darmawan, K. A. A.-A., Salsabilah, N. M., Fadilah, A., & Hasnita, N. (2026). Analisis tren belanja daerah sebagai indikasi risiko fraud di Pemerintah Kota Kendari. *Jurnal IAKP: Jurnal Inovasi Akuntansi Keuangan & Perpajakan, 7*(1), 72–84.

Herreros-Martínez, A., Magdalena-Benedicto, R., Vila-Francés, J., Serrano-López, A. J., Pérez-Díaz, S., & Martínez-Herráiz, J. J. (2025). Applied machine learning to anomaly detection in enterprise purchase processes: A hybrid approach using clustering and Isolation Forest. *Information, 16*(3), 177. https://doi.org/10.3390/info16030177

Krčmar, T., Šabanović, D., Köhler, M., & Lukić, I. (2026). Less is more: Principled diversity in heterogeneous anomaly detection ensembles. *AI, 7*(6), 214. https://doi.org/10.3390/ai7060214

Kusumadewi, M. R., Aseri, A. F., & Seff, S. M. (2022). E-procurement in the procurement system for goods/services by the government in Indonesia: Perspective of saddu al-dhariah. *Ulul Albab: Jurnal Studi dan Penelitian Hukum Islam, 6*(1), 101–122. https://doi.org/10.30659/jua.v6i1.36682

Ma, M. Q., Zhao, Y., Zhang, X., & Akoglu, L. (2023). The need for unsupervised outlier model selection: A review and evaluation of internal model selection criteria. *ACM SIGKDD Explorations Newsletter, 25*(1), 19–35. https://doi.org/10.1145/3606274.3606277 `[PERLU VERIFIKASI: metadata versi jurnal; versi arXiv 2104.01422 sudah dicek]`

Muñoz-Cancino, R., & Ríos, S. A. (2025). Data-driven transparency: Machine learning and social network analysis for corruption detection in public procurement. *Procedia Computer Science, 270*, 1788–1795. https://doi.org/10.1016/j.procs.2025.09.299

Nai, R., Sulis, E., & Meo, R. (2022). Public procurement fraud detection and artificial intelligence techniques: A literature review. *Proceedings of the Knowledge Management for Law Workshop (KM4LAW 2022)*, CEUR Workshop Proceedings. `[PERLU LENGKAPI: nomor volume CEUR]`

Putri, A. R., Ningrum, C. D., Raihannisa, D., Damanik, I. L., Sinurat, N. B., Salsabilah, S., & Siregar, O. K. (2024). Identifikasi penyebab korupsi dalam prosedur pengadaan barang dan jasa pemerintah. *Economic Reviews Journal, 3*(2), 1234–1242. https://doi.org/10.56709/mrj.v3i2.383

Schneider dos Santos, E., Machado dos Santos, M., Castro, M., & Carvalho, J. T. (2025). Detection of fraud in public procurement using data-driven methods: A systematic mapping study. *EPJ Data Science, 14*, 52. https://doi.org/10.1140/epjds/s13688-025-00569-3

Sukawati, N. K. Y. T., & Rojali. (2026). Hybrid fraud detection for government financial transactions using Deep Isolation Forest and Extreme Gradient Boosting: A case study from an Indonesian government institution. *Ilomata International Journal of Tax and Accounting, 7*(3), 1–10. https://doi.org/10.61194/ijtc.v7i3.2600

Syaifudin, Sofwan, A., & Nugraheni, D. M. K. (2026). A comparative evaluation of machine learning models for anomaly detection in government e-procurement systems. *Engineering, Technology & Applied Science Research, 16*(5), 38885–38897. https://doi.org/10.48084/etasr.19310

Zulfikar, A., Rahmani, F. A., & Azizah, N. (2023). Deteksi anomali menggunakan Isolation Forest belanja barang persediaan konsumsi pada satuan kerja Kepolisian Republik Indonesia. *Jurnal Manajemen Perbendaharaan, 4*(1), 1–15. https://doi.org/10.33105/jmp.v4i1.435

---

## Catatan untuk Tio (di luar naskah)

1. **Contoh kelemahan "hanya pasangan RUP dan Realisasi" belum ketemu di jurnal mana pun.** Studi Indonesia yang saya temukan memakai data tender (Ambarsari), transaksi e-procurement (Syaifudin), atau transaksi belanja SAKTI (Zulfikar, Sukawati & Rojali). Jadi kelemahannya saya rumuskan sebagai "memakai data yang sudah berjalan, sehingga paket yang masih RUP tidak dinilai". Ini tetap mendukung jalur perencanaan kamu, tapi jujur terhadap isi jurnalnya.
2. **Ensemble di literatur lebih kuat sebagai argumen "stabil/robust", bukan "pasti lebih akurat".** Krčmar et al. (2026) menemukan ensemble selalu di peringkat atas tapi setara dengan Isolation Forest sendiri. Kalau dosen minta "lebih baik dari satu model", sebaiknya klaimnya "akan diuji" dan dibandingkan di Bab 4.
3. **Sitasi "(KPK, 2025)" di draf lama tidak ada di Daftar Pustaka.** Kalimat tentang rekomendasi sistem deteksi anomali e-katalog saya buang dulu dari draf ini. Kalau mau dipakai, perlu sumbernya.
4. **Semua sitasi di naskah berada di rentang 2021–2026.** Westerski et al. (2021) dan Antwarg et al. (2021) ada di batas bawah. Liu et al. (2008), paper asli Isolation Forest, sengaja tidak dipakai di Latar Belakang; taruh di Bab 2.
5. Poin "penjelasan struktur paper" pada gambar biasanya untuk artikel jurnal. Di skripsi, itu sudah tercakup oleh Sistematika Penulisan, jadi tidak saya masukkan ke Latar Belakang.
6. Angka LKPP dan DJPK saya ambil dari draf kamu dan belum saya cek ulang ke portalnya.
