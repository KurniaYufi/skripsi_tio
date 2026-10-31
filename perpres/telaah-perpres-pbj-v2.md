# Telaah Konsolidasi Perpres Pengadaan Barang/Jasa untuk Skripsi

Sumber: *Konsolidasi Peraturan Presiden Nomor 16/2018, 12/2021 dan 46/2025 tentang Pengadaan Barang/Jasa Pemerintah* (Biro PBJ Provinsi NTB), file `Konsolidasi-Perpres-PBJ-16-2018-12-2021-46-2025.pdf`. Ditelaah 29 Oktober 2026.

**Versi 2 (30 Oktober 2026):** dicocokkan juga dengan *Konsolidasi Peraturan Presiden (Perpres) tentang Pengadaan Barang/Jasa Pemerintah* oleh Khalid Mustafa (Mei 2025), file `941509065-Konsolidasi-Perpres-Nomor-46-Tahun-2025-Final.pdf`. Hasilnya di bagian 9.

Semua nomor pasal di bawah adalah nomor pasal Perpres 16/2018 sebagaimana telah diubah terakhir dengan Perpres 46/2025 (versi yang berlaku sekarang).

---

## 1. Lima hal paling penting

1. **Perpres 46/2025 baru berlaku 30 April 2025** (Pasal II angka 2; ditetapkan dan diundangkan 30 April 2025, LN 2025 No. 67). Artinya data RUP 2025 sebagian besar disusun **sebelum** aturan baru. RUP Perangkat Daerah diumumkan setelah rancangan Perda APBD disetujui (Pasal 22 ayat (2)), jadi umumnya akhir 2024. Saat itu batas pengadaan langsung konstruksi masih Rp200 juta, belum Rp400 juta. Ini menjelaskan temuan lama: penumpukan paket di bawah Rp200 juta pada konstruksi kuat (2,90x), sedangkan di bawah Rp400 juta tidak nyata (1,10x). Jadi RF1 yang memakai dua jendela untuk konstruksi (180-200 jt dan 360-400 jt) **punya dasar aturan yang jelas**.
2. **Semua red flag yang dipakai punya pasal rujukan** (lihat bagian 3). Yang paling kuat: pemecahan paket dilarang secara tegas di Pasal 20 ayat (2) huruf d.
3. **Penunjukan langsung (RF4) sah dalam 11 keadaan tertentu** (Pasal 38 ayat (5)) dan 10 keadaan untuk jasa konsultansi (Pasal 41 ayat (5)). Jadi di naskah sebaiknya ditulis "perlu dicek alasannya", bukan "menyimpang".
4. **Lingkup data (penyedia saja, tanpa "Dikecualikan") punya dasar pasal**: Pasal 3 ayat (3) membagi cara pengadaan menjadi swakelola dan penyedia; Pasal 61 ayat (1) menyebut jenis pengadaan yang dikecualikan dari Perpres.
5. **Aturan realisasi tidak boleh melampaui anggaran** (Pasal 52 ayat (2)) dan **tambahan nilai kontrak paling banyak 10%** (Pasal 54 ayat (2)) bisa dipakai sebagai dasar aturan pembersihan realisasi di model v5 (catatan ganda, rasio realisasi ekstrem).

---

## 2. Batas nilai yang relevan dengan kolom data INAPROC

Kolom yang dipakai: `metode_pengadaan`, `jenis_pengadaan`, `total_nilai` (pagu RUP / nilai realisasi).

