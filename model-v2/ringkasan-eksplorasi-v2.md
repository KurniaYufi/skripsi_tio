# Ringkasan Eksplorasi Model: dari v1 ke v2

Dikerjakan 2026-10-28. Kode eksplorasi: `/mnt/project-files/model-v1/eksplorasi/` (exp.py, exp2.py, banding.py, banding2.py, beserta CSV hasilnya). Model terpilih: `/mnt/project-files/model-v2/`. Dashboard sudah memakai v2 (link sama). Dashboard v1 disimpan di `/mnt/project-files/dashboard-v1/arsip/`.

## 1. Intinya

1. **Angka v1 sebagian besar "bocoran".** Fitur one-hot metode memuat kategori *penunjukan langsung*, padahal penunjukan langsung juga red flag ke-4. Model seperti diberi tahu jawabannya. Di jalur perencanaan v1, 24,5% dari 200 paket teratas adalah penunjukan langsung (rata-rata semua paket 1,2%). Kalau red flag 4 tidak dihitung, P@K v1 perencanaan hanya 9,2%, lebih rendah dari rata-rata semua paket (11,5%).
2. **v2 membuang bocoran itu dan menambah fitur yang lebih bermakna.** Angka utamanya tetap setara v1, tetapi tidak lagi bergantung pada fitur yang sama dengan red flag. Daftar teratas juga tidak lagi didominasi satu satker.
3. **Ada batas yang tidak bisa diakali.** Red flag *pengadaan langsung mendekati ambang* dan *pemecahan paket* hampir tidak tertangkap model mana pun. Paket seperti itu memang dibuat supaya terlihat biasa, sedangkan model ketidaklaziman mencari paket yang berbeda dari kebanyakan. Ini temuan yang layak dibahas di Bab 4/5, bukan kegagalan model.

## 2. Cara uji supaya hasil tidak dipas-paskan

- 38 provinsi dibagi dua secara acak: 19 provinsi **pilih** dan 19 provinsi **uji**. Pengaturan dipilih dari provinsi pilih. Provinsi uji hanya untuk mengecek apakah hasilnya ikut bagus di provinsi lain.
- Setiap pengaturan dijalankan dengan **3 seed acak**. Yang dibandingkan adalah rata-ratanya, karena hasil satu kali jalan bisa naik turun cukup jauh (terutama Autoencoder).
- **Syarat keberagaman:** di 200 paket teratas, satu satker paling banyak 20 paket (10%). Tanpa syarat ini, P@K bisa tinggi hanya karena satu satker yang punya puluhan paket mirip.
- Aturan pemilihan ditetapkan **sebelum** melihat hasil putaran 2.
- Total yang diuji: 18 pengaturan di putaran 1, 31 pengaturan × 3 seed di putaran 2, dan 6 pengaturan × 3 seed di perbandingan akhir.

## 3. Apa yang diubah dan alasannya

