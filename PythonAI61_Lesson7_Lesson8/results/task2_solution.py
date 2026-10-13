from pathlib import Path
import matplotlib.pyplot as plt

months = ['Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер']
sales = [150, 200, 250, 300, 280, 320]
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(months, sales, color='royalblue')
ax.set_title('Продажі за 6 місяців')
ax.set_xlabel('Місяць')
ax.set_ylabel('Продажі')
plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
plt.show()
