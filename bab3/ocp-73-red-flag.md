# Daftar 73 Red Flag OCP (2024) dan Kecocokannya dengan Data Kita

Sumber: Open Contracting Partnership (2024), *Red flags in public procurement*, Tabel 3 (hlm. 19–21). PDF ada di Library: `/mnt/project-files/OCP2024-RedFlagProcurement-1.pdf`. Terjemahan nama red flag dibuat bebas supaya mudah dipahami; kode R### mengikuti aslinya.

Data kita hanya berisi RUP (nama paket, satker, metode, jenis, pagu, PDN, UMK) dan realisasi (penyedia, nilai realisasi, sumber transaksi, tahapan). **Tidak ada** data peserta/penawaran, tanggal, dokumen tender, sanggahan, atau data kepemilikan perusahaan. Karena itu sebagian besar red flag OCP tidak bisa dihitung.

Keterangan kolom "Data kita":
- **Dipakai**: sudah menjadi red flag di model v4.
- **Bisa, tidak dipakai**: bisa dihitung, tetapi sengaja tidak dijadikan red flag (alasannya di catatan).
- **Sebagian**: hanya sebagian yang bisa didekati.
- **Tidak**: butuh data yang tidak kita punya.

## 1. Transparansi rendah (6)

| Kode | Red flag | Data kita | Catatan |
|---|---|---|---|
| R001 | Dokumen perencanaan tidak tersedia | Tidak | Butuh data dokumen |
| R004 | Pengumuman tender tidak memadai | Tidak | Butuh data pengumuman |
| R005 | Informasi dan dokumen penting tender tidak tersedia | Tidak | |
| R013 | Banyak memakai metode tanpa persaingan | Bisa, tidak dipakai | Dihitung per satker (porsi pengadaan langsung/penunjukan langsung). Pernah jadi fitur, dibuang di v3 karena membuat model bergantung pada RF4 |
| R039 | Pertanyaan peserta tidak dijawab | Tidak | |
| R063 | Kontrak tidak dipublikasikan | Tidak | |

## 2. Persaingan rendah (5)

| Kode | Red flag | Data kita | Catatan |
|---|---|---|---|
| R018 | Hanya satu penawaran masuk | Tidak | Butuh data jumlah penawar |
| R019 | Jumlah penawar sedikit untuk kategori barang itu | Tidak | |
| R040 | Satu penyedia menguasai porsi besar kontrak satu pembeli | **Dipakai** | = **RF5** penyedia dominan (> 40% nilai realisasi satker, satker ≥ 5 paket) |
| R050 | Pangsa pasar penyedia tinggi | Bisa, tidak dipakai | Perlu definisi "pasar" (jenis/wilayah); mirip RF5 di tingkat yang lebih luas |
| R051 | Konsentrasi pasar tinggi | Bisa, tidak dipakai | Ukuran tingkat pasar, bukan tingkat paket |

## 3. Penipuan/pemalsuan (*fraud*) (12)

| Kode | Red flag | Data kita | Catatan |
|---|---|---|---|
| R042 | Alamat/nomor telepon penyedia tidak wajar | Tidak | Butuh data profil penyedia |
| R045 | Penyedia tidak terdaftar di registri usaha | Tidak | |
| R046 | Penyedia masuk daftar hitam/sanksi | Tidak | |
| R047 | Penyedia tidak bisa ditelusuri di internet | Tidak | |
| R048 | Penyedia serba-ada (menang di banyak jenis berbeda) | **Dipakai** | = **RF6** (menang di ≥ 3 jenis pengadaan) |
| R064 | Kontrak diubah (adendum) | Tidak | Butuh data adendum |
| R065 | Adendum mengurangi item | Tidak | |
| R066 | Adendum menambah item | Tidak | |
| R067 | Barang/pekerjaan tidak diserahkan | Tidak | Data kita hanya memuat paket yang sudah serah terima |
| R068 | Nilai transaksi melebihi nilai kontrak | Sebagian | Didekati dengan realisasi > pagu. Diuji sebagai kandidat, tidak dijadikan red flag karena sama dengan fitur rasio realisasi (evaluasi jadi berputar) |
| R069 | Adendum menaikkan harga | Tidak | |
| R073 | Hasil pekerjaan tidak sesuai spesifikasi | Tidak | |

*Catatan istilah: di naskah sebaiknya kategori ini disebut "penipuan/pemalsuan" atau dibiarkan *fraud*, sesuai aturan menghindari kata yang menuduh.*

## 4. Risiko kolusi antarpenyedia (19)

Semua butuh data penawaran, peserta, kepemilikan, atau subkontrak, jadi **tidak bisa** dihitung dari data kita.

| Kode | Red flag |
|---|---|
| R017 | Harga satuan item terlalu rendah atau terlalu tinggi |
| R022 | Selisih harga penawaran sangat lebar |
| R023 | Harga penawaran berkelipatan tetap |
| R024 | Harga penawaran dekat dengan pemenang |
| R025 | Terlalu banyak penawaran yang kalah |
| R026 | Banyak penawaran konsorsium |
| R027 | Penawar yang biasanya ikut tiba-tiba tidak ikut |
| R028 | Harga penawaran identik |
| R032 | Penawar punya pemilik manfaat yang sama |
| R033 | Penawar punya pemegang saham utama yang sama |
| R034 | Penawaran dimasukkan dalam urutan yang sama berulang kali |
| R041 | Dokumen penawar berbeda tetapi mirip secara fisik |
| R044 | Kemiripan usaha antarpenawar |
| R053 | Pasangan penawar yang selalu ikut bersama dengan pemenang yang sama |
| R057 | Arisan tender (pemenang bergiliran) |
| R058 | Penawaran dengan potongan harga sangat besar |
| R070 | Penawar yang kalah menjadi subkontraktor pemenang |
| R071 | Kontraktor mensubkontrakkan hampir seluruh pekerjaan |
| R072 | Banyak subkontrak |

