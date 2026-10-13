from pathlib import Path
import matplotlib.pyplot as plt

labels = ['Продукти', 'Одяг', 'Техніка']
shares = [40, 30, 30]
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(shares, labels=labels, autopct='%1.0f%%', startangle=90)
ax.set_title('Розподіл продажів')
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
