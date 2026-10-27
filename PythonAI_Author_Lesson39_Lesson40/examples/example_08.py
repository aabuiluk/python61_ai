"""**Факт. Critic знаходить конкретний дефект, Editor виправляє його, а Reflexion зберігає урок для наступної спроби.**

Почніть із чернетки: «b01 коштує 299 грн, повернення 30 днів». Джерела дають 320 грн
і 14 днів. Critic не пише «погано»: він повертає два дефекти зі зв'язком із джерелом.
Editor отримує початковий текст, ті самі джерела та список дефектів; виправляє тільки
підтверджені помилки. Потім зовнішній валідатор знову перевіряє результат.

Reflexion — не просто «перевір себе». Після зворотного зв'язку формулюється коротка
пам'ять про помилку: «не брати ціну з чернетки; звіряти з S1». Цю пам'ять додають
до наступної спроби. Ваги моделі не змінюються; у нашій реалізації пам'ять — явний список рядків.
Зупиняйте цикл після успішної перевірки або ліміту, наприклад двох ітерацій. Інакше
саморедагування може нескінченно переписувати правильний текст або додавати нові вигадки.

У Gemini та ChatGPT використовуйте три послідовні запити з позначками CRITIC, EDITOR,
REFLECTION. Результат кожного збережіть окремо. Код нижче — відтворювана ручна симуляція,
не автоматичний LLM-агент. Власна критика моделі теж може бути хибною; перевіряйте її джерелом.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
draft = {"price":299,"return_days":30}
facts = {"price":320,"return_days":14}
issues = [{"field":k,"actual":draft[k],"expected":v} for k,v in facts.items() if draft[k] != v]
edited = {**draft, **{i["field"]:i["expected"] for i in issues}}
reflection = "Наступного разу звірити ціну й термін із джерелами до відповіді."
print(issues,edited,reflection)

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Draft', 'Critic', 'Editor', 'Memory + check']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 8: data flow (not model measurements)')
fig.tight_layout()
plt.show()
