cd /mnt/project-files/eksperimen-lanjutan
for v in ren_penuh_2025 pel_penuh_2025 ren_lintas_2025 ren_tanpalintas_2025 pel_tanpapdnumk_2025 ren_tanpalintas_2024 pel_penuh_2024; do
  python3 j2_latih_rancangan.py $v > log/j2_$v.log 2>&1
done
echo SEMUA_SELESAI > log/j2_selesai.flag
