# 1.1 Latar Belakang (Draf v4)

> Draf v4: paragraf awal sama dengan v2; bagian penelitian terdahulu ke bawah ditulis ulang. v2 dan v3 tetap disimpan sebagai cadangan. Catatan untuk Tio ada di bagian paling bawah, di luar naskah.

---

**[Informasi umum → permasalahan umum]**

Pengadaan barang/jasa pemerintah merupakan instrumen utama untuk memenuhi kebutuhan barang, pekerjaan konstruksi, dan jasa dalam pelaksanaan program pemerintahan. Berdasarkan data Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah (LKPP), nilai Rencana Umum Pengadaan (RUP) mencapai Rp859,27 triliun dari total belanja barang/jasa sebesar Rp929,01 triliun per 8 Juni 2026 (LKPP, 2026). Pada tingkat daerah, data Direktorat Jenderal Perimbangan Keuangan menunjukkan bahwa total belanja daerah tahun 2025 pada 546 pemerintah daerah mencapai Rp1.414,62 triliun, dengan alokasi belanja barang dan jasa sebesar Rp418,76 triliun (DJPK, 2026). Pelaksanaan pengadaan tersebut berlangsung melalui tahapan persiapan, pemilihan, dan pelaksanaan kontrak, sehingga kualitas pengadaan sangat ditentukan sejak tahap perencanaan (Kusumadewi et al., 2022).

Besarnya nilai anggaran tersebut juga menjadikan pengadaan sebagai sektor yang rawan penyimpangan. Kajian terhadap kasus korupsi pengadaan di Indonesia menunjukkan pola berulang berupa penggelembungan anggaran, pengadaan fiktif, dan nepotisme dalam pemberian kontrak (Adhi et al., 2025), yang berakar pada lemahnya aturan dan maladministrasi dalam proses pengadaan (Putri et al., 2024). Pada pemerintah daerah, Komisi Pemberantasan Korupsi (KPK) mengidentifikasi pola pemecahan paket dengan nilai mendekati ambang pengadaan langsung serta penyedia yang menangani banyak paket konstruksi secara bersamaan di Pemerintah Provinsi Kalimantan Timur, dan menegaskan bahwa pola tersebut memerlukan klarifikasi lebih lanjut (KPK, 2026). Analisis terhadap realisasi belanja daerah juga menemukan bahwa tingkat penyerapan yang tampak wajar secara agregat dapat menyembunyikan ketidaksesuaian pada kategori belanja tertentu (Hasmi et al., 2026). Di sisi lain, mekanisme pengawasan yang mengandalkan audit manual sulit mengimbangi volume dan kompleksitas data pengadaan (Muñoz-Cancino & Ríos, 2025). Kondisi ini menunjukkan perlunya cara yang dapat membantu pengawas menentukan paket mana yang perlu ditelusuri lebih dahulu.

**[Riset sebelumnya → solusi umum: machine learning dan ensemble]**

Penelitian deteksi kecurangan pengadaan berbasis data telah berkembang luas. Telaah sistematis terhadap 93 studi menunjukkan bahwa sebagian besar penelitian di bidang ini menggunakan model machine learning (Schneider dos Santos et al., 2025). Karena data pengadaan umumnya tidak memiliki label kasus yang terverifikasi, pendekatan unsupervised anomaly detection banyak digunakan untuk menyusun prioritas pemeriksaan, yaitu menandai paket yang polanya menyimpang dari paket sejenis tanpa langsung menyimpulkan adanya pelanggaran (Westerski et al., 2021).

Isolation Forest merupakan salah satu metode unsupervised yang telah diterapkan pada data pengadaan publik, misalnya untuk mengidentifikasi penyedia dengan pola relasi tidak lazim di Chile (Muñoz-Cancino & Ríos, 2025). Namun, setiap metode deteksi anomali memiliki asumsi tersendiri mengenai bentuk penyimpangan. Pengujian terhadap 57 dataset menunjukkan bahwa tidak ada satu metode yang unggul secara konsisten pada semua tipe anomali (Han et al., 2022), sementara tanpa label, model terbaik juga tidak dapat dipilih secara andal (Ma et al., 2023). Penggabungan beberapa model dalam ensemble menjadi cara untuk mengurangi risiko tersebut. Krčmar et al. (2026) menemukan bahwa ensemble heterogen konsisten berada di peringkat teratas pada 22 dataset acuan dan mengungguli detektor individual yang lebih lemah, meskipun hasilnya setara dengan detektor tunggal terbaik. Dengan demikian, keunggulan utama ensemble pada data tanpa label adalah kestabilan hasil, bukan jaminan akurasi yang lebih tinggi.

