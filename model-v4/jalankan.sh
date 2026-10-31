#!/bin/bash
# Menjalankan seluruh tahap model v4 berurutan (tahap 3 dan 5 paralel). Log di model-v4/log/.
cd /mnt/project-files/model-v4
mkdir -p log validasi
python3 s2_model.py > log/s2.log 2>&1 || { echo "GAGAL s2"; exit 1; }
echo "s2 selesai"
python3 s3_shap.py perencanaan > log/s3_perencanaan.log 2>&1 &
P1=$!
python3 s3_shap.py pelaksanaan > log/s3_pelaksanaan.log 2>&1 &
P2=$!
python3 s5_validasi.py > log/s5.log 2>&1 &
P3=$!
wait $P1 || { echo "GAGAL s3 perencanaan"; exit 1; }
wait $P2 || { echo "GAGAL s3 pelaksanaan"; exit 1; }
python3 -c "
import pandas as pd
O='/mnt/project-files/model-v4/'
pd.to_pickle({j: pd.read_pickle(O+f'tahap3_{j}.pkl') for j in ['perencanaan','pelaksanaan']}, O+'tahap3.pkl')"
echo "s3 selesai"
python3 s6_shap_hapus.py > log/s6.log 2>&1 || { echo "GAGAL s6"; exit 1; }
echo "s6 selesai"
wait $P3 || { echo "GAGAL s5"; exit 1; }
echo "s5 selesai"
python3 s10_bukti_redflag.py > log/s10.log 2>&1 || { echo "GAGAL s10"; exit 1; }
python3 s4_export.py > log/s4.log 2>&1 || { echo "GAGAL s4"; exit 1; }
echo "s4 selesai"
python3 /mnt/project-files/dashboard-v1/build.py model-v4 > log/build.log 2>&1 || { echo "GAGAL build"; exit 1; }
echo "SEMUA SELESAI"
