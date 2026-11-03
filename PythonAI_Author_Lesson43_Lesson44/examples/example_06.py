"""43.4 · ADR: обрати мінімальний стек

**Факт 6. Архітектурне рішення має містити причину, відхилену альтернативу та ціну складності.**

ADR — короткий запис рішення: контекст, вимоги, вибір, альтернативи, наслідки та перевірка.
Для DocFlow потрібні локальний пошук, прозорий prompt, JSON-відповідь, ізоляція історії
та тести без мережі. Обираємо langchain-core для композиції, залишаємо TF-IDF і власну
предметну перевірку. LangGraph, CrewAI, LlamaIndex та Cloud не додаємо, доки немає вимоги,
яка окупить їхню складність. Це рішення для конкретної вправи, не універсальний рейтинг.

Уникайте формулювання «обрали LangChain, бо всі використовують». Поставте перевірювану
мету: той самий retrieval-id до та після обгортання; parser відхиляє поганий JSON;
сесія B не бачить історії A. Запишіть ризик: оновлення API можуть вимагати міграції,
а історія в RAM зникає після перезапуску. На 44 перевіримо саме ці наслідки.
"""
import json

# %% Основний код
adr = {"context":"DocFlow: 3 локальні правила","decision":"langchain-core + existing retrieval",
       "rejected":"додавання кількох агентних фреймворків без вимоги",
       "risk":"залежність від API-версії","acceptance":"ті самі ids + parser tests + session isolation"}
print(json.dumps(adr,ensure_ascii=False,indent=2))

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Context', 'Alternatives', 'Decision', 'Acceptance']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 6: data flow, not model measurements')
fig.tight_layout()
plt.show()
