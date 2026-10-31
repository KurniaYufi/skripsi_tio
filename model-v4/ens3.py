"""Model ensemble v4: IF + LOF + Autoencoder (seperti v2) yang dilatih dengan beberapa seed lalu dirata-rata.

Alasan: pada v2, daftar 200 paket teratas berubah cukup banyak bila seed acak diganti (rata-rata hanya
sekitar 40% paket yang sama). Merata-ratakan skor dari 5 kali pelatihan membuat peringkat lebih stabil.

v4: pilihan satu_arah = {kolom: 'nol' | 'median'}. Nilai kolom itu yang lebih kecil dari batas (0, atau median
data latih) disamakan dengan batasnya sebelum masuk model, sehingga hanya nilai yang LEBIH BESAR dari biasanya
yang bisa menaikkan skor. Dipakai untuk fitur pagu di jalur perencanaan (validasi-v3/pagu-kecil/).
"""
import sys
import numpy as np

sys.path.append('/mnt/project-files/model-v2')  # append, agar tidak menutupi s2_model milik v3
import ens2  # noqa: E402

SEEDS = [42, 1, 2, 3, 4]


class Ensemble3:
    def __init__(self, seeds=SEEDS, satu_arah=None, **kw):
        self.seeds, self.kw, self.satu_arah = list(seeds), kw, dict(satu_arah or {})

    def _potong(self, X):
        if not getattr(self, 'batas', None):
            return X
        X = np.array(X, dtype=float, copy=True)
        for j, b in self.batas.items():
            X[:, j] = np.maximum(X[:, j], b)
        return X

    def fit(self, F):
        self.cols = list(F.columns)
        self.batas = {self.cols.index(c): (0.0 if cara == 'nol' else float(F[c].median()))
                      for c, cara in self.satu_arah.items()}
        F = F.copy()
        for j, b in self.batas.items():
            F[self.cols[j]] = F[self.cols[j]].clip(lower=b)
        self.m = []
        for sd in self.seeds:
            ens2.SEED = sd
            self.m.append(ens2.Ensemble2(**self.kw).fit(F))
        ens2.SEED = 42
        return self

    def pct(self, X):
        """Persentil tiap model (rata-rata antar-seed), dibanding data latih."""
        X = self._potong(np.asarray(X, dtype=float))
        P = [m.pct(X) for m in self.m]
        return {k: np.mean([p[k] for p in P], axis=0) for k in ['IF', 'LOF', 'AE']}

    def score(self, X):
        P = self.pct(X)
        return (P['IF'] + P['LOF'] + P['AE']) / 3
