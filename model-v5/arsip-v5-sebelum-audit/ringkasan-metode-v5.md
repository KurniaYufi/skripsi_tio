# Ringkasan metode yang dipakai sekarang (model v5, 29 Oktober 2026)

Ini metode yang benar-benar dijalankan untuk dashboard saat ini. Naskah (Bab 3) **belum** disesuaikan dengan isi ini.

Kode ada di `/mnt/project-files/model-v5/`: s1_data.py (data, fitur, red flag), s2_model.py (model), s3_shap.py (SHAP), s5_validasi.py (uji), s4_export.py (dashboard).

---

## 1. Data dan lingkup

- **Sumber:** INAPROC 2025, yaitu RUP (rencana) dan Realisasi. Hanya 38 pemerintah provinsi.
- **Hanya paket penyedia.** Swakelola dan metode "Dikecualikan" tidak masuk.
- **Dua jalur yang dimodelkan terpisah:**

| Jalur | Isi | Jumlah paket |
|---|---|---|
| **Perencanaan** | semua paket RUP dalam lingkup, pagu ≥ Rp1 juta | 303.930 |
| **Pelaksanaan** | paket yang punya realisasi dan **semua** transaksinya sudah "Serah Terima" | 105.512 |

## 2. Pra-pemrosesan (pembersihan data)

**Data RUP**
1. Hanya cara pengadaan "Penyedia". Metode "Dikecualikan" dan isian "-" dibuang.
2. Pagu ≤ Rp10 ribu dibuang (hampir pasti salah isi). Tersisa 343.919 paket.
3. Kategori jenis dan metode **tidak digabung** (koreksi Tio, 29 Okt). "Terintegrasi" (172 paket) jadi jenis tersendiri, dan "Tender Cepat" (20 paket), Kontes, Sayembara, serta Kontrak Tahun Jamak jadi metode tersendiri. Paket Terintegrasi tidak ikut RF1–RF3, karena Perpres tidak memberi ambang pengadaan langsung untuk jenis ini.
4. Khusus jalur perencanaan: pagu < Rp1 juta tidak ikut model (lebih mirip salah isi atau belanja sangat kecil).

**Data realisasi** (7 aturan baru di v5, alasannya ada di `audit-data.md`)
1. **B1:** baris realisasi bernilai 0 atau minus dibuang (235 baris).
2. **B2:** baris yang provinsinya beda dengan provinsi RUP-nya dibuang (11 baris), karena kode RUP diduga salah ketik.
3. **B3, catatan ganda:** dalam satu kode RUP, baris dengan nilai persis sama dihitung sekali. Aturan ini hanya dipakai kalau totalnya melebihi pagu dan, setelah digabung, tidak lagi melebihi pagu. Ada 980 paket dan 1.362 baris yang terkena.
4. **B4:** nilai UMK 1–100 rupiah dibaca sebagai persen (379 baris).
5. **B5:** paket dengan realisasi < 1% atau > 10 kali pagu tidak masuk jalur pelaksanaan (59 paket), karena diduga salah satuan.
6. **C1:** nama penyedia dirapikan. "A, A" ditulis "A", dan PT/CV/UD dan sejenisnya diabaikan saat mencocokkan penyedia.
7. **C2:** penyedia yang sebenarnya unit pemerintah (kelurahan, dinas, dan sejenisnya) dianggap "tidak diketahui" (986 baris).

**Yang sengaja tidak diubah** (dicatat sebagai catatan kualitas data):
- RUP kembar
- pagu angka bulat
- nama paket pendek
- metode yang tidak cocok dengan jenisnya
- sisa 1.188 paket dengan realisasi melebihi pagu

## 3. Fitur (yang dilihat model)

**Prinsip:** fitur **tidak boleh** sama dengan red flag yang dipakai untuk menilai model. Karena itu kolom metode pengadaan, termasuk penunjukan langsung (= RF4), **tidak** jadi fitur.

