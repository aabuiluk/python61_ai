from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

X, _ = make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=42)   # номери хмар не беремо
df = pd.DataFrame(X, columns=["x1", "x2"])

kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster_kmeans"] = kmeans.fit_predict(df[["x1", "x2"]])
print(df["cluster_kmeans"].value_counts().sort_index().tolist())          # [125, 125, 125, 125]
print(round(silhouette_score(df[["x1", "x2"]], df["cluster_kmeans"]), 3))  # 0.791
# Міні-завдання 6: порахуйте silhouette для k = 3, 4, 5, 6 у циклі — яке k найкраще?

plt.scatter(df["x1"], df["x2"], c=df["cluster_kmeans"], s=12)
centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], marker="D", s=120, color="black")
plt.title("K-Means, k = 4")
plt.savefig(Path(__file__).parent / "results" / "my_kmeans.png")
