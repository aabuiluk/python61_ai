"""41 · Переносимо retrieval і джерела

**Факт 1. RAG починається з пошуку, а не з прохання моделі пригадати відповідь.**

На 41 ви ділили документи на чанки, додавали id та шукали top-k за cosine. Зараз беремо
три короткі правила магазину: доставка Україною 90 грн, самовивіз у Львові безкоштовний,
години роботи 09:00–18:00. Це синтетичні навчальні дані. Прочитайте знайдений текст перед
побудовою промпту: високий score означає схожість у цьому просторі, не істинність і не
ймовірність правильної відповіді. Нульовий збіг тут повертає порожній результат.

Три рядки не потребують окремого chunker: кожний уже є одним фрагментом. В реальному
корпусі збережіть document_id, chunk_id і шлях до джерела. Для питання без факту потрібна
відмова, а не довільний перший документ. Цей контракт переносимо в LangChain без змін.
"""
import json
from PythonAI_Author_Lesson43_Lesson44.workshop import retrieve

# %% Основний код
hits = retrieve("Доставка Україною",k=2)
print(json.dumps(hits,ensure_ascii=False,indent=2))
assert hits[0]["id"]=="delivery_ua"

# %% Окрема схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0,4); ax.set_ylim(0,1); ax.axis('off')
labels = ['Question', 'TF-IDF', 'Top-k', 'Source ids']
for j,label in enumerate(labels):
    ax.text(j+0.5,0.5,label,ha='center',va='center',fontsize=11,
            bbox=dict(boxstyle='round,pad=0.65',facecolor='#eaf1ff',edgecolor='#2459be'))
    if j<3:
        ax.annotate('',xy=(j+1.08,0.5),xytext=(j+0.92,0.5),arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 1: data flow, not model measurements')
fig.tight_layout()
plt.show()
