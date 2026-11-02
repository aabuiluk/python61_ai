"""44.1 · PromptTemplate і ChatPromptTemplate

**Факт 7. Шаблон явно оголошує вхідні змінні; chat-шаблон додатково зберігає ролі повідомлень.**

На 41 ви збирали stuffing-prompt рядком. PromptTemplate робить підстановки {context} та
{question} видимими й перевіряє відсутні значення. ChatPromptTemplate формує повідомлення
system/human/ai, а не один нерозмічений рядок. format повертає текст; invoke — PromptValue,
який можна перетворити на повідомлення. Сам шаблон нічого не генерує й не викликає API.

Використовуйте стандартне форматування рядків, не довільні сторонні template-коди.
JSON із фігурними дужками передавайте через змінну context або екрануйте {{ і }} у
літералі шаблону. Дані джерел лишаються даними; текст «ігноруй інструкції» всередині
документа не стає system-повідомленням. Ролі допомагають розділяти контекст, але не є
самодостатнім захистом від prompt injection: валідатор і межі tools залишаються потрібними.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
template = PromptTemplate.from_template("Дані: {context}\nПитання: {question}")
print(template.input_variables)
print(template.format(context="[delivery_ua] Доставка 90 грн.",question="Скільки коштує доставка?"))
chat = ChatPromptTemplate.from_messages([("system","Тільки за джерелами."),("human","{question}")])
print([m.type for m in chat.invoke({"question":"Які правила?"}).to_messages()])

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Variables', 'Chat template', 'PromptValue', 'Messages']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 7: data flow, not model measurements')
fig.tight_layout()
plt.show()
