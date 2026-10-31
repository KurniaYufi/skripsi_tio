# Ringkasan Perubahan Model v4

Dibuat 2026-10-29. Isinya semua hal yang berubah dari rancangan awal (model v1, sesuai keputusan 28 Oktober) sampai model v4 yang sekarang dipakai di dashboard. Bagian yang tidak disebut di sini berarti tetap sama.

## 1. Sekilas: dari v1 ke v4

| Versi | Perubahan utama | Kenapa |
|---|---|---|
| v1 | Rancangan awal: 6 red flag, fitur hasil review, IF + LOF + Autoencoder | Sesuai keputusan 28 Oktober |
| v2 | Kolom metode pengadaan dibuang dari fitur; tiga fitur baru; pengaturan model jalur perencanaan disesuaikan | Hasil v1 "bocor": metode penunjukan langsung ada di fitur sekaligus di red flag, sehingga angkanya tinggi karena berputar |
| v3 | Dua red flag diperbaiki berdasarkan data; dua fitur kebiasaan satker dibuang dari jalur perencanaan; skor dirata-rata dari 5 kali pelatihan | Supaya acuan penilaian lebih kuat, perencanaan tidak bergantung pada penunjukan langsung, dan hasil lebih stabil |
| **v4** | Jalur perencanaan: paket berpagu di bawah Rp1 jt tidak ikut dinilai, dan perbandingan pagu dibuat **satu arah** | Daftar teratas v3 banyak berisi paket bernilai sangat kecil yang lebih mirip salah isi data |

## 2. Data

| | Rancangan awal | v4 | Alasan |
|---|---|---|---|
| Lingkup | RUP & realisasi 2025, paket penyedia, tanpa "Dikecualikan", pagu > Rp10 rb | Sama | – |
| Jalur perencanaan | 343.919 paket | **303.930 paket** (pagu minimal **Rp1 jt**) | Paket di bawah Rp1 jt banyak yang jenisnya tidak cocok, misalnya "tinta printer" dicatat sebagai Pekerjaan Konstruksi. Ini masalah isian data, bukan risiko pengadaan. |
| Jalur pelaksanaan | 105.575 paket (realisasi sampai serah terima) | Sama | Masalah paket kecil hampir tidak ada di jalur ini (3% dari 200 teratas). |

## 3. Fitur

### 3.1 Jalur perencanaan (data RUP)

| Fitur | Rancangan awal | v4 | Alasan perubahan |
|---|---|---|---|
| Pagu | Dipakai | Dipakai | – |
| Pagu dibanding paket sejenis (jenis dan metode sama) | Dipakai | Dipakai, **satu arah** (v4) | Lihat penjelasan "satu arah" di bawah tabel |
| Porsi pagu di satker | Dipakai | Dipakai | – |
| Jumlah paket satker | Dipakai | Dipakai | – |
| Jenis pengadaan | Dipakai | Dipakai | – |
| Pagu dibanding median paket di satker yang sama | – | **Baru** (v2), **satu arah** (v4) | Paket yang jauh lebih besar dari kebiasaan satkernya sendiri patut dicek |
| Metode pengadaan | Dipakai | **Dibuang** (v2) | Penunjukan langsung juga dipakai sebagai red flag. Kalau ikut jadi fitur, model "menyontek" jawaban dan penilaiannya berputar. |
| PDN dan UMK (ya/tidak) | Dipakai | **Dibuang** (v2) | Hampir semua paket berstatus "ya" (98,7% dan 96%). Paket berstatus "tidak" jadi langka dan naik ke daftar teratas tanpa kaitan dengan red flag. |
| Proporsi pengadaan langsung di satker | Dipakai | **Dibuang** (v3) | Model mengangkat paket penunjukan langsung lewat kebiasaan satker, bukan lewat ciri paketnya sendiri |
| Porsi *e-purchasing* di satker | – | Ditambah (v2), lalu **dibuang** (v3) | Alasannya sama dengan baris di atas |

**Apa itu satu arah?** Dulu, paket yang 1.000 kali lebih *kecil* dari biasanya dianggap sama anehnya dengan paket yang 1.000 kali lebih *besar*. Sekarang, untuk dua fitur perbandingan pagu, hanya pagu yang lebih **besar** dari biasanya yang bisa menaikkan skor. Pagu yang lebih kecil dianggap normal. Alasannya: red flag dan risiko pengadaan berkaitan dengan pagu besar atau dekat ambang, bukan pagu kecil. Nilai pagunya sendiri tetap dua arah.

### 3.2 Jalur pelaksanaan (RUP + realisasi)

