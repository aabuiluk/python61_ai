from pathlib import Path
import matplotlib.pyplot as plt

labels = ["Продукти", "Одяг", "Техніка"]
shares = [40, 30, 30]
names = ["Alex", "Irene", "John", "Mary", "Boris"]
scores = [85, 92, 78, 90, 88]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].pie(shares, labels=labels, autopct="%1.0f%%", startangle=90)
axes[0].set_title("Розподіл продажів")

axes[1].bar(names, scores, color="darkorange")
axes[1].set_title("Результати тесту")
axes[1].set_xlabel("Студент")
axes[1].set_ylabel("Бали")

fig.tight_layout()
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