| No | Perubahan | Jalur | Alasan | Bukti (rata-rata P@50/100/200, 3 seed) |
|---|---|---|---|---|
| 1 | **Buang one-hot metode pengadaan** | Keduanya | Kategori penunjukan langsung = red flag 4, sehingga evaluasi berputar. Ini mengikuti prinsip yang sudah disepakati: fitur yang sama dengan red flag dikeluarkan. Informasi metode tetap ikut lewat fitur "pagu dibanding paket sejenis" (pembandingnya paket dengan jenis **dan metode** yang sama), jadi pengadaan langsung berpagu besar tetap bisa terdeteksi. | Perencanaan v1: 24,5% dari 200 teratas adalah penunjukan langsung. Pelaksanaan: porsi penunjukan langsung di 200 teratas turun dari 16,5% (v1) menjadi 2,8% (v2). |
| 2 | **Tambah "pagu dibanding paket lain di satker yang sama"** | Keduanya | Paket yang jauh lebih besar dari kebiasaan satkernya sendiri patut dicek. Ini melengkapi pembanding nasional ("paket sejenis"). | Perencanaan: 21,8% → 41,8% saat dua fitur tambahan (no 2 dan 3) masuk. |
| 3 | **Tambah "porsi e-purchasing satker"** | Keduanya | Melengkapi "proporsi pengadaan langsung satker" sehingga profil cara belanja satker lebih lengkap. | Sama dengan no 2. Di pelaksanaan, fitur tambahan membuat 200 teratas tidak lagi didominasi satu satker (32 → 17 paket per satker). |
| 4 | **Tambah "rasio realisasi dibanding paket sejenis"** | Pelaksanaan | Realisasi 90% bisa wajar untuk satu jenis paket tetapi janggal untuk jenis lain. Fitur ini membandingkan dengan paket sejenis, bukan dengan angka mutlak. | Paket peringkat 1 pelaksanaan v2: realisasi 268% dari pagu, selisih 169 poin dari median paket sejenis. |
| 5 | **Buang fitur PDN dan UMK (ya/tidak)** | Perencanaan | 98,7% paket PDN dan 96% paket UMK berstatus "ya". Paket berstatus "tidak" menjadi kategori langka yang menyedot daftar teratas, padahal tidak berkaitan dengan red flag. Di pelaksanaan fitur ini **tetap dipakai** karena hasilnya lebih baik. | Perencanaan: 31,2% (dengan PDN/UMK) vs 41,8% (tanpa). Pelaksanaan: 52,5% (dengan) vs 38,9% (tanpa). |
| 6 | **Penskalaan quantile** untuk LOF dan Autoencoder | Perencanaan | Pagu sangat timpang (median Rp15,9 jt, maksimum Rp2,29 T). Quantile meratakan sebarannya sehingga jarak antarpaket tidak didominasi beberapa nilai ekstrem. Pelaksanaan tetap memakai standardisasi biasa karena hasilnya lebih baik di sana. | Perencanaan: 8,5% (standar) vs 10,4% (quantile). Pelaksanaan: 59,2% (standar) vs 36,9% (quantile). |
| 7 | **Isolation Forest: sampel per pohon 2.048** (bawaan 256) | Perencanaan | Data perencanaan besar (343 ribu paket). Sampel yang lebih besar membuat pohon lebih mewakili data. | 41,8% → 42,2%; daftar teratas sedikit lebih beragam (13 → 12 paket per satker). |
| 8 | **Autoencoder: lapisan tengah 3 neuron** (sebelumnya 4) | Perencanaan | Lapisan tengah yang lebih sempit memaksa Autoencoder meringkas pola umum saja, sehingga hasilnya lebih stabil antar-seed. | Simpangan baku antar-seed turun dari 0,076 menjadi 0,018. |

**Dicoba tetapi tidak dipakai:**
- LOF dengan k = 50 dan 100: angkanya turun.
- Gabungan "maksimum": angkanya naik, tetapi 43 dari 200 paket teratas berasal dari satu satker.
- Gabungan "median" dan "bobot per keluarga model": tidak lebih baik dari rata-rata.
- Membuang fitur tingkat satker: perencanaan turun dari 41,8% menjadi 12,2%.
- Membuang one-hot jenis: turun.
- Isolation Forest 2.048 di pelaksanaan: tidak lolos syarat keberagaman.

Cara menggabungkan tetap **rata-rata peringkat persentil**, sama seperti v1 dan Bab 3.

## 4. Hasil v1 vs v2 (ensemble, rata-rata 3 seed)

**Jalur perencanaan** (acuan semua paket 12,6%; tanpa red flag 4: 11,5%)

| | P@50 | P@100 | P@200 | Tanpa red flag 4 | Di provinsi uji | Satker terbanyak di 200 teratas |
|---|---|---|---|---|---|---|
| v1 | 48,7% | 45,3% | 31,5% | 9,2% | 24,6% | 37 paket |
| **v2** | **49,3%** | **45,7%** | **31,5%** | 10,2% | 14,2% | **13 paket** |

**Jalur pelaksanaan** (acuan semua paket 37,0%; tanpa red flag 4: 36,3%)