Tidak berubah sejak v2.

| Fitur | Rancangan awal | v4 | Alasan perubahan |
|---|---|---|---|
| Semua fitur perencanaan di atas, kecuali metode | Dipakai | Dipakai | – |
| Proporsi pengadaan langsung di satker | Dipakai | Dipakai | Di jalur ini tidak membuat model bergantung pada penunjukan langsung |
| PDN dan UMK (ya/tidak), porsi nilai PDN dan UMK | Dipakai | Dipakai | Di jalur ini hasilnya lebih baik bila dipakai |
| Rasio realisasi terhadap pagu, selisih realisasi dan pagu | Dipakai | Dipakai | – |
| Perubahan metode, sumber transaksi | Dipakai | Dipakai | – |
| Metode pengadaan | Dipakai | **Dibuang** (v2) | Sama dengan jalur perencanaan |
| Pagu dibanding median paket di satker | – | **Baru** (v2) | Sama dengan jalur perencanaan |
| Porsi *e-purchasing* di satker | – | **Baru** (v2) | Melengkapi profil cara belanja satker; daftar teratas tidak lagi didominasi satu satker (32 → 17 paket) |
| Rasio realisasi dibanding paket sejenis | – | **Baru** (v2) | Realisasi 90% bisa wajar untuk satu jenis paket tetapi janggal untuk jenis lain |

## 4. Red flag

Red flag tidak dimasukkan ke model. Gunanya hanya sebagai acuan untuk menilai apakah paket yang diprioritaskan model memang lebih sering bermasalah.

| Red flag | Jalur | Rancangan awal | v4 | Alasan perubahan |
|---|---|---|---|---|
| RF1 Pengadaan langsung mendekati ambang | Keduanya | 90–100% ambang (barang/jasa lainnya Rp200 jt, konstruksi Rp400 jt, konsultansi Rp100 jt) | Sama, **ditambah** konstruksi Rp180–200 jt | 2025 tahun peralihan aturan (Perpres 46/2025). Data menunjukkan paket konstruksi masih menumpuk tepat di bawah ambang lama Rp200 jt (2,9 kali dari perkiraan), sedangkan di ambang baru Rp400 jt tidak. |
| RF2 Pengadaan langsung melebihi ambang | Keduanya | Pagu di atas ambang | Sama | – |
| RF3 Indikasi pemecahan paket | Keduanya | Paket bernama mirip di satker dan jenis yang sama, masing-masing di bawah ambang tetapi jumlahnya melewati ambang | Sama | – |
| RF4 Penunjukan langsung | Keduanya | Metode penunjukan langsung | Sama | – |
| RF5 Penyedia dominan | Pelaksanaan | Penyedia yang jumlah paketnya di satker termasuk 5% terbanyak | **Diganti**: satu penyedia menerima lebih dari 40% nilai realisasi satker yang punya minimal 5 paket | Definisi lama menandai 21% paket dan isinya hampir sama dengan "satker besar". Definisi baru mengikuti panduan OCP (2024) dan menandai 2.910 paket. |
| RF6 Penyedia serba-ada | Pelaksanaan | Penyedia yang menang di 3 jenis pengadaan atau lebih | Sama | – |

## 5. Cara model menghitung skor

| | Rancangan awal | v4 | Alasan |
|---|---|---|---|
| Model | IF + LOF + Autoencoder, skor dirata-rata | Sama | Dari 9 cara menggabungkan model yang diuji, rata-rata tiga model paling konsisten |
| Pelatihan | 1 kali | **Rata-rata 5 kali** dengan angka acak (seed) berbeda | Dengan 1 kali pelatihan, daftar teratas banyak berubah tiap kali dilatih ulang |
| Pengaturan jalur perencanaan | Bawaan | Penskalaan *quantile*, Isolation Forest 2.048 sampel per pohon, Autoencoder lapisan tengah 3 neuron (v2) | Pagu sangat timpang (median Rp15,9 jt, maksimum Rp2,29 T) dan datanya besar |
| Pengaturan jalur pelaksanaan | Bawaan | Bawaan | Hasilnya lebih baik dengan pengaturan bawaan |
| "Paket tidak lazim" | 5% skor tertinggi | Sama | – |

## 6. Cara menilai hasil

Rancangan awal hanya memakai Precision@K (berapa persen paket teratas yang punya red flag). Sekarang ada uji tambahan supaya hasilnya bisa dibuktikan dari beberapa arah:

