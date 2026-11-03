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

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson37_Lesson38.workshop import (
    books, build_prompt, cosine_similarity, diagram, evaluate_fixtures, fixtures, json, np,
    OUTPUT_DIR, pd, platforms, plt, re, recommend, validate_response,
)

# %% Початковий контекст


# %% Ваш код
# Завдання 3: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
jobs = pd.DataFrame([
    {'input':'текст + фото', 'output':'текста', 'approach': 'multimodal'},
    {'input':'текст', 'output':'жанр', 'approach': 'класифікатора або LLM'},
    {'input':'текст', 'output':'рекомендація', 'approach': 'multimodal'},
], columns=['input', 'output', 'approach'])
print(jobs.to_string(index=False))