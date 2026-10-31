cd /mnt/project-files/model-v5
python3 x8_audit_varian.py perencanaan std+sj+np > eksperimen-audit/log_p3a.txt 2>&1 &
python3 x8_audit_varian.py perencanaan std+sj+np+nm > eksperimen-audit/log_p3b.txt 2>&1 &
python3 x8_audit_varian.py pelaksanaan tk+sj+np > eksperimen-audit/log_l3a.txt 2>&1 &
wait
python3 x9_banding_audit.py > eksperimen-audit/banding.txt 2>&1
echo AUDIT3_SELESAI
