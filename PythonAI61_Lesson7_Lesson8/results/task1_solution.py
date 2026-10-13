from pathlib import Path
import matplotlib.pyplot as plt

x = list(range(1, 11))
y = [v ** 2 for v in x]
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, y, color='crimson', marker='o', linewidth=2)
ax.set_title('Графік функції y = x²')
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
