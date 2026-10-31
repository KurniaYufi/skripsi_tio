# Ringkasan Eksplorasi Validitas: Model v3

> **Pembaruan 2026-10-29: model terbaru v4.** Jalur perencanaan kini membuang paket berpagu < Rp1 jt dan memakai rasio pagu satu arah. Angka perencanaan v4 dan alasannya ada di [hasil-pagu-kecil.md](/mnt/project-files/validasi-v3/pagu-kecil/hasil-pagu-kecil.md). Angka jalur pelaksanaan di bawah tetap berlaku.

Dikerjakan 2026-10-28. Kode dan hasil ada di dua folder:
- `/mnt/project-files/validasi-v3/`: uji red flag dan pemilihan fitur.
- `/mnt/project-files/model-v3/`: model akhir dan uji validitasnya (hasil angka di `model-v3/validasi/`).

Dashboard sudah memakai v3 dengan link yang sama, dan sekarang punya bagian **"Seberapa bisa dipercaya hasil ini?"**. Model v2 tetap disimpan di `model-v2/`, dashboard v2 di `dashboard-v1/arsip/`. Naskah di Google Doc **belum** diubah.

## 1. Intinya

1. **Hasil model v3 sekarang didukung bukti dari empat arah**, bukan hanya Precision@K:
   - **Red flag.** Paket yang dinilai tidak lazim lebih sering punya red flag, juga di 19 provinsi yang tidak dipakai saat memilih pengaturan.
   - **Penilaian lembaga lain.** Di jalur pelaksanaan, 10 provinsi dengan skor integritas SPI KPK 2024 terendah punya paket tidak lazim 3,5 kali lebih banyak daripada 10 provinsi tertinggi (median 15,3% vs 4,3%). Bedanya tetap nyata walaupun provinsi Papua dikeluarkan.
   - **Anomali buatan.** Model menangkap pola yang tidak tertangkap cara sederhana. Contohnya pola gabungan antarfitur: ensemble 39–63%, skor-z hanya 1–2%.
   - **Kestabilan dan penjelasan.** Daftar teratas stabil bila model dilatih ulang: sekitar 7–8 dari 10 paket di 200 teratas tetap sama. Fitur yang disebut SHAP memang yang paling menaikkan skor: mengganti 3 fitur teratas SHAP menurunkan skor jauh lebih besar daripada mengganti 3 fitur acak, di 97–100% paket.
2. **Red flag diperbaiki dengan bukti dari data.**
   - Paket memang menumpuk tepat di bawah ambang pengadaan langsung. Untuk jasa konsultansi, jumlahnya 5,3 kali dari perkiraan.
   - RF5 diganti ke definisi panduan OCP, karena definisi lama menandai 21% paket.
3. **Fitur jalur perencanaan diganti**: profil cara belanja satker dibuang.
   - Di 5% teratas, paket ber-red flag 2,3 kali rata-rata.
   - Di provinsi uji, 2,7 kali rata-rata.
4. **Tiga model memang perlu digabung.** Dari 9 cara menggabungkan, rata-rata IF+LOF+AE paling konsisten dan tidak pernah menjadi yang terburuk. Tiap model tunggal pernah paling buruk di salah satu ukuran.
5. **Yang belum terbukti, dan harus ditulis jujur:**
   - Manipulasi yang sengaja dibuat tampak wajar tidak tertangkap model mana pun, misalnya pagu dinaikkan ke dekat ambang atau pagu digelembungkan.
   - Di jalur pelaksanaan, 5% teratas di provinsi uji hampir sama dengan rata-rata.
   - Jalur perencanaan belum sejalan dengan SPI.
   - Tidak ada label kebenaran, jadi semua bukti bersifat tidak langsung.

## 2. Apa saja yang saya jelajahi

| Bagian | Yang dicek | Kenapa perlu |
|---|---|---|
| Red flag | Uji *bunching* (penumpukan paket tepat di bawah ambang pengadaan langsung), keselarasan antar-red flag per satker, definisi lain dari panduan OCP (2024), dan kandidat red flag baru | Red flag dipakai sebagai acuan evaluasi. Kalau acuannya lemah, Precision@K ikut lemah. |
| Fitur | 6 varian fitur per jalur, masing-masing 3 seed. Dipilih di 19 provinsi pilih, dicek di 19 provinsi uji | Supaya fitur tidak dipas-paskan dengan data yang juga dipakai untuk menilai |
| Model | Rata-rata 5 seed, dan ablasi 9 cara menggabungkan IF, LOF, AE | Menjawab "kenapa harus ensemble?" dengan data, bukan hanya teori |
| Pembanding | Urutan acak, pagu terbesar, rasio pagu sejenis, skor-z sederhana, ECOD, HBOS, KNN, PCA | Model rumit baru berguna kalau lebih baik dari cara sederhana |
| Anomali buatan | 4 tipe gaya ADBench: ekstrem, lokal, gabungan antarfitur, kelompok kembar. 3 skenario pengadaan: realisasi melebihi pagu, pagu digelembungkan, dinaikkan ke dekat ambang. Ditambah paket wajar buatan sebagai kontrol | Cara mengecek "apakah model menangkap anomali" ketika label asli tidak ada (Han et al., 2022) |
| Kestabilan | Dua set 5 seed yang berbeda; ambang 1%, 5%, 10% | Hasil yang valid tidak boleh banyak berubah hanya karena angka acak atau pilihan ambang |
| SHAP | Uji hapus fitur: fitur teratas SHAP diganti, lalu dilihat seberapa turun skornya dibanding bila fitur acak yang diganti | Memastikan kalimat penjelasan menunjuk penyebab yang benar (Nauta et al., 2023) |
| Lintas tahap | Apakah skor perencanaan (hanya dari RUP) bisa menduga masalah yang baru terlihat saat pelaksanaan, setelah ukuran paket dikontrol | Bukti bahwa skor perencanaan berguna sebagai tanda awal |
| Data luar | Skor Survei Penilaian Integritas (SPI) KPK 2024 per provinsi | Pembanding dari lembaga lain yang bisa diakses gratis |
| Telaah buta | Lembar penilaian 40 paket per jalur: 20 pilihan model dan 20 acak, tanpa tanda asal | Cara paling kuat bila ada penelaah manusia (dosen atau praktisi) |

