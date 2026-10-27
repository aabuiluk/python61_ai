"""**Факт. У розгалуженому пошуку оцінюють проміжні варіанти й продовжують кілька гілок.**

Tree-of-Thought (ToT) працює з деревом можливих продовжень: generate → evaluate →
select → expand. Коли напрям виявляється невдалим, пошук може перейти до іншої збереженої
гілки. Оцінка може бути евристикою, перевіркою коду або оцінкою моделі; самооцінка LLM
не є незалежною гарантією правильності. Ширина пошуку та глибина збільшують кількість викликів.

Задача: обрати дві різні книги. На першому рівні є A, B, C. На другому додаємо другу
книгу, обчислюємо сумарну ціну й бал та відкидаємо перевищення бюджету. Дорогий перший
кандидат може залишити надто мало бюджету для другої книги: жадібний вибір першого
найбільшого score програє пошуку кількох гілок. Код зберігає журнал усіх розширень,
тому можна показати не тільки переможця, а й причину відмови від альтернатив.

Це точна навчальна аналогія дерева пошуку з ручними балами, не реалізація оригінального
LLM-ToT. Для живого варіанта в Gemini або ChatGPT надішліть запит створити перші кандидати,
оцініть ціни кодом, передайте тільки допустимі гілки назад і попросіть розширити другий рівень.
Так дані самооцінки та зовнішня арифметична перевірка лишаються розділеними.
У промпті просимо короткі варіанти й оцінки, а не приховану внутрішню трасу мислення.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
# Два рівні пошуку: перша книга -> друга книга; оцінка після кожного розширення.
pool = [{"id":"A","price":320,"score":2}, {"id":"B","price":450,"score":5}, {"id":"C","price":390,"score":3}]
frontier = [{"ids":[],"cost":0,"score":0}]
trace = []
for depth in (1,2):
    expanded = []
    for node in frontier:
        for item in pool:
            if item["id"] in node["ids"]:
                continue
            child = {"ids":node["ids"]+[item["id"]],"cost":node["cost"]+item["price"],"score":node["score"]+item["score"]}
            accepted = child["cost"] <= 750
            trace.append({"depth":depth,**child,"accepted":accepted})
            if accepted:
                expanded.append(child)
    frontier = expanded  # зберігаємо всі допустимі гілки, без жадібного обрізання
best = min(frontier,key=lambda n:(-n["score"],n["cost"],n["ids"])) if frontier else None
print("Найкраща пара:",best)
print("Перевірено гілок:",len(trace),"; відкинуто:",sum(not x["accepted"] for x in trace))

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Branches', 'Expand', 'Budget + score', 'Select / null']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 7: data flow (not model measurements)')
fig.tight_layout()
plt.show()
