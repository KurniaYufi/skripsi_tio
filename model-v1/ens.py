"""Kelas model ensemble (IF + LOF + Autoencoder) yang dipakai semua tahap."""
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

SEED = 42


class Ensemble:
    """Skor ensemble = rata-rata peringkat persentil tiga model terhadap sebaran skor nasional."""

    def fit(self, F):
        self.cols = list(F.columns)
        X = F.values.astype(float)
        self.sc = StandardScaler().fit(X)
        Z = self.sc.transform(X)
        rng = np.random.default_rng(SEED)
        self.iforest = IsolationForest(n_estimators=200, random_state=SEED, n_jobs=-1).fit(X)
        uniq = np.unique(Z.round(6), axis=0)
        idx = rng.choice(len(uniq), size=min(30000, len(uniq)), replace=False)
        self.lof = LocalOutlierFactor(n_neighbors=20, novelty=True, n_jobs=-1).fit(uniq[idx])
        idx = rng.choice(len(Z), size=min(100000, len(Z)), replace=False)
        k = Z.shape[1]
        self.ae = MLPRegressor(hidden_layer_sizes=(16, max(4, k // 4), 16), max_iter=60, early_stopping=True,
                               random_state=SEED).fit(Z[idx], Z[idx])
        S = self.raw(X)
        self.ref = {m: np.sort(s) for m, s in S.items()}
        return self

    def raw(self, X):
        Z = self.sc.transform(X)
        return {'IF': -self.iforest.score_samples(X),
                'LOF': -self.lof.score_samples(Z),
                'AE': ((self.ae.predict(Z) - Z) ** 2).mean(axis=1)}

    def pct(self, X):
        S = self.raw(X)
        return {m: np.searchsorted(self.ref[m], s, side='right') / len(self.ref[m]) for m, s in S.items()}

    def score(self, X):
        P = self.pct(np.asarray(X, dtype=float))
        return (P['IF'] + P['LOF'] + P['AE']) / 3