## 3. Red flag: diuji lalu diperbaiki

### 3.1 Penumpukan paket di bawah ambang (dasar RF1)

Kalau tidak ada ambang, jumlah paket di sekitar Rp200 jt seharusnya menurun halus. Cara ujinya:
1. Jumlah paket per 1% ambang dihitung pada rentang 50–150% ambang.
2. Kurva halus dipasang di luar jendela 90–110%, dengan koreksi untuk angka bulat seperti Rp150 jt. Kurva itu menjadi perkiraan "kalau tidak ada ambang".
3. Selang kepercayaan diambil dari 300 kali *bootstrap*.

Cara ini mengikuti Bertanha et al. (2021). Gambarnya ada di [penumpukan-ambang.png](/mnt/project-files/validasi-v3/gambar/penumpukan-ambang.png).

| Ambang | Paket di 90–100% ambang | Perkiraan tanpa ambang | Rasio (selang 95%) | Khusus pengadaan langsung |
|---|---|---|---|---|
| Barang dan Jasa Lainnya, Rp200 jt | 4.682 | 2.807 | 1,67× (1,57–1,77) | 2,47× |
| Pekerjaan Konstruksi, ambang lama Rp200 jt | 7.776 | 2.680 | **2,90×** (2,77–3,06) | 2,91× |
| Pekerjaan Konstruksi, ambang baru Rp400 jt | 615 | 559 | 1,10× (0,95–1,27), tidak nyata | 1,05× |
| Jasa Konsultansi, Rp100 jt | 4.532 | 852 | **5,32×** (4,88–5,83) | 5,70× |

Artinya:
- Penumpukan tepat di bawah ambang benar-benar ada di data 2025. RF1 punya dasar empiris, bukan hanya dasar aturan.
- Untuk konstruksi, penumpukan terjadi di ambang **lama** (Rp200 jt), bukan di ambang baru Rp400 jt. Perpres 46/2025 baru berlaku 30 April 2025, sehingga banyak RUP 2025 masih disusun dengan ambang lama.
- **Perubahan:** RF1 pekerjaan konstruksi sekarang memakai dua jendela, 180–200 jt dan 360–400 jt. Jumlah paket RF1 naik dari 7.383 menjadi 15.732 (perencanaan) dan dari 5.076 menjadi 9.839 (pelaksanaan).
- Per provinsi, penumpukan paling kuat di Lampung, Bengkulu, dan Riau (4,7–6,9 kali). Di Papua Pegunungan dan Papua Tengah justru tidak ada penumpukan.

### 3.2 RF5 diganti ke definisi OCP

- RF5 lama ("penyedia yang sama mendapat lebih dari 5 paket di satker") menandai **21% paket pelaksanaan**. Red flag yang menandai seperlima paket terlalu umum untuk menjadi tanda bahaya.
- Isinya hampir sama dengan "penyedia yang paketnya paling banyak" (kemiripan Jaccard 0,96). Jadi RF5 lama lebih mencerminkan satker yang besar daripada dominasi satu penyedia.
- **Perubahan:** RF5 memakai definisi OCP R040: satu penyedia menerima lebih dari 40% nilai realisasi satker yang punya minimal 5 paket. Paket yang ditandai turun dari 22.121 (21%) menjadi 2.910 (2,8%).
- Catatan: di tingkat satker, RF5 (lama maupun baru) cenderung berlawanan arah dengan RF1 dan RF3 (ρ −0,20 sampai −0,26). Ini masuk akal: satker yang memecah belanja menjadi banyak paket kecil biasanya memakai banyak penyedia, sedangkan dominasi penyedia terjadi di satker dengan sedikit paket besar. Jadi RF5 mengukur risiko yang berbeda, bukan red flag yang salah.

### 3.3 Red flag lain dan kandidat baru dari panduan OCP

