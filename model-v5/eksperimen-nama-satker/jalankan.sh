#!/bin/bash
# Varian fitur nama di satker; penanda selesai SELESAI.txt
cd /mnt/project-files/model-v5/eksperimen-nama-satker
rm -f SELESAI.txt
run() { python3 ../x3_nama_satker.py $1 $2 > log/$1_$2.log 2>&1 || echo "GAGAL $1 $2" >> GAGAL.txt; }
run perencanaan M2 & run perencanaan M3 & run pelaksanaan M2 & run pelaksanaan M3 & wait
date > SELESAI.txt
