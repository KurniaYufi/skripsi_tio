# Hasil 3 evaluasi model v5 (yang ada di dashboard), 29 Oktober 2026

Semua angka diambil dari `validasi/` (v_ablasi.csv, v_bootstrap.csv, v_sintetis.csv, v_stabilitas.csv). "Anomali" = 5% skor teratas.

## 1. Precision@K dengan red flag

Acuan = persentase paket ber-red flag di seluruh data (kalau paketnya dipilih acak).

| | Perencanaan | Pelaksanaan |
|---|---|---|
| P@50 | 30% | 54% |
| P@100 | 27% | 47% |
| P@200 | 33,5% | 40% |
| 5% teratas | 41,7% | 31,2% |
| Acuan (acak) | 15,8% | 26,3% |
| 5% teratas di provinsi uji (acuan) | 39,9% (13,8%) | 27,7% (25,6%) |

- **Perencanaan:** jelas di atas acak, sekitar 2 sampai 3 kali, dan tetap bertahan di provinsi uji.
- **Pelaksanaan:** di atas acak tetapi tipis. Di provinsi uji hanya 27,7% dibanding acuan 25,6%.

**Dibanding model individual** (rencana evaluasi di Bab 1):

| 5% teratas | Ensemble | IF saja | LOF saja | AE saja |
|---|---|---|---|---|
| Perencanaan | 41,7% | 26,5% | 38,7% | **60,8%** |
| Pelaksanaan | 31,2% | 23,8% | **43,7%** | 33,1% |

| P@200 | Ensemble | IF saja | LOF saja | AE saja |
|---|---|---|---|---|
| Perencanaan | **33,5%** | 27,5% | 2,5% | 18,5% |
| Pelaksanaan | 40% | 23% | **55%** | **55,5%** |

Ensemble **tidak selalu yang terbaik**. Ensemble menang di P@200 perencanaan, sedangkan LOF dan AE menang di pelaksanaan. Keunggulan ensemble lebih ke "tidak pernah jatuh paling buruk". Contohnya, LOF saja hanya dapat 2,5% di P@200 perencanaan, dan IF saja di bawah acak di pelaksanaan. Ini perlu ditulis jujur. Kalimat Bab 1 "ensemble lebih konsisten" masih cocok; "ensemble lebih akurat" tidak.

## 2. Anomali buatan

Ada 1.000 paket buatan per jenis. Angka di tabel = persen paket buatan yang masuk 5% teratas Ensemble. Kalau model menebak acak, angkanya 5%.

| Jenis anomali buatan | Perencanaan | Pelaksanaan |
|---|---|---|
| Global (nilai ekstrem) | 94% | 100% |
| Berkelompok (banyak paket kembar yang aneh) | 99,6% | 93% |
| Dependensi (kombinasi kolom tidak cocok) | 57% | 49% |
| Lokal (aneh dibanding paket sejenis) | 51% | 70% |
| Realisasi melebihi pagu | - | 61% |
| Dekat ambang penunjukan langsung | 13% | 17% |
| Pagu digelembungkan sedikit | 1% | 2% |
| **Kontrol: paket buatan yang normal** | 26% | 22% |

- **Tertangkap baik:** anomali ekstrem dan berkelompok.
- **Tertangkap sedang:** kombinasi tidak cocok, aneh lokal, dan realisasi melebihi pagu.
- **Hampir tidak tertangkap:** paket dekat ambang dan pagu yang digelembungkan sedikit. Ini wajar, karena paketnya tetap terlihat normal. Pola seperti ini lebih tepat ditangani dengan red flag berbasis aturan, dan bisa ditulis sebagai batasan.
- **Catatan jujur tentang baris kontrol.** Paket buatan yang normal pun 22-26% masuk 5% teratas, karena paket buatan memang sedikit berbeda dari paket asli. Jadi pembanding yang adil adalah angka tiap jenis dibanding baris kontrol, bukan dibanding 5%. Contoh: lokal di perencanaan 51% dibanding kontrol 26%, jadi sekitar 2 kali.

## 3. Kestabilan

| | Perencanaan | Pelaksanaan |
|---|---|---|
| 200 teratas yang sama (Jaccard), 5 seed vs 5 seed lain | 0,63 | 0,66 |
| 5% teratas yang sama (Jaccard) | 0,75 | 0,74 |
| Urutan skor seluruh paket (Spearman) | 0,97 | 0,98 |
| Jaccard 200 teratas kalau hanya 1 seed | 0,40 | 0,46 |

- Urutan keseluruhan sangat stabil (Spearman 0,97-0,98).
- Daftar 5% teratas sekitar tiga perempatnya sama.
- 200 teratas lebih mudah bergeser. Inilah alasan skor dirata-rata dari 5 seed: dengan 1 seed, kemiripannya hanya 0,40-0,46.
