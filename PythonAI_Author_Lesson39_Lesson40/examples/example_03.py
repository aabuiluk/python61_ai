"""**Факт. Складну задачу зручніше розбити на результати, які можна перевірити окремо.**

Chain of Thought (CoT) історично означає промпти з проміжними міркуваннями. У сучасному
практикумі вимагайте короткий план, перевірювані обчислення та підсумок; повна прихована
траса мислення не потрібна. Пояснення моделі саме по собі не доводить правильності.

Приклад: покупець має 800 грн. Дві книги по 320 коштують 640, залишок 160. Якщо розділити
задачу на пошук ціни → множення → порівняння з бюджетом, можна перевірити кожен результат.
Арифметику виконує Python. LLM може оформити коротке пояснення вже перевірених значень.
Це корисніше за безумовну віру у фразу «думай крок за кроком».

**Живий промпт прикладу:** «Дані: b01 = 320 грн; 2 примірники; бюджет 800 грн.
Поверніть JSON з total, remaining, fits. Використовуйте тільки ці числа.
Після JSON не додавайте тексту». Зіставте відповідь з обчисленням Python.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
price, quantity, budget = 320, 2, 800
total = price * quantity
print({"total": total, "remaining": budget-total, "fits": total <= budget})

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Price', 'Quantity', 'Total', 'Budget check']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 3: data flow (not model measurements)')
fig.tight_layout()
plt.show()
