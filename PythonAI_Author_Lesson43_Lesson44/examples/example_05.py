"""43.3 · LangGraph, CrewAI, AutoGen і Semantic Kernel

**Факт 5. Цикл станів і співпраця ролей — різні способи організації роботи.**

LangGraph зручно розглядати для явного стану, вузлів, переходів, умов зупинки та
відновлення виконання. CrewAI використовує ролі/задачі в Crews і керування процесом у
Flows. Це не взаємовиключні світи: у role-based системі також потрібні стан і контроль.
Назва «редактор» не створює окрему людину чи незалежне джерело істини — це роль агента.

AutoGen історично пов’язаний із взаємодією агентів через повідомлення; Semantic Kernel —
з інтеграцією AI-функцій та інструментів у застосунки. Підтримка, рекомендовані пакети й
маршрути міграції змінюються, тому перед вибором перевіряйте офіційний статус проєкту.
На цій парі для них даємо карту ролей, не встановлення та не обіцянку переваги.
Окремо позначте Microsoft Agent Framework: це набір засобів для агентів, workflows,
модельних клієнтів та інтеграцій. Уявна карта «AutoGen — тільки чат, Semantic Kernel —
тільки плагіни» надто вузька: екосистеми розвиваються, функції перекриваються.
Для нового Microsoft-стеку перевірте [актуальний Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/)
і рекомендації міграції, а не встановлюйте старий пакет із випадкового уроку.

Для DocFlow достатньо станів retrieve → answer → validate; при помилці одна спроба repair,
потім stop. Для процесу «дослідник → редактор → контролер» важливі артефакти кожної ролі
і критерії передачі. Навіть найсильніший framework не має права нескінченно повторювати запит.
У прикладі нижче — ручна схема переходів, не імпорт LangGraph або CrewAI.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
edges = {"retrieve":"answer","answer":"validate","validate_ok":"stop",
         "validate_error":"repair","repair":"stop"}
roles = {"researcher":"джерела","editor":"текст за джерелами","reviewer":"звіт дефектів"}
print(edges)
print(roles)

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['State', 'Transitions', 'Roles', 'Stop rule']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 5: data flow, not model measurements')
fig.tight_layout()
plt.show()