| Batas nilai | Isi aturan | Pasal | Dipakai di model? |
|---|---|---|---|
| ≤ Rp200 juta | Pengadaan langsung barang dan jasa lainnya | Pasal 1 angka 40; Pasal 38 ayat (3) huruf a | Ya (RF1, RF2, RF3) |
| ≤ Rp400 juta | Pengadaan langsung pekerjaan konstruksi (baru di Perpres 46/2025; sebelumnya Rp200 juta) | Pasal 1 angka 40a; Pasal 38 ayat (3) huruf b | Ya (RF1, RF2, RF3) |
| ≤ Rp100 juta | Pengadaan langsung jasa konsultansi; di atas itu wajib seleksi | Pasal 1 angka 41; Pasal 41 ayat (3) dan (6) | Ya (RF1, RF2, RF3) |
| > Rp50 juta | Pengadaan langsung wajib memakai aplikasi pengadaan elektronik yang transaksional (baru) | Pasal 38 ayat (8) | Belum (lihat ide bagian 7) |
| ≤ Rp10 juta | Bentuk kontrak cukup bukti pembelian; HPS tidak wajib disusun | Pasal 28 ayat (2); Pasal 26 ayat (7) | Tidak |
| ≤ Rp50 juta | Bentuk kontrak kuitansi | Pasal 28 ayat (3) | Tidak |
| ≤ Rp200 juta | E-purchasing dan penunjukan langsung dikerjakan Pejabat Pengadaan; di atas itu oleh PPK | Pasal 12 huruf b dan d; Pasal 11 ayat (1) huruf h | Tidak |
| ≤ Rp100 juta | E-purchasing tidak wajib menyusun HPS | Pasal 26 ayat (7) | Tidak |
| > Rp200 juta | Kontrak wajib jaminan pelaksanaan | Pasal 33 ayat (1) | Tidak |
| ≤ Rp15 miliar | Paket barang/konstruksi/jasa lainnya diperuntukkan bagi usaha mikro, kecil, dan koperasi (kecuali butuh kemampuan teknis yang tidak dimiliki UMK) | Pasal 65 ayat (3) dan (4) | Tidak langsung (fitur status UMK) |
| ≥ 40% belanja | Alokasi minimal untuk produk UMK dan koperasi | Pasal 20 ayat (3); Pasal 65 ayat (2) | Tidak langsung (porsi nilai UMK) |
| > Rp100 miliar / > Rp10 miliar | Pemenang ditetapkan PA, bukan Pokja (barang dll. / konsultansi) | Pasal 9 ayat (1) huruf n; Pasal 13 ayat (1) huruf c | Tidak |

Catatan: dasar ambang di Bab 2.2 (dasar-teori-v3, paragraf red flag) sudah benar: Rp200 juta, Rp400 juta, Rp100 juta. Tinggal ditambah pasalnya dan kalimat soal tanggal berlaku (poin 1 di atas).

---

## 3. Dasar aturan untuk red flag (Tabel 3.3)

| No | Red flag | Pasal rujukan | Catatan untuk naskah |
|---|---|---|---|
| 1 | Pengadaan langsung mendekati ambang | Pasal 38 ayat (3); Pasal 41 ayat (3); Pasal II angka 1 huruf a (peralihan) | Nilai di bawah ambang sah. Yang dilihat adalah penumpukan paket tepat di bawah batas. Jendela 180-200 jt pada konstruksi dibenarkan karena RUP 2025 banyak disusun sebelum 30 April 2025. |
| 2 | Pengadaan langsung melebihi ambang | Pasal 38 ayat (3); Pasal 41 ayat (3) dan (6) | Ini satu-satunya red flag yang langsung tidak sesuai aturan tertulis. Tetap bisa karena salah isi metode atau pagu di SIRUP, jadi tulis "tidak sesuai batas nilai", bukan "pelanggaran". |
| 3 | Pemecahan paket | Pasal 20 ayat (2) huruf d ("memecah Pengadaan Barang/Jasa menjadi beberapa paket dengan maksud menghindari Tender/Seleksi") | Pasal menyebut "dengan maksud", jadi data hanya bisa menunjukkan pola, bukan niat. Pasal 20 ayat (1) juga memberi alasan sah pemaketan (lokasi, volume, kemampuan pelaku usaha). |
| 4 | Penunjukan langsung | Pasal 1 angka 39; Pasal 38 ayat (4)-(5); Pasal 41 ayat (4)-(5); Pasal 50 ayat (6) | Hanya mengundang satu pelaku usaha, sehingga tidak ada persaingan. Sah dalam keadaan tertentu (mis. program prioritas, satu-satunya pelaku usaha, *repeat order*, tender ulang gagal). |
| 5 | Penyedia dominan di satu satker | Pasal 6 (prinsip bersaing, adil); Pasal 7 ayat (1) huruf c, e, g (etika: tidak saling memengaruhi, hindari pertentangan kepentingan dan kolusi) | Tidak ada pasal yang melarang satu penyedia mendapat banyak paket. Rujukan utama tetap OCP (2024) R040; Perpres dipakai sebagai dasar prinsip. |
| 6 | Penyedia serba-ada | Pasal 17 ayat (1) (penyedia wajib memenuhi kualifikasi sesuai barang/jasa yang diadakan); Pasal 44 ayat (1) | Penyedia yang menang di banyak jenis pengadaan sekaligus perlu dicek kualifikasinya. Rujukan utama tetap OCP (2024) R048. |

