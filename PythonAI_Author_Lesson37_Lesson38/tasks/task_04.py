"""**Завдання 4. Контекст переповнився.** В умовному бюджеті змініть catalog на 800.
Порахуйте дефіцит для limit=1200. Запропонуйте новий бюджет з catalog=400, зберігши
instruction, history й output_reserve. Поясніть, чому відбір кандидатів кращий за довільне обрізання тексту.

Підказки
1. Зробіть копію budget через dict, не змінюйте демонстраційний словник.
2. Для дефіциту використайте max(0, sum(values)-limit).
3. Створіть другу копію зі зменшеним catalog і перевірте суму.
4. Не називайте ці числа токенізацією живої моделі.

Готово, якщо: Дефіцит 280 умовних одиниць, новий залишок 120; split не названо tokenizer.
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
budget = {'instruction': 180, 'catalog': 420, 'history': 200, 'output_reserve': 300}
limit = 1200  # умовні одиниці лише для арифметики

# %% Ваш код
# Завдання 4: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
