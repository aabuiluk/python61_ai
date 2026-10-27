"""**Факт. Бібліотека промптів зберігає контракт і критерій перевірки для конкретного типу задачі.**

Папка з фразами «будь експертом» не є достатньою бібліотекою. Для кожного запису зберігайте
id, version, context, goal, format, prompt та acceptance. Додайте один контрольний вхід
і очікуваний результат. Версія дозволяє відтворити порівняння після зміни формулювання.

**Аналітика:** вхід — таблиця продажів; задача — сума й лідер; формат — JSON;
перевірка — незалежний підрахунок Python. **QA:** вхід — вимога; задача — тест-кейси;
формат — id/precondition/steps/expected; перевірка — позитивний, негативний і граничний кейси.
**Контент:** вхід — підтверджені факти про книгу; задача — короткий опис; формат — текст;
перевірка — відсутність вигаданих знижок і тверджень. **Код-рев’ю:** вхід — код і контракт;
задача — конкретні дефекти; формат — рядок/дефект/виправлення/тест; перевірка — виконані тести.

Нижче є чотири повні промпти. Використовуйте будь-який у Gemini або ChatGPT без змін даних.
Для порівняння сервісів зберігайте service окремо від prompt_version. Не намагайтесь визначити
«кращий сервіс» за одним текстом: оцінюйте всі кейси за тими самими правилами.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
library = {
 "analytics":{"version":"1.0","prompt":"Дані: b01 — 2 продажі, b02 — 3. Порахуйте total та leader. Тільки JSON з total і leader. Без інших даних.","acceptance":"total=5; leader=b02"},
 "qa":{"version":"1.0","prompt":"Вимога: знижка 10% діє при total >= 1000 грн. Створіть три тест-кейси для 999, 1000, 1001. Формат JSON: input_total, discount_percent. Не змінюйте поріг.","acceptance":"0,10,10"},
 "content":{"version":"1.0","prompt":"Факти: книга Python старт, 320 грн, тема python. Напишіть два короткі речення українською. Не додавайте автора, знижок, рейтингу чи доставки.","acceptance":"тільки надані факти; два речення"},
 "code_review":{"version":"1.0","prompt":"Контракт: для n >= 0 повернути ціну 320*n. Код Python: def total(n): return 320+n. Знайдіть дефект, запропонуйте мінімальне виправлення і тести для n=0,1,2. Не запускайте код уявно; наведіть перевірювані очікування.","acceptance":"множення; 0,320,640"}
}
print(json.dumps(library,ensure_ascii=False,indent=2))

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Case + version', 'Prompt', 'Acceptance', 'Library']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 13: data flow (not model measurements)')
fig.tight_layout()
plt.show()
