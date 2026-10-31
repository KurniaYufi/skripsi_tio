"""Model ensemble v2: IF + LOF + Autoencoder dengan penskalaan dan pengaturan per jalur."""
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import QuantileTransformer, StandardScaler

SEED = 42


class Ensemble2:
    def __init__(self, skala='std', if_max_samples='auto', lof_k=20, ae_b=None, ae_iter=60, skala_sama=None):
        # ae_iter: batas iterasi autoencoder. 60 (v2-v5 awal) ternyata berhenti sebelum konvergen; v5 audit memakai 300
        # dan berhenti sendiri lewat early_stopping (~160 iterasi).
        self.skala, self.if_max_samples, self.lof_k, self.ae_b, self.ae_iter = skala, if_max_samples, lof_k, ae_b, ae_iter
        # skala_sama {kolom: kolom_acuan}: kolom dibagi simpangan baku kolom acuan, bukan simpangan bakunya sendiri.
        # Untuk fitur yang hampir semuanya nol (simpangan baku sangat kecil), agar selisih kecil tidak tampak ekstrem.
        self.skala_sama = dict(skala_sama or {})

    def _fit_scaler(self, X):
        if self.skala == 'std':
            self.sc = StandardScaler().fit(X)
            for c, acuan in getattr(self, 'skala_sama', {}).items():
                self.sc.scale_[self.cols.index(c)] = self.sc.scale_[self.cols.index(acuan)]
        else:  # quantile untuk kolom kontinu, kolom biner (0/1) dibiarkan
            self.biner = np.array([set(np.unique(X[:, j])) <= {0.0, 1.0} for j in range(X.shape[1])])
            self.sc = QuantileTransformer(n_quantiles=1000, output_distribution='normal', subsample=200000,
                                          random_state=SEED).fit(X[:, ~self.biner])

    def _z(self, X):
        if self.skala == 'std':
            return self.sc.transform(X)
        Z = X.copy()
        Z[:, ~self.biner] = self.sc.transform(X[:, ~self.biner])
        return Z

    def fit(self, F):
        self.cols = list(F.columns)
        X = F.values.astype(float)
        self._fit_scaler(X)
        Z = self._z(X)
        self.iforest = IsolationForest(n_estimators=200, max_samples=self.if_max_samples, random_state=SEED, n_jobs=-1).fit(X)
        rng = np.random.default_rng(SEED)
        uniq = np.unique(Z.round(6), axis=0)
        idx = rng.choice(len(uniq), size=min(30000, len(uniq)), replace=False)
        self.lof = LocalOutlierFactor(n_neighbors=self.lof_k, novelty=True, n_jobs=-1).fit(uniq[idx])
        rng = np.random.default_rng(SEED)
        idx = rng.choice(len(Z), size=min(100000, len(Z)), replace=False)
        b = self.ae_b or max(4, Z.shape[1] // 4)
        self.ae = MLPRegressor(hidden_layer_sizes=(16, b, 16), max_iter=self.ae_iter, early_stopping=True, random_state=SEED).fit(Z[idx], Z[idx])
        self.ref = {m: np.sort(s) for m, s in self.raw(X).items()}
        return self

    def raw(self, X):
        Z = self._z(X)
        return {'IF': -self.iforest.score_samples(X), 'LOF': -self.lof.score_samples(Z),
                'AE': ((self.ae.predict(Z) - Z) ** 2).mean(axis=1)}

    def pct(self, X):
        return {m: np.searchsorted(self.ref[m], s, side='right') / len(self.ref[m]) for m, s in self.raw(X).items()}

    def score(self, X):
        P = self.pct(np.asarray(X, dtype=float))
        return (P['IF'] + P['LOF'] + P['AE']) / 3
