# Referensi Precision@K untuk Bab 2.2 Metrik Evaluasi

Dicari 2026-10-29. Semua sumber di bawah **gratis** (open access, arXiv, atau buku daring berlisensi CC) dan terbit 2022-2026. Isi tiap sumber sudah dibaca langsung, bukan dari abstrak saja.

## Hasil cek PDF yang sudah ada di Library

Tidak ada PDF di Library yang mendefinisikan Precision@K.

- **ADBench (Han et al., 2022)** hanya memakai AUCROC dan AUCPR, jadi tidak bisa dijadikan sumber Precision@K.
- **Schiavon et al. (2026)** juga tidak memakai Precision@K, tetapi berguna untuk bagian "validasi dengan acuan pengganti" (lihat nomor 4).

## Ringkasan per paper

### 1. Le Borgne et al. (2022): buku saku *fraud detection* ULB

- **Yang dijelaskan:** Precision@K paling jelas dijelaskan di sini. Nilai K = jumlah *alert* yang sanggup diperiksa petugas dalam satu hari. Precision@K = berapa bagian dari K kasus teratas yang memang terbukti bermasalah. Alasannya praktis: petugas sedikit dan pemeriksaan lambat, jadi yang penting adalah ketepatan daftar teratas, bukan seluruh data.
- **Link gratis:** https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_4_PerformanceMetrics/TopKBased.html (teks berlisensi CC BY-SA 4.0)
- **Rumus (Bab 4.4):** P@k(d) = |A_d^Fraud| / |A_d| = |A_d^Fraud| / k, dengan A_d = himpunan k *alert* pada hari d.
- **Kutipan:** "The k parameter quantifies the maximum number of alerts that can be checked by investigators in a day." / "The number of alerts that may be checked during a given period is therefore necessarily limited."
- **Cocok untuk:** alasan memilih Precision@K (kapasitas pemeriksa terbatas), lalu dianalogikan ke APIP/pengawas pengadaan.

### 2. Škvára, Pevný, & Šmídl (2023): "Is AUC the best measure…?"

- **Yang dijelaskan:** Paper ini membandingkan AUC dengan metrik yang dipakai praktisi. Menurut penulisnya, AUC bisa menyesatkan karena merata-ratakan semua ambang, padahal praktisi hanya sempat memeriksa K kasus teratas. Precision@p dirumuskan sebagai proporsi anomali asli di antara p% sampel paling anomali.
- **Link gratis:** https://arxiv.org/abs/2305.04754
- **Rumus (Pers. 4):** precision@p = |{x ∈ X_p ∧ label x positif}| / |X_p|, dengan X_p = p% sampel dengan skor anomali tertinggi.
- **Kutipan:** "precision@k is popular … since the security officer can investigate at most k-most anomalous samples a day" dan "AUC may be misleading since it is an integral over all possible thresholds".
- **Kelemahan yang disebut:** nilainya sulit dibandingkan antar-dataset karena bergantung pada proporsi anomali. Ini bisa dipakai untuk menjelaskan kenapa perlu pembanding acak (*baseline*).
- **Catatan:** statusnya masih preprint arXiv (belum terbit di jurnal). Isinya bisa dibuka gratis.

### 3. Dağıdır, Hubert, & Rousseeuw (2025): "Kernel outlier detection"

- **Yang dijelaskan:** Paper ini memakai P@N untuk mengevaluasi metode deteksi pencilan. Alasannya, banyak metode hanya menghasilkan peringkat tanpa ambang batas, sehingga P@N cocok karena tidak membutuhkan ambang. Alasan ini sama dengan kondisi ensemble skor IF+LOF+AE.
- **Link gratis:** https://doi.org/10.52933/jdssv.v5i8.152 (PDF: https://jdssv.org/index.php/jdssv/article/view/152/78, CC BY 4.0)
- **Rumus (Pers. 14):** P@N = (jumlah pencilan sebenarnya di antara N nilai skor tertinggi) / N
- **Kutipan (Subbab 4.2):** P@N "circumvents the need for a threshold, by focusing on the proportion of true outliers among the N top ranked cases."
- **Cocok untuk:** sumber jurnal (bukan preprint) untuk rumus Precision@K di Bab 2.2.

### 4. Schiavon, Castro, & Carvalho (2026): ensemble anomali belanja DPR Brasil (sudah ada di Library)

- **Yang dijelaskan:** Paper ini tidak membahas Precision@K. Isinya relevan karena memakai ensemble tanpa label di data publik, lalu memvalidasi hasilnya dengan **acuan pengganti** (*proxy validation*), yaitu temuan audit LSM OPS. Penulis mengakui bahwa tanpa *ground truth*, presisi sebenarnya tidak bisa dihitung.
- **Link gratis:** https://doi.org/10.1007/s41060-026-01079-9 (open access)
- **Kutipan (hlm. 12-13):** "ground-truth labels exceedingly rare. To address this limitation, we adopt a proxy validation strategy" dan "Without an internal ground truth, we cannot estimate real-world precision."
- **Cocok untuk:** dasar memakai red flag sebagai acuan pengganti, sekaligus kalimat keterbatasan.

