from pathlib import Path
import matplotlib.pyplot as plt

height = [160, 165, 170, 175, 180]
weight = [55, 60, 70, 72, 80]
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(height, weight, color='green', s=80)
ax.set_title('Залежність ваги від зросту')
ax.set_xlabel('Зріст, см')
ax.set_ylabel('Вага, кг')
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
