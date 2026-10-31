cd /mnt/project-files/model-v5
python3 x8_audit_varian.py perencanaan ns > eksperimen-audit/log_p_ns.txt 2>&1 &
python3 x8_audit_varian.py pelaksanaan ns > eksperimen-audit/log_l_ns.txt 2>&1 &
wait
python3 x9_banding_audit.py > eksperimen-audit/banding.txt 2>&1
python3 x10_tanpa_rf2.py > eksperimen-audit/banding_tanpa_rf2.txt 2>&1
echo AUDIT4_SELESAI
