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

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson37_Lesson38.workshop import (
    books, build_prompt, cosine_similarity, diagram, evaluate_fixtures, fixtures, json, np,
    OUTPUT_DIR, pd, platforms, plt, re, recommend, validate_response,
)

# %% Початковий контекст
budget = {'instruction': 180, 'catalog': 420, 'history': 200, 'output_reserve': 300}
limit = 1200  # умовні одиниці лише для арифметики

# %% Ваш код
# Завдання 4: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
