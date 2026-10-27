"""**Факт. LLM генерує текст, а код магазину перевіряє ціну за каталогом.**

Класичний класифікатор може прогнозувати категорію звернення. LLM може написати відповідь;
diffusion-модель — створити зображення обкладинки; multimodal-модель — обробити текст разом
із зображенням. Тип входу й виходу допомагає обрати модель. Назва хмарної платформи не є типом моделі.

У 37 ми розкладали систему на клієнт, сервіс і модель. Повторіть межу: правдоподібна відповідь
не стає записом бази даних. Якщо модель написала ціну 299, а каталог містить 320, прийняти 299
не можна. Для публічного сервісу потрібні ще контроль доступу й журналювання; у цьому практикумі
вистачить синтетичного каталогу й локального валідатора.

**За 15 хв:** 3 хв пригадати типи; 4 хв приклад; 6 хв власна вправа; 2 хв обговорення.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
operations = {"визначити тему листа": "classification", "написати опис": "generation"}
print(operations)
print("Ціну перевіряємо у каталозі:", CATALOG[0]["price"])

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Input', 'Model / code', 'Output', 'Check']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 1: data flow (not model measurements)')
fig.tight_layout()
plt.show()
