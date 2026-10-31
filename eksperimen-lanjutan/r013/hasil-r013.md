# Uji usulan red flag perencanaan dari Tio (31 Oktober 2026)

Kode: `eksperimen-lanjutan/m1_r013.py`. Angka lengkap: `r013/m1_eval.csv` dan `r013/m1_bocor.csv`. Model perencanaan **tidak dilatih ulang**; yang diuji hanya red flag penilainya.

## 1. Pagu paket ekstrem (adaptasi R016)

- Ini sudah menjadi **fitur** model ("pagu dibanding paket sejenis" dan "pagu dibanding satker").
- Kalau dijadikan red flag juga, model dinilai dengan penggarisnya sendiri, jadi angkanya pasti naik tetapi tidak membuktikan apa-apa.
- Uji 29 Oktober (`eksperimen-r016-r068/hasil-eksperimen.md`): sebagai red flag, R016 terlalu umum (14–30% paket kena). Jadi R016 tetap fitur.
- Di dashboard, R016 tetap terlihat lewat SHAP, misalnya "pagu 11 kali paket sejenis".

## 2. Indikasi pemecahan paket (adaptasi R011)

- Ini sudah ada sebagai **RF3**.
- Model sulit menangkapnya karena tiap pecahan memang dibuat terlihat normal: kecil dan di bawah ambang. Itu justru tujuan pemecahan.

## 3. Proporsi metode non-kompetitif tinggi (adaptasi R013), BARU diuji

**Definisi OCP:** satker ditandai bila porsi paket non-kompetitifnya ≥ Q3 + 1,5 × IQR.

**Masalah di data kita:** pagar itu 149–167%, karena porsi PL+PenL per satker terbelah dua kelompok (Q1 11%, Q3 66–68%). Jadi aturan OCP apa adanya tidak menandai satker mana pun.

**Adaptasi:**
- Satker (≥ 5 paket) yang **semua** paketnya Pengadaan Langsung atau Penunjukan Langsung, tanpa satu pun E-Purchasing atau tender.
- Jumlahnya 256 satker (2024) dan 304 satker (2025), sekitar 2–3% paket.
- Hasilnya sama untuk ukuran jumlah paket maupun nilai pagu.
- Contoh satker: Bappeda, Kesbangpol, DPMPTSP, Biro Organisasi, Inspektorat.

**Kebocoran:** tidak ada. AUC fitur vs R013 ≤ 0,65.

**Hasil (2024 / 2025 / 2025 provinsi uji):**

| Ukuran | R013 saja | RF1+RF3+RF4 (sekarang) | + R013 |
|---|---|---|---|
| Lipat 5% teratas | 2,00 / 2,11 / 2,26 | 0,84 / 0,95 / 0,98 | 0,98 / 1,17 / 1,21 |
| Lipat terkontrol (pagu × metode) | 1,63 / 2,04 / 2,12 | 0,98 / 0,80 / 0,83 | 1,08 / 1,00 / 1,04 |
| P@200 | 3,0% / 3,5% / 5,5% (acuan 2,2 / 3,3 / 3,4) | 6,5% / 2,0% / 2,5% | 8,5% / 5,0% / 7,0% |
| Acuan acak | | 15,9% / 13,4% / 12,3% | 17,7% / 15,9% / 14,9% |

Yang sama jika paket RF2 dikeluarkan dari daftar: R013 saja lipat terkontrol 2,07 / 2,05 / 2,38.

**Artinya:**
- R013 adalah red flag perencanaan pertama yang ditemukan model **2 kali lebih sering dari acak**. Hasil ini konsisten di dua tahun dan provinsi uji, dan tidak bocor.
- Tetapi P@200 di dashboard hanya naik 2% → 5% (2025). Sebabnya, 200 teratas perencanaan didominasi paket E-Purchasing dan tender, yang tidak mungkin kena RF1, RF3, RF4, maupun R013.
- R013 dipilih setelah melihat data, jadi di naskah statusnya red flag tambahan dengan adaptasi ambang yang harus ditulis.
