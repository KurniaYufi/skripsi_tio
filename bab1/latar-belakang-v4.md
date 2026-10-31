# 1.1 Latar Belakang (Draf v4)

> Draf v4: paragraf awal sama dengan v2; bagian penelitian terdahulu ke bawah ditulis ulang. v2 dan v3 tetap disimpan sebagai cadangan. Catatan untuk Tio ada di bagian paling bawah, di luar naskah.

---

**[Informasi umum → permasalahan umum]**

Pengadaan barang/jasa pemerintah merupakan instrumen utama untuk memenuhi kebutuhan barang, pekerjaan konstruksi, dan jasa dalam pelaksanaan program pemerintahan. Berdasarkan data Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah (LKPP), nilai Rencana Umum Pengadaan (RUP) mencapai Rp859,27 triliun dari total belanja barang/jasa sebesar Rp929,01 triliun per 8 Juni 2026 (LKPP, 2026). Pada tingkat daerah, data Direktorat Jenderal Perimbangan Keuangan menunjukkan bahwa total belanja daerah tahun 2025 pada 546 pemerintah daerah mencapai Rp1.414,62 triliun, dengan alokasi belanja barang dan jasa sebesar Rp418,76 triliun (DJPK, 2026). Pelaksanaan pengadaan tersebut berlangsung melalui tahapan persiapan, pemilihan, dan pelaksanaan kontrak, sehingga kualitas pengadaan sangat ditentukan sejak tahap perencanaan (Kusumadewi et al., 2022).

Besarnya nilai anggaran tersebut juga menjadikan pengadaan sebagai sektor yang rawan penyimpangan. Kajian terhadap kasus korupsi pengadaan di Indonesia menunjukkan pola berulang berupa penggelembungan anggaran, pengadaan fiktif, dan nepotisme dalam pemberian kontrak (Adhi et al., 2025), yang berakar pada lemahnya aturan dan maladministrasi dalam proses pengadaan (Putri et al., 2024). Pada pemerintah daerah, Komisi Pemberantasan Korupsi (KPK) mengidentifikasi pola pemecahan paket dengan nilai mendekati ambang pengadaan langsung serta penyedia yang menangani banyak paket konstruksi secara bersamaan di Pemerintah Provinsi Kalimantan Timur, dan menegaskan bahwa pola tersebut memerlukan klarifikasi lebih lanjut (KPK, 2026). Analisis terhadap realisasi belanja daerah juga menemukan bahwa tingkat penyerapan yang tampak wajar secara agregat dapat menyembunyikan ketidaksesuaian pada kategori belanja tertentu (Hasmi et al., 2026). Di sisi lain, mekanisme pengawasan yang mengandalkan audit manual sulit mengimbangi volume dan kompleksitas data pengadaan (Muñoz-Cancino & Ríos, 2025). Kondisi ini menunjukkan perlunya cara yang dapat membantu pengawas menentukan paket mana yang perlu ditelusuri lebih dahulu.

**[Riset sebelumnya → solusi umum: machine learning dan ensemble]**

Penelitian deteksi kecurangan pengadaan berbasis data telah berkembang luas. Telaah sistematis terhadap 93 studi menunjukkan bahwa sebagian besar penelitian di bidang ini menggunakan model machine learning (Schneider dos Santos et al., 2025). Karena data pengadaan umumnya tidak memiliki label kasus yang terverifikasi, pendekatan unsupervised anomaly detection banyak digunakan untuk menyusun prioritas pemeriksaan, yaitu menandai paket yang polanya menyimpang dari paket sejenis tanpa langsung menyimpulkan adanya pelanggaran (Westerski et al., 2021).

Salah satu metode unsupervised yang telah diterapkan pada data pengadaan adalah Isolation Forest (Muñoz-Cancino & Ríos, 2025). Namun, penggunaan satu metode saja memiliki kelemahan karena setiap metode hanya peka terhadap jenis penyimpangan tertentu, sehingga tidak ada satu metode yang selalu unggul pada semua data (Han et al., 2022). Penggabungan beberapa metode dalam ensemble memberikan hasil yang lebih konsisten karena tidak bergantung pada satu model saja (Krčmar et al., 2026).

**[Penelitian terdahulu → permasalahan khusus / research problem]**

Di Indonesia, Isolation Forest telah digunakan untuk membantu pengawasan anggaran pemerintah, antara lain oleh Zulfikar et al. (2023) pada realisasi belanja persediaan satuan kerja Polri dan oleh Ambarsari et al. (2025) pada data tender pengadaan nasional. Kedua penelitian tersebut menunjukkan bahwa deteksi anomali dapat mendukung pengawasan, tetapi sama-sama bertumpu pada satu model dan belum menjelaskan alasan suatu data dianggap anomali. Keduanya juga menganalisis data dari tahap yang sudah berjalan, yaitu realisasi dan tender. Bahkan, pada penelitian Ambarsari et al. (2025), hasil analisis masih berupa bulan yang tidak wajar sehingga belum menunjukkan paket mana yang perlu diperiksa.

Di luar Indonesia, penggabungan beberapa metode deteksi anomali telah diterapkan untuk memprioritaskan transaksi pembelian yang perlu diaudit (Herreros-Martínez et al., 2025), dan alat bantu prioritas juga telah dikembangkan untuk lembaga pengawas pengadaan (Salazar et al., 2024). Namun, sejauh penelusuran yang dilakukan, pendekatan tersebut belum diterapkan pada pengadaan bersumber APBD pemerintah provinsi, terutama untuk menilai paket sejak tahap RUP. Padahal, data RUP tersedia secara terbuka melalui SiRUP dan Data INAPROC (LKPP, 2025a, 2025b), dan kualitas pengadaan sangat ditentukan sejak tahap perencanaan (Kusumadewi et al., 2022).

**[Kebutuhan penjelasan dan dashboard]**

Penjelasan atas hasil deteksi penting karena pengawas sulit menindaklanjuti skor anomali tanpa mengetahui alasannya. Westerski et al. (2021) menunjukkan bahwa deteksi anomali pengadaan baru dapat dipakai dalam praktik jika hasilnya dapat dijelaskan. Salah satu metode penjelasan yang dapat digunakan adalah SHapley Additive exPlanations (SHAP), yang mampu menunjukkan fitur yang paling memengaruhi skor anomali, termasuk pada model Autoencoder (Antwarg et al., 2021).

Selain dapat dijelaskan, hasil deteksi juga perlu mudah diakses oleh pengguna. Dari 93 studi yang ditelaah, hanya dua yang benar-benar diterapkan dalam sistem yang dipakai lembaga pengawas (Schneider dos Santos et al., 2025). VigIA menunjukkan bahwa alat yang dirancang untuk pengguna dapat membantu pengawas membandingkan risiko antarinstansi dan antarwilayah (Salazar et al., 2024). Oleh karena itu, hasil penelitian ini disajikan dalam dashboard agar pengawas dapat melihat sebaran hasil antarprovinsi, lalu menelusuri paket prioritas beserta penjelasannya. Perbandingan antarprovinsi memakai ukuran relatif, seperti proporsi paket berskor tinggi, agar provinsi dengan jumlah paket besar tidak otomatis terlihat paling berisiko.

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
