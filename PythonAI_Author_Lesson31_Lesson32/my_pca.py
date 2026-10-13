from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler

df = load_wine(as_frame=True).frame
X_scaled = StandardScaler().fit_transform(df.drop(columns="target"))

Z_svd = TruncatedSVD(n_components=2, random_state=42).fit_transform(X_scaled)
pca = PCA(n_components=2, random_state=42)
Z_pca = pca.fit_transform(X_scaled)
print(pca.explained_variance_ratio_.round(4), pca.explained_variance_ratio_.sum().round(4))
# Міні-завдання 8: домножте першу вісь PCA на -1 →  Z_pca[:, 0] *= -1
# Міні-завдання 9 (крок 15): надрукуйте PCA(n_components=0.95).fit(X_scaled).n_components_

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, Z, name in [(axes[0], Z_svd, "SVD"), (axes[1], Z_pca, "PCA")]:
    ax.scatter(Z[:, 0], Z[:, 1], c=df["target"])
    ax.set_title(f"{name} Projection")
    ax.set_xlabel(f"{name}-1")
    ax.set_ylabel(f"{name}-2")
fig.savefig(Path(__file__).parent / "results" / "my_comparison.png")
