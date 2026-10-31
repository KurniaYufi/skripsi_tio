# Perbandingan fitur dan red flag: project ini vs project sebelah (31 Oktober 2026)

**Sumber:**
- Project ini: model-v5/s1_data.py dan s2_model.py.
- Project sebelah: laporan dan dashboard "TRAIN ANOMALY DETECTION".

## 1. Fitur

### Jalur perencanaan

| Yang diukur | Project ini (4 fitur) | Project sebelah (6 fitur) |
|---|---|---|
| Besar pagu | **log_pagu** | – (tidak ada) |
| Pagu dibanding paket sejenis | rasio ke median jenis + metode, **satu arah** (hanya yang lebih mahal) | posisi peringkat di jenis + metode, **dua arah** (yang sangat murah juga dianggap aneh) |
| Pagu dibanding satker | rasio ke median satker × jenis (minimal 4 paket), satu arah | posisi peringkat di semua paket satker (minimal 5 paket), dua arah |
| Pagu dibanding paket bernama sama | **ada** (nama spesifik, ≥ 2 paket lain) | – |
| Porsi anggaran satker yang diserap | – | **log_pangsa_pagu_satker** |
| Kebulatan pagu | – (dicoba di eksperimen, tidak membantu) | **kebulatan_pagu** |
| Pagu kembar di satker | – (mirip "paket kembar" yang bocor ke pemecahan) | **log_pagu_kembar_satker** |
| Kebiasaan satker memakai PL/PenL | – (dibuang, karena metode dipakai red flag) | **pangsa_nilai_nonkompetitif_satker** |

### Jalur pelaksanaan

| Yang diukur | Project ini (+2) | Project sebelah (+3) |
|---|---|---|
| Realisasi dibanding pagu | rasio_realisasi (mentah, dipotong maks. 5) | posisi rasio di jenis × metode × kuintil pagu |
| Selisih rupiah | log_selisih_realisasi | – |
| Jangkauan penyedia | – (penyedia = bahan red flag) | **log_jangkauan_penyedia** |
| Nilai dibanding kebiasaan penyedia | – | **log_nilai_vs_kebiasaan_penyedia** |

### Perbedaan cara pikir

1. **Arah:** project ini hanya menghukum paket yang lebih mahal. Project sebelah juga menandai paket yang sangat murah. Akibatnya, puncak perencanaan project sebelah berisi pagu Rp1.958, Rp8.372, dan sejenisnya. Dari 40 paket teratas, 11 adalah salah isi data.
2. **Batas pagu kecil:** project ini membuang pagu < Rp1 jt di perencanaan, project sebelah hanya < Rp1.000. Ini sejalan dengan poin 1.
3. **Fitur satker:** project sebelah memakai lebih banyak fitur tingkat satker (porsi anggaran, pagu kembar, porsi non-kompetitif). Kelemahannya, porsi non-kompetitif bernilai sama untuk semua paket satker itu. Akibatnya, satu satker bisa naik bersama-sama, dan fitur ini berkaitan dengan red flag E6.
4. **Fitur penyedia:** project sebelah memakai fitur penyedia di pelaksanaan. Project ini sengaja tidak, karena penyedia dipakai untuk red flag RF5/RF6.

## 2. Red flag

| Pola | Project ini | Project sebelah | Catatan |
|---|---|---|---|
| PL mendekati ambang (90–100%) | **RF1** (konstruksi: dua jendela, ambang lama dan baru) | P2, **bocor** | Project sebelah menganggapnya bocor (AUC ≥ 0,85). Di project ini RF1 masih dipakai |
| PL melebihi ambang | RF2, **dihilangkan** (bocor) | P3, bocor | Keduanya sepakat: bocor |
| Pemecahan paket | **RF3** | **P1** | Sama-sama dipakai, definisi mirip (nama sama, jumlah > ambang) |
| Penunjukan langsung | **RF4** (semua PenL) | **P4** (hanya PenL > ambang PL) | Project sebelah lebih sempit: 666 paket |
| Bukan PDN / tidak dicadangkan UMK (RUP) | – | **P5, P6** | Project ini memperlakukan PDN/UMK sebagai bahan fitur, lalu membuangnya |
| Realisasi > pagu | – (sama dengan fitur rasio realisasi) | E1, bocor | Keduanya tidak memakai untuk menilai |
| Nilai tender ≥ 99% pagu | – | E2, bocor | |
| Metode realisasi ≠ RUP | – | **E3** (139 paket) | Terlalu sedikit untuk berpengaruh |
| PDN / UMK realisasi < 50% | – | **E4, E5** | E5 terbanyak di 200 teratas mereka (45 paket) |
| Penyedia dominan di satker | **RF5** (> 40% nilai, OCP R040) | **E6** (≥ 50% paket non-katalog) | Mirip. Di project sebelah, E6 inilah penyumbang keunggulan pelaksanaan |
| Penyedia serba-ada (≥ 3 jenis) | **RF6** (OCP R048) | – | |

**Jumlah red flag yang dipakai untuk menilai:**
- Project ini: perencanaan 3 (RF1, RF3, RF4), pelaksanaan 5 (+RF5, RF6).
- Project sebelah: perencanaan 4 (P1, P4, P5, P6), pelaksanaan 4 (E3–E6).

## 3. Kesimpulan

1. **Fitur:** keduanya sama-sama berbasis "pagu dibanding pembanding". Bedanya, project ini satu arah dan memakai nama paket. Project sebelah dua arah dan memakai lebih banyak fitur satker dan penyedia.
   - Satu arah membuat daftar teratas project ini lebih bersih: sekitar 3/4 dari 40 teratas layak ditelaah, project sebelah 15/40.
2. **Red flag:** inti yang sama ada di keduanya: pemecahan, penunjukan langsung, penyedia dominan, dan PL melebihi ambang yang dianggap bocor.
   - Project sebelah menambah red flag kepatuhan PDN/UMK (P5, P6, E4, E5).
   - Project ini menambah penyedia serba-ada dan PL mendekati ambang.
3. **Satu hal yang perlu dicek di project ini:** project sebelah menilai "PL mendekati ambang" (P2) bocor. Project ini masih memakai RF1. Fitur kita satu arah dan berbasis rasio, jadi kebocorannya mungkin lebih kecil, tetapi belum diuji dengan tabel AUC seperti yang mereka lakukan.
4. **Yang bisa diadopsi tanpa mengubah model:** red flag PDN/UMK (P5, P6, E4, E5) sebagai penguji tambahan. Catatannya: menambah red flag setelah melihat hasil harus ditulis sebagai uji tambahan, bukan hasil utama.
