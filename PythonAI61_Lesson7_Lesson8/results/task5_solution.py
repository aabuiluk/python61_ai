from pathlib import Path
import matplotlib.pyplot as plt

hours = [0, 4, 8, 12, 16, 20, 24]
temp = [15, 14, 18, 22, 25, 20, 17]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(hours, temp, color='darkorange', marker='o')
ax.set_title('Температура протягом доби')
ax.set_xlabel('Година')
ax.set_ylabel('Температура, °C')
ax.grid(True, alpha=0.3)
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
