from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

df = load_wine(as_frame=True).frame
print(df.shape)                                   # (178, 14)
X = df.drop(columns="target")                     # target не йде в SVD
X_scaled = StandardScaler().fit_transform(X)

# Міні-завдання 6: поставте n_components=3 і надрукуйте суму часток
# Міні-завдання 7 (блок 2): замініть TruncatedSVD на PCA
svd = TruncatedSVD(n_components=2, random_state=42)
Z = svd.fit_transform(X_scaled)
print(Z.shape, svd.explained_variance_ratio_.round(3))   # (178, 2) [0.362 0.192]

plt.scatter(Z[:, 0], Z[:, 1], c=df["target"])
plt.xlabel("SVD-1")
plt.ylabel("SVD-2")
plt.title("SVD Projection")
plt.savefig(Path(__file__).parent / "results" / "my_svd_projection.png")
