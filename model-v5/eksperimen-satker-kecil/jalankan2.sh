#!/bin/bash
# Putaran 2: varian D, R, X5 (penanda selesai: SELESAI2.txt)
cd /mnt/project-files/model-v5/eksperimen-satker-kecil
rm -f SELESAI2.txt
run() { python3 ../x1_satker_kecil.py $1 $2 > log/$1_$2.log 2>&1 || echo "GAGAL $1 $2" >> GAGAL.txt; }
run perencanaan D & run perencanaan R & run perencanaan X5 & wait
run pelaksanaan D & run pelaksanaan R & wait
date > SELESAI2.txt