**[Penelitian terdahulu → permasalahan khusus / research problem]**

Beberapa penelitian terdahulu yang paling dekat dengan topik ini menunjukkan kemajuan sekaligus keterbatasan. Zulfikar et al. (2023) menerapkan Isolation Forest pada data realisasi belanja persediaan bulanan seluruh satuan kerja Polri tahun 2019–2021. Penelitian ini menunjukkan bahwa deteksi anomali dapat mendukung pengawasan belanja pemerintah, tetapi hanya menggunakan satu model, menilai belanja yang sudah terealisasi, dan tidak menjelaskan alasan suatu data ditandai sebagai anomali. Ambarsari et al. (2025) menerapkan Isolation Forest dengan fitur berbasis teori chaos pada 447.878 data tender pengadaan nasional. Namun, data dianalisis dalam bentuk agregat bulanan sehingga hasilnya menunjukkan bulan yang tidak lazim, bukan paket yang perlu diperiksa, dan penulis menyarankan analisis per tender sebagai pengembangan.

Dua penelitian lain menunjukkan arah yang dapat melengkapi keterbatasan tersebut. Herreros-Martínez et al. (2025) menggabungkan beberapa metode deteksi anomali, termasuk Isolation Forest, ke dalam satu kerangka prioritas dan menggunakan SHAP agar auditor dapat memahami alasan setiap transaksi diprioritaskan. Namun, penerapannya pada data pembelian perusahaan, bukan pengadaan pemerintah. Salazar et al. (2024) mengembangkan VigIA, alat bantu bagi lembaga pengawas pengadaan di Kolombia untuk memprioritaskan kontrak berisiko. Meskipun demikian, model VigIA bersifat supervised dan membutuhkan variabel target berupa pembengkakan biaya atau keterlambatan dari kontrak yang telah selesai, sehingga penilaian baru dapat dilakukan setelah kontrak ditandatangani.

Dari keempat penelitian tersebut terdapat tiga kesenjangan yang relevan dengan pengadaan bersumber APBD pemerintah provinsi. Pertama, penelitian di Indonesia masih menggunakan satu model, padahal kinerja satu model sulit diverifikasi tanpa label. Kedua, analisis dilakukan pada data yang sudah berjalan, yaitu realisasi belanja, tender, atau kontrak, sehingga paket yang masih berupa RUP dan belum memiliki realisasi tidak ikut dinilai. Padahal, data RUP tersedia secara terbuka melalui SiRUP dan portal Data INAPROC (LKPP, 2025a, 2025b), dan kualitas pengadaan sangat ditentukan sejak tahap perencanaan (Kusumadewi et al., 2022). Ketiga, penjelasan berbasis explainable AI (XAI) sudah digunakan pada data pembelian, tetapi belum menyertai penelitian deteksi anomali pengadaan di Indonesia yang ditemukan dalam penelusuran ini.

**[Kebutuhan penjelasan dan dashboard]**

Penjelasan diperlukan karena skor anomali tanpa alasan sulit ditindaklanjuti oleh pengawas. Westerski et al. (2021) menunjukkan bahwa penjelasan hasil merupakan syarat agar deteksi anomali pengadaan dapat digunakan dalam praktik, dan Antwarg et al. (2021) menunjukkan bahwa SHapley Additive exPlanations (SHAP) dapat mengungkap fitur yang berkontribusi terhadap anomali yang dideteksi Autoencoder.

Selain dijelaskan, hasil deteksi juga perlu sampai ke tangan pengguna. Dari 93 studi yang ditelaah Schneider dos Santos et al. (2025), hanya dua yang menerapkan metodenya dalam sistem yang digunakan lembaga pengawas. VigIA menunjukkan bahwa alat yang dirancang untuk pengguna dapat membantu pengawas membandingkan risiko antarinstansi dan antarwilayah serta menentukan alokasi sumber daya pemeriksaan (Salazar et al., 2024). Oleh karena itu, hasil deteksi dalam penelitian ini perlu disajikan melalui dashboard yang memungkinkan pengawas melihat sebaran hasil antarprovinsi, lalu menelusuri paket prioritas beserta penjelasannya. Perbandingan antarwilayah menggunakan ukuran relatif, seperti proporsi paket berskor tinggi, agar provinsi dengan jumlah paket besar tidak otomatis tampak paling berisiko.

