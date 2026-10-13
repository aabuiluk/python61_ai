from pathlib import Path
import matplotlib.pyplot as plt

names = ['Alex', 'Irene', 'John', 'Mary', 'Boris']
scores = [85, 92, 78, 90, 88]
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(names, scores, color='darkorange')
ax.set_title('Результати тесту')
ax.set_xlabel('Студент')
ax.set_ylabel('Бали')
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