| Red flag | Hasil uji | Keputusan |
|---|---|---|
| RF1 dengan ambang 95% atau 98% | Hasil model hampir sama dengan 90% | Tetap 90–100% |
| RF3 pemecahan paket, kemiripan 0,7 atau 0,9 | Hasil model hampir sama dengan 0,8 | Tetap 0,8 |
| RF1 dan RF3 | Saling menguatkan. Muncul bersama 4,9–6,3 kali lebih sering dari kebetulan; korelasi tingkat satker 0,54–0,64 | Tetap |
| RF6 penyedia serba-ada | Hampir tidak berkaitan dengan red flag lain | Tetap, dicatat sebagai red flag yang berdiri sendiri |
| R049: PL dekat ambang berulang ke penyedia yang sama | Seluruhnya sudah tercakup RF1 | Tidak ditambah |
| R055: PL berulang ke penyedia yang sama, jumlahnya melewati ambang | 12,6% paket pelaksanaan; searah dengan RF1/RF3; bisa diduga dari skor perencanaan | **Kandidat RF7** (keputusan Tio) |
| R012: metode berubah ke penunjukan langsung | Hanya 19 paket | Tidak ditambah |
| R068: realisasi melebihi pagu | Tidak searah dengan red flag lain, dan sudah menjadi fitur (rasio realisasi) | Tidak ditambah, agar evaluasi tidak berputar |
| Judul paket sangat pendek | Tidak searah dengan red flag lain | Tidak ditambah |

### 3.4 Apakah red flag sendiri sejalan dengan penilaian lembaga lain?

Ya. Proporsi paket ber-red flag di 10 provinsi dengan SPI terendah jauh lebih tinggi daripada di 10 provinsi tertinggi:
- perencanaan: median 30,1% vs 8,4% (p = 0,002);
- pelaksanaan: 42,7% vs 21,0% (p = 0,016).

Ini mendukung pemakaian red flag sebagai acuan evaluasi.

## 4. Fitur: varian yang dicoba dan yang dipilih

Cara pilihnya sama dengan v2:
- 19 provinsi **pilih** dipakai untuk memilih, 19 provinsi **uji** hanya untuk mengecek.
- Tiap varian dijalankan dengan 3 seed.
- Aturan pilih ditulis di kode sebelum hasil keluar (`r6_pilih_v3.py`):
  - satu satker paling banyak 20 paket di 200 teratas;
  - di provinsi pilih, model harus lebih baik dari rata-rata untuk red flag **selain** penunjukan langsung (RF4).

Varian yang dicoba:
- **N**: tambah fitur "pagu dibanding 30 paket yang namanya paling mirip" (kemiripan kata nama paket, TF-IDF). Ini menjawab ide TF-IDF yang pernah dibahas.
- **L**: profil cara belanja satker (porsi pengadaan langsung dan porsi *e-purchasing*) dihitung tanpa paket itu sendiri.
- **E**: profil cara belanja satker dibuang.
- **U** (pelaksanaan): status PDN/UMK dibuang.
- **Q** (pelaksanaan): penskalaan *quantile*.

**Jalur pelaksanaan.** v2 tetap yang terbaik dan lolos syarat, jadi tidak diubah.

| Varian | P@200 | Provinsi uji (rata-rata 50–200 teratas) | Tanpa RF4, provinsi pilih | Satker terbanyak di 200 teratas |
|---|---|---|---|---|
| **v2 (dipakai)** | **47,0%** | **38,7%** | **45,0%** | 14 |
| N | 41,0% | 38,2% | 38,7% | 19 |
| L | 46,5% | 37,2% | 44,8% | 15 |
| U | 32,0% | 28,7% | 36,8% | 11 |
| NU | 36,5% | 32,3% | 33,3% | 11 |
| Q | 38,0% | 25,7% | 39,8% | 12 |
| Acuan (rata-rata semua paket) | 24,7% | 24,7% | 23,6% | |

**Jalur perencanaan.** Semua varian gagal syarat "tanpa RF4". Di 50–200 teratas, paket ber-red flag selain penunjukan langsung masih di bawah rata-rata provinsi pilih (15,0%). Artinya puncak daftar perencanaan masih ditarik penunjukan langsung lewat profil satker.

Karena itu saya memakai aturan lanjutan:
1. Lihat 5% teratas, yang menjadi dasar peta dashboard.
2. Pilih varian terbaik di provinsi pilih.
3. Cek hasilnya di provinsi uji.

Aturan ini dibuat **setelah** putaran pertama, jadi harus ditulis jujur di naskah sebagai keputusan lanjutan. Pilihan ini tetap layak karena dua hal:
- E juga paling baik di provinsi uji;
- alasannya jelas secara isi: jalur bocoran penunjukan langsung lewat profil satker berkurang.

