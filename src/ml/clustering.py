"""Patient phenotyping, unsupervised clustering, auto-labeling, and anomaly detection."""

from typing import Any

import numpy as np
from sklearn.cluster import HDBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.svm import OneClassSVM


def evaluate_optimal_k(
    X: np.ndarray, k_range: range = range(2, 7), random_state: int = 42
) -> tuple[int, dict[int, float], dict[int, float]]:
    """Determine optimal number of clusters using Silhouette and Davies-Bouldin metrics."""
    silhouette_scores: dict[int, float] = {}
    davies_bouldin_scores: dict[int, float] = {}

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(X)
        sil = float(silhouette_score(X, labels))
        db = float(davies_bouldin_score(X, labels))
        silhouette_scores[k] = sil
        davies_bouldin_scores[k] = db

    # Pick k that maximizes silhouette score while keeping DB low
    best_k = max(silhouette_scores.keys(), key=lambda k: silhouette_scores[k])
    return best_k, silhouette_scores, davies_bouldin_scores


class PatientPhenotypeSegmenter:
    """Unsupervised patient phenotyping engine with auto-labeling and anomaly detection."""

    def __init__(self, n_clusters: int = 4, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans: KMeans | None = None
        self.gmm: GaussianMixture | None = None
        self.hdbscan: HDBSCAN | None = None
        self.pca: PCA | None = None
        self.isolation_forest: IsolationForest | None = None
        self.one_class_svm: OneClassSVM | None = None
        self.cluster_profiles: dict[int, dict[str, Any]] = {}

    def fit(self, X: np.ndarray, feature_names: list[str]) -> "PatientPhenotypeSegmenter":
        """Fit clustering models, auto-generate cluster labels, and calibrate anomaly detector."""
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state, n_init=10)
        labels = self.kmeans.fit_predict(X)

        self.gmm = GaussianMixture(n_components=self.n_clusters, random_state=self.random_state)
        self.gmm.fit(X)

        self.hdbscan = HDBSCAN(min_cluster_size=15)
        self.hdbscan.fit(X)

        # 2D PCA for visual map embedding
        self.pca = PCA(n_components=2, random_state=self.random_state)
        self.pca.fit(X)

        # Anomaly detectors for flagging erroneous or dangerous outlier readings
        self.isolation_forest = IsolationForest(contamination=0.03, random_state=self.random_state)
        self.isolation_forest.fit(X)

        self.one_class_svm = OneClassSVM(nu=0.03, kernel="rbf")
        self.one_class_svm.fit(X)

        # Compute cluster center profiles and generate automated semantic labels
        self.cluster_profiles = self._generate_cluster_profiles(X, labels, feature_names)
        return self

    def _generate_cluster_profiles(
        self, X: np.ndarray, labels: np.ndarray, feature_names: list[str]
    ) -> dict[int, dict[str, Any]]:
        """Synthesize clinical labels by analyzing mean biomarker deviations per cluster."""
        profiles = {}
        global_mean = np.mean(X, axis=0)

        for c in range(self.n_clusters):
            c_mask = labels == c
            if not np.any(c_mask):
                continue
            c_mean = np.mean(X[c_mask], axis=0)

            # Analyze relative differences
            diffs = c_mean - global_mean
            top_positive = np.argsort(diffs)[-2:]
            top_negative = np.argsort(diffs)[:2]

            pos_traits = [feature_names[i] for i in top_positive if diffs[i] > 0.2]
            neg_traits = [feature_names[i] for i in top_negative if diffs[i] < -0.2]

            # Semantic auto-labeling rules
            label = "Balanced Health Profile"
            priorities = ["Maintain routine annual health check-up", "Balanced nutritious diet"]

            traits_str = " ".join(pos_traits + neg_traits).lower()
            if "bmi" in traits_str or "weight" in traits_str:
                if "physical_activity" in traits_str or "activity" in traits_str:
                    label = "Elevated BMI & Low Physical Activity"
                    priorities = [
                        "Target 150 minutes of moderate aerobic activity weekly",
                        "Portion control and calorie reduction per ICMR dietary guidelines",
                        "Weekly self-monitoring of weight and waist circumference",
                    ]
                else:
                    label = "Central Adiposity & Metabolic Risk"
                    priorities = [
                        "Screen for insulin resistance and lipid dyslipidemia",
                        "Reduce refined carbohydrates and saturated cooking oils",
                    ]
            elif "bp" in traits_str or "systolic" in traits_str or "diastolic" in traits_str:
                label = "Vascular Strain & Elevated Blood Pressure"
                priorities = [
                    "Limit dietary sodium to < 5g (1 teaspoon) daily",
                    "Home blood pressure monitoring twice weekly",
                    "Stress reduction through yoga or pranayama",
                ]
            elif "glucose" in traits_str or "hba1c" in traits_str:
                label = "Impaired Glycemic Control & High Diabetes Risk"
                priorities = [
                    "Consult doctor for formal Fasting Blood Glucose and OGTT",
                    "Eliminate sugar-sweetened beverages and sweets",
                    "Increase high-fiber legumes and millets (bajra, ragi, jowar)",
                ]

            profiles[c] = {
                "cluster_id": c,
                "label": label,
                "size": int(np.sum(c_mask)),
                "priorities": priorities,
            }

        return profiles

    def segment_patient(
        self, x_patient: np.ndarray
    ) -> tuple[int, str, list[str], bool, float, list[float]]:
        """Assign patient to cluster, detect anomalies, and compute 2D visual PCA coordinates."""
        if self.kmeans is None or self.pca is None or self.isolation_forest is None:
            raise RuntimeError("Segmenter is not fitted.")

        cluster_id = int(self.kmeans.predict(x_patient)[0])
        profile = self.cluster_profiles.get(
            cluster_id,
            {"label": "General Metabolic Risk Group", "priorities": ["Lifestyle modification"]},
        )

        # Anomaly detection: -1 indicates anomaly in Isolation Forest
        anomaly_pred = int(self.isolation_forest.predict(x_patient)[0])
        is_anomaly = anomaly_pred == -1
        anomaly_score = float(-self.isolation_forest.score_samples(x_patient)[0])

        # PCA 2D coordinates for interactive front-end visual risk scatter
        pca_coords = [float(c) for c in self.pca.transform(x_patient)[0]]

        return (
            cluster_id,
            profile["label"],
            profile["priorities"],
            is_anomaly,
            anomaly_score,
            pca_coords,
        )
