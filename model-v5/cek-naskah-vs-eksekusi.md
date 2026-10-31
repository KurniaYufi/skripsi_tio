# Cek naskah vs eksekusi model (30 Oktober 2026)

Naskah yang dicek: tab **"Bab 1-3 (LLM)"** di Google Doc SKRIPSI TIO (seluruh isi tab dibaca).
Eksekusi yang dicek: kode model-v5 hasil audit (dashboard versi 10).

**Ringkasnya:**
- **Kerangka besarnya masih sesuai.** Dua jalur, ensemble IF + LOF + Autoencoder, tanpa label, Precision@K K = 50/100/200 dibanding model individual, Kernel SHAP 200 teratas, paket anomali = 5% teratas nasional, peta proporsi per provinsi.
- **Isi tekniknya banyak yang berubah.** Ada di 4 tempat: lingkup data, pra-pemrosesan, fitur (Tabel 3.2), dan red flag (Tabel 3.3). Cara menggabungkan skor juga berubah.
- **LLM belum dijalankan.** Naskah menulis kalimat dibuat oleh LLM, tapi dashboard sekarang masih memakai kalimat templat.
- **Banyak uji tambahan yang belum ada di naskah.** Contohnya anomali buatan, 5 seed, pembagian provinsi pilih/uji, dan Precision@K tanpa RF2.

---

## 1. Yang sudah sesuai

| Bagian naskah | Isi | Status |
|---|---|---|
| Bab 1, 3.2.3.3 | Dua jalur: perencanaan (RUP) dan pelaksanaan (RUP + realisasi), dipasangkan lewat kode RUP | Sesuai |
| 3.2.4 | Model dilatih nasional, lalu hasilnya diringkas per provinsi | Sesuai |
| 3.2.4.1 | Fitur distandardisasi sebelum LOF dan Autoencoder | Sesuai (skala std) |
| 3.2.4.3 | Tiga model diberi bobot sama | Sesuai |
| 3.2.5.2 | Precision@K pada K = 50, 100, 200, per jalur | Sesuai |
| 3.2.5.3 | Ensemble dibanding IF, LOF, AE | Sesuai |
| 3.2.5.5 | Kernel SHAP untuk 200 paket teratas per jalur | Sesuai |
| 3.2.6.1 | Paket anomali = 5% skor tertinggi nasional; peta memakai proporsi | Sesuai |
| 3.2.6.2 | Peta 38 provinsi, pilihan jalur, daftar peringkat, rincian paket + SHAP | Sesuai |
| 3.2.3.4 (paragraf akhir) | Red flag tidak dimasukkan langsung sebagai fitur | Prinsipnya sesuai, tapi RF2 masih bocor lewat fitur sejenis (lihat bagian 3) |

## 2. Yang berbeda dari naskah