1. **Provinsi pilih dan provinsi uji.** Pengaturan dipilih di 19 provinsi, lalu dicek di 19 provinsi lain, supaya hasil tidak hanya cocok untuk data yang dipakai memilih.
2. **Tanpa RF4.** Precision@K dihitung ulang tanpa penunjukan langsung, untuk memastikan model tidak hanya menangkap satu red flag.
3. **Pembanding sederhana.** Hasil dibandingkan dengan urutan acak, pagu terbesar, skor-z, dan beberapa metode lain.
4. **Anomali buatan.** Paket tidak wajar sengaja disisipkan, lalu dicek apakah model menemukannya.
5. **Kestabilan.** Model dilatih ulang dengan seed lain, lalu dilihat berapa banyak daftar teratas yang tetap sama.
6. **Uji SHAP.** Fitur yang disebut SHAP diganti, lalu dicek apakah skor memang turun.
7. **Data luar.** Hasil per provinsi dibandingkan dengan skor integritas SPI KPK 2024.

## 7. Hasil v4

Angka v1 tidak dibandingkan langsung karena red flag dan fiturnya berbeda, dan angka v1 ikut terdongkrak oleh kebocoran penunjukan langsung.

| Uji | Perencanaan v3 | **Perencanaan v4** | Pelaksanaan (v3 = v4) |
|---|---|---|---|
| 200 teratas yang punya red flag (rata-rata semua paket) | 25,5% (14,2%) | **38,5% (15,8%)** | 48,0% (24,7%) |
| 50–200 teratas tanpa menghitung RF4 | 9,3%, di bawah rata-rata | **22,0%, di atas rata-rata 14,6%** | 49,2% (23,9%) |
| 5% teratas yang punya red flag | 32,6% | **38,3%** | 29,2% |
| Provinsi uji, 50–200 teratas | 14,7% (12,0%) | **20,7% (13,8%)** | 38,0% (24,7%) |
| Paket di bawah Rp10 jt di 200 teratas | 36,5% | **13%** | 7,5% |
| Dari 10 paket di 200 teratas, yang tetap sama saat dilatih ulang | sekitar 8 | sekitar 7 | sekitar 7 |
| Peta provinsi sejalan dengan red flag | ya (ρ 0,55) | ya, lebih lemah (ρ 0,40) | belum (ρ 0,32) |
| Sejalan dengan SPI KPK 2024 | tidak | tidak | ya (15,3% vs 4,3%) |

**Yang membaik:** daftar teratas perencanaan lebih sering punya red flag, tidak lagi bergantung pada penunjukan langsung, dan hampir bebas paket bernilai sangat kecil.
**Yang sedikit turun:** kestabilan dan keselarasan peta perencanaan.
**Yang tetap jadi batasan:** paket yang sengaja dibuat tampak wajar (pagu dinaikkan ke dekat ambang atau digelembungkan) tidak tertangkap model mana pun. Karena itu red flag tetap ditampilkan di samping skor.

## 8. Yang perlu ditulis jujur di naskah

- Fitur perencanaan (v3) dan cara satu arah (v4) dipilih **setelah** melihat hasil putaran sebelumnya. Tulis apa adanya, beserta hasil provinsi uji yang mendukungnya.
- Pada v4, LOF dan Autoencoder secara tunggal lemah di 200 teratas perencanaan; puncak daftar terutama didorong Isolation Forest. Rata-rata tiga model tetap paling konsisten di semua ukuran.

## 9. Bagian naskah yang perlu disesuaikan (menunggu persetujuan, di tab baru)

| Bagian | Perubahan |
|---|---|
| Bab 1 Batasan Masalah | Paket perencanaan minimal Rp1 jt; evaluasi memakai beberapa uji di bagian 6; tidak ada label kebenaran |
| Bab 3 Pra-pemrosesan | Batas bawah pagu Rp1 jt di jalur perencanaan |
| Bab 3 Tabel 3.2 Fitur | Isi bagian 3 |
| Bab 3 Tabel 3.3 Red Flag | RF1 ditambah jendela Rp180–200 jt; RF5 definisi OCP |
| Bab 3 subbab model | Rata-rata 5 seed; pengaturan jalur perencanaan; fitur pagu satu arah |
| Bab 3 subbab evaluasi | Daftar uji di bagian 6 |

Rincian lebih lengkap: [ringkasan-validasi-v3.md](/mnt/project-files/validasi-v3/ringkasan-validasi-v3.md) (red flag, uji validitas) dan [hasil-pagu-kecil.md](/mnt/project-files/validasi-v3/pagu-kecil/hasil-pagu-kecil.md) (perubahan v4).
