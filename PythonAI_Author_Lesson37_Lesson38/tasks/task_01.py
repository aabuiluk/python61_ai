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


# %% Ваш код
# Завдання 1: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
