"""**Факт. Контекст має обмеження; частини тексту потрібно зберігати разом з ідентифікаторами.**

У запит входять інструкції, історія, документи та питання; для відповіді теж потрібен бюджет.
Токен — одиниця токенізатора моделі, а не слово. Українське слово може складатися з кількох
токенів. Нижче ми ділимо за словами для прозорої демонстрації; це не точний token counter.
Для реального API використовуйте [підрахунок токенів](https://ai.google.dev/gemini-api/docs/tokens).

Overlap повторює хвіст попередньої частини в наступній. Це допомагає зберегти зв'язок,
але збільшує сумарний обсяг. Умова overlap < size потрібна для просування індексу вперед.
Коли працюєте з документом, не втрачайте document_id і chunk_id. У великій системі добирають
лише релевантні частини; передача всіх частин в один запит не розв'язує проблему обмеження.

Почніть із size=8, overlap=2 і вручну звірте останні два слова першого фрагмента.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
text = "Книга допомагає вивчати Python через короткі вправи та приклади. Після кожного розділу є перевірка знань."
parts = chunks(text, size=8, overlap=2)
print(list(enumerate(parts, 1)))

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Document', 'Word windows', 'Overlap', 'Chunk IDs']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 7: data flow (not model measurements)')
fig.tight_layout()
plt.show()
