cd /mnt/project-files/model-v5
until grep -q AUDIT1_SELESAI eksperimen-audit/jalankan1.log; do sleep 20; done
python3 x8_audit_varian.py pelaksanaan tk > eksperimen-audit/log_l_tk.txt 2>&1 &
python3 x8_audit_varian.py pelaksanaan tk+sj > eksperimen-audit/log_l_tk_sj.txt 2>&1 &
wait
python3 x9_banding_audit.py > eksperimen-audit/banding.txt 2>&1
echo AUDIT2_SELESAI