| Bagian naskah | Naskah sekarang | Yang benar-benar dijalankan |
|---|---|---|
| Batasan 1.3 no. 2, 3.2.3.1 | Tahun anggaran **2025–2026** | **2025 saja** |
| Batasan 1.3, 3.2.3.2 | Swakelola disebut di pra-pemrosesan; tidak ada batasan cara pengadaan | Hanya **paket penyedia**. Swakelola dan metode "Dikecualikan" tidak dipakai (keputusan 28 Okt). Belum ditulis di Batasan |
| 3.2.3.2 Pra-pemrosesan | 4 langkah umum (saring, hapus ganda, seragamkan, gabung realisasi) | Ada aturan tambahan: pagu ≤ Rp10 ribu dibuang; perencanaan hanya pagu ≥ Rp1 jt; pelaksanaan hanya realisasi yang seluruhnya **Serah Terima**; aturan B1–B6 (realisasi ≤ 0, beda provinsi, catatan ganda, UMK persen, rasio < 0,01 atau > 9,5, tender banyak penyedia); nama penyedia dirapikan (C1/C2) |
| 3.2.3.3 | Perencanaan = "seluruh paket RUP" | 303.930 paket (pagu ≥ Rp1 jt). Pelaksanaan 105.499 paket |
| 3.2.3.4 + **Tabel 3.2** | 13 fitur: one-hot metode, jenis, sumber transaksi, cara pengadaan, PDN, porsi pagu satker, jumlah paket satker, ubah metode, porsi PDN/UMK, dll. | **Hanya fitur angka, tanpa one-hot.** Perencanaan (4): log pagu, rasio pagu vs sejenis, rasio pagu vs satker (kelompok ≥ 4), rasio pagu vs paket bernama sama di satker. Pelaksanaan (5): tiga yang pertama + rasio realisasi (dipotong 5) + log selisih realisasi. Rasio pagu bersifat **satu arah** (hanya yang lebih mahal dianggap aneh) |
| 3.2.3.4 kalimat | "Kolom kategori diubah dengan one-hot encoding" | Tidak dipakai lagi. Alasannya, kategori jarang dianggap aneh dan kolom metode/jenis bocor ke red flag |
| 2.2.9 + 3.2.4.2 | Normalisasi **min-max** (Pers. 2.9) | **Persentil (peringkat)** tiap model, lalu dirata-rata. Min-max tidak dipakai |
| 3.2.4 (tidak disebut) | Satu kali pelatihan | Skor = **rata-rata 5 seed** supaya peringkat stabil |
| 2.2.6 | 100 pohon, subsampel 256 | 200 pohon; subsampel 2.048 (perencanaan) dan bawaan (pelaksanaan) |
| 3.2.4.1 (tidak disebut) | — | LOF k = 20 dilatih pada 30.000 sampel; Autoencoder 16–b–16 (b = 2 perencanaan, 3 pelaksanaan), 300 iterasi, dilatih pada 100.000 sampel |
| **Tabel 3.3** Red flag | 4 indikator: dekat ambang PL (≥ 90%), pemecahan paket, penyedia banyak paket (**persentil 95**), penunjukan langsung | **6 red flag**: RF1 dekat ambang (+ konstruksi 180–200 jt), **RF2 PL lewat ambang (baru)**, RF3 pemecahan paket (TF-IDF ≥ 0,8), RF4 penunjukan langsung, **RF5 penyedia dominan > 40% realisasi satker (OCP R040, ganti persentil 95)**, **RF6 penyedia serba-ada ≥ 3 jenis (OCP R048, baru)** |
| 2.2.3 Red flag | Hanya Decarolis & Giorgiantonio + KPK; menyebut penyerapan ~100% sebagai red flag (Hasmi) | Sumber RF5/RF6 = **OCP (2024)**, belum ada di Bab 2. Penyerapan ~100% **tidak dipakai**. Hasmi membahas per akun, bukan per paket, jadi kalimat ini sebaiknya dihapus |
| 2.2.5 | Anomali "dari sisi pagu, metode pemilihan, jenis pengadaan, waktu, ..." | Metode, jenis, dan waktu **bukan fitur lagi** |
| Gambar 2.6 (contoh SHAP) | Fitur contoh: metode pemilihan, jenis pengadaan, waktu pemilihan | Fitur itu tidak ada di model. Contohnya sebaiknya diganti dengan fitur yang dipakai |
| 3.2.5.6–3.2.5.7, RM2, Batasan no. 6 | Kalimat dari **LLM lokal** + pemeriksaan otomatis, templat sebagai cadangan | **LLM belum dijalankan.** Dashboard memakai **kalimat templat** untuk semua paket (Hugging Face diblokir dari server). Pilihannya: LLM dijalankan di laptop Tio, atau naskah diubah |

## 3. Yang sudah dijalankan tapi belum ada di naskah

| Yang dijalankan | Keterangan | Saran letak |
|---|---|---|
| Precision@K **5% teratas** | Selain K = 50/100/200 | 3.2.5.2 |
| Pembagian **19 provinsi pilih / 19 provinsi uji** | Fitur dipilih di provinsi pilih, lalu diuji di provinsi uji (supaya tidak "menyontek") | 3.2.4 atau 3.2.5 |
| **Precision@K tanpa RF2** | Karena fitur sejenis bocor ke RF2. Tanpa RF2, hasilnya setara acak | 3.2.5 + Bab 4 (menunggu pilihan Tio di kartu) |
| **Precision@K per red flag** | Menunjukkan pola mana yang terbaca model (RF2, RF4, RF5) dan mana yang tidak (RF1, RF3, RF6) | 3.2.5 (opsi yang saya sarankan) |
| **Anomali buatan** (8 pola) | Bukti utama bahwa model bereaksi terhadap pola ketidaklaziman | 3.2.5 (bagian baru) |
| **Stabilitas 5 seed** | Hasil dilaporkan sebagai rentang | 3.2.4 / 3.2.5 |
| **Ablasi** (kombinasi 2 model) | LOF+AE kadang lebih tinggi dari ensemble 3 model | 3.2.5.3 |
| **Uji SHAP-hapus** | Menghapus 3 fitur SHAP teratas → skor turun pada 100% paket | 3.2.5.5 |
| **SPI KPK** | Provinsi rentan punya lebih banyak paket tidak lazim (perencanaan p = 0,004, tanpa Papua p = 0,08) | 3.2.7 / Bab 4 |
| Red flag tampil di dashboard | Centang red flag ditampilkan di samping skor | 3.2.6.2 |