| Varian | P@200 | 5% teratas, lift provinsi pilih | 5% teratas, lift provinsi uji | Lift tanpa RF4 (pilih / uji) | Satker terbanyak |
|---|---|---|---|---|---|
| v2 | 32,0% | 1,86 | 1,84 | 1,62 / 1,67 | 7 |
| N | 31,5% | 1,49 | 1,31 | 1,17 / 1,10 | 5 |
| L | 30,5% | 1,89 | 2,20 | 1,64 / 2,08 | 5 |
| NL | 31,0% | 1,50 | 1,31 | 1,19 / 1,11 | 5 |
| NE | 23,0% | 1,33 | 1,25 | 1,22 / 1,17 | 18 |
| **E (dipakai)** | 21,5% | **2,01** | **3,06** | **1,91 / 3,14** | 18 |

Lift adalah persentase paket ber-red flag di 5% teratas dibagi rata-ratanya. Angka di tabel ini dari 3 seed; model akhir memakai 5 seed.

Harga yang dibayar: puncak daftar E lebih lemah. P@200-nya 21,5% (3 seed) atau 25,5% (model akhir), sedangkan v2 32,0%.
- 36,5% dari 200 paket teratas model akhir berpagu di bawah Rp10 jt. Paket ini tidak lazim bagi satkernya, tetapi jarang punya red flag.
- Penunjukan langsung masih 18,5% dari 200 teratas, padahal rata-rata semua paket 1,2%.
- Di 5% teratas, yang menjadi dasar peta, porsi penunjukan langsung tinggal 3,2%. Jadi kesesuaian di tingkat ini sebagian besar datang dari red flag lain.

**Fitur nama serupa (N) tidak dipakai.** Fitur ini menurunkan hasil di kedua jalur. Penyebabnya, pagu paket yang namanya mirip memang sangat beragam secara wajar:
- 14,1% paket asli sudah punya pagu lebih dari 5 kali median 30 paket yang namanya paling mirip;
- 3,8% bahkan lebih dari 20 kali.

Jadi pagu yang digelembungkan 5–20 kali tidak bisa dibedakan dari variasi wajar. Untuk itu dibutuhkan data harga satuan dan volume, yang tidak ada di kolom RUP dan realisasi.

## 5. Model v3: apa yang diubah dan alasannya

| No | Perubahan | Alasan | Bukti |
|---|---|---|---|
| 1 | Skor = rata-rata **5 seed** (42, 1, 2, 3, 4) | IF dan Autoencoder memakai angka acak. Dengan satu seed, daftar teratas berubah-ubah setiap kali dilatih ulang | Kesamaan 200 teratas antara dua kali pelatihan (Jaccard) naik: perencanaan 0,38 → 0,61, pelaksanaan 0,42 → 0,56 |
| 2 | **Red flag v3**: RF1 konstruksi memakai dua jendela, RF5 memakai definisi OCP | Bagian 3.1 dan 3.2 | Bagian 3 |
| 3 | **Fitur perencanaan E**: porsi pengadaan langsung dan porsi *e-purchasing* satker dibuang | Bagian 4 | Lift 5% teratas di provinsi uji 3,06 (v2 1,84) |
| 4 | Cara menggabungkan **tetap rata-rata** | Diuji ulang terhadap 8 cara lain dan tetap paling konsisten | Bagian 6.3 |
| 5 | Dashboard: panel bukti validitas, tanda * untuk provinsi dengan kurang dari 100 paket, red flag tetap tampil di samping skor | Pembaca perlu tahu seberapa kuat hasilnya. Red flag menutup kelemahan model pada manipulasi yang tampak wajar | Bagian 6 dan 7 |

Jalur pelaksanaan tetap memakai fitur dan pengaturan v2.

## 6. Hasil uji validitas model v3

### 6.1 Ringkasan per uji

