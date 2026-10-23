"""Приклад 2. 36 · Що дозволяє сказати історія оцінок

## Схожість людей не дає біографію читача

**Факт 2. Collaborative filtering використовує реакції людей; пояснення має відповідати доступному сигналу.**

Схема: оцінки → спільні книги → схожість читачів → кандидат → обмежене пояснення.

Пригадайте пару 36: user-item матриця містить відомі оцінки й пропуски. Пропуск не означає
нуль зірок. Для маленького прикладу порівняємо Olia та Ira лише за b01 і b04,
які оцінили обидві. За цими двома оцінками вони схожі. Ira також високо оцінила b02.
Це сигнал запропонувати b02 Олі, але двох спільних книг замало для надійного висновку про всі смаки.

Фраза «схожий читач оцінив цю книгу на 5» прив'язана до таблиці. Фраза «ви завжди любите магію»
додає невідоме узагальнення. Генерація може зробити речення переконливим, не додавши доказів.
Новий користувач без історії потребує іншої стратегії: запитання про інтерес, контент або популярність.

Майбутні оцінки не можна використовувати для рекомендації в минулому. Тут таблиця — маленький
статичний приклад, а не оцінка точності recommender. У продукті зберігаємо часову межу з пари 36.

Пропуск збережено, є cosine для двох спільних книг і пояснення з названим обмеженням.
"""
from pathlib import Path
import sys

# Працює і з кореня репозиторію, і з папки examples/tasks.
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
from workshop import (
    np, pd, plt, json, re, books, fixtures, platforms, cosine_similarity,
    recommend, build_prompt, validate_response, evaluate_fixtures, diagram, OUTPUT_DIR,
)

# %% Початковий контекст
ratings = pd.DataFrame([[5, np.nan, 1], [5, 5, 1], [1, 2, 5]],
                       index=['Olia', 'Ira', 'Max'], columns=['b01', 'b02', 'b04'])

# %% Основний код прикладу
common = ratings.loc[['Olia', 'Ira']].dropna(axis=1)
similarity = cosine_similarity(common.iloc[[0]], common.iloc[[1]])[0, 0]
print('Спільні книги:', common.columns.tolist())
print('Cosine на спільних оцінках:', round(float(similarity), 3))
print('Ira оцінила b02:', ratings.loc['Ira', 'b02'])

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(6, 3))
masked = np.ma.masked_invalid(ratings.to_numpy(dtype=float))
image = ax.imshow(masked, vmin=1, vmax=5, cmap='YlGnBu')
ax.set_xticks(range(3), ratings.columns)
ax.set_yticks(range(3), ratings.index)
ax.set_title('Білий пропуск — оцінки немає')
fig.colorbar(image, ax=ax, label='Оцінка 1–5')
fig.tight_layout()
plt.show()
