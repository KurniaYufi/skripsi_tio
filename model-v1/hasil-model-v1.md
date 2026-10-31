# Hasil Model v1 (dijalankan 2026-10-28)

Kode: `s1_data.py` (data, fitur, red flag) → `s2_model.py` (IF, LOF, AE, ensemble, Precision@K) → `s3_shap.py` (Kernel SHAP) → `s4_export.py` (kalimat + data dashboard). Kelas model ada di `ens.py`. Dashboard: `/mnt/project-files/dashboard-v1/` (`dashboard-mandiri.html` bisa langsung dibuka di peramban atau di-host di GitHub Pages).

## Data
- Paket penyedia RUP 2025, tanpa "Dikecualikan": 344.665; setelah pagu > Rp10.000: **343.919** (jalur perencanaan).
- Realisasi: 136.163 paket punya pasangan; yang semua barisnya sudah tahap "Serah Terima" dan nilai > 0: **105.575** (jalur pelaksanaan, 30,7% paket RUP).
- Realisasi diagregasi per kode_rup; 1.546 baris dengan lebih dari satu kode_rup tidak dipakai.

## Red flag (hanya untuk evaluasi)
| Red flag | Jumlah paket |
|---|---|
| PL mendekati ambang (≥90% ambang) | 7.383 |
| PL melebihi ambang | 7.486 |
| Pemecahan paket (TF-IDF ≥0,8, satker+jenis sama, total > ambang) | 28.503 |
| Penunjukan langsung | 3.984 |
| Penyedia dominan di satker (pelaksanaan) | 22.121 |
| Penyedia serba-ada (≥3 jenis, pelaksanaan) | 2.707 |

## Precision@K (bagian K teratas yang punya ≥1 red flag)
**Perencanaan** (acuan semua paket 12,6%)

| Model | P@50 | P@100 | P@200 |
|---|---|---|---|
| Ensemble | **38,0%** | **29,0%** | **35,0%** |
| Isolation Forest | 16,0% | 10,0% | 8,0% |
| LOF | 14,0% | 12,0% | 19,0% |
| Autoencoder | 18,0% | 20,0% | 16,5% |

**Pelaksanaan** (acuan semua paket 37,0%)

| Model | P@50 | P@100 | P@200 |
|---|---|---|---|
| Ensemble | 48,0% | 55,0% | 53,5% |
| Isolation Forest | 34,0% | 26,0% | 23,5% |
| LOF | 20,0% | 57,0% | 50,0% |
| Autoencoder | **68,0%** | **66,0%** | **61,5%** |

Catatan baca: di perencanaan ensemble paling tinggi di semua K. Di pelaksanaan Autoencoder lebih tinggi daripada ensemble, sedangkan ensemble tetap di atas acuan dan di atas IF. Ini selaras dengan Krčmar (2026): ensemble lebih konsisten, belum tentu paling akurat. Red flag penyedia dominan cukup longgar (persentil 95 = 5 paket per satker), sehingga acuan jalur pelaksanaan sudah 37%.

## SHAP (rata-rata |SHAP| 200 paket teratas)
- Perencanaan: metode 0,118; porsi pagu di satker 0,107; jenis 0,082; pagu 0,047; UMK 0,046.
- Pelaksanaan: metode 0,090; sumber transaksi 0,076; jenis 0,067; porsi pagu di satker 0,040; pagu 0,038.

## Kalimat penjelasan
LLM lokal belum bisa dipakai di sini karena unduhan model dari Hugging Face diblokir jaringan container. Kalimat memakai templat dari 3 fitur SHAP terbesar (cadangan yang sudah disetujui). Masukan untuk LLM nanti sama: nama fitur, nilai paket, median pembanding.
