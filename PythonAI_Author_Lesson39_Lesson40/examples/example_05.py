"""**Факт. Self-Consistency агрегує відповіді кількох різних спроб; більшість не гарантує істини.**

В оригінальному підході генерують різні шляхи розв’язання, витягують кінцеві відповіді
та обирають найузгодженішу. У навчальній версії зберігаємо п'ять окремих результатів і рахуємо
частоти. Це відрізняється від прохання в одному повідомленні «подумай п'ятьма способами»:
таке повідомлення не забезпечує п'ять незалежних запусків. Навіть нові чати не роблять
виходи статистично незалежними: та сама модель може повторювати одну помилку.

Спершу нормалізуйте відповіді: "1170 грн" і "1170" мають дати одне число. Не порівнюйте
неочищені рядки. Окремо відкиньте непридатні відповіді та повідомте їхню кількість.
При нічиїй не обирайте перший елемент випадково: поверніть статус tie або відмову.
Після голосування перевірте результат Python, каталогом чи іншим зовнішнім джерелом.

Для живої роботи повторіть один промпт у п'яти нових чатах Gemini АБО ChatGPT, не змішуючи
провайдерів у межах одного досліду. Збережіть усі відповіді, модель і дату. При вичерпанні
безкоштовного ліміту використовуйте fixtures та явно назвіть дослід симуляцією агрегації.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
from collections import Counter
answers = [1170, 1170, 1190, 1170, 1200]  # ручні fixtures
counts = Counter(answers)
winner, votes = counts.most_common(1)[0]
print({"winner":winner,"votes":votes,"attempts":len(answers),"verified":winner == 390*3})

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['New attempts', 'Normalize', 'Vote / tie', 'External check']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 5: data flow (not model measurements)')
fig.tight_layout()
plt.show()