### 5. Medina-Hernández, Kertész, & Fazekas (2025): pemasok yang dikenai sanksi di Meksiko

- **Yang dijelaskan:** Paper ini memakai daftar pemasok yang dikenai sanksi sebagai label positif yang **tidak lengkap**. Paket yang tidak berlabel tidak otomatis dianggap bersih (*positive-unlabeled*). Karena itu, peringkat dievaluasi dengan kurva kumulatif dan **lift@k**, yaitu jumlah positif di K teratas dibandingkan dengan tebakan acak: Lift(k) = CR(k) / (π·k), dengan π = proporsi positif di seluruh data.
- **Link gratis:** https://arxiv.org/abs/2512.19491 (preprint)
- **Kutipan:** "Using sanctions as positive labels implies the lack of true negative examples."
- **Cocok untuk:** menjelaskan bahwa red flag adalah acuan yang tidak lengkap. Paket tanpa red flag belum tentu wajar, sehingga Precision@K dibaca relatif terhadap pembanding acak.

## Draf kalimat untuk Bab 2.2 (Metrik Evaluasi)

> Precision@K mengukur seberapa tepat daftar peringkat teratas yang dihasilkan model. Nilai K menyatakan jumlah paket teratas yang diperiksa. Pemilihan K mencerminkan kapasitas pemeriksa yang terbatas, karena pengawas hanya sanggup menelaah sebagian kecil paket dalam satu periode (Le Borgne et al., 2022; Škvára et al., 2023). Metrik ini tidak membutuhkan ambang batas skor, sehingga sesuai untuk model yang hanya menghasilkan peringkat (Dağıdır et al., 2025). Precision@K dihitung dengan Persamaan (2.x).
>
> Precision@K = (jumlah paket ber-red flag di antara K paket dengan skor tertinggi) / K
>
> Data pengadaan tidak memiliki label anomali yang pasti. Karena itu, red flag pengadaan dipakai sebagai acuan pengganti (*proxy*), seperti pada penelitian yang memvalidasi model tanpa label dengan temuan audit (Schiavon et al., 2026). Acuan ini tidak lengkap, sebab paket tanpa red flag belum tentu wajar (Medina-Hernández et al., 2025). Nilai Precision@K kemudian dibandingkan dengan proporsi paket ber-red flag di seluruh data, yaitu nilai yang diharapkan bila paket dipilih secara acak.

Catatan: ganti "2.x" dengan nomor persamaan di tab Bab 2 v.4 / Bab 1-3 (LLM). Definisi "ber-red flag" (minimal satu red flag atau ambang lain) ikut keputusan red flag v3/v5.

## Daftar Pustaka (APA 7)

Dağıdır, C. H., Hubert, M., & Rousseeuw, P. J. (2025). Kernel outlier detection. *Journal of Data Science, Statistics, and Visualisation, 5*(8). https://doi.org/10.52933/jdssv.v5i8.152

Le Borgne, Y.-A., Siblini, W., Lebichot, B., & Bontempi, G. (2022). *Reproducible machine learning for credit card fraud detection: Practical handbook*. Université Libre de Bruxelles. https://github.com/Fraud-Detection-Handbook/fraud-detection-handbook

Medina-Hernández, M., Kertész, J., & Fazekas, M. (2025). *Learning from sanctioned government suppliers: A machine learning and network science approach to detecting fraud and corruption in Mexico* (arXiv:2512.19491). arXiv. https://doi.org/10.48550/arXiv.2512.19491

Schiavon, J. P., Castro, M., & Carvalho, J. T. (2026). Ensemble-based anomaly detection in Brazilian parliamentary expenses using unlabeled public data. *International Journal of Data Science and Analytics, 22*, Article 139. https://doi.org/10.1007/s41060-026-01079-9

Škvára, V., Pevný, T., & Šmídl, V. (2023). *Is AUC the best measure for practical comparison of anomaly detectors?* (arXiv:2305.04754). arXiv. https://doi.org/10.48550/arXiv.2305.04754

## Yang sengaja tidak dipakai

- **Campos et al. (2016)**, sumber klasik P@n: terbit lebih dari 5 tahun lalu dan berbayar (Springer, repositori kampus juga terkunci).
- **Ma et al. (survei graph anomaly detection, 2021)** dan **Herreros-Martínez et al. (2025)**: ternyata tidak membahas Precision@K.
