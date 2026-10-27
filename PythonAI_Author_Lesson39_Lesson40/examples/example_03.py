"""**Факт. Zero-shot задає правило без прикладів, а few-shot додає приклади потрібного перетворення.**

Слово shot означає приклад «вхід → правильний вихід» усередині промпту, а не кількість
спроб запуску. Zero-shot: «Позначте відгук як positive, negative або mixed». Few-shot додає
приклади перед новим відгуком. Вага моделі від цього не оновлюється: це навчання за контекстом
запиту (in-context learning), а не fine-tuning.

Візьміть відгук «Доставка швидка, але обкладинка пошкоджена». Без категорії mixed модель
може вибрати один бік. Приклади допомагають показати межу, але не виправлять суперечливу
інструкцію. У прикладі нижче створюємо два промпти для того самого відгуку. Ми ще не викликаємо LLM.

Для живого порівняння запустіть zero-shot у новому чаті Gemini або ChatGPT, збережіть відповідь.
У другому новому чаті запустіть few-shot. Не додавайте правильну відповідь для тестового відгуку
в приклади: інакше ви підказали розв’язок. Перевірте результат вручну за однаковою рубрикою:
positive — тільки позитив, negative — тільки негатив, mixed — обидва. Один запуск не доводить,
що few-shot завжди кращий. Приклади мають охоплювати межові випадки, а не повторювати один клас.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workshop import *

# %% Основний код
review = "Доставка швидка, але обкладинка пошкоджена"
instruction = "Класифікуйте відгук: positive, negative або mixed. Поверніть тільки мітку."
zero_prompt = instruction + "\nВідгук: " + review
few_prompt = instruction + "\nПриклади: Чудова книга → positive; Книга порвана → negative; Цікава, але порвана → mixed.\nВідгук: " + review
print(zero_prompt)
print(few_prompt)

# %% Схема
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 2.3))
ax.set_xlim(0, 4)
ax.set_ylim(0, 1)
ax.axis('off')
labels = ['Zero-shot', 'Examples', 'Few-shot', 'Same test']
for j, label in enumerate(labels):
    ax.text(j+0.5, 0.5, label, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf1ff', edgecolor='#2459be'))
    if j < 3:
        ax.annotate('', xy=(j+1.1,0.5), xytext=(j+0.9,0.5), arrowprops=dict(arrowstyle='->'))
ax.set_title('Example 3: data flow (not model measurements)')
fig.tight_layout()
plt.show()