| | P@50 | P@100 | P@200 | Tanpa red flag 4 | Di provinsi uji | Satker terbanyak di 200 teratas |
|---|---|---|---|---|---|---|
| v1 | 58,7% | 57,3% | 57,0% | 48,9% | 31,2% | 17 paket |
| **v2** | **60,0%** | 49,3% | 48,2% | 48,5% | **38,3%** | 17 paket |

**Per red flag** (persentase 200 paket teratas ensemble yang memenuhi red flag itu, dibanding rata-rata semua paket)

| Red flag | Perencanaan v1 | Perencanaan v2 | Acuan | Pelaksanaan v1 | Pelaksanaan v2 | Acuan |
|---|---|---|---|---|---|---|
| PL mendekati ambang | 0,0% | 0,7% | 2,2% | 6,3% | 5,2% | 4,8% |
| PL melebihi ambang | 6,0% | 8,2% | 2,2% | 18,5% | 16,3% | 2,9% |
| Pemecahan paket | 1,0% | 0,2% | 8,3% | 5,2% | 7,3% | 11,1% |
| Penunjukan langsung | 24,5% | 22,5% | 1,2% | 16,5% | 2,8% | 0,9% |
| Penyedia dominan | | | | 30,0% | 27,5% | 21,0% |
| Penyedia serba-ada | | | | 1,7% | 2,5% | 2,6% |

Angka di dashboard berasal dari satu kali jalan (seed 42), jadi sedikit berbeda dari rata-rata 3 seed di atas:
- **Perencanaan:** ensemble 42/44/36%, IF 24/22/23%, LOF 22/22/25%, AE 92/96/95,5%.
- **Pelaksanaan:** ensemble 58/49/51,5%, IF 44/35/37%, LOF 30/60/58%, AE 54/49/48,5%.

## 5. Hal yang perlu diketahui sebelum dipakai di naskah

1. **Pelaksanaan v2 jelas lebih baik.** Kemampuan nyatanya (tanpa red flag 4) sama dengan v1, tetapi tanpa bocoran, dan hasilnya lebih baik di provinsi uji (38,3% vs 31,2%). Turunnya P@200 dari 57% ke 48% hanya karena bocoran penunjukan langsung sudah dibuang.
2. **Perencanaan masih lemah.** Walaupun one-hot metode sudah dibuang, model (terutama Autoencoder) masih banyak mengangkat paket penunjukan langsung. Jalurnya lewat profil satker: satker yang jarang memakai e-purchasing dan pengadaan langsung cenderung banyak memakai penunjukan langsung. Ini bukan bocoran langsung, tetapi sebagian besar angka perencanaan tetap berasal dari red flag 4. Di provinsi uji, P@K perencanaan (14,2%) hampir sama dengan acuan (12,6%).
   - Versi yang lebih ketat (porsi PL dan e-purchasing satker juga dibuang) menurunkan P@200 menjadi sekitar 20–25%. Pilihan ini bisa diambil kalau Tio ingin hasil perencanaan yang lebih "bersih" walaupun angkanya lebih kecil.
3. **Red flag mendekati ambang dan pemecahan paket memang sulit dideteksi.** Paket seperti ini dibuat agar terlihat wajar. Ini bisa jadi bahan pembahasan Bab 4 sekaligus alasan red flag tetap ditampilkan di dashboard di samping skor model.
4. **Ensemble tidak selalu yang tertinggi.** Di perencanaan, Autoencoder sendirian mencapai sekitar 87–95%, tetapi itu karena ia menumpuk paket penunjukan langsung dari beberapa satker saja (sampai 75 dari 200 paket berasal dari satu satker). Ensemble lebih stabil dan daftar teratasnya lebih beragam. Ini sejalan dengan Krčmar (2026): ensemble lebih konsisten, belum tentu paling akurat.
5. **Yang perlu disesuaikan di naskah kalau v2 dipakai:**
   - Tabel 3.2 Fitur: tanpa one-hot metode, tambah 3 fitur baru, dan PDN/UMK tidak dipakai di perencanaan.
   - Uraian 3.2.4: penskalaan quantile dan pengaturan model.
   - Bab 3/4: pembagian provinsi pilih/uji dan 3 seed sebagai cara memilih pengaturan.
