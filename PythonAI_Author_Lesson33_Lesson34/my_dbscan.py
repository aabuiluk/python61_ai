from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=42)
df = pd.DataFrame(X, columns=["x1", "x2"])
df["cluster_kmeans"] = KMeans(n_clusters=4, random_state=42).fit_predict(X)
df["cluster_dbscan"] = DBSCAN(eps=0.8, min_samples=5).fit_predict(X)

noise = int((df["cluster_dbscan"] == -1).sum())
print(df["cluster_dbscan"].nunique() - 1, noise)                           # 4 16  (кластери без шуму, шум)
# Міні-завдання 9: допишіть кількість шумових точок у заголовок правої панелі

fig = plt.figure(figsize=(11, 4.5))
plt.subplot(1, 2, 1)
plt.scatter(df["x1"], df["x2"], c=df["cluster_kmeans"], s=12)
plt.title("K-Means Clustering")
plt.subplot(1, 2, 2)
plt.scatter(df["x1"], df["x2"], c=df["cluster_dbscan"], s=12)
plt.title("DBSCAN Clustering")
fig.savefig(Path(__file__).parent / "results" / "clustering_comparison.png")