**Satu arah** artinya hanya nilai yang **lebih besar** dari biasanya yang menaikkan skor. Pagu yang lebih kecil dari biasanya dianggap wajar.

| # | Fitur | Arti sederhana | Perencanaan | Pelaksanaan |
|---|---|---|---|---|
| 1 | log_pagu | besar pagu | ✓ | ✓ |
| 2 | log_rasio_pagu_sejenis | pagu dibanding median paket nasional dengan jenis + metode yang sama | ✓ satu arah | ✓ |
| 3 | log_rasio_pagu_satker | pagu dibanding median paket di satker yang sama | ✓ satu arah | ✓ |
| 4 | log_rasio_pagu_rata_satker | pagu dibanding rata-rata paket di satker yang sama | ✓ satu arah | ✓ satu arah |
| 5 | jenis pengadaan | Barang / Konstruksi / Konsultansi / Jasa Lainnya | ✓ | ✓ |
| 6 | pdn, umk | paket ditandai produk dalam negeri / untuk UMK di RUP | – | ✓ |
| 7 | proporsi_pl_satker | porsi paket pengadaan langsung di satker | – | ✓ |
| 8 | porsi_epurchasing_satker | porsi paket e-purchasing di satker | – | ✓ |
| 9 | rasio_realisasi | realisasi dibagi pagu (maksimal 5) | – | ✓ |
| 10 | log_selisih_realisasi | besar selisih rupiah realisasi dan pagu | – | ✓ |
| 11 | selisih_rasio_realisasi_sejenis | rasio realisasi dibanding paket sejenis | – | ✓ |
| 12 | ubah_metode | metode di realisasi beda dengan di RUP | – | ✓ |
| 13 | porsi_pdn, porsi_umk | porsi nilai realisasi untuk PDN / UMK | – | ✓ |
| 14 | sumber transaksi | E-Katalog / Non Tender / Tender | – | ✓ |

Perencanaan memakai 5 fitur (8 kolom). Pelaksanaan memakai 14 fitur (21 kolom).

**Fitur yang pernah ada tapi dibuang:**
- **one-hot metode:** sama dengan RF4.
- **jumlah paket satker dan porsi pagu satker:** membuat satker yang hanya punya 1–4 paket menguasai peringkat atas.
- **profil metode satker di perencanaan:** model jadi mengangkat penunjukan langsung lewat kebiasaan satker.

## 4. Red flag (untuk menilai model, BUKAN fitur)

| RF | Nama | Aturan | Jalur | Jumlah paket |
|---|---|---|---|---|
| RF1 | PL dekat ambang | pengadaan langsung dengan pagu 90–100% dari batas PL. Untuk konstruksi juga Rp180–200 jt (batas lama) | keduanya | 15.732 |
| RF2 | PL melewati ambang | pengadaan langsung dengan pagu di atas batas PL | keduanya | 7.486 |
| RF3 | Pemecahan paket | ≥ 2 paket PL bernama sangat mirip (TF-IDF ≥ 0,8) di satker dan jenis yang sama, dan jumlahnya melewati batas PL | keduanya | 28.503 |
| RF4 | Penunjukan langsung | metode = Penunjukan Langsung | keduanya | 3.984 |
| RF5 | Penyedia dominan | satu penyedia menerima > 40% nilai realisasi satker yang punya ≥ 5 paket (OCP R040) | pelaksanaan | 2.640 |
| RF6 | Penyedia serba-ada | penyedia menang di ≥ 3 jenis pengadaan berbeda (OCP R048) | pelaksanaan | 4.503 |

Batas PL: Barang dan Jasa Lainnya Rp200 jt, Konstruksi Rp400 jt, Konsultansi Rp100 jt (Perpres 46/2025).

## 5. Model