| Uji | Perencanaan | Pelaksanaan |
|---|---|---|
| Paket teratas lebih sering punya red flag? | ✓ 200 teratas 25,5% vs rata-rata 14,2% (p < 0,001). 5% teratas 32,6% (2,3×) | ✓ 200 teratas 48,0% vs 24,7% (p < 0,001). 5% teratas 29,2% (1,2×) |
| Berlaku di provinsi uji? | ✓ 5% teratas 32,4% vs 12,0% (2,7×). 50–200 teratas lemah: 14,7% vs 12,0% | ~ 50–200 teratas 38,0% vs 24,7% (1,5×). 5% teratas 25,3% vs 24,7%, hampir sama |
| Tetap sejalan tanpa RF4? | ~ 5% teratas 29,5% vs 13,1% (2,3×). 50–200 teratas 9,3%, di bawah rata-rata | ✓ 50–200 teratas 49,2% vs 23,9%. 5% teratas 26,3% (1,1×) |
| Red flag mana yang terangkat (lift 5% teratas)? | Semua: RF1 2,3×, RF2 4,1×, RF3 1,9×, RF4 2,7× | RF2 3,7×, RF4 3,5×, RF5 3,2×. RF1 0,4×, RF3 0,4×, RF6 0,8× |
| Stabil bila dilatih ulang? | ✓ Jaccard 200 teratas 0,61 (satu seed 0,38). P@200 set seed kedua 29,5% | ~ Jaccard 200 teratas 0,56 (satu seed 0,42). P@200 set seed kedua 41,0% |
| Ambang 1/5/10% | ✓ 26,6 / 32,6 / 33,9%. Urutan provinsi 5% vs 10%: ρ 0,89 | ✓ 38,7 / 29,2 / 27,7%. Urutan provinsi 5% vs 10%: ρ 0,97 |
| Peta provinsi sejalan dengan red flag? | ✓ ρ 0,55 (p < 0,001); tanpa Papua ρ 0,50 (p = 0,004) | ✗ ρ 0,32 (p = 0,052); tanpa Papua 0,21 |
| Sejalan di tingkat satker (≥ 30 paket)? | ✓ lemah: ρ 0,16 (p < 0,001); RF1 0,26, RF3 0,17 | ✓ lemah: ρ 0,09 (p = 0,005); RF2 0,20 |
| Sejalan dengan SPI KPK 2024? | ✗ 7,6% vs 4,7% (p = 0,12); tanpa Papua terbalik | ✓ 15,3% vs 4,3% (p < 0,001); tanpa Papua 7,5% vs 4,3% (p = 0,002) |
| Menangkap anomali buatan? | ~ Kuat untuk ekstrem, lokal, gabungan, kelompok; tidak untuk dekat ambang dan pagu digelembungkan | ~ Sama, ditambah realisasi melebihi pagu 56% |
| Penjelasan SHAP setia? | ✓ Mengganti 3 fitur teratas SHAP menurunkan skor 0,142; 3 fitur acak hanya 0,0005. Berlaku di 100% paket | ✓ 0,099 vs 0,001. Berlaku di 97% paket |
| Skor perencanaan menduga masalah saat pelaksanaan? | ✓ setelah ukuran paket dikontrol: R049 1,85×, R055 1,33× (p < 0,001). RF5 1,08× (tidak nyata) | (tidak berlaku) |

✓ = mendukung, ~ = sebagian, ✗ = belum mendukung. Selang *bootstrap* per satker untuk P@200: perencanaan 16,5–34,5%, pelaksanaan 39,5–57,5%; keduanya di atas rata-rata.

### 6.2 Dibanding cara lain

Persentase paket ber-red flag (Precision@K):

| Cara | Perencanaan P@200 | Perencanaan 5% teratas | Perencanaan 5%, provinsi uji | Pelaksanaan P@200 | Pelaksanaan 5% teratas | Pelaksanaan 5%, provinsi uji |
|---|---|---|---|---|---|---|
| **Ensemble v3** | 25,5% | **32,6%** | 32,4% | 48,0% | 29,2% | 25,3% |
| IF saja | 36,0% | 16,6% | 11,3% | 34,0% | 26,3% | 17,8% |
| LOF saja | 5,5% | 27,8% | 31,8% | 57,0% | **40,0%** | **40,0%** |
| AE saja | 23,0% | 27,4% | 29,1% | 39,0% | 26,3% | 22,5% |
| Skor-z sederhana | 10,5% | 11,7% | 5,8% | **79,5%** | 30,3% | 21,3% |
| Rasio pagu sejenis terbesar | 34,5% | 30,0% | 22,8% | 46,5% | 29,6% | 28,3% |
| Pagu terbesar | 18,0% | 17,2% | 13,1% | 38,0% | 25,0% | 17,8% |
| HBOS | **40,5%** | 17,8% | 10,7% | 43,0% | 31,2% | 22,8% |
| KNN | 10,0% | 35,8%* | 42,2%* | 52,0% | 30,5% | 27,6% |
| ECOD | 16,5% | 11,9% | 6,0% | 48,5% | 26,4% | 17,3% |
| PCA | 3,0% | 26,4% | 31,7% | 39,0% | 30,3% | 27,6% |
| Urutan acak | 12,5% | 14,7% | 12,0% | 26,5% | 24,8% | 25,5% |
| Rata-rata semua paket | 14,2% | 14,2% | 12,0% | 24,7% | 24,7% | 24,7% |

\* KNN perencanaan menumpuk 63 dari 200 paket teratasnya di satu satker.

Cara membaca:
- **Perencanaan.** Di 5% teratas (dasar peta), ensemble paling baik di antara cara yang tidak menumpuk di satu satker, dan tetap baik di provinsi uji. Di puncak daftar (P@200), HBOS dan IF lebih tinggi, tetapi di 5% teratas keduanya jauh lebih lemah (16,6–17,8%). IF terutama mengangkat pengadaan langsung berpagu besar (RF2: 33,5% dari 200 teratasnya).
- **Pelaksanaan.** Skor-z sederhana jauh lebih tinggi di 200 teratas (79,5%), karena red flag pelaksanaan dihitung dari besaran yang sama dengan fiturnya:
  - porsi pagu di satker sangat dekat dengan RF5 (AUC 0,79);
  - pagu sangat dekat dengan RF2 (AUC 0,90).
  
  Jadi cara satu-fitur mudah "menemukan" red flag tersebut. Di 5% teratas keunggulannya hilang, dan di provinsi uji skor-z lebih rendah (21,3% vs 25,3%). LOF sendirian paling sejalan dengan red flag pelaksanaan, tetapi paling sering salah menandai paket wajar buatan (39%) dan paling buruk di perencanaan (P@200 5,5%).

