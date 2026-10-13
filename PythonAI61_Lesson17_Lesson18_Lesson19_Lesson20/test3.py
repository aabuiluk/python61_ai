import matplotlib.pyplot as plt
vals = [0.8, 0.32, 0.064, 0.0064]
fig, ax = plt.subplots(figsize=(5.2, 3.0))
ax.plot([1, 2, 3, 4], vals, marker="o", color="#ff7d9a", lw=2.4)
ax.set_xlabel("глибина"); ax.set_ylabel("добуток похідних")
ax.set_yscale("log")
fig.tight_layout()
plt.show()
# -> лінія вниз на log-осі