Penelaahan jumlah red flag (3.2.5.4) **sudah dihitung**: rata-rata jumlah red flag di K teratas, serta sebaran jumlah red flag di 200 teratas dibanding seluruh paket. Hasilnya sudah ada di data dashboard, tinggal dijadikan tabel untuk Bab 4.

## 4. Yang perlu diputuskan Tio sebelum naskah diubah

1. Cara melaporkan evaluasi: per red flag / tambah fitur / model + aturan (kartu di thread).
2. Perbaikan fitur sejenis tanpa metode (latih ulang) atau tetap.
3. LLM: **DIPUTUSKAN Tio 2026-10-30: tidak pakai LLM.** Naskah nanti diganti menjadi kalimat templat. Bagian yang terdampak: RM2, Tujuan 2, dan Batasan no. 6 di Bab 1; subbab 2.2.11 LLM di Bab 2 (penomoran 2.2.12–2.2.13 bergeser kembali) beserta 4 referensi LLM; Gambar 3.2 dan 3.7 serta 3.2.5.6–3.2.5.7 di Bab 3. Cukup tambahkan satu kalimat LLM sebagai saran penelitian lanjutan.
4. Tahun data: ubah naskah menjadi 2025 saja (saran), atau tambah data 2026.
5. Uji tambahan mana yang masuk naskah (saran: anomali buatan, per red flag, 5 seed, provinsi pilih/uji).

Setelah itu, revisi naskah dibuat di **tab baru** (Bab 1 Batasan, Bab 2.2.3/2.2.5/2.2.9/Gambar 2.6, Bab 3 Tabel 3.2/3.3 dan 3.2.3–3.2.5).

## 5. Nasib 13 fitur di Tabel 3.2 (semuanya sudah diuji, v1 sampai audit v5)

| Fitur di Tabel 3.2 | Status | Alasan (bukti) |
|---|---|---|
| Nilai pagu (log) | **Dipakai** | Tanpa log pagu, peringkat tidak sejalan dengan red flag mana pun (eksperimen np) |
| Rasio pagu terhadap paket sejenis | **Dipakai, diperbaiki** | Median, satu arah. Catatan: masih bocor ke RF2 karena kelompoknya jenis + metode |
| Porsi pagu pada satker | **Diganti** rasio pagu dibanding median satker × jenis (kelompok ≥ 4) | Porsi dan jumlah paket membuat satker kecil otomatis aneh (58% dari 50 teratas berasal dari satker kecil) |
| Jumlah paket satker | **Dibuang** | Sama seperti di atas |
| Metode pengadaan (one-hot) | **Dibuang** | Penunjukan langsung = RF4. Di v1, tanpa RF4 Precision@K perencanaan 9,2%, di bawah acak 11,5% |
| Jenis pengadaan (one-hot) | **Dibuang** | Jenis yang jarang dianggap aneh: 114 dari 200 teratas Jasa Konsultansi, SHAP jenis terbesar di 152 paket; bocor ke RF1/RF3 |
| Cara pengadaan | **Tidak relevan** | Data hanya paket penyedia |
| Produk dalam negeri (biner RUP) | **Dibuang** | 98% bernilai 1, jadi yang 0 otomatis dianggap aneh |
| Rasio realisasi terhadap pagu | **Dipakai** | Dipotong di 5 kali; fitur SHAP terbanyak di pelaksanaan |
| Perubahan metode | **Dibuang** | Hanya 161 paket (0,15%). Satu kolom biner langka langsung mengisi puncak |
| Porsi nilai PDN | **Dibuang** | Nilai 0 menumpuk di "Pencatatan Non Tender", jadi yang terbaca cara pencatatan, bukan ketidaklaziman |
| Porsi nilai UMK | **Dibuang** | Sama seperti PDN |
| Sumber transaksi (one-hot) | **Dibuang** | Tender hanya 2,6%, dan sumber transaksi sebenarnya wakil dari metode |
| (baru) Selisih realisasi (log) | **Dipakai** | Besar selisih rupiah antara realisasi dan pagu |
| (baru) Pagu dibanding paket bernama sama di satker | **Dipakai, perencanaan saja** | Pola A-B-C usulan Tio. Di pelaksanaan fitur ini menutupi keanehan realisasi |