### 6.3 Perlukah tiga model digabung? (ablasi)

Sembilan cara diuji: IF, LOF, AE masing-masing; tiga pasangan; serta rata-rata, maksimum, dan median ketiganya. Masing-masing dinilai pada 6 ukuran per jalur:
1. P@200;
2. 5% teratas;
3. 5% teratas di provinsi uji;
4. cakupan anomali buatan;
5. salah tanda pada paket wajar buatan;
6. penumpukan satker di 200 teratas.

| Cara | Peringkat rata-rata (1 = terbaik, dari 9) | Peringkat terburuk |
|---|---|---|
| **Rata-rata IF+LOF+AE (dipakai)** | **3,9** | **6** |
| LOF saja | 4,4 | 9 |
| IF+AE | 4,7 | 8 |
| LOF+AE | 4,8 | 9 |
| Maksimum IF+LOF+AE | 4,9 | 9 |
| Median IF+LOF+AE | 5,3 | 7 |
| IF+LOF | 5,5 | 8 |
| AE saja | 5,5 | 9 |
| IF saja | 6,0 | 9 |

Ketiga model juga memang melihat hal berbeda:
- Korelasi skor IF dengan LOF hanya 0,21–0,25.
- Irisan 5% teratas antar model hanya 9–25%.
- Dari paket yang ditandai ensemble, hanya 7–8% yang juga ditandai ketiga model sekaligus. 42–44% hanya ditandai satu model, dan 16–19% tidak masuk 5% teratas model mana pun.

Kesimpulannya sejalan dengan Krčmar (2026) dan Han et al. (2022): ensemble tidak selalu yang paling tinggi, tetapi paling konsisten. Memilih satu model tanpa label juga tidak bisa diandalkan (Ma et al., 2021).

### 6.4 Anomali buatan

Persentase 1.000 paket buatan yang masuk 5% skor teratas. Gambarnya ada di [gambar-anomali-buatan.png](/mnt/project-files/model-v3/gambar-anomali-buatan.png).

| Tipe | Perencanaan: ensemble | Perencanaan: skor-z | Pelaksanaan: ensemble | Pelaksanaan: skor-z |
|---|---|---|---|---|
| Ekstrem (global) | 100% | 95% | 100% | 100% |
| Lokal | 72% | 39% | 66% | 33% |
| Gabungan antarfitur | 63% | 1% | 39% | 2% |
| Kelompok kembar | 100% | 46% | 94% | 30% |
| Realisasi 1,3–3× pagu | – | – | 56% | 63% |
| Pagu digelembungkan 5–20× | 0% | 12% | 1% | 6% |
| Dinaikkan ke dekat ambang PL | 11% | 11% | 12% | 13% |
| Kontrol: paket wajar (makin kecil makin baik) | 28% | 9% | 24% | 5% |

Ensemble unggul jelas pada pola lokal, gabungan, dan kelompok. Di situlah nilai tambahnya dibanding cara per fitur.

Manipulasi yang meniru paket wajar tidak tertangkap model mana pun. Karena itu red flag tetap ditampilkan di samping skor. Model dan red flag saling melengkapi, bukan saling menggantikan.

### 6.5 Data luar: SPI KPK 2024

KPK hanya mengumumkan 10 provinsi dengan skor SPI 2024 tertinggi dan 10 terendah. Kedua kelompok dibandingkan dengan uji Mann-Whitney satu arah. Gambarnya ada di [gambar-spi.png](/mnt/project-files/model-v3/gambar-spi.png).

| Ukuran (median per provinsi) | 10 SPI terendah | 10 SPI tertinggi | p | Tanpa Papua (5 vs 10 provinsi) |
|---|---|---|---|---|
| Pelaksanaan: paket tidak lazim, ambang 5% | 15,3% | 4,3% | < 0,001 | 7,5% vs 4,3% (p = 0,002) |
| Pelaksanaan: paket tidak lazim, ambang 1% | 2,3% | 0,7% | 0,001 | 1,8% vs 0,7% (p = 0,004) |
| Perencanaan: paket tidak lazim, ambang 5% | 7,6% | 4,7% | 0,12 | 3,4% vs 4,7% (p = 0,74) |
| Perencanaan: paket ber-red flag | 30,1% | 8,4% | 0,002 | 14,9% vs 8,4% (p = 0,065) |
| Pelaksanaan: paket ber-red flag | 42,7% | 21,0% | 0,016 | 37,7% vs 21,0% (p = 0,038) |

Catatan:
- SPI menilai integritas instansi secara umum, bukan khusus pengadaan.
- Hanya 20 provinsi yang skornya diumumkan.
- Ini bukti tingkat provinsi, bukan bukti per paket.

Hasil pelaksanaan tetap bukti luar yang kuat, karena didapat tanpa memakai SPI sama sekali saat membangun model.

## 7. Batasan yang perlu ditulis jujur

