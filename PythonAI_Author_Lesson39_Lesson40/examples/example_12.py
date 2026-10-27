"""**Факт. Посилання має вести до тексту, який справді підтримує відповідь.**

Grounding означає прив'язування відповіді до наданих джерел. Саме слово «цитуй» не захищає
від вигаданої цитати. Перевірте: id джерела відомий, цитата дослівно міститься в ньому,
а відповідь підтримується цитатою. Останню перевірку в загальному випадку не можна
замінити простим пошуком підрядка: «320» і «не 320» мають різний сенс.

У прикладі перевіримо точний вузький контракт із ціною. Для іншого питання — окремі правила
або ручна перевірка. Коли в тексті немає автора книги, answer=null — правильна відмова.
Вона відрізняється від помилки сервера і від порожнього рядка.

**Живий промпт прикладу:** «Джерело S1: Книга b01 коштує 320 грн. Яка ціна b01?
Поверніть answer, source_id, quote; quote дослівна. Якщо немає факту — три null».

**Контрольне переформулювання:** замість «Які у вас правила повернення?» поставте
«Витягніть тільки кількість днів із S2; якщо її немає, answer=null». Це звужує задачу
до перевірюваного факту, але не гарантує усунення галюцинацій. Послідовність перевірки:
JSON читається → ключі й типи правильні → id джерела існує → цитата дослівна → число
відповідає цитаті → відповідь стосується питання. Не повторюйте запит до отримання
приємного результату: це приховує невдалі спроби. Кожне переформулювання має власну версію
і перевіряється на тих самих питаннях, включно з питанням без відповіді.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
sources = {"S1":"Книга b01 коштує 320 грн.", "S2":"Повернення можливе протягом 14 днів."}
response = {"answer":320,"source_id":"S1","quote":"Книга b01 коштує 320 грн."}  # fixture
quote_present = response["quote"] in sources[response["source_id"]]
fact_correct = response["answer"] == 320 and response["source_id"] == "S1"
print({"quote_present":quote_present,"fact_correct":fact_correct})

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Question', 'Source', 'Quote', 'Fact check']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 12: data flow (not model measurements)')
fig.tight_layout()
plt.show()
