"""**Завдання 10. Звіт і наступний дослід.** Додайте case 'outside': правильну книгу b04 з непорожнім reason.
Перевірте весь набір для b02, b03 та збережіть eval_report.csv. Створіть live_protocol.json із
двома версіями промпту, однаковими case_id та статусом not_run. Перелічіть, що треба зафіксувати
для справжнього порівняння. Не записуйте вигадані результати моделі.

Підказки
1. Скопіюйте fixtures через dict та додайте outside з правильним title каталогу.
2. evaluate_fixtures повертає DataFrame; to_csv(..., index=False, encoding='utf-8-sig').
3. Для protocol використайте списки prompt_versions, case_ids та metadata_required.
4. Збережіть JSON через json.dumps(..., ensure_ascii=False, indent=2).

Готово, якщо: CSV має 6 кейсів і 1 прийнятий; протокол not_run не містить вигаданих вимірювань LLM.
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
evaluation_ids = ['b02', 'b03']

# %% Ваш код
# Завдання 10: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