Saran kalimat umum untuk Bab 3: "Red flag pada penelitian ini bukan bukti penyimpangan. Red flag menunjukkan pola yang perlu ditelaah lebih lanjut oleh pengawas, karena sebagian pola tersebut dapat sah menurut Peraturan Presiden Nomor 46 Tahun 2025, misalnya penunjukan langsung dalam keadaan tertentu (Pasal 38 ayat (5))."

---

## 4. Dasar aturan untuk fitur (Tabel 3.2)

| Fitur | Pasal rujukan | Kegunaan di naskah |
|---|---|---|
| Metode pengadaan (one-hot) | Pasal 38 ayat (1) (e-purchasing, pengadaan langsung, penunjukan langsung, tender cepat, tender); Pasal 41 ayat (1) (e-purchasing, pengadaan langsung, penunjukan langsung, seleksi untuk konsultansi) | Menjelaskan kategori yang ada di kolom data |
| Jenis pengadaan (one-hot) | Pasal 3 ayat (1) dan (2); Pasal 1 angka 29-32 | "Terintegrasi" digabung ke Pekerjaan Konstruksi: sesuai Pasal 3 ayat (2) bahwa pengadaan dapat dilakukan secara terintegrasi |
| Produk dalam negeri | Pasal 1 angka 46a; Pasal 19 ayat (1) huruf a; Pasal 66 ayat (1), (11), (12) | Pasal 66 ayat (12): kewajiban PDN **dicantumkan dalam RUP**, jadi kolom ini memang isian resmi RUP |
| Status UMK | Pasal 20 ayat (3); Pasal 65 ayat (1)-(4) | Paket ≤ Rp15 miliar seharusnya untuk UMK (lihat bagian 7) |
| Porsi nilai PDN dan UMK (realisasi) | Pasal 52 ayat (3); Pasal 66; Pasal 76 ayat (4) huruf c-e; Pasal 82 ayat (1a) | Pasal 76 ayat (4): penggunaan PDN dan peruntukan paket untuk usaha kecil termasuk ruang lingkup pengawasan APIP. Pasal 82 ayat (1a): ada sanksi administratif bagi pejabat di satker yang tidak memenuhi target persentase PDN/UMK |
| Rasio realisasi terhadap pagu, selisih realisasi-pagu | Pasal 52 ayat (2) (PPK dilarang berkontrak melebihi anggaran tersedia); Pasal 54 ayat (2) (tambahan nilai kontrak paling banyak 10% dari kontrak awal) | Dasar bahwa realisasi jauh di atas pagu adalah tidak lazim |
| Sumber transaksi (one-hot) | Pasal 1 angka 35 dan Pasal 72 (e-purchasing lewat katalog elektronik); Pasal 38 ayat (8) | Menjelaskan arti E-Katalog, Non Tender, Pencatatan |
| Proporsi pengadaan langsung per satker, jumlah paket satker | Pasal 5 huruf b (pengadaan yang lebih transparan, terbuka, dan kompetitif) | Dasar prinsip saja, tidak ada batas angka |
| Log pagu, rasio pagu terhadap paket sejenis | Pasal 4 huruf a (*value for money*: tepat kualitas, kuantitas, waktu, biaya) | Dasar prinsip saja |

---

## 5. Dasar aturan untuk pra-pemrosesan dan lingkup data

