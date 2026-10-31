"""Tahap 4: kalimat penjelasan (templat) dan data JSON untuk dashboard."""
import json
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v1')
OUT = '/mnt/project-files/model-v1/'
d = pd.read_pickle(OUT + 'tahap1.pkl')
import s2_model  # noqa: F401,E402  (kelas Ensemble untuk membuka pickle)
hasil = pd.read_pickle(OUT + 'tahap2.pkl')
sh = pd.read_pickle(OUT + 'tahap3.pkl')
info, rf = d['info'], d['rf']
# Samakan nama provinsi dengan GeoJSON 38 provinsi
info['provinsi'] = info.provinsi.replace({'Bangka Belitung': 'Kepulauan Bangka Belitung',
                                          'Di Yogyakarta': 'Daerah Istimewa Yogyakarta', 'Dki Jakarta': 'DKI Jakarta'})

NAMA_RF = {'rf1_pl_dekat_ambang': 'Pengadaan langsung mendekati ambang',
           'rf2_pl_lewat_ambang': 'Pengadaan langsung melebihi ambang',
           'rf3_pemecahan_paket': 'Indikasi pemecahan paket',
           'rf4_penunjukan_langsung': 'Penunjukan langsung',
           'rf5_penyedia_dominan': 'Penyedia dominan di satker',
           'rf6_penyedia_serba_ada': 'Penyedia serba-ada'}
NAMA_F = {'log_pagu': 'Pagu', 'log_rasio_pagu_sejenis': 'Pagu dibanding paket sejenis',
          'porsi_pagu_satker': 'Porsi pagu di satker', 'log_jumlah_paket_satker': 'Jumlah paket satker',
          'proporsi_pl_satker': 'Proporsi pengadaan langsung satker', 'pdn': 'Produk dalam negeri',
          'umk': 'Status UMK', 'metode': 'Metode pengadaan', 'jenis': 'Jenis pengadaan',
          'rasio_realisasi': 'Rasio realisasi terhadap pagu', 'log_selisih_realisasi': 'Selisih realisasi dan pagu',
          'ubah_metode': 'Perubahan metode', 'porsi_pdn': 'Porsi nilai PDN', 'porsi_umk': 'Porsi nilai UMK',
          'sumber': 'Sumber transaksi'}


def rp(x):
    x = float(x)
    for b, s in [(1e12, ' T'), (1e9, ' M'), (1e6, ' jt'), (1e3, ' rb')]:
        if abs(x) >= b:
            return 'Rp' + f'{x / b:,.1f}'.replace(',', 'X').replace('.', ',').replace('X', '.') + s
    return f'Rp{x:,.0f}'


def pct(x):
    return f'{100 * x:.1f}%'.replace('.', ',')


def uraian(g, kode, F, med):
    """Nilai fitur paket dalam kalimat biasa, dibandingkan dengan median nasional jalurnya."""
    i, f = info.loc[kode], F.loc[kode]
    if g == 'log_pagu':
        return f'pagu {rp(i.pagu)}, median nasional {rp(10 ** med["log_pagu"])}'
    if g == 'log_rasio_pagu_sejenis':
        return f'pagu {10 ** f[g]:.1f} kali median paket {i.jenis.lower()} dengan metode yang sama'.replace('.', ',')
    if g == 'porsi_pagu_satker':
        return f'pagu ini {pct(f[g])} dari total pagu satker (median {pct(med[g])})'
    if g == 'log_jumlah_paket_satker':
        return f'satker memiliki {10 ** f[g]:,.0f} paket (median {10 ** med[g]:,.0f})'.replace(',', '.')
    if g == 'proporsi_pl_satker':
        return f'{pct(f[g])} paket satker lewat pengadaan langsung (median {pct(med[g])})'
    if g == 'pdn':
        return 'memakai produk dalam negeri' if f[g] else 'tidak memakai produk dalam negeri (sebagian besar paket memakai)'
    if g == 'umk':
        return 'paket untuk UMK' if f[g] else 'bukan paket untuk UMK (sebagian besar paket untuk UMK)'
    if g == 'metode':
        return f'metode {i.metode_pengadaan.lower()}'
    if g == 'jenis':
        return f'jenis {i.jenis.lower()}'
    if g == 'rasio_realisasi':
        return f'realisasi {pct(f[g])} dari pagu (median {pct(med[g])})'
    if g == 'log_selisih_realisasi':
        return f'selisih realisasi dan pagu {rp(abs(i.realisasi - i.pagu))}'
    if g == 'ubah_metode':
        return (f'metode berubah dari {i.metode_pengadaan.lower()} ke {str(i.metode_realisasi).lower()}'
                if f[g] else 'metode tidak berubah')
    if g == 'porsi_pdn':
        return f'porsi nilai PDN {pct(f[g])} (median {pct(med[g])})'
    if g == 'porsi_umk':
        return f'porsi nilai UMK {pct(f[g])} (median {pct(med[g])})'
    if g == 'sumber':
        return f'sumber transaksi {str(i.sumber_transaksi)}'
    return g


