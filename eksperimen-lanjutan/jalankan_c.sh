#!/bin/bash
cd /mnt/project-files/eksperimen-lanjutan
for v in lofk10 lofk50 lofk100 lof100rb per_metode gabung_tahun plus_bulat plus_kembar plus_ambang lofk5 seed10; do
  python3 c_latih.py $v > log/c_$v.log 2>&1 && echo "OK $v" || echo "GAGAL $v"
done
echo SELESAI
