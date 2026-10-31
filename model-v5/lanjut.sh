cd /mnt/project-files/model-v5
python3 s8_spi.py > log/s8.log 2>&1 || echo "GAGAL s8"
python3 s9_satker.py > log/s9.log 2>&1 || echo "GAGAL s9"
python3 s4_export.py > log/s4.log 2>&1 || echo "GAGAL s4"
python3 /mnt/project-files/dashboard-v1/build.py model-v5 > log/build.log 2>&1 || echo "GAGAL build"
python3 g2_anomali_buatan.py > log/g2.log 2>&1; python3 g3_spi.py > log/g3.log 2>&1
python3 x7_seed_noise.py > eksperimen-seed.log 2>&1 || echo "GAGAL x7"
echo LANJUT_SELESAI
