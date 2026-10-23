"""**Завдання 6. Мінімальний контекст.** З вигаданого запису user_id='u17', email='reader@example.invalid',
interest='fantasy', phone='000000' створіть payload лише з interest і кандидатами b01, b02.
Перевірте invented через validate_response. Назвіть ризик, якого валідатор не виявляє.

Підказки
1. Вихідний запис створіть локально; не пересилайте контакти.
2. Побудуйте новий dict, явно обравши дозволені поля.
3. Перетворіть fixture у рядок через json.dumps.
4. Відрізніть невідомий ID від суб'єктивного чи стереотипного пояснення.

Готово, якщо: Контакти відсутні в payload, невідомий ID відхилено, межу валідатора названо.
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
# Завдання 6: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