| Aturan di model | Pasal rujukan | Keterangan |
|---|---|---|
| Hanya paket melalui penyedia; swakelola tidak masuk | Pasal 3 ayat (3); Pasal 1 angka 23 dan 26; Pasal 18 ayat (4)-(7) | Swakelola punya tata cara sendiri (tipe I-IV, tanpa metode pemilihan), jadi kolom metode/jenis di RUP berisi "-" |
| Metode "Dikecualikan" dibuang | Pasal 61 ayat (1): BLU/BLUD, tarif yang dipublikasikan luas, praktik bisnis yang mapan, diatur peraturan lain | Paket ini tidak mengikuti aturan metode dan ambang Perpres, jadi red flag ambang tidak berlaku |
| Pemisahan jalur perencanaan (RUP) dan pelaksanaan (realisasi) | Bab IV Pasal 18-22 (perencanaan, RUP, SIRUP); Bab VII Pasal 50-58 (pemilihan, kontrak, serah terima) | Dua jalur model sesuai dua tahap di Perpres |
| Realisasi hanya yang selesai (serah terima) | Pasal 57 ayat (1)-(3): serah terima setelah pekerjaan selesai 100% | Nilai realisasi baru final setelah serah terima |
| B3 catatan ganda dan B5 rasio realisasi ekstrem | Pasal 52 ayat (2); Pasal 54 ayat (2)-(3) | Realisasi > 110% pagu tidak lazim secara aturan; bisa dipakai sebagai alasan tambahan di Bab 3 |
| Metode "Kontes", "Sayembara", "Pembayaran untuk Kontrak Tahun Jamak" digabung jadi "Lainnya" (14 paket) | Kontes/Sayembara hanya disebut di Pasal 9 ayat (1) huruf l, tidak ada di daftar metode Pasal 38 ayat (1)/41 ayat (1); kontrak tahun jamak di Pasal 27 ayat (12) | Penggabungan sudah wajar. "Pembayaran untuk Kontrak Tahun Jamak" (6 paket) adalah pembayaran kontrak lama, bisa juga dibuang |
| Batas bawah pagu Rp1 juta di jalur perencanaan (v4) | Tidak ada pasal untuk Rp1 juta. Batas resmi terdekat Rp10 juta (Pasal 26 ayat (7), Pasal 28 ayat (2)) | Rp1 juta tetap boleh dipakai, tetapi alasannya data (banyak salah isi), bukan aturan. Tulis jujur. |

---

## 6. Istilah untuk Bab 2.2 (hanya yang ada di kolom data)

