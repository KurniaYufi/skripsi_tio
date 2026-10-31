# Rancangan dari nol: fitur dan red flag (30 Oktober 2026)

**Pertanyaan Tio:** kalau sejak awal hanya diberi data RUP dan realisasi 2024–2025 serta panduan red flag OCP dan aturan (Perpres), fitur dan red flag apa yang akan dibuat?

**Catatan jujur:** saya tidak bisa benar-benar lupa hasil eksperimen sebelumnya. Bagian yang dipengaruhi pengalaman itu ditandai **(pelajaran)**.

## Langkah 1. Tetapkan aturan main dulu

1. **Red flag dulu, baru fitur.** Red flag adalah penguji, jadi harus ada sebelum model dibuat.
2. **Fitur dan red flag tidak boleh dihitung dari logika yang sama.** Kalau red flag = "PL dengan pagu > ambang" dan fitur = "pagu", model pasti terlihat menangkap red flag itu. Itu menyontek, bukan menemukan **(pelajaran: RF2)**.
3. **Fitur menjawab satu pertanyaan:** "seberapa berbeda paket ini dari paket yang mirip?" Pembandingnya bisa paket sejenis, satker yang sama, nama yang sama, atau tahun lalu.
4. **Satu tahun untuk mengembangkan, tahun lain untuk menguji.** 2024 untuk memilih fitur dan pengaturan, 2025 untuk menguji. Sebagian provinsi disisihkan sebagai provinsi uji.

## Langkah 2. Red flag yang akan saya pilih

Hanya yang (a) punya sumber jelas dan (b) bisa dihitung dari kolom INAPROC. Red flag OCP yang butuh data penawaran (penawar tunggal, masa pengumuman, harga penawaran) tidak bisa dipakai.

| No | Red flag | Sumber | Jalur | Berlaku untuk |
|---|---|---|---|---|
| 1 | PL dengan pagu tepat di bawah ambang (90–100%) | Perpres 16/2018 jo. 46/2025 Psl 38(3); pola *bunching* di OCP | perencanaan + pelaksanaan | paket PL |
| 2 | Pemecahan paket: beberapa PL bernama mirip di satker yang sama, jumlahnya melewati ambang | Psl 20(2)d | perencanaan + pelaksanaan | paket PL |
| 3 | Penunjukan Langsung | Psl 38(5); prosedur non-kompetitif di OCP | perencanaan + pelaksanaan | semua |
| 4 | Penyedia dominan: > 40% nilai satker × jenis | OCP R050 / R040 | pelaksanaan | paket berpenyedia |
| 5 | Penyedia serba-ada (≥ 3 jenis pengadaan) | OCP R048 | pelaksanaan | paket berpenyedia |
| 6 | Penyedia "kecil lalu besar": tahun lalu dapat paket kecil di satker itu, tahun ini ≥ 10 kali lipat | OCP R052 (bisa karena ada data 2024) | pelaksanaan 2025 | paket berpenyedia |
| 7 | PL > Rp50 jt yang hanya lewat Pencatatan Non Tender | Psl 38(8), berlaku sejak 30 Apr 2025 | pelaksanaan 2025 | paket PL |

**Yang sengaja tidak saya jadikan red flag evaluasi:**
- **PL melebihi ambang.** Ini pelanggaran nyata, jadi tetap ditampilkan di dashboard sebagai penanda aturan. Tetapi red flag ini dihitung dari pagu, jadi model yang memakai pagu pasti "menangkapnya" **(pelajaran)**.
- **Realisasi > pagu (OCP R031/R054).** Sama dengan fitur rasio realisasi. Tampilkan di dashboard saja.
- **Ketidaksesuaian PDN/UMK.** Lebih cocok sebagai fitur pelaksanaan daripada penguji. Setelah dikontrol ukuran paket, efeknya juga hilang **(pelajaran)**.

## Langkah 3. Fitur yang akan saya buat

Semua rasio dalam log10 dan satu arah (lebih murah dari pembanding = 0). Fitur yang sama dengan red flag dikeluarkan.

### Perencanaan (hanya RUP)

| No | Fitur | Cara hitung | Status |
|---|---|---|---|
| 1 | Besar pagu | log10(pagu) | sudah ada |
| 2 | Pagu dibanding paket sejenis | pagu ÷ median jenis yang sama, nasional (**tanpa metode**, karena metode = red flag 3) | mirip yang ada (sekarang jenis + metode) |
| 3 | Pagu dibanding satker | pagu ÷ median satker × jenis | sudah ada |
| 4 | Pagu dibanding paket bernama sama di satker | pagu ÷ median paket lain bernama sama | sudah ada |
| 5 | **Pagu dibanding tahun lalu** | pagu ÷ pagu paket bernama sama di satker yang sama tahun sebelumnya | **baru, belum diuji** |
| 6 | **Lonjakan anggaran satker** | total pagu satker × jenis tahun ini ÷ tahun lalu | **baru, belum diuji** |
| 7 | **Kejelasan nama paket** | jumlah kata yang bermakna; nama terlalu umum ("Belanja Barang") lebih sulit diawasi | **baru, belum diuji**; perlu dicek sumbernya |
| 8 | **Konsistensi label UMK** | paket ≤ Rp15 M tapi tidak dicadangkan untuk UMK (Psl 65(3)) | **baru sebagai fitur**, belum diuji |

### Pelaksanaan (RUP + realisasi)

Fitur 1–3 di atas, ditambah:

| No | Fitur | Cara hitung | Status |
|---|---|---|---|
| 9 | Rasio realisasi | realisasi ÷ pagu | sudah ada |
| 10 | Selisih rupiah | log10(1 + \|realisasi − pagu\|) | sudah ada |
| 11 | **Selisih PDN** | porsi PDN di realisasi dibanding status PDN di RUP | pernah dicoba, lalu dibuang |
| 12 | **Selisih UMK** | sama, untuk UMK | pernah dicoba, lalu dibuang |

**Tidak dipakai sebagai fitur:**
- metode (sama dengan red flag 3);
- kemiripan nama untuk pemecahan (sama dengan red flag 2);
- apa pun tentang penyedia (sama dengan red flag 4–6);
- kategori jenis/sumber dana sebagai *one-hot*, karena model menganggap kategori yang jarang sebagai aneh **(pelajaran)**.

## Langkah 4. Bedanya dengan yang sekarang

| Hal | Sekarang | Dari nol |
|---|---|---|
| Red flag evaluasi | 6 (termasuk PL lewat ambang) | 7, **tanpa** PL lewat ambang, ditambah R052 dan Psl 38(8) |
| Data | dilatih per tahun | 2024 untuk mengembangkan, 2025 untuk menguji, dan data 2024 juga dipakai sebagai pembanding fitur |
| Fitur baru | – | pagu dibanding tahun lalu, lonjakan satker, kejelasan nama, label UMK |
| Pagu sejenis | jenis + metode | jenis saja |

**Yang paling berbeda adalah pemanfaatan dua tahun.** Sekarang 2024 dan 2025 diperlakukan terpisah. Kalau dari awal saya punya keduanya, saya akan memakai tahun lalu sebagai pembanding. "Paket ini naik 5 kali dari tahun lalu" lebih mudah dijelaskan ke dosen daripada "paket ini 5 kali median nasional".

**Peringatan:** fitur 5–8 belum pernah diuji, jadi belum tentu menaikkan Precision@K. Kalau ditambahkan sekarang setelah melihat hasil, statusnya sama dengan red flag tambahan: eksperimen lanjutan yang harus ditulis jujur.
