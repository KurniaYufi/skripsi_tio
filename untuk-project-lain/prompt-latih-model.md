Saya mahasiswa yang sedang mengerjakan skripsi tentang identifikasi anomali paket pengadaan barang/jasa pemerintah provinsi di Indonesia tanpa label (unsupervised). Tolong latih dan jalankan model dari nol memakai file yang sudah saya unggah. Kerjakan sendiri sampai selesai, dan tanyakan ke saya hanya untuk keputusan yang mengubah tujuan penelitian.

## 1. Data

- `data_rup_2025.csv` (atau versi .zip): Rencana Umum Pengadaan (RUP) 2025 seluruh pemerintah provinsi, sekitar 481 ribu baris. Kolom: nama_instansi, nama_satuan_kerja, tahun_anggaran, cara_pengadaan, metode_pengadaan, jenis_pengadaan, nama_paket, kode_rup, sumber_dana, produk_dalam_negeri, status_umk, total_nilai (pagu).
- `dara_realisasi_2025.csv` (atau versi .zip): realisasi/transaksi 2025. Kolom: nama_instansi, nama_satuan_kerja, kode_paket, kode_rup, tahun_anggaran, sumber_transaksi, sumber_dana, nama_penyedia, metode_pengadaan, jenis_pengadaan, nama_paket, status_paket, tahapan_pengadaan, total_nilai, nilai_pdn, nilai_umk.
- Penghubung RUP dan realisasi adalah `kode_rup`. Provinsi diambil dari `nama_instansi` (38 provinsi).

Lingkup yang sudah saya tetapkan:
- Hanya paket dengan cara pengadaan Penyedia dan metode bukan "Dikecualikan". Swakelola tidak masuk.
- Jalur pelaksanaan hanya memakai realisasi yang sudah selesai. Cek nilai status/tahapan yang ada, lalu jelaskan nilai mana yang kamu anggap selesai.
- Unit analisis adalah satu paket (`kode_rup`).

## 2. Rancangan penelitian (sudah tetap)

1. Dua jalur: **Perencanaan** (data RUP saja, semua paket dalam lingkup) dan **Pelaksanaan** (paket RUP yang punya pasangan realisasi).
2. Model: ensemble **Isolation Forest + Local Outlier Factor + Autoencoder**, dilatih secara nasional per paket, tanpa label. Skor tiap model dinormalisasi lalu digabung. Bandingkan beberapa cara normalisasi (misalnya persentil/peringkat, min-max, skor-z robust), pilih satu dengan alasan, dan pastikan tidak ada satu model yang menguasai skor gabungan.
3. Penjelasan: **SHAP** untuk kontribusi fitur pada paket yang diprioritaskan (minimal 200 teratas per jalur). Dari 3 kontribusi terbesar, buat kalimat penjelasan dengan templat (tanpa LLM). Bahasanya netral: pakai "anomali", "tidak lazim", atau "perlu ditelaah". Jangan pakai kata "kecurangan" atau kata yang menuduh.
4. Evaluasi: **Precision@K** ensemble dibandingkan tiap model individual, dengan indikator **red flag** pengadaan sebagai acuan (pengganti label). Tambahkan telaah jumlah red flag pada paket peringkat teratas.
5. Agregasi: **proporsi** paket anomali per provinsi (bukan jumlah mentah) untuk 38 provinsi.

## 3. Yang perlu kamu rancang sendiri

- **Fitur**: rancang sendiri dari kolom yang tersedia. Jelaskan alasan dan cara hitung tiap fitur.
- **Red flag**: rancang sendiri indikator red flag yang bisa dihitung dari kolom yang tersedia, berdasarkan Perpres PBJ (konsolidasi sampai Perpres 46/2025) dan panduan red flag OCP 2024 yang saya unggah. Tulis dasar pasal atau kode indikator untuk masing-masing, dan tulis metode/jenis pengadaan apa saja yang bisa terkena indikator itu.

Sebelum melatih model, tunjukkan dulu daftar fitur dan red flag rancanganmu beserta alasannya.

## 4. Pelajaran dari percobaan saya sebelumnya (wajib diperhatikan)