**Tiga model dijalankan bersama:**
- **Isolation Forest (IF):** mencari paket yang paling cepat "terpisah" dari yang lain. Memakai 200 pohon.
- **Local Outlier Factor (LOF):** membandingkan paket dengan 20 tetangga terdekatnya.
- **Autoencoder (AE):** belajar meniru data. Paket yang sulit ditiru dianggap aneh. Strukturnya 16–3–16 di perencanaan dan 16–5–16 di pelaksanaan.

**Penskalaan data:** perencanaan memakai quantile, pelaksanaan memakai standar (z).

**Cara skor dibuat:**
1. Skor tiap model diubah menjadi **persentil** (0–1), supaya ketiganya bisa dibandingkan.
2. **Skor ensemble = rata-rata persentil IF, LOF, dan AE.**
3. Semua dilatih ulang **5 kali dengan seed berbeda** lalu dirata-rata, supaya peringkat tidak berubah-ubah.
4. **Paket tidak lazim (anomali) = 5% skor teratas** di tiap jalur.

## 6. Penjelasan (SHAP)

- **Kernel SHAP** dihitung untuk 200 paket teratas di tiap jalur, dengan 50 paket acak sebagai pembanding.
- Kolom one-hot (jenis, sumber) dijumlahkan menjadi satu fitur.
- **Kalimat penjelasan disusun dari templat**, dari 3 fitur SHAP terbesar. LLM belum bisa dipakai karena server model diblokir dari lingkungan kerja ini.
- **Uji kesetiaan SHAP:** kalau 3 fitur teratas menurut SHAP diganti nilai normal, skor turun jauh lebih besar dibanding mengganti 3 fitur acak. Ini terjadi pada 98% paket perencanaan dan 93% paket pelaksanaan. Jadi SHAP memang menunjuk fitur yang berpengaruh.

## 7. Evaluasi

| Evaluasi | Isi | Hasil singkat |
|---|---|---|
| **Precision@K** (utama) | dari K paket teratas (50/100/200 dan 5%), berapa persen punya ≥ 1 red flag, dibanding acak | perencanaan 41,7% vs acak 15,8%; pelaksanaan 31,2% vs 26,3% |
| Provinsi pilih / uji | 19 provinsi untuk memilih pengaturan, 19 provinsi lain untuk menguji | perencanaan tetap kuat (39,9% vs 13,8%); pelaksanaan tipis (27,7% vs 25,6%) |
| Banding model tunggal | ensemble vs IF / LOF / AE saja | ensemble tidak selalu menang, tapi tidak pernah paling buruk |
| Penelaahan jumlah red flag | rata-rata jumlah red flag di paket teratas | ada di `validasi/` |
| Anomali buatan | 1.000 paket aneh buatan per jenis, berapa yang masuk 5% teratas | ekstrem & berkelompok 93–100%; lokal & dependensi 49–70%; dekat ambang & pagu dinaikkan sedikit 1–17% |
| Kestabilan | ganti seed, apakah peringkat sama | Spearman 0,97–0,98; 5% teratas sekitar 75% sama |

Rincian angka: `hasil-evaluasi-v5.md`.

## 8. Dashboard

- **Peta 38 provinsi.** Warnanya menunjukkan proporsi paket tidak lazim, dengan pilihan tampilan Perencanaan atau Pelaksanaan.
- **Daftar paket:** 500 teratas nasional ditambah 50 teratas tiap provinsi.
- **Rincian paket:** skor, grafik SHAP (untuk 200 teratas), kalimat penjelasan, bukti tiap red flag (misalnya daftar paket untuk pemecahan paket), dan "yang perlu dicek".

## 9. Yang belum diputuskan

1. Fitur "pagu dibanding paket bernama sama di satker yang sama" (pola A-B-C): dimasukkan ke model, dijadikan penanda terpisah, atau tidak dipakai.
2. Aturan catatan ganda dibatasi hanya untuk Non Tender/Pencatatan, tanpa E-Katalog.
3. Jalur pelaksanaan masih lemah: dilaporkan apa adanya, atau diperbaiki dulu.
4. Naskah Bab 1–3 belum disesuaikan dengan semua isi di atas.
