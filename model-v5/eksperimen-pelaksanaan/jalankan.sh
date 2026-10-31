#!/bin/bash
cd /mnt/project-files/model-v5
for v in Q S QS K QSK L50 P; do
  python3 x5_pelaksanaan.py $v > eksperimen-pelaksanaan/log_$v.txt 2>&1 || echo "GAGAL $v"
done
python3 x6_banding_pelaksanaan.py > eksperimen-pelaksanaan/banding.txt 2>&1
echo EKSPLORASI_SELESAI