| Istilah | Definisi singkat menurut Perpres | Pasal | Kolom data |
|---|---|---|---|
| Pengadaan Barang/Jasa Pemerintah | Kegiatan pengadaan oleh K/L/Perangkat Daerah yang dibiayai APBN/APBD, dari identifikasi kebutuhan sampai serah terima | Pasal 1 angka 1 | seluruh data |
| Rencana Umum Pengadaan (RUP) | Daftar rencana pengadaan yang akan dilaksanakan K/L/Perangkat Daerah | Pasal 1 angka 19; Pasal 18 ayat (8); Pasal 22 | file RUP, `kode_rup` |
| SIRUP | Aplikasi tempat pengumuman RUP | Pasal 22 ayat (3) | sumber data RUP |
| Swakelola | Barang/jasa dikerjakan sendiri oleh K/L/PD, K/L/PD lain, ormas, atau kelompok masyarakat | Pasal 1 angka 23 | `cara_pengadaan` |
| Pengadaan melalui Penyedia | Barang/jasa disediakan oleh pelaku usaha | Pasal 1 angka 26 | `cara_pengadaan` |
| Penyedia | Pelaku usaha yang menyediakan barang/jasa berdasarkan kontrak | Pasal 1 angka 28 | `nama_penyedia` |
| Barang, Pekerjaan Konstruksi, Jasa Konsultansi, Jasa Lainnya | Empat jenis pengadaan | Pasal 1 angka 29-32; Pasal 3 ayat (1) | `jenis_pengadaan` |
| E-purchasing | Pembelian barang/jasa melalui katalog elektronik | Pasal 1 angka 35; Pasal 38 ayat (2); Pasal 50 ayat (5) | `metode_pengadaan`, `sumber_transaksi` |
| Katalog elektronik | Platform yang memuat informasi barang/jasa, harga, dan penyedia | Pasal 72 ayat (1) | `sumber_transaksi` (E-Katalog v5/v6) |
| Pengadaan Langsung | Metode pemilihan dengan batas nilai Rp200 juta / Rp400 juta / Rp100 juta | Pasal 1 angka 40, 40a, 41 | `metode_pengadaan` |
| Penunjukan Langsung | Metode pemilihan dalam keadaan tertentu, mengundang satu pelaku usaha | Pasal 1 angka 39; Pasal 50 ayat (6) | `metode_pengadaan` |
| Tender, Tender Cepat, Seleksi | Metode pemilihan bersaing (Seleksi untuk jasa konsultansi) | Pasal 1 angka 36-37; Pasal 38 ayat (6)-(7) | `metode_pengadaan` |
| Pemaketan | Penyusunan paket pengadaan; ada larangan memecah paket untuk menghindari tender | Pasal 20 | dasar RF3 |
| Produk Dalam Negeri | Barang/jasa yang diproduksi di Indonesia dengan tenaga kerja dan bahan baku sebagian/seluruhnya dari dalam negeri | Pasal 1 angka 46a | `produk_dalam_negeri`, `nilai_pdn` |
| Usaha Mikro, Usaha Kecil | Mengacu pada PP tentang koperasi dan UMKM | Pasal 1 angka 45-46 | `status_umk`, `nilai_umk` |
| Kontrak | Perjanjian tertulis PA/KPA/PPK dengan penyedia | Pasal 1 angka 44 | realisasi |
| APIP | Aparat yang melakukan audit, reviu, pemantauan, dan evaluasi | Pasal 1 angka 22; Pasal 76 | pengguna dashboard (Manfaat bagi pengawas) |

Saran kecil untuk dasar-teori-v3 paragraf 1: tahap pengadaan di Perpres dimulai dari **perencanaan** (Bab IV, Pasal 18), lalu persiapan (Bab V), lalu pelaksanaan yang berisi pemilihan dan kontrak (Bab VII). Kalimat "tiga tahap utama, yaitu persiapan, pemilihan, dan pelaksanaan (Kusumadewi et al., 2022)" bisa dilengkapi dengan tahap perencanaan dari Perpres, karena jalur perencanaan di model berasal dari tahap ini.

Untuk Manfaat/Bab 1: Pasal 76 ayat (2) menyebut pengawasan dilakukan lewat audit, reviu, **pemantauan**, dan evaluasi; Pasal 77 ayat (6) meminta kepala daerah memfasilitasi masyarakat mengawasi pengadaan. Dua pasal ini cocok sebagai dasar bahwa dashboard membantu pemantauan oleh APIP dan masyarakat.

---

## 7. Ide tambahan dari Perpres (sudah dicek cepat ke data 2025, BELUM disarankan dipakai)

| Ide | Pasal | Hasil cek data | Pendapat |
|---|---|---|---|
| Pengadaan langsung > Rp50 juta yang hanya "Pencatatan Non Tender" (tidak lewat aplikasi transaksional) | Pasal 38 ayat (8) | 6.622 dari 33.536 paket PL > Rp50 juta di realisasi (19,7%) | Menarik dan punya pasal jelas, tetapi aturan baru berlaku 30 April 2025 dan bertumpang tindih dengan fitur sumber transaksi. Cocok untuk saran penelitian lanjutan. |
| Paket ≤ Rp15 miliar yang tidak ditandai UMK | Pasal 65 ayat (3) | 10.654 dari 343.951 paket (3,1%) | Bertumpang tindih dengan fitur status UMK, dan ada pengecualian teknis di ayat (4). Tidak disarankan jadi red flag. |
| Penumpukan e-purchasing di bawah Rp200 juta (batas Pejabat Pengadaan vs PPK, jaminan pelaksanaan) | Pasal 11 ayat (1) huruf h; Pasal 12 huruf d; Pasal 33 ayat (1) | Rasio 90-100% vs 100-110% = 2,25x (titik pembanding 150 jt 1,14x, 250 jt 1,32x, tetapi 500 jt juga 1,85x) | Ada penumpukan, tetapi sebagian karena angka bulat. Lebih lemah dari RF1 pengadaan langsung (Rp200 juta = 5,51x). Tidak disarankan. |
| Penumpukan pengadaan langsung di bawah Rp50 juta | Pasal 28 ayat (3); Pasal 38 ayat (8) | 1,93x (pembanding 40 jt 1,50x, 60 jt 1,09x) | Lemah, juga terpengaruh angka bulat. Tidak disarankan. |

