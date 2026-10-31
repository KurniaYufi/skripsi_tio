#!/bin/bash
# Model v4: jalankan seluruh tahap, lalu uji tambahan (ablasi, SPI, satker), export ulang, dan gambar.
cd /mnt/project-files/model-v4
bash jalankan.sh || exit 1
python3 s7_ablasi.py > log/s7.log 2>&1 || { echo "GAGAL s7"; exit 1; }
python3 s8_spi.py > log/s8.log 2>&1 || { echo "GAGAL s8"; exit 1; }
python3 s9_satker.py > log/s9.log 2>&1 || { echo "GAGAL s9"; exit 1; }
python3 s4_export.py > log/s4.log 2>&1 || { echo "GAGAL s4 kedua"; exit 1; }
python3 /mnt/project-files/dashboard-v1/build.py model-v4 > log/build.log 2>&1 || { echo "GAGAL build kedua"; exit 1; }
python3 g2_anomali_buatan.py > log/g2.log 2>&1; python3 g3_spi.py > log/g3.log 2>&1
echo "SEMUA SELESAI (termasuk s7-s9)"