**[Kontribusi / usulan → solusi khusus dan ringkasan metode]**

Berdasarkan kesenjangan tersebut, tugas akhir ini mengusulkan deteksi anomali anggaran pengadaan barang/jasa bersumber APBD pemerintah provinsi di seluruh Indonesia dengan pendekatan ensemble unsupervised learning dan XAI. Analisis dilakukan melalui dua jalur: jalur perencanaan yang menilai seluruh paket berdasarkan data RUP, dan jalur pelaksanaan yang menilai paket dengan pasangan data RUP dan realisasi. Ensemble disusun dari Isolation Forest, Local Outlier Factor (LOF), dan Autoencoder, yang masing-masing menilai ketidaklaziman melalui isolasi observasi, kepadatan lokal, dan galat rekonstruksi. Skor ketiga model digabungkan menjadi skor prioritas, lalu SHAP digunakan untuk menjelaskan kontribusi fitur pada paket dengan skor tertinggi. Karena tidak ada label acuan, manfaat ensemble akan diuji melalui perbandingan dengan model individual dan pemeringkatan berdasarkan pagu, pengujian stabilitas peringkat, serta telaah sampel paket prioritas. Hasilnya disajikan dalam dashboard berisi peta sebaran antarprovinsi dan rincian paket beserta penjelasannya.

**[Harapan]**

Hasil tugas akhir ini diharapkan menjadi bahan pendukung bagi pengawas dalam menentukan urutan penelusuran paket pengadaan bersumber APBD sejak tahap perencanaan hingga pelaksanaan. Skor anomali menunjukkan ketidaklaziman statistik, bukan bukti pelanggaran, sehingga tetap memerlukan klarifikasi dan verifikasi lebih lanjut.

---

## Daftar Pustaka (yang dipakai di v4)

Adhi, S., Arifin, R., & Sani, T. (2025). From administrative irregularities to criminal acts: Uncovering corruption in state procurement systems. *PAMPAS: Journal of Criminal Law, 6*(2). `[PERLU LENGKAPI: halaman dan DOI]`

Ambarsari, E. W., Desyanti, & Fathudin, D. (2025). Hybrid Chaos-Isolation Forest framework for anomaly detection in Indonesia's public procurement. *Bulletin of Informatics and Data Science, 4*(2), 114–123. https://doi.org/10.61944/bids.v4i2.137

Antwarg, L., Miller, R. M., Shapira, B., & Rokach, L. (2021). Explaining anomalies detected by autoencoders using Shapley Additive Explanations. *Expert Systems with Applications, 186*, 115736. https://doi.org/10.1016/j.eswa.2021.115736

Direktorat Jenderal Perimbangan Keuangan [DJPK]. (2026). *Postur APBD nasional tahun 2025* [Portal data SIKD]. Kementerian Keuangan Republik Indonesia. https://djpk.kemenkeu.go.id/portal/data/apbd?p=&periode=12&tahun=2025

Han, S., Hu, X., Huang, H., Jiang, M., & Zhao, Y. (2022). ADBench: Anomaly detection benchmark. *Advances in Neural Information Processing Systems, 35*, 32142–32159.

Hasmi, M., Darmawan, K. A. A.-A., Salsabilah, N. M., Fadilah, A., & Hasnita, N. (2026). Analisis tren belanja daerah sebagai indikasi risiko fraud di Pemerintah Kota Kendari. *Jurnal IAKP: Jurnal Inovasi Akuntansi Keuangan & Perpajakan, 7*(1), 72–84.

Herreros-Martínez, A., Magdalena-Benedicto, R., Vila-Francés, J., Serrano-López, A. J., Pérez-Díaz, S., & Martínez-Herráiz, J. J. (2025). Applied machine learning to anomaly detection in enterprise purchase processes: A hybrid approach using clustering and Isolation Forest. *Information, 16*(3), 177. https://doi.org/10.3390/info16030177

Komisi Pemberantasan Korupsi [KPK]. (2026, 23 September). *PBJ Pemprov Kaltim capai Rp566 miliar, KPK petakan celah dan anomali tata kelola daerah*. https://www.kpk.go.id/id/ruang-informasi/berita/pbj-pemrpov-kaltim-capai-rp566-miliar-kpk-petakan-celah-dan-anomali-tata-kelola-daerah