1. **Tidak ada label kebenaran.** Semua bukti tidak langsung: red flag (acuan pengganti), SPI (tingkat provinsi), anomali buatan (skenario). Kalimat di naskah sebaiknya "paket yang diprioritaskan untuk ditelaah", bukan "paket bermasalah".
2. **Manipulasi yang dibuat tampak wajar tidak tertangkap**, yaitu dekat ambang dan pagu digelembungkan. Ini sifat dasar deteksi ketidaklaziman, bukan kesalahan kode. Penyelesaiannya: tampilan gabungan skor dan red flag, serta data harga satuan di penelitian lanjutan.
3. **Pelaksanaan: skor-z mengalahkan ensemble di 200 teratas.** Penyebabnya tumpang tindih red flag dengan fitur (bagian 6.2). Ini perlu dibahas di Bab 4, bukan disembunyikan.
4. **Pelaksanaan: 5% teratas lemah di provinsi uji** (25,3% vs 24,7%). Peta pelaksanaan juga belum sejalan dengan red flag per provinsi (ρ 0,32, p = 0,052). Bukti terkuat jalur ini justru dari luar, yaitu SPI.
5. **Perencanaan: puncak daftar lemah tanpa RF4**, dan sepertiga 200 teratas berpagu sangat kecil. Untuk perencanaan, yang paling bisa dipegang adalah 5% teratas (peta), bukan 50 paket teratas.
   - 22,5% dari 200 teratas berpagu di bawah Rp1 jt (rata-rata semua paket 11,6%). Peringkat 1 bahkan paket Rp29 rb.
   - Paket seperti ini lebih mirip salah isi data atau belanja sangat kecil daripada risiko.
   - Bisa dipertimbangkan batas bawah pagu sebagai pemeriksaan kualitas data. Saat ini yang dibuang hanya pagu ≤ Rp10 rb (keputusan Tio).
6. **Papua.** Paket pelaksanaan provinsi Papua hanya 1,2% dari semua paket, tetapi 4,6% dari paket tidak lazim. Papua Selatan hanya punya 37 paket pelaksanaan dan Papua Pegunungan 15, jadi proporsinya mudah berubah. Hal ini sejalan dengan SPI Papua yang rendah, tetapi bisa juga karena pola provinsi baru. Dashboard sudah memberi tanda * untuk provinsi dengan kurang dari 100 paket.
7. **Keputusan fitur perencanaan diambil setelah putaran pertama** (bagian 4). Tulis apa adanya, beserta hasil provinsi uji yang mendukungnya.

## 8. Keputusan untuk Tio

1. **Pakai model v3 di naskah?** Rekomendasi: **ya**. Dashboard sudah v3; naskah menyusul setelah Tio setuju, di tab baru.
2. **R055 sebagai RF7?**
   - a. Tidak ditambah; R055 dipakai hanya sebagai uji lintas tahap dan saran penelitian lanjutan (**rekomendasi**: daftar 6 red flag sudah disetujui, dan R055 mirip RF3).
   - b. Ditambah sebagai RF7 khusus pelaksanaan.
3. **Telaah buta oleh manusia?**
   - a. Minta dosen atau satu praktisi pengadaan menilai lembar [lembar-telaah-buta.xlsx](/mnt/project-files/validasi-v3/telaah-buta/lembar-telaah-buta.xlsx), sekitar 1 jam untuk 80 paket (**rekomendasi**, karena ini satu-satunya bukti dari penilaian manusia). File kunci jangan dibuka sebelum selesai dinilai. Hasilnya dihitung dengan `r5_analisis_telaah.py`.
   - b. Tidak dilakukan, ditulis sebagai saran.
4. **Uji mana yang masuk Bab 3?** Rekomendasi:
   - Inti (Bab 3 dan Bab 4):
     - kesesuaian red flag (Precision@K, 5% teratas, provinsi pilih/uji);
     - pembanding dan ablasi;
     - anomali buatan;
     - kestabilan seed;
     - uji hapus SHAP;
     - SPI.
   - Pendukung (lampiran atau satu paragraf Bab 4):
     - *bootstrap*;
     - kepekaan ambang;
     - tingkat satker;
     - lintas tahap.

## 9. Bagian naskah yang terdampak (dikerjakan setelah Tio setuju, di tab baru)

| Bagian | Perubahan |
|---|---|
| Bab 1 Batasan Masalah | Red flag v3; evaluasi juga memakai anomali buatan dan SPI; tidak ada label kebenaran |
| Bab 2 Dasar Teori | Tambah sub-bahasan evaluasi tanpa label (anomali buatan, Han et al., 2022), uji *bunching* untuk red flag (Bertanha et al., 2021), dan evaluasi penjelasan (Nauta et al., 2023) |
| Bab 3 Tabel 3.2 Fitur | Perencanaan tanpa porsi pengadaan langsung dan porsi *e-purchasing* satker |
| Bab 3 Tabel 3.3 Red Flag | RF1 konstruksi dua jendela; RF5 definisi OCP R040 |
| Bab 3 subbab model | Skor rata-rata 5 seed; cara memilih pengaturan (provinsi pilih/uji) |
| Bab 3 subbab evaluasi | Daftar uji validitas (bagian 8 nomor 4) |
| Daftar Pustaka | Referensi baru di bagian 10 |

