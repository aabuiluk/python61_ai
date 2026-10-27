"""**Факт. Формат JSON і правдивість даних — дві різні перевірки.**

У 38 ми будували інструкцію з ролі, контексту, задачі та формату. Роль задає стиль,
контекст містить факти, задача визначає дію, формат дозволяє прочитати результат кодом.
Фраза «будь експертом» не додає каталогу, якого модель не бачить.

Приклад нижче — ручний fixture, не відповідь сервісу. Валідатор спочатку читає JSON,
потім перевіряє точний набір ключів, тип ціни та пару id/ціна за каталогом. Значення true
у Python є підкласом int, тому для ціни тут навмисно використано type(...) is int.

**За 15 хв:** 3 хв структура промпту; 4 хв приклад; 6 хв вправа; 2 хв перевірка.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
fixture = '{"book_id":"b01","price":320}'
print(validate(fixture))  # True
print(validate('{"book_id":"b01","price":299}'))  # False

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Role + data', 'Task', 'JSON', 'Validator']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 2: data flow (not model measurements)')
fig.tight_layout()
plt.show()
