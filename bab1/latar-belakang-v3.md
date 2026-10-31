# 1.1 Latar Belakang (Draf v3)

> Revisi dari v2 (v2 tetap disimpan di `latar-belakang-v2.md` sebagai cadangan). Perubahan: bahasa dipadatkan, penelitian terdahulu dibatasi 4 studi dengan analisis gap, dan ditambah bahasan dashboard.

---

Pengadaan barang/jasa pemerintah merupakan instrumen utama dalam memenuhi kebutuhan barang, pekerjaan konstruksi, dan jasa untuk program pemerintahan. Nilai Rencana Umum Pengadaan (RUP) nasional mencapai Rp859,27 triliun dari total belanja barang/jasa sebesar Rp929,01 triliun per 8 Juni 2026 (LKPP, 2026). Pada tingkat daerah, belanja barang dan jasa dari 546 pemerintah daerah tahun 2025 mencapai Rp418,76 triliun dari total belanja daerah Rp1.414,62 triliun (DJPK, 2026).

Besarnya anggaran tersebut menjadikan pengadaan rawan penyimpangan. Korupsi pengadaan di Indonesia berakar pada lemahnya aturan dan maladministrasi dalam prosesnya (Putri et al., 2024). Pada Pemerintah Provinsi Kalimantan Timur, misalnya, KPK menemukan pemecahan paket dengan nilai mendekati ambang pengadaan langsung serta penyedia yang menangani banyak paket konstruksi secara bersamaan (KPK, 2026). Namun, pengawasan yang mengandalkan audit manual sulit mengimbangi volume dan kompleksitas data pengadaan (Muñoz-Cancino & Ríos, 2025). Oleh karena itu, pengawas membutuhkan cara untuk menentukan paket mana yang perlu ditelusuri lebih dahulu.

Machine learning menjadi pendekatan yang paling banyak digunakan untuk kebutuhan tersebut. Telaah sistematis terhadap 93 studi menunjukkan bahwa sebagian besar penelitian deteksi kecurangan pengadaan publik memakai model machine learning (Schneider dos Santos et al., 2025). Karena data pengadaan umumnya tidak memiliki label kasus yang terverifikasi, pendekatan unsupervised anomaly detection digunakan untuk menandai pola yang menyimpang dari paket sejenis, dan Isolation Forest merupakan salah satu metode yang telah diterapkan pada data pengadaan publik (Muñoz-Cancino & Ríos, 2025). Meski demikian, setiap metode memiliki asumsi tersendiri tentang bentuk anomali, dan pengujian pada 57 dataset menunjukkan tidak ada satu metode yang unggul secara konsisten (Han et al., 2022). Temuan ini membuka peluang penggunaan ensemble, yaitu penggabungan beberapa model agar hasil tidak bergantung pada satu model yang kinerjanya tidak dapat diverifikasi tanpa label.

Beberapa penelitian terdahulu menunjukkan kemajuan sekaligus keterbatasan pendekatan tersebut. Zulfikar et al. (2023) menerapkan Isolation Forest pada transaksi belanja persediaan satuan kerja Polri, tetapi hanya menggunakan satu model, menilai transaksi yang sudah terealisasi, dan tidak menyertakan penjelasan atas hasil deteksi. Ambarsari et al. (2025) menerapkan Isolation Forest pada data tender pengadaan nasional, tetapi analisisnya dilakukan pada agregat bulanan sehingga belum menghasilkan prioritas per paket dan belum memakai metode penjelasan. Herreros-Martínez et al. (2025) telah menggabungkan beberapa metode deteksi anomali dan menggunakan SHAP untuk memprioritaskan transaksi yang perlu diaudit, tetapi penerapannya pada data pembelian perusahaan, bukan pengadaan pemerintah. Sementara itu, Salazar et al. (2024) mengembangkan VigIA, alat bantu pengawas pengadaan di Kolombia yang memprioritaskan kontrak berisiko, tetapi modelnya bersifat supervised dan membutuhkan variabel target dari kontrak yang telah selesai dilaksanakan.

Dari keempat penelitian tersebut terlihat tiga kesenjangan. Pertama, kedua penelitian di Indonesia masih menggunakan satu model. Kedua, analisis dilakukan pada data yang sudah berjalan, yaitu tender, transaksi, atau kontrak, sehingga paket yang masih berupa RUP dan belum memiliki realisasi tidak ikut dinilai. Ketiga, kedua penelitian di Indonesia tersebut belum menyertakan penjelasan berbasis explainable AI (XAI), sedangkan penelitian yang sudah memakai SHAP belum diterapkan pada pengadaan pemerintah. Padahal, skor anomali tanpa alasan sulit ditindaklanjuti oleh pengawas.

Selain kesenjangan metode, hasil deteksi juga jarang sampai ke tangan pengguna. Dari 93 studi yang ditelaah, hanya dua yang menerapkan metodenya dalam sistem yang digunakan lembaga pengawas (Schneider dos Santos et al., 2025). VigIA menunjukkan bahwa alat yang dirancang untuk pengguna dapat membantu pengawas membandingkan risiko antarinstansi dan antarwilayah serta menentukan alokasi sumber daya pemeriksaan (Salazar et al., 2024). Oleh karena itu, hasil deteksi perlu disajikan dalam dashboard yang memungkinkan pengawas melihat sebaran hasil antarprovinsi, lalu menelusuri paket prioritas beserta alasannya.

