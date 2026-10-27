"""**Факт. Зміна промпту оцінюється на тих самих прикладах і за наперед визначеними критеріями.**

Мініпайплайн: питання → добір джерела → промпт → відповідь → перевірка → журнал.
У ручному досліді замініть тільки етап відповіді на чат; інші етапи лишаються видимими.
Зберігайте question_id, prompt_version, model, mode, passed і фактичну відповідь.
Не записуйте секрети чи чужі персональні дані.

Маємо три ручні відповіді, дві з яких правильні. Частка 2/3 вимірює прийняття цих fixtures
нашим валідатором. Вона не є точністю моделі чи доказом, що один промпт кращий.
Для живого порівняння підготуйте v1 і v2, ту саму модель, ті самі три питання, новий чат
для кожного запуску та однакове число повторів. Записуйте невдалі й успішні спроби.
Малий набір дає навчальне спостереження, а не загальний висновок про модель.

**Exit ticket:** коли потрібен інструмент, а не лише промпт? Чому точна цитата ще не доводить
правильність відповіді? Де перечитати: блок 6 (дія), блок 12 (підтримка цитатою), блок 16 (оцінка).
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
fixtures = ['{"book_id":"b01","price":320}', '{"book_id":"b02","price":450}', '{"book_id":"b03","price":1}']
report = [{"case_id":i,"mode":"fixture","passed":validate(raw)} for i,raw in enumerate(fixtures,1)]
print(report)
print("Частка прийнятих fixtures:", sum(r["passed"] for r in report)/len(report))

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Cases', 'Response', 'Validation', 'CSV log']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 16: data flow (not model measurements)')
fig.tight_layout()
plt.show()