## 5. Pengaturan tender (*bid rigging*) (31)

| Kode | Red flag | Data kita | Catatan |
|---|---|---|---|
| R002 | Manipulasi ambang pengadaan | **Dipakai** | = **RF1** pengadaan langsung mendekati ambang (dan uji *bunching* di Bab 3) |
| R003 | Masa pemasukan penawaran terlalu singkat | Tidak | Butuh tanggal |
| R006 | Syarat prakualifikasi tidak wajar | Tidak | |
| R007 | Spesifikasi teknis tidak wajar | Tidak | |
| R008 | Biaya ikut tender tidak wajar | Tidak | |
| R009 | Pembeli menaikkan biaya dokumen tender | Tidak | |
| R010 | Memakai metode tanpa persaingan tanpa alasan kuat | **Dipakai** (didekati) | = **RF4** penunjukan langsung dan **RF2** pengadaan langsung melebihi ambang. Alasan pemakaian metode tidak ada di data, jadi hanya bisa ditandai, tidak dinilai |
| R011 | Memecah pembelian untuk menghindari ambang | **Dipakai** | = **RF3** indikasi pemecahan paket |
| R012 | Penunjukan langsung tidak sesuai rencana pengadaan | Sebagian | Didekati dengan "metode berubah dari RUP ke realisasi"; sudah jadi **fitur** jalur pelaksanaan, bukan red flag |
| R014 | Jarak pengumuman ke pembukaan penawaran terlalu singkat | Tidak | Butuh tanggal |
| R015 | Jarak pembukaan ke evaluasi penawaran terlalu lama | Tidak | Butuh tanggal |
| R016 | Nilai tender lebih tinggi/rendah dari rata-rata kategori | Sebagian | Sama dengan **fitur** "pagu dibanding paket sejenis", jadi tidak dipakai sebagai red flag |
| R020 | Tender disanggah | Tidak | |
| R021 | Banyak memakai kriteria evaluasi yang subjektif | Tidak | |
| R029 | Harga penawaran menyimpang dari hukum Benford | Tidak | Butuh harga penawaran |
| R030 | Penawaran yang terlambat justru menang | Tidak | |
| R031 | Harga pemenang sangat dekat atau di atas HPS | Tidak | Butuh HPS |
| R035 | Semua penawar selain pemenang digugurkan | Tidak | |
| R036 | Penawar termurah digugurkan | Tidak | |
| R037 | Pengguguran tanpa alasan kuat | Tidak | |
| R038 | Terlalu banyak penawaran digugurkan | Tidak | |
| R043 | Kontak penawar sama dengan kontak pejabat | Tidak | |
| R049 | Penunjukan berulang ke penyedia yang sama di bawah ambang | Bisa, tidak dipakai | Diuji di uji lintas tahap (skor perencanaan vs pelaksanaan) |
| R052 | Pembelian awal kecil, lalu diikuti pembelian jauh lebih besar | Tidak | Butuh urutan waktu |
| R054 | Penunjukan langsung lalu adendum melewati ambang | Tidak | Butuh data adendum |
| R055 | Banyak pengadaan langsung ke penyedia yang sama, di atas atau tepat di bawah ambang | Bisa, tidak dipakai | Kandidat RF7; diputuskan tidak ditambah (mirip RF3), dipakai di uji lintas tahap |
| R056 | Pemenang tidak memenuhi kriteria | Tidak | |
| R059 | Selisih besar antara nilai kontrak awal dan akhir | Sebagian | Didekati dengan selisih realisasi dan pagu; sudah jadi **fitur** jalur pelaksanaan |
| R060 | Jarak penetapan pemenang ke tanda tangan kontrak terlalu lama | Tidak | Butuh tanggal |
| R061 | Masa keputusan terlalu singkat | Tidak | |
| R062 | Masa keputusan terlalu lama | Tidak | |

## Ringkasan

| | Jumlah |
|---|---|
| Red flag OCP | 73 |
| Dipakai sebagai red flag di model v4 | 5 kode OCP (R002, R010, R011, R040, R048), menjadi 6 red flag kita karena R010 didekati dua kali (RF2 dan RF4) |
| Bisa dihitung (penuh/sebagian) tetapi sengaja tidak dipakai, atau sudah jadi fitur | 9 (R012, R013, R016, R049, R050, R051, R055, R059, R068) |
| Tidak bisa, karena butuh data penawaran/tanggal/dokumen/profil penyedia | 59 |

Pemetaan ke 6 red flag kita: RF1 = R002, RF2 = R010, RF3 = R011, RF4 = R010, RF5 = R040, RF6 = R048.
Kalimat untuk Batasan Masalah: sebagian besar red flag OCP (misalnya penawar tunggal, R018) membutuhkan data penawaran dan tanggal yang tidak tersedia di data RUP dan realisasi INAPROC, sehingga penelitian ini memakai red flag yang bisa dihitung dari kedua data tersebut.
