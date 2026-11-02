"""44.5 · Бюджет пам’яті та межі контексту

**Факт 11. Історію обмежують завершеними парами реплік, не випадковими останніми рядками.**

Безмежний список повідомлень збільшує контекст і може повернути давно неактуальні факти.
Збережіть системні правила окремо, потім додайте перевірений стан, актуальні джерела,
обмежену історію та нове питання. Якщо бюджет малий, не залишайте відповідь assistant
без її попереднього user-питання. Нижче обмежуємо кількість завершених пар, а не токени.

Дві пари довгих реплік можуть зайняти більше токенів, ніж десять коротких. Для справжнього
провайдера потрібен сумісний token counter та резерв під відповідь. Підрахунок символів
або слів — лише евристика. Обрізання повідомлень не дорівнює підсумуванню; summary може
втратити заперечення, тому вимагає перевірки та джерела. In-memory wrapper сам не задає
бюджет і не видаляє старі повідомлення за вашим бізнес-правилом.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
history = [HumanMessage(content="Q1"),AIMessage(content="A1"),
           HumanMessage(content="Q2"),AIMessage(content="A2"),
           HumanMessage(content="Q3"),AIMessage(content="A3")]
recent = history[-4:]  # тут точно дві завершені пари з підготовленого входу
print([m.content for m in recent])
print("Це ліміт реплік, не підрахунок токенів.")

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Full turns', 'Pair budget', 'Recent turns', 'Token reserve']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 11: data flow, not model measurements')
fig.tight_layout()
plt.show()
