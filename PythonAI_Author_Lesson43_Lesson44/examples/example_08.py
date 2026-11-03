"""44.2 · LCEL: контракт кожного Runnable

**Факт 8. Оператор | з’єднує вихід одного Runnable зі входом наступного.**

LCEL читається зліва направо: prompt | model | parser. Для нашого прикладу це
dict → PromptValue → AIMessage → str. RunnableLambda адаптує звичайну функцію до
інтерфейсу invoke. StrOutputParser дістає текст повідомлення, а не перевіряє його факти.
Оператор | тут належить справжньому langchain-core; ми не перевизначаємо __or__ у FakeLLM.

Помилка форми входу лишається помилкою: якщо lambda очікує повідомлення, а отримує dict,
бібліотека не вгадає правильний шлях. Спочатку запишіть таблицю типів, потім складайте chain.
Виклик invoke виконує вузли синхронно. batch приймає кілька входів; це не повторне навчання
й не гарантія, що довільна функція потокобезпечна. Наша fixture-функція локальна й детермінована.
"""
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# %% Основний код
prompt = ChatPromptTemplate.from_messages([("human","Питання: {question}")])
model = RunnableLambda(lambda value: AIMessage(content="Навчальний fixture: "+value.to_messages()[-1].content))
chain = prompt | model | StrOutputParser()
print(chain.invoke({"question":"Коли працює магазин?"}))
print(chain.batch([{"question":"A"},{"question":"B"}]))

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Input dict', 'PromptValue', 'AIMessage', 'String']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 8: data flow, not model measurements')
fig.tight_layout()
plt.show()
