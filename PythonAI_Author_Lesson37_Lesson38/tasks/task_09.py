"""**Завдання 9. Перевірте контракт.** Візьміть valid, wrong_title, empty_reason з fixtures.
Перевірте кожну відповідь для allowed_ids=['b03'], надрукуйте помилки.
Потім перевірте valid із дозволеним b02. Поясніть, чому правильний ID каталогу може бути відхилений.

Підказки
1. fixtures — словники; передавайте json.dumps(...), а не dict.
2. Для кожного кейсу викличте validate_response з allowed_ids=['b03'].
3. Повторіть valid з ['b02']; очікується порожній список помилок.
4. Розрізняйте «існує в каталозі» та «дозволений для цього запиту».

Готово, якщо: Є відхилення через кандидата, неправильний title і порожній reason; valid з b02 прийнято.
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
allowed = ['b02', 'b03']

# %% Ваш код
# Завдання 9: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
