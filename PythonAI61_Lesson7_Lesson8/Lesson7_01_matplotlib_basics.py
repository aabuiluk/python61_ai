from pathlib import Path
import matplotlib.pyplot as plt

x = list(range(1, 11))
y = [value ** 2 for value in x]
hours = [0, 4, 8, 12, 16, 20, 24]
temp = [15, 14, 18, 22, 25, 20, 17]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(x, y, color="crimson", marker="o")
axes[0].set_title("y = x²")
axes[0].set_xlabel("X")
axes[0].set_ylabel("Y")

axes[1].plot(hours, temp, color="darkorange", marker="o")
axes[1].set_title("Температура протягом доби")
axes[1].set_xlabel("Година")
axes[1].set_ylabel("°C")
axes[1].grid(True, alpha=0.3)

fig.tight_layout()
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
