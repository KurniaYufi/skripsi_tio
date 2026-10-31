#!/bin/bash
# Menjalankan semua varian satker kecil, paling banyak 3 proses bersamaan. Penanda selesai: SELESAI.txt
cd /mnt/project-files/model-v5/eksperimen-satker-kecil
rm -f SELESAI.txt
run() { python3 ../x1_satker_kecil.py $1 $2 > log/$1_$2.log 2>&1 || echo "GAGAL $1 $2" >> GAGAL.txt; }
run perencanaan N5 & run perencanaan N3 & run perencanaan N10 & wait
run perencanaan N5-tanpaJ & run pelaksanaan N5 & run pelaksanaan N10 & wait
date > SELESAI.txt
