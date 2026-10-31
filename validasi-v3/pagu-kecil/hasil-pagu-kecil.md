# Uji paket pagu kecil di jalur perencanaan (2026-10-29)

Masalah: 45 dari 200 paket teratas model v3 (22,5%) berpagu di bawah Rp1 jt. Penyebabnya fitur pagu berupa rasio, sehingga pagu ratusan kali lebih kecil dari biasanya dianggap sama tidak lazimnya dengan ratusan kali lebih besar. Sebagian besar paket ini lebih mirip salah isi data (misalnya tinta printer dicatat sebagai Pekerjaan Konstruksi).

## Varian yang diuji

| Varian | Isi |
|---|---|
| v3 | Model sekarang |
| v3 + saring | Skor v3, paket < Rp1 jt tidak ditampilkan di daftar (tanpa latih ulang) |
| B | Paket < Rp1 jt dibuang sebelum model dilatih |
| S | Skor satu arah: hanya pagu yang **lebih besar** dari biasanya yang bisa menaikkan skor |
| B+S | Keduanya |

Semua varian: fitur varian E, 5 seed, dinilai dengan aturan yang sama seperti pemilihan fitur v3 (5% teratas, provinsi pilih lalu provinsi uji). Kecuali baris v3 dan S, angka dihitung pada paket ≥ Rp1 jt (acuan 15,8%), supaya adil.

| Ukuran | v3 | v3 + saring | B | S | **B+S** |
|---|---|---|---|---|---|
| Paket < Rp1 jt di 200 teratas | 22,5% | 0% | 0% | 2% | **0%** |
| Paket < Rp10 jt di 200 teratas | 36,5% | 18,5% | 31% | 9% | **4%** |
| 5% teratas ber-red flag, provinsi pilih | 32,6% (1,98×) | 35,1% (1,96×) | 32,3% (1,80×) | 38,8% (2,35×) | **41,4% (2,31×)** |
| 5% teratas ber-red flag, provinsi uji | 32,4% (2,69×) | 37,0% (2,69×) | 31,0% (2,25×) | 34,0% (2,83×) | **39,5% (2,87×)** |
| 5% teratas tanpa RF4, provinsi uji | 2,74× | 2,73× | 2,26× | 2,89× | **2,94×** |
| P@50 / P@100 / P@200 | 32 / 32 / 25,5% | 42 / 38 / 28,5% | 36 / 40 / 28% | 14 / 16 / 19,5% | 26 / 25 / 22% |
| P@200 tanpa RF4 | 7% | 9% | 8,5% | 11% | **18%** |
| Satker terbanyak di 200 teratas | – | 14 | – | – | 22 |

## Artinya

- **B+S menang menurut aturan pemilihan** (5% teratas, provinsi pilih lalu uji) dan daftar teratasnya hampir bebas paket berpagu kecil. Di 5% teratas, RF2 (pengadaan langsung melewati ambang) 5,4 kali rata-rata.
- **Kelemahan B+S:** puncak daftar (P@50–200) lebih rendah dari v3. Penyebabnya, puncak daftar v3 banyak diisi penunjukan langsung (RF4 19,5% dari 200 teratas, B+S 4%). Tanpa RF4, puncak B+S justru dua kali lebih sering ber-red flag (18% vs 9%). Satu satker mengisi 22 dari 200 teratas, sedikit di atas batas 20 yang dipakai sebelumnya.
- **v3 + saring** paling sederhana: angka puncak naik, 5% teratas sama dengan v3, tetapi masih ada 18,5% paket < Rp10 jt di 200 teratas.
- **B saja** justru lebih buruk dari v3 di 5% teratas.

Kode: `u1_latih.py` (latih varian), `u2_nilai.py` (penilaian), angka di `u2_nilai.csv`.

## Keputusan dan model v4 akhir (2026-10-29)

Tio memilih "batas Rp1 jt + skor satu arah". Setelah semua uji dijalankan, versi yang ikut memotong pagu mentah di median ternyata 200 teratasnya hanya 22% ber-red flag dan kurang stabil (Jaccard 0,41). Saya menguji satu perbaikan: rasio pagu tetap satu arah, tetapi pagu mentah tidak dipotong, karena paket < Rp1 jt sudah dibuang. Di 5% teratas provinsi pilih keduanya setara (2,29× vs 2,31×), sedangkan di 200 teratas versi perbaikan jauh lebih kuat (38,5% vs 22%) dan lebih stabil (0,52 vs 0,41). Tio memilih yang terbaik, jadi model v4 memakai versi perbaikan (`u3_tanpa_potong_pagu.py`, `u4_banding.csv`). Pemilihan ini dilakukan setelah melihat hasil, jadi perlu ditulis jujur di naskah.

Kode: `/mnt/project-files/model-v4/` (v3 tetap di `model-v3/`; hasil versi pagu ikut dipotong di `model-v4/arsip-BS/`).

### Perencanaan: v3 dibanding v4

| Uji | v3 | v4 |
|---|---|---|
| Paket yang dinilai | 343.919 | 303.930 (pagu ≥ Rp1 jt) |
| 200 teratas ber-red flag (acuan) | 25,5% (14,2%) = 1,8× | **38,5% (15,8%) = 2,4×** |
| 200 teratas tanpa RF4 | 9,3%, di bawah acuan 13,1% | **22,0%, di atas acuan 14,6%** |
| 5% teratas ber-red flag | 32,6% (2,3×) | **38,3% (2,4×)** |
| Provinsi uji, 50–200 teratas | 14,7% (acuan 12,0%) | **20,7% (acuan 13,8%)** |
| Provinsi uji, 5% teratas | 32,4% (2,7×) | 34,2% (2,5×) |
| Paket < Rp1 jt / < Rp10 jt di 200 teratas | 22,5% / 36,5% | **0% / 13%** |
| Kestabilan 200 teratas (Jaccard) | **0,61** | 0,52 |
| Peta provinsi vs red flag (ρ) | **0,55** | 0,40 (p = 0,013) |
| Pola gabungan antarfitur tertangkap | 63% | 59% |
| SPI KPK | tidak nyata | tidak nyata (p = 0,093) |
| Uji hapus SHAP (paket turun lebih besar) | 100% | 97% |
| Ablasi, peringkat rata-rata ensemble dari 9 cara | 3,9 | **3,6** |

Jalur pelaksanaan tidak berubah.

**Catatan jujur:** di v4, LOF dan Autoencoder secara tunggal lemah di 200 teratas perencanaan (4,5% dan 2,5%). Puncak daftar ensemble terutama didorong IF. Pada 5% teratas, LOF tunggal tetap kuat (38,0%), dan rata-rata tiga model tetap paling konsisten di semua ukuran (ablasi). Kestabilan dan keselarasan peta sedikit turun dibanding v3.

Lembar telaah buta sudah dibuat ulang dari model v4 (versi v3 di `telaah-buta/arsip-v3/`).
