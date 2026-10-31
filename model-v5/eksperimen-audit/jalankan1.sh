cd /mnt/project-files/model-v5
python3 x8_audit_varian.py perencanaan std > eksperimen-audit/log_p_std.txt 2>&1 &
python3 x8_audit_varian.py perencanaan std+sj > eksperimen-audit/log_p_std_sj.txt 2>&1 &
wait
python3 x8_audit_varian.py perencanaan std+rata > eksperimen-audit/log_p_std_rata.txt 2>&1 &
python3 x8_audit_varian.py pelaksanaan sj > eksperimen-audit/log_l_sj.txt 2>&1 &
wait
echo AUDIT1_SELESAI
