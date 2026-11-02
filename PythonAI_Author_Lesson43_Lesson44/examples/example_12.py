"""44.6 · Збираємо DocFlow і перевіряємо перехід

**Факт 12. Після переходу на framework мають зберегтися перевірювані бізнес-контракти.**

Остаточний ланцюжок: рядок question → паралельне формування context/question →
ChatPromptTemplate → модельний вузол → JsonOutputParser. Окремий validate_answer
перевіряє результат щодо тих самих retrieved docs. RunnablePassthrough передає вхідне
питання без змін. Словник runnable-вузлів у LCEL формує словник входів для prompt.

Ми перенесли структуру, а не довели поліпшення якості. Для відомого питання перевірте
answer і sources; для невідомого — null/[]; для зламаного контракту — rejected.
Зафіксуйте langchain-core, mode=fixture і випадки в JSON-звіті. Якщо пізніше заміните
fixture на живу модель, повторіть ці самі кейси й окремо оцініть факти, latency та витрати.
Автоматичне повторення мережевих запитів тут не додаємо.

**Exit ticket:** що лишилося від 41–42? Retrieval, джерела, allowlist, валідація, бюджет.
Що дав framework? Стандартні контракти компонентів і композицію. Де пам’ять? У сховищі
конкретної сесії, яке ми явно підставляємо в prompt. Де перечитати: блоки 1, 2, 8, 10, 11.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
chain = make_chain()
question = "Доставка Україною"
result = chain.invoke(question)
print(result)
print("Контракт:",validate_answer(result,retrieve(question)))
print("Невідомий факт:",chain.invoke("Марсіанський телепорт"))

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Retrieve', 'Prompt + fixture', 'Parser', 'Validate + log']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 12: data flow, not model measurements')
fig.tight_layout()
plt.show()
