"""**Факт. У запит потрібно переносити потрібні факти й обмеження, а не всю розмову без відбору.**

Відділіть три модулі: instructions — що робити та які правила, data — документи й факти,
task — актуальне питання. Історія допомагає з посиланнями «ця книга», але старі припущення
можуть суперечити новому каталогу. Якщо у попередній репліці було 299, а нове довірене джерело
дає 320, сформуйте явний актуальний контекст. Просте обрізання останніх N повідомлень
може викинути ключове обмеження або лишити відповідь без питання.

Стратегія: незмінні інструкції + перевірений стислий стан + кілька останніх пар реплік +
актуальне джерело + нова задача. Стислий стан теж перевіряйте: підсумок, створений LLM,
може втратити заперечення чи вигадати уподобання. Зберігайте джерело й версію фактів.
Не плутайте переписку у вікні з гарантованою довгостроковою пам'яттю продукту.

«Вага фрагмента» тут означає його вплив на відповідь, а не доступний повзунок attention.
Не можна призначити реченню точну вагу 0.8 звичайним чатом. Відбирайте релевантне,
позначайте пріоритет джерел, приберіть дублікати, розмістіть явну задачу поруч із потрібними
даними й перевірте перестановку фрагментів на тих самих питаннях. Позиція не гарантує уваги.
Сума інструкцій, даних, історії та резерву відповіді має вкладатися в ліміт конкретної моделі;
рахунок слів нижче — тільки наочна евристика, не токенізація Gemini чи ChatGPT.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
instructions = "Використовуйте актуальний каталог; стару ціну не переносіть."
state = {"selected_id":"b01","budget":400,"source_version":"catalog_v2"}
history = [{"role":"user","content":"Покажіть ціну обраної книги"},
           {"role":"assistant","content":"Потрібен актуальний каталог"}]
payload = {"instructions":instructions,"state":state,"recent_history":history,
           "data":CATALOG[0],"task":"Чи вистачить бюджету?"}
print(json.dumps(payload,ensure_ascii=False,indent=2))

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Instructions', 'Verified state', 'Data + task', 'Answer']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 11: data flow (not model measurements)')
fig.tight_layout()
plt.show()
