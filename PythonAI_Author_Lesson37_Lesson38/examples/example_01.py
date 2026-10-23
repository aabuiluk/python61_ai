"""Приклад 1. 35 · Рекомендація стає контекстом

## Спершу знайдіть книгу, потім пояснюйте

**Факт 1. Content-based метод ранжує наявні книги за ознаками, а не створює нові записи каталогу.**

Схема: опис книги → TF-IDF → cosine → top-n → контекст майбутньої відповіді.

У парі 35 ми перетворювали описи на числові вектори. TF-IDF підсилює слова, які допомагають
розрізняти документи; cosine порівнює напрямки цих векторів. Значення 0.7 не означає
«70% імовірності покупки». Це лише подібність у вибраному просторі ознак.

Тепер беремо шість вигаданих книг. recommend повертає рядки каталогу, виключає seed-книгу,
сортує за score, а за рівного score — за book_id. Ця домовленість робить порядок відтворюваним.
Книгу без спільних слів теж можна отримати в кінці списку з нульовим score; це слабкий кандидат.

Майбутній генеративний помічник може отримати цей список як контекст і пояснити вибір.
Він не повинен сам вигадувати book_id або ціну. Відділіть рішення «що рекомендуємо» від тексту
«як це пояснюємо». Так легше перевірити і алгоритм, і відповідь.

Є два різні ID з каталогу, JSON-контекст і пояснення значення score.
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


# %% Основний код прикладу
candidates = recommend('b01', n=3)
print(candidates[['book_id', 'title', 'score']].to_string(index=False))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(7, 3))
ax.barh(candidates.title.iloc[::-1], candidates.score.iloc[::-1])
ax.set(xlabel='Cosine, не ймовірність', title='Ранжування локального каталогу')
fig.tight_layout()
plt.show()
