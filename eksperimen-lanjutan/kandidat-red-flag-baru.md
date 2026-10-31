# Kandidat red flag baru dari sumber luar (30 Oktober 2026)

**Pertanyaan Tio:** adakah red flag yang bersumber dan valid, yang kira-kira menaikkan Precision@K? Cari di OCP maupun sumber lain.

**Sumber yang dicek:**
- panduan OCP 2024 *Red flags in public procurement* (CC BY-NC-SA 4.0);
- daftar indikator Cardinal OCP;
- indikator Fazekas (CRI);
- Perpres PBJ konsolidasi 46/2025.

Model, naskah, dan dashboard tidak diubah.

## Aturan pilih (ditetapkan sebelum melihat hasil)

1. Punya sumber yang jelas.
2. Bisa dihitung dari kolom INAPROC yang ada.
3. Tidak dibuat dari fitur model di jalur itu. Kalau dibuat dari fitur, itu menyontek.
4. Lipat di 5% teratas ≥ 1,2 di 2024 **dan** di provinsi uji 2025.
5. Juga dicek **setelah dikontrol pagu dan metode**. Paket teratas model cenderung berpagu besar, jadi red flag yang memang lebih sering di paket besar bisa tampak "tertangkap" hanya karena ukuran.

**Yang tidak bisa dihitung:** sebagian besar red flag OCP dan Fazekas butuh data penawaran, misalnya jumlah peserta (penawar tunggal), harga penawaran, atau tanggal (masa pengumuman singkat). Data seperti ini tidak ada di INAPROC yang dipakai.

## Hasil 7 kandidat

Angka = lipat 5% teratas. Biasa / dikontrol pagu + metode. Urutan kolom: 2024 / 2025 / 2025 uji.

| Kandidat | Sumber | Perencanaan | Pelaksanaan | Putusan |
|---|---|---|---|---|
| C1. PL yang pagunya ≤ ambang tetapi realisasinya > ambang | OCP R054 | 1,5 / 0,4 / 0,7 | 9,2 / 10,7 / 8,6 | **Tidak.** Di pelaksanaan menyontek fitur realisasi dibanding pagu. Hanya ±110 paket |
| C2. Penyedia dapat pembelian kecil di satker yang sama tahun lalu, lalu paket ≥ 10× tahun ini | OCP R052 | – / 2,3 / 2,8 (kontrol 1,2 / 1,4) | – / 2,6 / 2,8 (kontrol 1,3 / 1,1) | Lemah. Hanya 379 paket dan hanya bisa di 2025 (butuh data tahun sebelumnya) |
| C3. PL > Rp50 jt yang hanya lewat "Pencatatan Non Tender" | Perpres 46/2025 Pasal 38 ayat (8) | – / 2,5 / 2,7 (kontrol 0,9 / 1,1) | – / 3,5 / 3,3 (kontrol 1,5 / 2,2) | **Kandidat untuk pelaksanaan.** Hanya 2025, dan aturannya baru berlaku 30 April 2025 |
| C4. Penyedia menerima > 40% nilai realisasi satker × jenis (≥ 5 paket) | OCP R050 | 2,5 / 1,7 / 1,4 (kontrol 1,7 / 1,3 / 1,4) | 2,5 / 2,1 / 1,8 (kontrol 1,8 / 1,8 / 1,9) | **Kandidat terkuat.** Tetap di atas 1,2 setelah dikontrol, di kedua tahun. Separuh paketnya sama dengan RF5 |
| C5. RUP mencantumkan PDN, tetapi nilai PDN realisasi 0 (di luar Pencatatan) | Perpres Pasal 66, 76 ayat (4) | 1,4 / 1,3 / 1,3 (kontrol 1,5 / 1,0 / 0,8) | 0,9 / 1,2 / 1,4 | **Tidak.** Hilang setelah dikontrol, jadi hanya efek ukuran |
| C6. RUP untuk UMK, tetapi nilai UMK realisasi 0 (di luar Pencatatan) | Perpres Pasal 65 ayat (3) | 1,3 / 1,3 / 1,5 (kontrol ±1,0) | 1,2 / 1,5 / 1,6 (kontrol ±1,1) | **Tidak.** Hilang setelah dikontrol |
| C7. Realisasi ≥ pagu (tidak ada penghematan) | OCP R031 | 0,8 / 0,9 / 0,7 | 0,9 / 1,6 / 1,2 | **Tidak.** Perencanaan di bawah acak, pelaksanaan menyontek fitur realisasi |

## Kalau kandidat terbaik ditambahkan

Ukurannya: lipat 5% dan Precision@200, dengan paket RF2 dikeluarkan. Data 2025, semua provinsi / provinsi uji.

| Set red flag | Perencanaan | Pelaksanaan |
|---|---|---|
| Sekarang (RF1, RF3–RF6) | lipat 1,34 / 1,14; P@200 3% / 7% | lipat 0,90 / 0,86; P@200 22% / 24% |
| + C3 (Pasal 38 ayat 8) | 1,33 / 1,15 | 1,05 / 1,02 |
| + C3 + C4 (R050) | lipat 1,35 / 1,18; P@200 5% / 10% | **lipat 1,14 / 1,12; P@200 30% / 34%** |

## Kesimpulan

- **Tidak ada red flag baru yang menaikkan Precision@K banyak dengan cara yang sah.**
- **Pelaksanaan bisa naik sedikit.** Dengan C3 dan C4, pelaksanaan naik dari di bawah acak (0,90) ke sedikit di atas acak (1,14). P@200 tanpa RF2 naik dari 22% ke 30%. Keduanya bersumber dan tidak dibuat dari fitur.
- **Catatan C4 (R050):** mirip RF5 (RF5 = penyedia > 40% di seluruh satker; C4 = per satker × jenis). Bisa ditulis sebagai versi RF5 per jenis pengadaan, sesuai definisi OCP R050.
- **Catatan C3 (Pasal 38 ayat 8):**
  - hanya berlaku sejak 30 April 2025, jadi paket yang dicatat sebelum itu sebenarnya belum wajib;
  - tidak bisa diuji di 2024;
  - 59% paketnya sudah kena red flag lain, terutama RF2.
- **Perencanaan praktis tidak berubah.** Red flag yang berasal dari penyedia dan realisasi tidak berhubungan dengan pola pagu yang dilihat model perencanaan.

## Pilihan untuk Tio

1. **Tidak menambah red flag (saran).** Kenaikannya kecil, dan menambah red flag setelah melihat hasil bisa dipertanyakan.
2. **Tambah C4 (OCP R050) saja**, sebagai RF5 versi per jenis. Bersumber kuat dan tetap bertahan setelah dikontrol.
3. **Tambah C4 dan C3**, hanya untuk pelaksanaan 2025. Hasilnya paling naik, tetapi C3 punya catatan waktu berlaku aturan.

Kalau pilih 2 atau 3, naskah perlu menulis jujur bahwa red flag ini ditambahkan setelah eksperimen. Precision@K dengan set lama juga tetap dilaporkan.

File:
- i_kandidat_rf.py dan i_kandidat_rf.csv (7 kandidat);
- i2_terkontrol.py dan i2_terkontrol.csv (kontrol pagu + metode);
- i3_r050.py dan i3_r050.csv (R050 dan efeknya pada Precision@K).
