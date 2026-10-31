"""Tahap 2: Isolation Forest, LOF, Autoencoder, ensemble peringkat persentil, dan evaluasi."""
import sys
import pandas as pd

sys.path.insert(0, '/mnt/project-files/model-v1')
from ens import Ensemble  # noqa: E402

OUT = '/mnt/project-files/model-v1/'


def main():
    d = pd.read_pickle(OUT + 'tahap1.pkl')
    rf = d['rf']
    hasil = {}
    for jalur, F, flags in [('perencanaan', d['f_ren'], ['rf1_pl_dekat_ambang', 'rf2_pl_lewat_ambang',
                                                        'rf3_pemecahan_paket', 'rf4_penunjukan_langsung']),
                            ('pelaksanaan', d['f_pel'], list(rf.columns))]:
        m = Ensemble().fit(F)
        P = m.pct(F.values.astype(float))
        sk = pd.DataFrame(P, index=F.index)
        # Peringkat persentil dihitung ulang di dalam jalur; ensemble = rata-rata ketiganya
        for c in ['IF', 'LOF', 'AE']:
            sk[c] = sk[c].rank(pct=True)
        sk['Ensemble'] = sk[['IF', 'LOF', 'AE']].mean(axis=1)
        sk['anomali'] = sk.Ensemble >= sk.Ensemble.quantile(0.95)
        R = rf.loc[F.index, flags]
        sk['jumlah_rf'] = R.sum(axis=1)

        ev = []
        for mdl in ['Ensemble', 'IF', 'LOF', 'AE']:
            order = sk[mdl].sort_values(ascending=False).index
            row = {'model': mdl}
            for K in [50, 100, 200]:
                top = sk.loc[order[:K], 'jumlah_rf']
                row[f'P@{K}'] = (top > 0).mean()
                row[f'rata_rf@{K}'] = top.mean()
            ev.append(row)
        ev.append({'model': 'Semua paket (acuan)', **{f'P@{K}': (sk.jumlah_rf > 0).mean() for K in [50, 100, 200]},
                   **{f'rata_rf@{K}': sk.jumlah_rf.mean() for K in [50, 100, 200]}})
        ev = pd.DataFrame(ev)
        print('\n==', jalur, F.shape, 'iterasi AE', m.ae.n_iter_)
        print(ev.round(3).to_string(index=False))
        top200 = sk.Ensemble.sort_values(ascending=False).index[:200]
        print('sebaran jumlah red flag 200 teratas:', sk.loc[top200, 'jumlah_rf'].value_counts().sort_index().to_dict())
        print('sebaran jumlah red flag semua     :', (sk.jumlah_rf.value_counts(normalize=True).sort_index() * 100).round(2).to_dict())
        print('korelasi spearman antarmodel:\n', sk[['IF', 'LOF', 'AE']].corr('spearman').round(2))
        hasil[jalur] = dict(model=m, skor=sk, eval=ev, flags=flags)

    pd.to_pickle(hasil, OUT + 'tahap2.pkl')


if __name__ == '__main__':
    main()
