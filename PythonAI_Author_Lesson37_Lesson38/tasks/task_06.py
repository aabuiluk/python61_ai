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

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson37_Lesson38.workshop import (
    books, build_prompt, cosine_similarity, diagram, evaluate_fixtures, fixtures, json, np,
    OUTPUT_DIR, pd, platforms, plt, re, recommend, validate_response,
)

# %% Початковий контекст


# %% Ваш код
# Завдання 6: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
