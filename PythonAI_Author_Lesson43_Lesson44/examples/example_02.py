"""42 · Агентний цикл і явний стан

**Факт 2. Інструмент виконує програма, а модель лише пропонує дію.**

На 42 у вас був цикл model → tool call → перевірка аргументів → Python → observation →
нова репліка моделі. Зберігайте ліміт кроків, allowlist інструментів і журнал навіть після
переходу на фреймворк. Структура {tool, arguments} сама не виконує функцію.

Нижче звичайний Python виконує дозволений пошук. Це один крок маршруту, не автономний
LLM-агент. Невідома дія повинна завершитись помилкою до виконання; порожній retrieval
повертає observation з порожнім списком. LangGraph згодом може організувати переходи стану,
але не прийме за вас бізнес-рішення, які інструменти дозволені.
"""
import json
from PythonAI_Author_Lesson43_Lesson44.workshop import retrieve

# %% Основний код
request = {"tool":"search_knowledge","arguments":{"question":"Доставка Україною"}}
if request["tool"]!="search_knowledge":
    raise ValueError("Невідомий tool")
observation = retrieve(request["arguments"]["question"],1)
trace = [{"step":1,"request":request,"observation":observation}]
print(json.dumps(trace,ensure_ascii=False,indent=2))

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Request', 'Allowlist', 'Tool', 'Observation']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 2: data flow, not model measurements')
fig.tight_layout()
plt.show()