1. **Kebocoran (evaluasi melingkar).** Fitur jangan dibuat dari bahan atau ambang yang sama dengan red flag penguji. Untuk setiap pasangan fitur dan red flag, hitung AUC fitur itu sendirian terhadap red flag. Kalau satu fitur sendirian sudah sangat tinggi (misalnya di atas 0,85), red flag itu bocor dan Precision@K-nya tidak boleh diklaim sebagai keberhasilan model. Laporkan Precision@K dengan dan tanpa red flag yang bocor.
2. **Red flag yang hanya berlaku untuk metode tertentu.** Hitung juga Precision@K khusus pada paket yang memang bisa terkena red flag itu, supaya peringkat atas yang didominasi metode lain tidak membuat angka tampak buruk atau baik secara semu.
3. **Pembanding.** Selalu tulis acuan acak (prevalensi red flag) di samping Precision@K dan nyatakan hasilnya sebagai "berapa kali lipat dari acak". Bandingkan juga dengan aturan sederhana tanpa model, misalnya mengurutkan paket berdasarkan satu fitur terkuat saja.
4. **Variabel kategori.** One-hot untuk kategori yang jarang cenderung membuat model menganggap "kategori jarang = aneh". Cek apakah peringkat atas didominasi satu kategori. Utamakan fitur angka yang relatif terhadap kelompok paket sebanding.
5. **Kolom yang hampir semuanya satu nilai** (biner yang jarang, atau kolom yang ~95% nol) tampak ekstrem setelah standardisasi. Cek dan buang atau ubah kolom seperti itu.
6. **Cek setelah setiap pelatihan, sebelum melapor:**
   - fitur mana yang paling sering menjadi SHAP terbesar di 200 teratas tiap jalur, dan apakah nilai aslinya memang ekstrem atau hanya sedikit di atas normal;
   - komposisi jenis, metode, sumber dana, ukuran satuan kerja, dan besar pagu di 200 teratas dan 5% teratas, dibandingkan seluruh data;
   - peringatan konvergensi autoencoder;
   - baca baris data mentah 20–40 paket teratas, cari yang masuk peringkat atas karena salah data, bukan karena anomali.
   Kalau ada masalah, perbaiki dan latih ulang dulu, baru laporkan sekaligus.
7. **Pembersihan data realisasi.** Cek nilai ≤ 0, catatan ganda per paket, provinsi realisasi yang berbeda dengan provinsi RUP, rasio realisasi terhadap pagu yang tidak masuk akal (termasuk pola kelebihan atau kekurangan satu angka nol), kolom yang semestinya rupiah tapi terisi persen atau sebaliknya, dan satu paket tender yang tercatat dengan banyak penyedia. Tulis setiap aturan pembersihan beserta jumlah baris yang terdampak.
8. **Keacakan.** Latih minimal 5 seed dan laporkan rentangnya, bukan satu angka. Paket dengan skor yang persis sama diurutkan acak, bukan menurut urutan file. Selisih antarvarian yang masih di dalam rentang seed dianggap tidak berbeda.
9. **Jangan mengejar angka Precision@K.** Kalau sebuah varian menaikkan angka secara drastis, periksa dulu apakah itu kebocoran atau artefak (misalnya tumpukan pagu bernilai bulat, atau efek perubahan ambang). Pilih varian di satu bagian data, lalu uji di bagian lain, misalnya sisihkan beberapa provinsi sebagai data uji.
10. **Bukti selain Precision@K:**
    - uji anomali buatan: sisipkan paket dengan pola janggal, bandingkan dengan baris kontrol yang tidak diubah; fitur yang dipaksa 0 harus tetap 0;
    - uji SHAP-hapus: apakah skor turun kalau fitur top-3 dinetralkan;
    - telaah manual 40 paket teratas per jalur: berapa yang layak diperiksa dan berapa yang wajar (misalnya proyek besar).
11. **Komputasi.** LOF dan KernelSHAP berat untuk ratusan ribu baris. Atur ukurannya (misalnya SHAP hanya untuk paket teratas dengan sampel background) dan tulis pengaturannya.

## 5. Luaran yang saya minta

- Kode Python per tahap (data, fitur, red flag, model, SHAP, evaluasi, ekspor) yang bisa dijalankan ulang dengan seed tetap.
- Laporan ringkas berbahasa Indonesia berisi: aturan pembersihan data, daftar fitur dan alasannya, daftar red flag dan dasar hukumnya, hasil Precision@K (ensemble vs IF/LOF/Autoencoder, dengan acuan acak dan rentang seed), hasil cek kebocoran, ringkasan SHAP, hasil cek di poin 4.6, dan proporsi per provinsi.
- File hasil per paket (skor, peringkat, top-3 SHAP, kalimat penjelasan) dan per provinsi.
- Opsional, dashboard web satu halaman: peta choropleth 38 provinsi memakai `provinsi38.geojson` (warna = proporsi paket anomali), tombol pilih Perencanaan/Pelaksanaan, daftar paket teratas, dan rincian paket dengan grafik SHAP.

Gaya: jelaskan dengan bahasa sederhana dan pakai format angka Indonesia (koma untuk desimal). Jujur kalau hasilnya setara acak; jangan dipoles.
