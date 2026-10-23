"""**Завдання 8. Приклад без підглядання.** Складіть few-shot промпт із трьома новими навчальними
прикладами, включно з unknown. Окремий тест: 'river crime detective'. Додайте роль редактора
та явний формат «лише одна мітка». Поясніть, чому це не fine-tuning.

Підказки
1. Виберіть приклади, яких немає в тестовому рядку.
2. Невідомий випадок має показати допустиму мітку unknown.
3. Зберігайте test_case окремою змінною й додавайте наприкінці.
4. Жодна функція тренування не викликається; міняється лише вхідний текст.

Готово, якщо: Є три приклади, unknown, окремий тест і пояснення різниці few-shot та fine-tuning.
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
# Завдання 8: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