Krčmar, T., Šabanović, D., Köhler, M., & Lukić, I. (2026). Less is more: Principled diversity in heterogeneous anomaly detection ensembles. *AI, 7*(6), 214. https://doi.org/10.3390/ai7060214

Kusumadewi, M. R., Aseri, A. F., & Seff, S. M. (2022). E-procurement in the procurement system for goods/services by the government in Indonesia: Perspective of saddu al-dhariah. *Ulul Albab: Jurnal Studi dan Penelitian Hukum Islam, 6*(1), 101–122. https://doi.org/10.30659/jua.v6i1.36682

Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah [LKPP]. (2025a, 14 Januari). *Isi SiRUP untuk transparansi pengadaan yang lebih baik* (Siaran Pers Nomor 1/SP-Ses.3/1/2025). https://www.lkpp.go.id/read/s/isi-sirup-untuk-transparansi-pengadaan-yang-lebih-baik

Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah [LKPP]. (2025b). *Profil Pengadaan Monitoring*. PPID LKPP. https://ppid.lkpp.go.id/information/public/566/profil-pengadaan-monitoring

Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah [LKPP]. (2026, 17 Juni). *LKPP perkuat pengadaan pemerintah sebagai instrumen strategis pendukung program prioritas nasional*. https://www.lkpp.go.id/read/bu/lkpp-perkuat-pengadaan-pemerintah-sebagai-instrumen-strategis-pendukung-program-prioritas-nasional

Ma, M. Q., Zhao, Y., Zhang, X., & Akoglu, L. (2023). The need for unsupervised outlier model selection: A review and evaluation of internal model selection criteria. *ACM SIGKDD Explorations Newsletter, 25*(1), 19–35. https://doi.org/10.1145/3606274.3606277 `[PERLU VERIFIKASI: metadata versi jurnal]`

Muñoz-Cancino, R., & Ríos, S. A. (2025). Data-driven transparency: Machine learning and social network analysis for corruption detection in public procurement. *Procedia Computer Science, 270*, 1788–1795. https://doi.org/10.1016/j.procs.2025.09.299

Putri, A. R., Ningrum, C. D., Raihannisa, D., Damanik, I. L., Sinurat, N. B., Salsabilah, S., & Siregar, O. K. (2024). Identifikasi penyebab korupsi dalam prosedur pengadaan barang dan jasa pemerintah. *Economic Reviews Journal, 3*(2), 1234–1242. https://doi.org/10.56709/mrj.v3i2.383

Salazar, A., Pérez, J. F., & Gallego, J. (2024). VigIA: Prioritizing public procurement oversight with machine learning models and risk indices. *Data & Policy, 6*, e75. https://doi.org/10.1017/dap.2024.83

Schneider dos Santos, E., Machado dos Santos, M., Castro, M., & Carvalho, J. T. (2025). Detection of fraud in public procurement using data-driven methods: A systematic mapping study. *EPJ Data Science, 14*, 52. https://doi.org/10.1140/epjds/s13688-025-00569-3

Westerski, A., Kanagasabai, R., Shaham, E., Narayanan, A., Wong, J., & Singh, M. (2021). Explainable anomaly detection for procurement fraud identification—lessons from practical deployments. *International Transactions in Operational Research, 28*(6), 3276–3302. https://doi.org/10.1111/itor.12968

Zulfikar, A., Rahmani, F. A., & Azizah, N. (2023). Deteksi anomali menggunakan Isolation Forest belanja barang persediaan konsumsi pada satuan kerja Kepolisian Republik Indonesia. *Jurnal Manajemen Perbendaharaan, 4*(1), 1–15. https://doi.org/10.33105/jmp.v4i1.435

---

## Catatan untuk Tio (di luar naskah)

- Penelitian terdahulu yang dianalisis mendalam sekarang 4 studi (Zulfikar, Ambarsari, Herreros-Martínez, VigIA), masing-masing dengan kontribusi dan kekurangannya. Sitasi lain di paragraf ML dan ensemble berfungsi sebagai dasar argumen, bukan penelitian terdahulu yang dibandingkan.
- Kesenjangan berlaku sebatas penelitian yang dibahas dan penelusuran yang dilakukan. Hindari menulis "belum pernah diteliti".
- Sitasi "(KPK, 2025)" dari draf lama tetap tidak dipakai karena sumbernya belum ada di Daftar Pustaka.
- Angka LKPP dan DJPK diambil dari draf awal Tio dan belum dicek ulang ke portalnya.
