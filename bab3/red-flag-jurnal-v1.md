# Red Flag yang Biasa Dipakai di Jurnal, dan Mana yang Bisa Dihitung dari Data Tio

Dicek 2026-10-28. Data: data_rup_2025.csv dan dara_realisasi_2025.csv, paket penyedia selain "Dikecualikan" dan pagu > Rp10.000 (343.920 paket; 136.163 punya pasangan realisasi).

## 1. Sumber yang dipakai (semua gratis)

| Sumber | Status akses | Isi tentang red flag |
|---|---|---|
| Schneider dos Santos et al. (2025) | Sudah di Library | Tinjauan pustaka. Red flag yang paling sering dipakai: penawar tunggal (11 studi), prosedur terbatas/tidak kompetitif (7), pengumuman tidak dipublikasikan (6), kriteria evaluasi berisiko (5). Penyedia yang sering menang disebut masih perlu divalidasi. |
| Salazar et al. (2024), VigIA | Sudah di Library | 11 red flag biner: penawar tunggal, penyedia serba-ada, riwayat kontrak penyedia sangat tinggi (persentil 95), penunjukan langsung, rezim khusus, masa pengumuman ekstrem, data salah/kosong, masa keputusan ekstrem, riwayat pembengkakan biaya, riwayat keterlambatan, kontrak tanpa proses pengadaan. |
| Decarolis & Giorgiantonio (2022) | Sudah dirujuk di Bab 2.2.3 | 4 kelompok: kelengkapan informasi, prosedur pemilihan, kriteria pemenang, hambatan peserta. |
| KPK (2026) | Sudah dirujuk | Pemecahan paket mendekati ambang pengadaan langsung, penyedia dengan banyak paket. |
| **Open Contracting Partnership (2024), *Red flags in public procurement: A guide to using data to detect and mitigate risks*** | **Baru.** PDF gratis (lisensi CC BY-NC-SA 4.0): https://open-contracting.org/wp-content/uploads/2024/12/OCP2024-RedFlagProcurement-1.pdf. Sudah diunggah Tio ke Library (/mnt/project-files/OCP2024-RedFlagProcurement-1.pdf, 100 halaman). | Katalog 73 red flag (R001-R073) dari tahap perencanaan sampai pelaksanaan. Penulis utamanya Camila Salazar, orang yang sama dengan VigIA. Ini bukan jurnal, tapi panduan lembaga, setara dengan sumber LKPP/KPK. |
| Fazekas & Kocsis (2020), *British Journal of Political Science* | Gratis (open access di Cambridge) | Rujukan klasik indikator risiko dari data pengadaan. **Tahun 2020, di luar batas 2021-2026**, jadi tidak disarankan. |

## 2. Red flag dari jurnal vs data Tio