data = {'jalur': {}}
for jalur in ['perencanaan', 'pelaksanaan']:
    F = d['f_ren'] if jalur == 'perencanaan' else d['f_pel']
    h, s = hasil[jalur], sh[jalur]
    sk, flags = h['skor'], h['flags']
    med = F.median()
    sk['peringkat'] = sk.Ensemble.rank(ascending=False, method='first').astype(int)
    R = rf.loc[sk.index, flags]
    inf = info.loc[sk.index]

    # Ringkasan per provinsi
    prov = pd.DataFrame({'n': sk.groupby(inf.provinsi).size(),
                         'anomali': sk.anomali.groupby(inf.provinsi).sum(),
                         'pagu': inf.pagu.groupby(inf.provinsi).sum(),
                         'pagu_anomali': inf.pagu[sk.anomali].groupby(inf.provinsi[sk.anomali]).sum()}).fillna(0)
    prov['proporsi'] = prov.anomali / prov.n
    tot_rup = info.groupby('provinsi').size()
    prov['cakupan'] = prov.n / tot_rup.loc[prov.index]
    for c in flags:
        prov[c] = R[c].groupby(inf.provinsi).sum()

    # Paket yang ditampilkan: 200 teratas nasional (ada SHAP) + 25 teratas tiap provinsi
    pilih = set(s['shap'].index)
    for _, grp in sk.groupby(inf.provinsi):
        pilih |= set(grp.Ensemble.nlargest(25).index)
    paket = []
    for kode in sk.loc[list(pilih)].sort_values('peringkat').index:
        i, r_ = inf.loc[kode], sk.loc[kode]
        row = {'kode': kode, 'rank': int(r_.peringkat), 'skor': round(float(r_.Ensemble), 4),
               'IF': round(float(r_.IF), 3), 'LOF': round(float(r_.LOF), 3), 'AE': round(float(r_.AE), 3),
               'prov': i.provinsi, 'satker': i.nama_satuan_kerja.split(' - ')[0], 'nama': i.nama_paket,
               'metode': i.metode_pengadaan, 'jenis': i.jenis, 'pagu': float(i.pagu),
               'rf': [NAMA_RF[c] for c in flags if R.at[kode, c]]}
        if jalur == 'pelaksanaan':
            row.update(realisasi=float(i.realisasi), penyedia=str(i.penyedia), sumber=str(i.sumber_transaksi))
        if kode in s['shap'].index:
            v = s['shap'].loc[kode].sort_values(key=abs, ascending=False)
            row['shap'] = [[NAMA_F[g], round(float(x), 4), uraian(g, kode, F, med)] for g, x in v.items()]
            naik = [g for g, x in v.items() if x > 0][:3]
            alasan = '; '.join(uraian(g, kode, F, med) for g in naik)
            row['kalimat'] = (f'Paket ini berada di peringkat {r_.peringkat} dari {len(sk):,} paket jalur {jalur}. '.replace(',', '.')
                              + f'Faktor yang paling menaikkan skornya: {alasan}. '
                              + 'Ini penanda untuk ditelaah lebih lanjut, bukan bukti pelanggaran.')
        paket.append(row)

    ev = h['eval'].copy()
    data['jalur'][jalur] = {
        'n': int(len(sk)), 'anomali': int(sk.anomali.sum()), 'ambang': round(float(sk.Ensemble.quantile(0.95)), 4),
        'base': s['base'],
        'prov': {p: {k: (float(v) if not isinstance(v, str) else v) for k, v in r.items()} for p, r in prov.iterrows()},
        'paket': paket,
        'eval': ev.round(3).to_dict(orient='records'),
        'rf_total': {NAMA_RF[c]: int(R[c].sum()) for c in flags},
        'rf_dist_top200': sk.loc[sk.peringkat <= 200, 'jumlah_rf'].value_counts().sort_index().to_dict(),
        'rf_dist_semua': (sk.jumlah_rf.value_counts(normalize=True).sort_index()).round(4).to_dict(),
        'shap_global': {NAMA_F[g]: round(float(x), 4) for g, x in s['shap'].abs().mean().sort_values(ascending=False).items()},
        'korelasi': sk[['IF', 'LOF', 'AE']].corr('spearman').round(2).to_dict(),
    }
    print(jalur, 'paket ditampilkan', len(paket), 'dengan SHAP', sum('shap' in p for p in paket))

data['total_rup'] = int(len(info))
data['rf_nama'] = list(NAMA_RF.values())


def conv(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    raise TypeError(type(o))


json.dump(data, open(OUT + 'dashboard-data.json', 'w'), ensure_ascii=False, default=conv)
# Contoh kalimat
for j in data['jalur']:
    print(j, data['jalur'][j]['paket'][0]['kalimat'])
