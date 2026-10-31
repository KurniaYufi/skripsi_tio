# Kandidat red flag khusus tahap pelaksanaan dari OCP (29 Oktober 2026)

Permintaan Tio: cari red flag khusus pelaksanaan dari OCP, jelaskan, **jangan train dulu**. Model **tidak dilatih ulang**. Yang dihitung hanya:
- jumlah paket yang terkena,
- tumpang tindih dengan RF1–RF6,
- seberapa sering kandidat muncul di peringkat skor v5 yang **sudah ada**.

Kode: `../c1_kandidat_rf_pelaksanaan.py`. Angka: `kandidat.csv`.

## Syarat kandidat

1. Bisa dihitung dari kolom realisasi INAPROC.
2. **Bukan fitur model.** Karena itu, realisasi > pagu (R068), selisih nilai kontrak (R059), dan perubahan metode (R012) tidak bisa dipakai: ketiganya sudah jadi fitur.
3. Tidak butuh tanggal atau data penawaran.

Dari 73 red flag OCP, hanya **4** yang lolos. Keempatnya memakai **nama penyedia**, karena hanya informasi itu yang baru muncul di tahap pelaksanaan dan belum dipakai sebagai fitur.

## Empat kandidat

| Kode | Arti sederhana | Aturan yang dipakai |
|---|---|---|
| **K1 (R049)** | Penyedia yang sama berulang kali dapat paket langsung yang nilainya mepet ambang | ≥ 2 paket pengadaan/penunjukan langsung dari satker yang sama ke penyedia yang sama, masing-masing 90–100% ambang PL |
| **K2 (R055)** | Penyedia yang sama dapat banyak paket langsung kecil yang kalau dijumlah melewati ambang (indikasi paket dipecah lewat penyedia) | ≥ 2 paket langsung di bawah ambang dari satker dan jenis yang sama ke penyedia yang sama, jumlahnya > ambang |
| **K3 (R050)** | Penyedia menguasai "pasar" satu satker untuk satu jenis pengadaan | Penyedia menerima > 40% nilai realisasi untuk satu satker × jenis (minimal 5 paket) |
| **K4 (R051)** | Pasar terkonsentrasi | HHI provinsi × jenis > 1.800 |

## Hasilnya

| | K1 (R049) | K2 (R055) | K3 (R050) | K4 (R051) |
|---|---|---|---|---|
| Jumlah paket (dari 105.456) | 2.274 (2,2%) | 12.403 (11,8%) | 4.644 (4,4%) | 2.039 (1,9%) |
| Paket baru (belum punya RF1–RF6) | **0** | 3.845 | 2.129 | 1.278 |
| Sama dengan red flag lama | hampir semua = RF1 | banyak = RF1/RF3 | separuh = RF5 | – |
| 5% teratas model v5 (acuan acak) | 1% (2,2%) | 3,5% (11,8%) | **7,7% (4,4%)** | 2,9% (1,9%) |
| Provinsi uji 5% (acuan acak) | 0,1% (1,8%) | 2,6% (14,2%) | **8,7% (6,0%)** | 0,4% (0,1%) |

## Penjelasan

- **K1 (R049) tidak menambah apa-apa.** Semua paketnya sudah kena RF1 (PL dekat ambang). Tidak disarankan.
- **K2 (R055) paling "khas pelaksanaan".** Polanya adalah pemecahan paket yang terlihat dari penyedianya: banyak paket kecil ke penyedia yang sama. Ada 3.845 paket baru. Tetapi model v5 **tidak menangkapnya**, bahkan di bawah acak. Ini wajar, karena model tidak punya informasi penyedia. Kalau K2 dijadikan red flag, Precision@K pelaksanaan malah turun.
- **K3 (R050) sedikit tertangkap.** Di provinsi uji 8,7% dibanding acak 6,0% (1,45 kali). Separuh paketnya sama dengan RF5, jadi K3 lebih tepat disebut "RF5 per jenis pengadaan".
- **K4 (R051) tidak cocok.** Ini ukuran tingkat pasar, bukan tingkat paket. Hanya 15 dari 151 pasar yang terkonsentrasi.

## Kesimpulan utama

Masalahnya bukan kurang red flag. **Model pelaksanaan melihat keanehan nilai realisasi** (realisasi dibanding pagu, PDN/UMK, sumber transaksi). Tetapi semua red flag OCP yang bisa dihitung untuk keanehan nilai realisasi (R059, R068) **sudah dipakai sebagai fitur**. Red flag yang tersisa semuanya soal **penyedia**, sedangkan model tidak melihat penyedia.

Jadi, dengan data yang ada, belum ada red flag OCP yang mengukur hal yang sama dengan yang dicari model pelaksanaan, tanpa sekaligus menjadi fitur.

## Pilihan

1. **Tidak menambah red flag (saran saya).** Evaluasi pelaksanaan bertumpu pada anomali buatan, karena "realisasi melebihi pagu" tertangkap 61%. Precision@K dilaporkan apa adanya, dan alasan di atas ditulis di pembahasan dan batasan.
2. **Tambah K3 (R050) sebagai RF7 khusus pelaksanaan.** Kenaikannya kecil (1,45 kali acak) dan mirip RF5.
3. **Tambah K2 (R055) sebagai red flag, lalu tambah fitur penyedia ke model.** Ini harus dilatih ulang. Risikonya kebocoran: fitur penyedia dan red flag penyedia saling "menyontek", sama seperti masalah metode di v1.
