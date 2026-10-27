"""**Факт. Кілька альтернатив корисні лише разом із явним правилом відбору.**

Tree of Thoughts (ToT) досліджує кілька можливих продовжень із оцінюванням і пошуком.
Ми реалізуємо навчальний фрагмент: кандидати → фільтр бюджету → вибір. Одноразове прохання
«дай три варіанти» не є повною реалізацією алгоритму ToT із поверненням до попередніх станів.

Для магазину спершу відкиньте пропозиції понад бюджет. Серед решти максимізуйте тематичну
відповідність, при рівності оберіть нижчу ціну. Такий порядок критеріїв важливий: висока
релевантність не дозволяє порушити жорстке обмеження. Якщо жоден кандидат не проходить,
правильний результат — None, а не вигадана знижка. Оцінки нижче задані вручну, не LLM.

**Живий промпт прикладу:** «Кандидати A: 320 грн, relevance 2; B: 450 грн, relevance 3.
Бюджет 400. Відкиньте перевищення бюджету, оберіть найрелевантніший допустимий.
Поверніть id і коротку перевірювану причину».
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
options = [{"id":"A","price":320,"relevance":2}, {"id":"B","price":450,"relevance":3}]
feasible = [x for x in options if x["price"] <= 400]
best = sorted(feasible, key=lambda x:(-x["relevance"], x["price"], x["id"]))[0] if feasible else None
print(best)

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Candidates', 'Budget filter', 'Rank', 'Select / null']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 5: data flow (not model measurements)')
fig.tight_layout()
plt.show()
