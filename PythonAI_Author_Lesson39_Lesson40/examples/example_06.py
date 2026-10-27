"""**Факт. Назва інструмента в тексті ще не означає, що інструмент був виконаний.**

ReAct поєднує планування дії та отримання спостереження. У нашій простій реалізації
чат пропонує JSON-запит, Python перевіряє дозволену назву дії й аргументи, виконує пошук,
а отриманий результат ми вручну повертаємо в чат. Це один справжній цикл із людиною
як диспетчером. Кілька реплік моделі «Action/Observation» без виконання — лише імітація.

Дозволимо тільки lookup_book. Невідомий id дає None, а невідома дія — помилку. Жоден
рядок із чату не виконуємо через eval або exec. Модель не має самостійного доступу до БД.
Після результату пошуку фінальна відповідь має спиратися саме на повернений запис.

**Живий промпт прикладу:** «Доступна дія lookup_book(book_id). Потрібна ціна b01.
Поверніть тільки {"action":"lookup_book","book_id":"b01"}. Не вигадуйте observation».
Виконайте lookup у Python та наступною реплікою передайте фактичний результат.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
request = {"action":"lookup_book", "book_id":"b01"}  # ручний запит
if request["action"] != "lookup_book":
    raise ValueError("Недозволена дія")
observation = next((b for b in CATALOG if b["id"] == request["book_id"]), None)
print(json.dumps({"observation":observation}, ensure_ascii=False))

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Request', 'Allowlist', 'Lookup', 'Observation']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 6: data flow (not model measurements)')
fig.tight_layout()
plt.show()
