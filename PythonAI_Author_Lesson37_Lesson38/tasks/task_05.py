"""**Завдання 5. Маршрут запиту.** Опишіть план для каталогу магазину: cloud, identity,
context_source, validation, on_timeout. Оберіть одну з трьох платформ і наведіть дві причини
вибору та два питання, які треба перевірити в офіційній документації до реального запуску.

Підказки
1. Збережіть план як словник, без endpoint із секретом або ключа.
2. У validation назвіть структуру і відповідність ID каталогу.
3. При timeout передбачте зрозуміле повідомлення або базову рекомендацію.
4. Регіон і умови зберігання даних — питання, а не припущення.

Готово, якщо: Є повний маршрут, резервна поведінка, обґрунтування й два відкриті питання без секретів.
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
# Завдання 5: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
