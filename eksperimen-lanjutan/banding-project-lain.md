# Perbandingan dengan project "TRAIN ANOMALY DETECTION" (31 Oktober 2026)

**Sumber:**
- **Project lain:** dokumen [Laporan deteksi anomali PBJ provinsi 2025](https://claude.ai/artifact/G5fNg2a2SMxLRsziJ6yx9U). Dibaca seluruhnya, kecuali paragraf keterbatasan di akhir yang terpotong. File hasil per paket project itu tidak bisa diakses dari sini.
- **Project ini:** model v5 hasil audit (dashboard), laporan eksperimen lanjutan, dan evaluasi tanpa RF2.

**Catatan penting:** kedua project memakai red flag yang berbeda, jadi angka Precision@K **tidak bisa dibandingkan satu lawan satu**. Yang bisa dibandingkan adalah pola besarnya dan kualitas daftar teratas.

## Ringkasan

| Aspek | Project lain | Project ini |
|---|---|---|
| Fitur | 6 fitur (+3 pelaksanaan). Posisi pagu dalam kelompok, pangsa pagu satker, kebulatan pagu, pagu kembar, porsi non-kompetitif satker, jangkauan penyedia | 4 fitur (+2 pelaksanaan). Rasio pagu ke sejenis, satker, nama sama; realisasi |
| Red flag | 12 (P1–P6, E1–E6), 4 di antaranya bocor | 6 (RF1–RF6); RF2 bocor dan sekarang dihilangkan |
| Batas pagu kecil | dibuang hanya pagu < Rp1.000 | perencanaan minimal Rp1 jt |
| **Perencanaan, P@200 dengan red flag bersih** | 0,80× acak | 0,2× acak (3% vs 13,7%) |
| **Perencanaan, 5% teratas** | 1,11× (provinsi uji 1,53×, tetapi aturan satu fitur 2,70×) | **1,34×** (provinsi uji 1,14×) |
| **Pelaksanaan, P@200** | **1,75×**. Sebagian besar dari E6 (penyedia dominan), yang berkaitan dengan fitur porsi non-kompetitif. Tanpa E6, 5% teratas = 0,98× (setara acak) | 0,9× (set lama); 1,31× dengan set red flag rancangan (termasuk R050) |
| **Telaah 40 teratas** | 15 layak / **11 kesalahan data** / 14 wajar (perencanaan); 15 / 6 / 19 (pelaksanaan) | **±31 layak** (perencanaan), **±28 layak** (pelaksanaan) |
| Penyebab utama di puncak perencanaan | pagu **sangat kecil** (Rp1.958, Rp8.372) → banyak salah isi data | pagu jauh lebih besar dari paket bernama sama di satker |
| Anomali buatan | pagu ×30: 13% masuk 5% teratas; realisasi 2,5× pagu: 75% | pola gabungan 40–55% (skor-z 2%); pagu 5–20× sejenis 16–19% |
| Uji SHAP-hapus | 100% turun | 100% turun |
| Kestabilan 200 teratas antar-seed | irisan 0,74–0,76 | Jaccard 0,65–0,73 |

## Kesimpulan

1. **Dari sisi Precision@K, keduanya sama-sama lemah.** Terhadap red flag yang tidak bocor, perencanaan setara acak di kedua project.
   - Pelaksanaan project lain tampak lebih tinggi, tetapi keunggulannya datang dari satu red flag (E6) yang berhubungan dengan fitur modelnya sendiri.
   - Laporan project lain mengakuinya: tanpa E6 hasilnya setara acak.
2. **Daftar teratas project ini lebih berguna.**
   - Project ini: sekitar 3/4 dari 40 paket teratas layak ditelaah.
   - Project lain: hanya 15 dari 40, dan 11 di jalur perencanaan adalah salah isi data (pagu ribuan rupiah). Penyebabnya, project lain tidak membuang pagu sangat kecil, sedangkan project ini memakai batas Rp1 jt.
3. **Project lain lebih rapi dalam melapor.** Bagian ini layak ditiru:
   - tabel AUC kebocoran setiap fitur × red flag;
   - Precision@K di beberapa K dengan rentang seed;
   - interval Wilson 95% untuk proporsi per provinsi;
   - katalog red flag dengan prevalensi di paket yang berlaku.
4. **Project lain punya beberapa fitur yang belum pernah dicoba di sini:** kebulatan pagu, pagu kembar di satker, jangkauan penyedia, dan nilai dibanding kebiasaan penyedia.
   - Kebulatan pagu sudah dicoba di eksperimen lanjutan dan tidak membantu.
   - Pagu kembar mirip fitur "paket kembar" yang bocor ke RF3.

**Saran:** tetap pakai model project ini. Ambil cara melapor dari project lain (tabel AUC kebocoran, rentang seed, interval Wilson provinsi) untuk Bab 4.

Perbandingan yang benar-benar adil (kedua model diuji dengan red flag yang sama) membutuhkan file hasil per paket dari project lain: `hasil/paket_perencanaan.csv` dan `hasil/paket_pelaksanaan.csv`.
