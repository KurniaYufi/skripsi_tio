"""Membandingkan model v4 (BS: log_pagu ikut dipotong) dengan BS2 (log_pagu tidak dipotong), jalur perencanaan,
pada populasi yang sama (paket >= Rp1 jt). Keluaran: u4_banding.csv
"""
import json
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v4')
from s2_model import FLAGS  # noqa: E402

V1 = '/mnt/project-files/model-v1/'
OUT = '/mnt/project-files/validasi-v3/pagu-kecil/'
info = pd.read_pickle(V1 + 'tahap1.pkl')['info']
DEV = set(json.load(open(V1 + 'eksplorasi/provinsi_pilih.json')))
R = pd.read_pickle('/mnt/project-files/validasi-v3/red_flag_v3.pkl')[FLAGS['perencanaan']]
h = pd.read_pickle('/mnt/project-files/model-v4/tahap2.pkl')['perencanaan']
st = pd.read_csv('/mnt/project-files/model-v4/validasi/v_stabilitas.csv')
st = st[(st.jalur == 'perencanaan') & st.perbandingan.str.startswith('rata')].iloc[0]
var = {'v4 (BS)': dict(s=h['skor'].Ensemble, P=h['pct_rata'], jac200=st.jaccard_top200, jac5=st.jaccard_anomali5persen)}
s2, s2b = pd.read_pickle(OUT + 'skor_BS2.pkl'), pd.read_pickle(OUT + 'skor_BS2_seedB.pkl')
n5 = int(len(s2) * 0.05)
j = lambda a, b, k: len(set(a.nlargest(k).index) & set(b.nlargest(k).index)) / len(set(a.nlargest(k).index) | set(b.nlargest(k).index))  # noqa: E731
var['BS2'] = dict(s=s2, P=pd.read_pickle(OUT + 'pct_BS2.pkl'), jac200=j(s2, s2b, 200), jac5=j(s2, s2b, n5))
rows = []
for nama, v in var.items():
    s = v['s']
    ada = R.loc[s.index].any(axis=1)
    t4 = R.loc[s.index].drop(columns='rf4_penunjukan_langsung').any(axis=1)
    o = s.sort_values(ascending=False).index
    row = {'varian': nama, 'acuan': ada.mean()}
    for K in [50, 100, 200]:
        row[f'P@{K}'] = ada.loc[o[:K]].mean()
    row['P@200_tanpaRF4'] = t4.loc[o[:200]].mean()
    for mdl in ['IF', 'LOF', 'AE']:
        row[f'{mdl}_P@200'] = ada.loc[v['P'][mdl].nlargest(200).index].mean()
    dev = info.provinsi.loc[s.index].isin(DEV)
    for grp, m in [('pilih', dev), ('uji', ~dev)]:
        sg = s[m].sort_values(ascending=False).index
        row[f'{grp}_5%'] = ada.loc[sg[:int(len(sg) * 0.05)]].mean()
        row[f'{grp}_lift5%'] = row[f'{grp}_5%'] / ada[m].mean()
        row[f'{grp}_P@100'] = ada.loc[sg[:100]].mean()
    row['top200_pagu<10jt'] = (info.pagu.loc[o[:200]] < 1e7).mean()
    row['satker_terbanyak_top200'] = (info.provinsi + '|' + info.nama_satuan_kerja).loc[o[:200]].value_counts().iloc[0]
    row['jaccard_top200'], row['jaccard_5%'] = v['jac200'], v['jac5']
    rows.append(row)
df = pd.DataFrame(rows)
df.to_csv(OUT + 'u4_banding.csv', index=False)
print(df.round(3).T.to_string())
