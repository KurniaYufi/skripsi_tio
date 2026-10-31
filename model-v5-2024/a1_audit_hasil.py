"""Audit hasil model setelah dilatih (aturan sejak 2026-10-29): komposisi paket teratas vs seluruh data, dan fitur
SHAP terbesar (bila tahap3.pkl sudah sesuai dengan tahap2.pkl). Tidak mengubah apa pun, hanya mencetak.
Pemakaian: python3 a1_audit_hasil.py [folder_tahap2]"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v5')
import ens3  # noqa: E402,F401

O = '/mnt/project-files/model-v5-2024/'
d = pd.read_pickle(O + 'tahap1.pkl')
info = d['info']
H = pd.read_pickle((sys.argv[1] if len(sys.argv) > 1 else O) + 'tahap2.pkl')
sat = info.provinsi + '|' + info.nama_satuan_kerja
n_sat = sat.map(sat.value_counts())


def pagu_kelas(p):
    return pd.cut(p, [0, 1e6, 1e7, 1e8, 1e9, 1e10, 1e13], labels=['<1jt', '1-10jt', '10-100jt', '100jt-1M', '1-10M', '>10M'])


for j in H:
    s = H[j]['skor'].Ensemble.sort_values(ascending=False)
    idx = s.index
    top200, top5 = idx[:200], idx[:int(len(idx) * .05)]
    print(f'\n######## {j}: {len(idx)} paket, fitur {list(H[j]["F"].columns)}')
    kol = {'jenis': info.jenis, 'metode': info.metode_pengadaan, 'pagu': pagu_kelas(info.pagu),
           'satker<10 paket': (n_sat < 10).map({True: 'ya', False: 'tidak'}), 'provinsi': info.provinsi}
    if j == 'pelaksanaan':
        kol['sumber'] = info.sumber_transaksi
    for nama, ser in kol.items():
        t = pd.DataFrame({'semua': ser.loc[idx].value_counts(normalize=True),
                          '5% teratas': ser.loc[top5].value_counts(normalize=True),
                          '200 teratas': ser.loc[top200].value_counts(normalize=True)}).fillna(0)
        t['lipat 200/semua'] = t['200 teratas'] / t['semua']
        t = t.sort_values('semua', ascending=False)
        print(f'-- {nama}'); print((t.head(8) * [100, 100, 100, 1]).round(1).to_string())
    print('satker terbanyak di 200 teratas:', sat.loc[top200].value_counts().head(3).to_dict())
    F = H[j]['F']
    print('-- nilai fitur: median semua vs median 200 teratas')
    print(pd.DataFrame({'semua': F.median(), '200 teratas': F.loc[top200].median(),
                        '% 200 teratas di atas p99': (F.loc[top200] > F.quantile(.99)).mean() * 100}).round(3).to_string())
    for m in ['IF', 'LOF', 'AE']:
        print(f'   200 teratas {m} vs Ensemble beririsan: {len(set(H[j]["skor"][m].nlargest(200).index) & set(top200))}')
try:
    S = pd.read_pickle(O + 'tahap3.pkl')
    for j in S:
        sv = S[j]['shap']
        if not set(sv.index) <= set(H[j]['skor'].index) or len(set(sv.columns) - set(H[j]['F'].columns)):
            print(j, 'tahap3 tidak cocok dengan tahap2 (belum dihitung ulang)')
            continue
        print(f'\n-- SHAP {j}: fitur terbesar per paket', sv.abs().idxmax(axis=1).value_counts().to_dict())
        print('   rata |SHAP|', sv.abs().mean().sort_values(ascending=False).round(3).to_dict())
except FileNotFoundError:
    pass