Konstruksi pengadaan langsung bernilai Rp200-400 juta di RUP 2025: 1.725 paket. Menurut aturan lama ini sudah melewati ambang, menurut Perpres 46/2025 masih sah. Model sekarang memakai batas baru (Rp400 juta) untuk RF2, dan ini sesuai Pasal II angka 1 huruf a (pengadaan yang sudah berjalan dapat dilanjutkan dengan aturan baru). Sebaiknya disebut satu kalimat di Bab 3 atau Batasan.

---

## 8. Catatan sitasi (APA 7)

- File konsolidasi ini **bukan dokumen resmi**. Ia disusun Biro PBJ Provinsi NTB, dan catatan kaki "Catatan: ..." adalah tafsiran mereka, bukan isi Perpres. Di naskah, sitasi tetap ke Perpres aslinya. Konsolidasi cukup dipakai sebagai alat bantu baca.
- Kalau dosen bertanya "dapat dari mana": Perpres 46/2025 dan Perpres 16/2018 tersedia gratis di JDIH BPK (peraturan.bpk.go.id) dan JDIH LKPP. Konsolidasi tersedia di biropbj.ntbprov.go.id.
- Contoh daftar pustaka (gaya peraturan dalam APA 7 versi Indonesia, sama dengan yang sudah dipakai di dasar-teori-v3):
  - Peraturan Presiden Nomor 46 Tahun 2025 tentang Perubahan Kedua atas Peraturan Presiden Nomor 16 Tahun 2018 tentang Pengadaan Barang/Jasa Pemerintah. (2025). Lembaran Negara Republik Indonesia Tahun 2025 Nomor 67.
- Contoh sitasi dalam teks dengan pasal: "(Peraturan Presiden Nomor 46 Tahun 2025, 2025, Pasal 20 ayat (2))".
- Pasal yang tidak diubah oleh Perpres 46/2025 (mis. Pasal 20 ayat (2) huruf d, Pasal 52 ayat (2), Pasal 61 ayat (1) huruf a-d) secara teknis berasal dari Perpres 16/2018. Cukup ditulis "Peraturan Presiden Nomor 16 Tahun 2018 sebagaimana telah diubah terakhir dengan Peraturan Presiden Nomor 46 Tahun 2025" sekali di awal, lalu sitasi singkat seperti di atas.

---

## 9. Pembaruan dari konsolidasi final (Khalid Mustafa, Mei 2025)

**Isi buku.** Buku 1 (hlm. 1-68) berisi naskah konsolidasi Perpres 16/2018, 12/2021, dan 46/2025. Isinya sama dengan versi Biro PBJ NTB. Saya cocokkan pasal-pasal yang dipakai di telaah ini (Pasal 20, 38, 41, 52, 54, 61, 65, 66, 82, Pasal II), dan bunyinya sama. Hanya ada sedikit beda redaksi, misalnya Pasal 66 ayat (12) "dan/atau Dokumen Pemilihan". Jadi **semua temuan di bagian 1-8 tetap berlaku**.

**Yang benar-benar baru adalah Buku 2 (hlm. 69-161): matriks perbedaan aturan lama vs Perpres 46/2025, lengkap dengan kolom keterangan.** Matriks ini berguna karena data 2025 berada di masa peralihan. Perubahan yang berpengaruh ke data dan model:

| Topik | Aturan lama (Perpres 16/2018 jo. 12/2021) | Perpres 46/2025 (berlaku 30 April 2025) | Pengaruh ke skripsi |
|---|---|---|---|
| Ambang pengadaan langsung konstruksi (Pasal 1 angka 40/40a; Pasal 38 ayat (3)) | Rp200 juta, sama dengan barang/jasa lainnya | Rp400 juta, dipisah jadi huruf b | Dasar jendela ganda RF1 dan batas RF2 (bagian 1 poin 1). Matriks menyebut "diperjelas dan dinaikkan menjadi Rp400 juta". |
| Bentuk kontrak SPK konstruksi (Pasal 28 ayat (4)-(5)) | SPK sampai Rp200 juta | SPK sampai Rp400 juta | Ikut berubah bersama ambang pengadaan langsung |
| Kewajiban e-purchasing (Pasal 50 ayat (5)) | Wajib hanya untuk barang/jasa kebutuhan nasional/strategis yang ditetapkan menteri/kepala daerah | **Wajib bila barang/jasa tersedia di katalog elektronik**, dengan pengecualian di ayat (5a)-(5c) atas penilaian PPK | Menjelaskan kenapa e-purchasing mendominasi data 2025 (190.882 dari 344.668 paket penyedia di RUP). Cocok untuk kalimat di Bab 2.2 atau deskripsi data Bab 4. |
| E-purchasing jasa konsultansi (Pasal 41 ayat (1)-(2)) | Belum ada; metode konsultansi hanya seleksi, pengadaan langsung, penunjukan langsung | Ditambah e-purchasing untuk konsultan perorangan/badan usaha di katalog | Kategori "E-Purchasing + Jasa Konsultansi" di data sah sejak 30 April 2025 |
| Kewajiban aplikasi transaksional (Pasal 38 ayat (8); Pasal 41 ayat (7)) | Belum ada | Pengadaan langsung > Rp50 juta, penunjukan langsung, tender cepat, tender, dan seleksi wajib lewat aplikasi transaksional | Dasar ide red flag "Pencatatan Non Tender" (bagian 7). Karena baru, wajar banyak paket awal 2025 masih dicatat manual. |
| Kriteria penunjukan langsung (Pasal 38 ayat (5); Pasal 41 ayat (5)) | Huruf a-i (barang/konstruksi/jasa lainnya) | Ditambah huruf a (program prioritas/arahan Presiden) dan huruf k (*repeat order*); untuk konsultansi aturan lama "*repeat order* paling banyak 2 kali" dihapus | Alasan sah penunjukan langsung makin banyak, jadi RF4 makin perlu ditulis sebagai "perlu dicek alasannya" |
| Peruntukan paket UMK (Pasal 65) | Ayat (4): paket ≤ Rp15 miliar untuk usaha kecil dan/atau koperasi | Ayat (3): paket ≤ Rp15 miliar untuk usaha mikro, usaha kecil, dan koperasi; ayat (2) tetap minimal 40% | **Nomor ayat bergeser** dari (4) ke (3). Di naskah pakai nomor versi 46/2025. |
| Pengecualian (Pasal 61 ayat (1a)) | Belum ada | Pengecualian tidak berlaku untuk kewajiban PDN dan produk UMK | Paket "Dikecualikan" tetap terkena kewajiban PDN/UMK, tetapi tidak mengubah keputusan membuang paket ini dari model (ambang dan metode tetap tidak berlaku) |
| Uang muka (Pasal 29 ayat (2)) | Persentase lama | Uang muka UMK minimal 50% (Rp50-200 juta) dan minimal 30% (Rp200 juta-2,5 miliar) | Tidak ada kolom uang muka di data, tidak dipakai |

**Catatan sitasi.** Buku ini masih draf terbitan pribadi (ISBN dan penerbit masih kosong "xxxxxxxxxx"), dan kata pengantarnya sendiri meminta pembaca tetap merujuk ke peraturan resmi. Jadi buku ini **tidak dikutip** di naskah. Yang dikutip tetap Perpres 46/2025 dan Perpres 16/2018. Matriksnya cukup dipakai sebagai alat bantu untuk menulis kalimat "sebelum/sesudah 30 April 2025".
