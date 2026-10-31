# Kolom detail RUP: apakah layak di-scrape?

Bahan: 4 contoh detail paket dari Tio (2026-10-30) dan panduan OCP (2024) *Red flags in public procurement* (Library). Di halaman detail ada 23 kolom. Sebagian besar sudah ada di data massal. Kolom yang baru hanya: **volume pekerjaan, uraian pekerjaan, spesifikasi pekerjaan, jadwal (pemilihan, kontrak, pemanfaatan; mulai-akhir), Pra DIPA/DPA, aspek sosial/ekonomi/lingkungan**.

## Kesimpulan singkat

Kolom baru ini **lebih berguna sebagai red flag baru dan bahan telaah** daripada sebagai fitur model. Kalau dijadikan fitur, peningkatan model kemungkinan kecil:

- Jadwal hanya tercatat per **bulan**, bukan tanggal. Akibatnya red flag waktu dari OCP yang dihitung dalam hari tidak bisa dihitung, yaitu:
  - R003 masa penawaran terlalu pendek,
  - R014 jarak pengumuman–pembukaan penawaran,
  - R060–R062 jarak penetapan–kontrak.
- Kombinasi jadwal yang jarang belum tentu janggal. Contohnya kontrak tahun jamak atau pemilihan sebelum tahun anggaran (Pra DIPA). Model anomali akan menganggapnya aneh hanya karena jarang.
- Kalau satu informasi dijadikan fitur sekaligus red flag, evaluasi jadi berputar (prinsip "mencontek" yang sudah dibahas). Jadi tiap kolom baru harus dipilih: masuk fitur, **atau** masuk red flag, tidak boleh dua-duanya.

## Kolom per kolom

| Kolom | Padanan di OCP | Bisa dipakai untuk | Catatan |
|---|---|---|---|
| Uraian dan spesifikasi pekerjaan | R001 dokumen perencanaan tidak tersedia; R005 informasi kunci tender tidak tersedia (kelompok *low transparency*) | **Red flag baru: informasi pekerjaan tidak terbuka.** Contoh: isi hanya "Uraian pekerjaan pada KAK" atau sama persis dengan nama paket. | Paling menarik karena tidak berasal dari pagu. Kalau model ternyata menemukan paket seperti ini, itu bukti yang tidak "mencontek". Tetapi bisa juga model tidak menemukannya, karena fitur model hanya angka pagu dan realisasi. |
| Volume pekerjaan | R016 nilai di atas atau di bawah rata-rata kategori; R017 harga satuan sangat tinggi atau rendah | Harga per satuan, misalnya pagu / (88 × 13) untuk PPSU = Rp5.396.761 = UMP DKI 2025 | 3 dari 4 contoh bervolume "1 Paket", sehingga harga satuan hanya bisa dihitung untuk sebagian kecil paket. Lebih cocok untuk **menjelaskan** paket teratas daripada sebagai fitur. |
| Jadwal pemilihan, kontrak, pemanfaatan (bulan) | Tidak ada padanan langsung (red flag waktu OCP dihitung dalam hari) | (a) pemilihan menumpuk di akhir tahun (Nov–Des); (b) kontrak sangat pendek untuk pagu besar; (c) jadwal tidak konsisten, misalnya pemanfaatan dimulai sebelum kontrak | Masih bisa dihitung, tetapi tidak ada rujukan OCP yang pas. Untuk (a) perlu dicari sumber gratis lain. |
| Pra DIPA/DPA | – | Penjelas (paket dipilih sebelum anggaran disahkan itu wajar) | Bukan red flag. |
| Aspek sosial/ekonomi/lingkungan | – | – | Hampir selalu "Tidak", tidak informatif. |

## Yang sebenarnya sudah ada tanpa scraping

**OCP R012 (penunjukan langsung yang menyimpang dari rencana pengadaan):** di data realisasi sudah ada `metode_realisasi`, sedangkan di RUP ada `metode_pengadaan`. Paket yang direncanakan Tender/Seleksi tetapi realisasinya Penunjukan Langsung atau Pengadaan Langsung bisa langsung dijadikan red flag jalur pelaksanaan. Dulu `ubah_metode` sempat menjadi fitur lalu dibuang, jadi informasi ini masih bebas dipakai sebagai red flag.

## Saran sebelum scraping semua paket

1. **Cek dulu unduhan massal INAPROC.** Kalau dataset RUP massal ternyata punya kolom volume, uraian, atau jadwal, scraping tidak perlu.
2. **Kalau tetap scraping, mulai dari uji coba sekitar 2.000 paket**: 1.000 teratas dan 1.000 acak per jalur. Dari sampel itu hitung:
   - berapa persen volume berupa angka (bukan "1 Paket");
   - berapa persen uraian atau spesifikasi yang tidak informatif;
   - apakah red flag "informasi tidak terbuka" lebih sering muncul di paket teratas daripada di paket acak.

   Kalau di paket teratas tidak lebih sering, scraping 300 ribu paket tidak sepadan.
3. **Etika scraping.** Beri jeda antar permintaan (misalnya 1–2 detik), jangan paralel besar-besaran, dan baca ketentuan situsnya. Pada kecepatan itu, 300 ribu paket butuh sekitar 4–7 hari nonstop.