## 10. Referensi baru (semua bisa diakses gratis, 2021–2026)

Sudah ada di Library atau naskah: Open Contracting Partnership (2024), Decarolis dan Giorgiantonio (2022), Han et al. (2022), Krčmar (2026), Perpres 46/2025.

Baru, bisa dibuka tanpa berlangganan:
1. Bertanha, M., McCallum, A. H., & Seegert, N. (2021). *Better bunching, nicer notching* (arXiv:2101.01170). arXiv. https://doi.org/10.48550/arXiv.2101.01170
   - Dasar uji penumpukan di bawah ambang.
   - Versi jurnalnya (Journal of Econometrics, 2023) berbayar, jadi yang dikutip versi arXiv.
2. Lyra, M. S., Damásio, B., Pinheiro, F. L., & Bacao, F. (2022). Fraud, corruption, and collusion in public procurement activities, a systematic literature review on data-driven methods. *Applied Network Science, 7*(1), Article 83. https://doi.org/10.1007/s41109-022-00523-6
   - Akses terbuka (CC BY 4.0).
   - Tinjauan metode berbasis data untuk pengadaan.
3. Tas, B. (2021). *Detecting authorities that manipulate public procurement* [Preprint]. Research Square. https://doi.org/10.21203/rs.3.rs-144691/v1
   - CC BY 4.0.
   - Contoh pemakaian penumpukan di bawah ambang untuk menandai instansi.
4. Ma, M. Q., Zhao, Y., Zhang, X., & Akoglu, L. (2021). *The need for unsupervised outlier model selection: A review and evaluation of internal evaluation strategies* (arXiv:2104.01422). arXiv. https://doi.org/10.48550/arXiv.2104.01422
   - Memilih satu model tanpa label hasilnya tidak lebih baik dari pilihan acak. Karena itu pengaturan ditetapkan di awal dan diuji di provinsi lain.
   - Versi jurnalnya (SIGKDD Explorations, 2023) ada di ACM, jadi yang dikutip versi arXiv.
5. Li, Z., Zhao, Y., Hu, X., Botta, N., Ionescu, C., & Chen, G. H. (2022). *ECOD: Unsupervised outlier detection using empirical cumulative distribution functions* (arXiv:2201.00382). arXiv. https://doi.org/10.48550/arXiv.2201.00382
   - Salah satu pembanding.
6. Perini, L., Bürkner, P.-C., & Klami, A. (2023). Estimating the contamination factor's distribution in unsupervised anomaly detection. *Proceedings of the 40th International Conference on Machine Learning, 202*, 27668–27679. https://proceedings.mlr.press/v202/perini23a.html
   - Proporsi anomali (ambang 5%) tidak bisa diketahui pasti, jadi perlu uji kepekaan 1/5/10%.
7. Nauta, M., Trienes, J., Pathak, S., Nguyen, E., Peters, M., Schmitt, Y., Schlötterer, J., van Keulen, M., & Seifert, C. (2023). From anecdotal evidence to quantitative evaluation methods: A systematic review on evaluating explainable AI. *ACM Computing Surveys, 55*(13s), 1–42. https://doi.org/10.1145/3583558
   - Akses terbuka (CC BY 4.0).
   - Dasar uji hapus fitur untuk SHAP.
8. Komisi Pemberantasan Korupsi. (2025, 30 Januari). *Ini 10 kementerian/lembaga dan pemerintah daerah dengan skor SPI 2024 terbaik*. https://kpk.go.id/id/ruang-informasi/berita/ini-10-kementerianlembaga-dan-pemerintah-daerah-dengan-skor-spi-2024-terbaik
9. GoodStats. (2025). *10 provinsi paling rentan korupsi 2024*. https://data.goodstats.id/statistic/10-provinsi-paling-rentan-korupsi-2024-bSA5x
   - Sumber sekunder yang mengutip dasbor SPI KPK.
   - Tiga angkanya cocok dengan berita detik.com 22 Januari 2025.

## 11. File

- Ringkasan ini: `validasi-v3/ringkasan-validasi-v3.md`
- Uji red flag: `validasi-v3/r1_redflag.py` dan `r1_*.csv`; gambar `validasi-v3/gambar/penumpukan-ambang.png`
- Pemilihan fitur: `validasi-v3/r6_pilih_v3.py`, `r6b_pilih_E.py`, `r6c_lima_persen.py` dan CSV-nya
- Model v3: `model-v3/` (`ens3.py`, `s2_model.py`, `s3_shap.py`, `s4_export.py`). Jalankan ulang semuanya dengan `bash jalankan.sh`
- Uji validitas: `model-v3/s5_validasi.py`, `s6_shap_hapus.py`, `s7_ablasi.py`, `s8_spi.py`, `s9_satker.py`; hasil di `model-v3/validasi/*.csv`
- Gambar: `model-v3/gambar-anomali-buatan.png`, `model-v3/gambar-spi.png`
- Telaah buta: `validasi-v3/telaah-buta/` (lembar, kunci, dan `r5_analisis_telaah.py` untuk menghitung hasilnya)
