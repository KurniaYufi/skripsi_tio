#!/bin/bash
cd /mnt/project-files/model-v5
bash jalankan_semua.sh > log/semua.log 2>&1
python3 a1_audit_hasil.py > log/a1.log 2>&1
python3 x10_tanpa_rf2.py > log/x10.log 2>&1
python3 x7_seed_noise.py > log/x7.log 2>&1
echo SELESAI_AUDIT5 >> log/semua.log
