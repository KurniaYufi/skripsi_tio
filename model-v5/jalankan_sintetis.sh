#!/bin/bash
cd /mnt/project-files/model-v5
python3 s5_validasi.py > log/s5.log 2>&1 || { echo GAGAL_s5 > log/sintetis.log; exit 1; }
python3 s7_ablasi.py > log/s7.log 2>&1 || { echo GAGAL_s7 > log/sintetis.log; exit 1; }
python3 s4_export.py > log/s4.log 2>&1 || { echo GAGAL_s4 > log/sintetis.log; exit 1; }
python3 /mnt/project-files/dashboard-v1/build.py model-v5 > log/build.log 2>&1
python3 g2_anomali_buatan.py > log/g2.log 2>&1
echo SELESAI_SINTETIS > log/sintetis.log
