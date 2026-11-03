"""**Завдання 1. Інший читацький інтерес.** Отримайте дві рекомендації до b03.
Залиште book_id, title, description та перетворіть їх у текст JSON для майбутнього промпту.
Переконайтеся, що b03 не повернувся у списку; поясніть, чому score не є ймовірністю.

Підказки
1. Викличте recommend із seed_id='b03' та n=2.
2. Виберіть три названі колонки через список у квадратних дужках.
3. Використайте to_json(orient='records', force_ascii=False).
4. Перевірте унікальність book_id і відсутність seed-книги.

Готово, якщо: Є два різні ID з каталогу, JSON-контекст і пояснення значення score.
"""

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson37_Lesson38.workshop import (
    books, build_prompt, cosine_similarity, diagram, evaluate_fixtures, fixtures, json, np,
    OUTPUT_DIR, pd, platforms, plt, re, recommend, validate_response,
)

# %% Початковий контекст


# %% Ваш код
# Завдання 1: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
candidates = recommend('b03', n=3)
print(candidates[['book_id', 'title', 'score']].to_string(index=False))

candidates = recommend('b03', n=2)
print(candidates[['book_id', 'title', 'description']].to_string(index=False))
print(candidates[['book_id', 'title', 'description']].to_json(orient='records', force_ascii=False))