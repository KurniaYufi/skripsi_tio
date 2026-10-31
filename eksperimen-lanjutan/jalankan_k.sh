#!/bin/bash
# Dua antrean paralel varian K3 (ide project sebelah)
cd /mnt/project-files/eksperimen-lanjutan
q() { for vt in "$@"; do set -- $vt; python3 k3_latih_sebelah.py ${vt%:*} ${vt#*:} > log/k3_${vt%:*}_${vt#*:}.log 2>&1 && echo "OK $vt" || echo "GAGAL $vt"; done; }
A="ren_pangsa:2024 ren_kembar:2024 ren_nonkomp:2024 ren_zrank:2024 ren_robust:2024 ren_sebelah:2024 ren_pangsa:2025 ren_kembar:2025 ren_nonkomp:2025 ren_zrank:2025 ren_robust:2025 ren_sebelah:2025"
B="pel_zrasio:2024 pel_jangkauan:2024 pel_kebiasaan:2024 pel_pangsa:2024 pel_nonkomp:2024 pel_kembar:2024 pel_robust:2024 pel_sebelah:2024 pel_zrasio:2025 pel_jangkauan:2025 pel_kebiasaan:2025 pel_pangsa:2025 pel_nonkomp:2025 pel_kembar:2025 pel_robust:2025 pel_sebelah:2025"
q $A > log/k3_antrean_A.log 2>&1 &
q $B > log/k3_antrean_B.log 2>&1 &
wait
echo SELESAI > log/k3_selesai.flag
