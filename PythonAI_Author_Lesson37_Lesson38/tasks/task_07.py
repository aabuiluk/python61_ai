"""**Завдання 7. Свій структурований промпт.** Візьміть дві рекомендації до b03.
Складіть промпт для читача, який любить космічні подорожі: лише кандидат зі списку,
проста українська, reason до двох речень, JSON із трьома ключами. Збережіть prompt.txt.

Підказки
1. recommend('b03', 2) дасть незалежний від попередніх вправ контекст.
2. Перетворіть потрібні поля на JSON records.
3. Передайте конкретну дію і формат у build_prompt.
4. Створіть OUTPUT_DIR і write_text(..., encoding='utf-8').

Готово, якщо: prompt.txt існує; роль, контекст, дія, обмеження й формат сформульовані явно.
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
prompt_context = recommend('b01', n=2)[['book_id', 'title', 'description']].to_json(orient='records', force_ascii=False)

# %% Ваш код
# Завдання 7: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.

prompt = build_prompt(prompt_context,
    'Обери одну книгу з кандидатів. Поясни вибір простою українською для початківця, без обіцянки покупки.',
    'JSON із рядками book_id, title, reason; reason — 1–2 речення; без Markdown')
print(prompt)