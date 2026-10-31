"""Model ensemble v3: IF + LOF + Autoencoder (seperti v2) yang dilatih dengan beberapa seed lalu dirata-rata.

Alasan: pada v2, daftar 200 paket teratas berubah cukup banyak bila seed acak diganti (rata-rata hanya
sekitar 40% paket yang sama). Merata-ratakan skor dari 5 kali pelatihan membuat peringkat lebih stabil.
"""
import sys
import numpy as np

sys.path.append('/mnt/project-files/model-v2')  # append, agar tidak menutupi s2_model milik v3
import ens2  # noqa: E402

SEEDS = [42, 1, 2, 3, 4]


class Ensemble3:
    def __init__(self, seeds=SEEDS, **kw):
        self.seeds, self.kw = list(seeds), kw

    def fit(self, F):
        self.cols = list(F.columns)
        self.m = []
        for sd in self.seeds:
            ens2.SEED = sd
            self.m.append(ens2.Ensemble2(**self.kw).fit(F))
        ens2.SEED = 42
        return self

    def pct(self, X):
        """Persentil tiap model (rata-rata antar-seed), dibanding data latih."""
        X = np.asarray(X, dtype=float)
        P = [m.pct(X) for m in self.m]
        return {k: np.mean([p[k] for p in P], axis=0) for k in ['IF', 'LOF', 'AE']}

    def score(self, X):
        P = self.pct(X)
        return (P['IF'] + P['LOF'] + P['AE']) / 3
