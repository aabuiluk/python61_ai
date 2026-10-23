"""**Завдання 3. Оберіть вихід.** Створіть таблицю для трьох задач: визначити жанр за описом;
створити три заголовки; відповісти на питання про фото обкладинки.
Додайте колонки input, output, approach та поясніть, чому multimodal і LLM можуть перетинатися.

Підказки
1. Кожна задача — один словник у списку для pd.DataFrame.
2. У input вкажіть текст або текст + фото.
3. В output запишіть очікуваний артефакт, а не бренд моделі.
4. Для жанру допустимі класифікатор або LLM; поясніть вибір.

Готово, якщо: Три задачі мають визначені вхід і вихід; модальність не переплутано з архітектурою.
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
# Завдання 3: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
