"""44.3 · Parser і предметна валідація

**Факт 9. Прочитаний JSON ще не означає правильний тип, джерело чи факт.**

JsonOutputParser перетворює текст на Python-об’єкт; вивід може потребувати перевірки
ключів, типів і дозволених source ids. Наша validate_answer вимагає рівно answer/sources,
відомі у переданому контексті id, відсутність дублікатів і узгоджену відмову null/[]
або непорожню відповідь з джерелом. Це контракт форми й походження, не універсальний
детектор істини. Відповідь «90 грн» і «900 грн» із тим самим id обидві можуть мати
правильну структуру, але фактично коректна тільки одна.

Не виправляйте погану відповідь мовчазно підстановкою очікуваного значення. Збережіть
помилку й статус rejected, а потім, якщо потрібно, окремий обмежений repair. Для цього
корпусу фактичну відповідність можемо додатково звірити з точним реченням джерела.
"""
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import JsonOutputParser
from PythonAI_Author_Lesson43_Lesson44.workshop import retrieve, validate_answer

# %% Основний код
parsed = JsonOutputParser().invoke(AIMessage(content='{"answer":"Доставка Україною коштує 90 грн.","sources":["delivery_ua"]}'))
hits = retrieve("Доставка",1)
print(parsed,validate_answer(parsed,hits))
print("Факт збігається:",parsed["answer"]==hits[0]["text"])

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Raw text', 'JSON parser', 'Contract', 'Fact check']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 9: data flow, not model measurements')
fig.tight_layout()
plt.show()