Berdasarkan kesenjangan tersebut, tugas akhir ini mengembangkan deteksi anomali anggaran pengadaan barang/jasa bersumber APBD pemerintah provinsi di seluruh Indonesia menggunakan ensemble unsupervised learning dan XAI. Analisis dilakukan melalui dua jalur: jalur perencanaan yang menilai seluruh paket berdasarkan data RUP, dan jalur pelaksanaan yang menilai paket dengan pasangan data RUP dan realisasi. Ensemble disusun dari Isolation Forest, Local Outlier Factor (LOF), dan Autoencoder yang menilai ketidaklaziman melalui prinsip berbeda, yaitu isolasi, kepadatan lokal, dan galat rekonstruksi. SHAP digunakan untuk menjelaskan kontribusi fitur pada paket prioritas. Karena tidak ada label acuan, manfaat ensemble akan diuji melalui perbandingan dengan model individual dan pemeringkatan berdasarkan pagu, serta melalui stabilitas peringkat. Hasilnya disajikan dalam dashboard berisi peta sebaran antarprovinsi dan rincian paket beserta penjelasannya.

Hasil tugas akhir ini diharapkan menjadi bahan pendukung bagi pengawas dalam menentukan urutan penelusuran paket pengadaan APBD sejak tahap perencanaan hingga pelaksanaan. Skor anomali menunjukkan ketidaklaziman statistik, bukan bukti pelanggaran, sehingga tetap memerlukan verifikasi lebih lanjut.

---

## Daftar Pustaka (yang dipakai di v3)

Ambarsari, E. W., Desyanti, & Fathudin, D. (2025). Hybrid Chaos-Isolation Forest framework for anomaly detection in Indonesia's public procurement. *Bulletin of Informatics and Data Science, 4*(2), 114–123. https://doi.org/10.61944/bids.v4i2.137

Direktorat Jenderal Perimbangan Keuangan [DJPK]. (2026). *Postur APBD nasional tahun 2025* [Portal data SIKD]. Kementerian Keuangan Republik Indonesia. https://djpk.kemenkeu.go.id/portal/data/apbd?p=&periode=12&tahun=2025

Han, S., Hu, X., Huang, H., Jiang, M., & Zhao, Y. (2022). ADBench: Anomaly detection benchmark. *Advances in Neural Information Processing Systems, 35*, 32142–32159.

Herreros-Martínez, A., Magdalena-Benedicto, R., Vila-Francés, J., Serrano-López, A. J., Pérez-Díaz, S., & Martínez-Herráiz, J. J. (2025). Applied machine learning to anomaly detection in enterprise purchase processes: A hybrid approach using clustering and Isolation Forest. *Information, 16*(3), 177. https://doi.org/10.3390/info16030177

Komisi Pemberantasan Korupsi [KPK]. (2026, 23 September). *PBJ Pemprov Kaltim capai Rp566 miliar, KPK petakan celah dan anomali tata kelola daerah*. https://www.kpk.go.id/id/ruang-informasi/berita/pbj-pemrpov-kaltim-capai-rp566-miliar-kpk-petakan-celah-dan-anomali-tata-kelola-daerah

Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah [LKPP]. (2026, 17 Juni). *LKPP perkuat pengadaan pemerintah sebagai instrumen strategis pendukung program prioritas nasional*. https://www.lkpp.go.id/read/bu/lkpp-perkuat-pengadaan-pemerintah-sebagai-instrumen-strategis-pendukung-program-prioritas-nasional

Muñoz-Cancino, R., & Ríos, S. A. (2025). Data-driven transparency: Machine learning and social network analysis for corruption detection in public procurement. *Procedia Computer Science, 270*, 1788–1795. https://doi.org/10.1016/j.procs.2025.09.299

Putri, A. R., Ningrum, C. D., Raihannisa, D., Damanik, I. L., Sinurat, N. B., Salsabilah, S., & Siregar, O. K. (2024). Identifikasi penyebab korupsi dalam prosedur pengadaan barang dan jasa pemerintah. *Economic Reviews Journal, 3*(2), 1234–1242. https://doi.org/10.56709/mrj.v3i2.383

Salazar, A., Pérez, J. F., & Gallego, J. (2024). VigIA: Prioritizing public procurement oversight with machine learning models and risk indices. *Data & Policy, 6*, e75. https://doi.org/10.1017/dap.2024.83

Schneider dos Santos, E., Machado dos Santos, M., Castro, M., & Carvalho, J. T. (2025). Detection of fraud in public procurement using data-driven methods: A systematic mapping study. *EPJ Data Science, 14*, 52. https://doi.org/10.1140/epjds/s13688-025-00569-3

Zulfikar, A., Rahmani, F. A., & Azizah, N. (2023). Deteksi anomali menggunakan Isolation Forest belanja barang persediaan konsumsi pada satuan kerja Kepolisian Republik Indonesia. *Jurnal Manajemen Perbendaharaan, 4*(1), 1–15. https://doi.org/10.33105/jmp.v4i1.435

---

## Catatan untuk Tio (di luar naskah)

- Ketiga kesenjangan berlaku sebatas penelitian yang dibahas dan penelusuran yang saya lakukan. Hindari menulis "belum pernah diteliti".
- Westerski (2021), Antwarg (2021), dan sumber LKPP 2025 tidak dipakai lagi di v3 agar referensi lebih ramping. Mereka bisa dipindah ke Bab 2.
