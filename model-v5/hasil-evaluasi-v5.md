# Hasil evaluasi model v5 (versi terbaru, 29 Oktober 2026 sore)

> **USANG (29 Okt malam):** angka dan fitur di file ini sudah diganti hasil audit. Lihat `hasil-audit-latih-ulang.md`.

Versi ini sudah memakai koreksi kategori:
- Jenis dan metode tidak digabung.
- Paket Terintegrasi (172 paket) tidak dinilai.

Versi sebelum koreksi diarsipkan di `arsip-sebelum-pisah-kategori/`. Angka dalam kurung adalah versi sebelum koreksi. "Anomali" berarti 5% skor teratas.

## 0. Seberapa besar angka bergeser hanya karena acak (penting dibaca dulu)

Model yang sama persis dilatih lagi dengan dua set seed lain (`eksperimen-seed/hasil.csv`):

| Jalur | 5% teratas | Provinsi uji 5% | P@200 |
|---|---|---|---|
| Perencanaan, 3 set seed | 35,9 / 38,6 / 38,6% | 33,7 / 32,9 / 35,7% | 33 / 30,5 / 25% |
| Pelaksanaan, 3 set seed | 29,9 / 30,1 / 29,3% | 26,2 / 26,5 / 26,2% | 37,5 / 36,5 / 38% |

Artinya:
- Selisih **sampai sekitar 3 poin di 5% teratas** dan **sampai sekitar 8 poin di P@200** bisa muncul hanya karena acak.
- Perbandingan antarvarian sebelumnya (R, M3, varian pelaksanaan) yang selisihnya sebesar itu **belum bisa disebut lebih baik atau lebih buruk**.
- Untuk naskah, sebaiknya dilaporkan rentangnya, bukan satu angka. Contoh: perencanaan 5% teratas 36–39%.

## 1. Precision@K dengan red flag

| | Perencanaan | Pelaksanaan |
|---|---|---|
| P@50 | 30% | 60% |
| P@100 | 40% | 49% |
| P@200 | 33% (33,5%) | 37,5% (40%) |
| 5% teratas | 35,9% (41,7%) | 29,9% (31,2%) |
| Acuan (acak) | 15,9% | 26,3% |
| Provinsi uji 5% (acuan) | 33,7% (39,9%), acuan 13,8% | 26,2% (27,7%), acuan 25,6% |

- **Perencanaan:** tetap sekitar 2,4 kali acak, termasuk di provinsi uji.
- **Pelaksanaan:** di provinsi uji setara acak.
- **Perbandingan dengan versi sebelum koreksi:**
  - Perencanaan turun sekitar 3–6 poin. Sebagian besar penurunan ini masih dalam rentang acak di bagian 0, jadi tidak bisa dipastikan apakah karena koreksi kategori atau hanya karena acak.
  - Satu hal lagi: angka 41,7% versi lama didapat dari varian R, yang dipilih setelah melihat hasil. Angka yang dipilih dengan cara seperti itu cenderung lebih tinggi daripada yang akan muncul lagi kalau dilatih ulang.

**Dibanding model tunggal (5% teratas):**

| | Ensemble | IF saja | LOF saja | AE saja |
|---|---|---|---|---|
| Perencanaan | 35,9% | 26,7% | 36,6% | **60,2%** |
| Pelaksanaan | 29,9% | 24,3% | **44,4%** | 30,3% |

**Dibanding model tunggal (P@200):**

| | Ensemble | IF saja | LOF saja | AE saja |
|---|---|---|---|---|
| Perencanaan | **33%** | 24% | 4% | 17% |
| Pelaksanaan | 37,5% | 23% | 54% | **56,5%** |

Polanya sama dengan sebelumnya:
- Ensemble tidak selalu menang.
- Ensemble juga tidak pernah paling buruk.

## 2. Anomali buatan (persen yang masuk 5% teratas, acak = 5%)

| Jenis | Perencanaan | Pelaksanaan |
|---|---|---|
| Global | 95% | 100% |
| Berkelompok | 100% | 86% |
| Dependensi | 59% | 45% |
| Lokal | 51% | 71% |
| Realisasi melebihi pagu | – | 61% |
| Dekat ambang | 13% | 19% |
| Pagu dinaikkan sedikit | 1% | 1% |
| Kontrol (paket buatan normal) | 27% | 21% |

Hasilnya hampir sama dengan versi sebelum koreksi.

## 3. Kestabilan (5 seed dibanding 5 seed lain)

| | Perencanaan | Pelaksanaan |
|---|---|---|
| Spearman urutan skor | 0,97 | 0,99 |
| 5% teratas yang sama (Jaccard) | 0,74 | 0,77 |
| 200 teratas yang sama (Jaccard) | 0,46 | 0,63 |

## 4. Kesetiaan SHAP

Kalau 3 fitur teratas menurut SHAP diganti nilai normal, skor turun lebih besar daripada kalau 3 fitur acak yang diganti. Ini terjadi pada **100%** paket perencanaan dan **95%** paket pelaksanaan.