| Red flag | Dipakai oleh | Bisa dihitung? | Jumlah paket 2025 | Catatan |
|---|---|---|---|---|
| Penawar tunggal | Schneider (11 studi), VigIA, OCP R018 | **Tidak** | - | Tidak ada data jumlah penawar |
| Masa pengumuman / masa keputusan terlalu pendek atau panjang | VigIA, OCP R003, R014, R061, R062 | **Tidak** | - | Tidak ada tanggal |
| Kriteria evaluasi, harga penawaran, penawar didiskualifikasi | Schneider, OCP R021-R038 | **Tidak** | - | Tidak ada data penawaran |
| Riwayat pembengkakan biaya / keterlambatan penyedia | VigIA | **Tidak** | - | Tidak ada data riwayat kontrak |
| Pengadaan langsung mendekati ambang (90-100%) | KPK (2026), OCP R002 (hlm. 24) | Ya (RUP) | 7.383 | Sudah dipakai |
| **Pengadaan langsung melebihi ambang** | OCP R010 (hlm. 32); Perpres 46/2025 Pasal 38 ayat (3) | Ya (RUP) | **7.485** | Ambang Rp200 jt (barang/jasa lainnya) dan Rp400 jt (konstruksi) sudah dicek di Pasal 38 ayat (3). Ambang konsultansi Rp100 jt belum dicek ulang |
| Pemecahan paket | KPK (2026), OCP R011 (hlm. 33), R055 (hlm. 77) | Ya (RUP) | ±61 ribu (kasar) | Sudah dipakai; aturannya perlu dipersempit |
| Penunjukan langsung | Schneider (prosedur terbatas), VigIA, OCP R010 | Ya (RUP) | 3.992 | Sudah dipakai |
| Penyedia dengan banyak paket di satu satker | VigIA (persentil 95), OCP R040 (hlm. 62), KPK (2026) | Ya (realisasi) | 35.331 (jumlah paket > p95) atau 5.590 (penyedia memegang > 50% nilai satker, satker ≥ 5 paket) | Sudah dipakai. Versi porsi nilai lebih ketat dan sesuai OCP R040 |
| **Penyedia serba-ada** (menang di banyak jenis pengadaan) | VigIA, OCP R048 (hlm. 70) | Ya (realisasi), kasar | **4.766** (264 penyedia menang di ≥ 3 jenis pengadaan) | Baru. Kasar: OCP memakai klasifikasi barang, data Tio hanya punya 4 jenis pengadaan |
| Realisasi melebihi pagu | OCP R059, R068 | Ya (realisasi) | 3.579 (2,6%) | **Bentrok dengan fitur rasio realisasi/pagu.** Hanya bisa dipakai kalau fitur itu dibuang |
| Metode di realisasi berbeda dari rencana | OCP R012 | Ya, tapi sedikit | 469 (kebanyakan PL menjadi "-") | Terlalu sedikit dan bentrok dengan fitur perubahan metode |
| Kontrak tanpa proses pengadaan (realisasi tanpa RUP) | VigIA, OCP R063 | Bisa dihitung, **tidak bisa dipakai** | 89.250 baris realisasi kodenya tidak ada di RUP | Paket ini tidak masuk dataset (tidak punya RUP), jadi tidak ikut diperingkat model. Kebanyakan dari E-Katalog, kemungkinan beda kode, bukan pelanggaran |
| Data penting kosong | VigIA, OCP R005 | Ya | 19.597 baris realisasi penyedia "-" | Kemungkinan besar paket yang belum selesai, jadi lebih cocok untuk pra-pemrosesan |

## 3. Usulan set red flag

| No | Red flag | Jalur | Sumber |
|---|---|---|---|
| 1 | Pengadaan langsung mendekati ambang | Perencanaan + pelaksanaan | KPK (2026); OCP (2024) |
| 2 | Pengadaan langsung melebihi ambang | Perencanaan + pelaksanaan | Perpres 46/2025; OCP (2024) |
| 3 | Pemecahan paket | Perencanaan + pelaksanaan | KPK (2026); OCP (2024) |
| 4 | Penunjukan langsung | Perencanaan + pelaksanaan | Schneider dos Santos et al. (2025); Salazar et al. (2024) |
| 5 | Penyedia dominan di satu satker | Pelaksanaan saja | Salazar et al. (2024); OCP (2024) |
| 6 | Penyedia serba-ada | Pelaksanaan saja | Salazar et al. (2024); OCP (2024) |

Catatan:
- Red flag 5 dan 6 butuh nama penyedia, yang hanya ada di data realisasi. Jadi jalur perencanaan dinilai dengan 4 red flag, jalur pelaksanaan dengan 6.
- Tidak ada yang bentrok dengan fitur model di review-fitur-v1.md, kecuali penunjukan langsung yang masih tercakup di one-hot metode (catatan lama).
- Jumlah 4-6 red flag itu wajar. VigIA memakai 11, tetapi data Kolombia punya tanggal dan jumlah penawar. Sebagian besar dari 73 red flag OCP juga butuh data penawaran, tanggal, atau kontrak yang tidak ada di RUP dan realisasi.

Nomor halaman OCP = nomor yang tercetak di halaman PDF (nomor halaman file PDF = tercetak + 1).
