"""Приклад 9. 38.3 · JSON треба розібрати і перевірити

## parse → schema → catalog → candidates

**Факт 9. Перевірка структури, типів і належності ID є окремими кроками після отримання тексту.**

Схема: текст → json.loads → словник і ключі → непорожні рядки → каталог → дозволені кандидати.

json.loads відповідає лише на питання синтаксису. [] — коректний JSON, але не об'єкт рекомендації.
Число 2 замість рядка 'b02' теж синтаксично коректне. Тому validate_response спочатку
перевіряє контейнер, точний набір ключів і типи. Лише потім шукає ID у каталозі.

Відома книга може бути недозволеним кандидатом для цього запиту. Передайте allowed_ids,
щоб перевірити і цю межу. title має відповідати саме обраному ID. Причина не може бути порожньою,
але непорожній reason ще може містити вигадку — зміст вимагає окремої перевірки.

Не виправляйте невідомий ID мовчки на «щось схоже». Поверніть зрозумілу помилку, зробіть
обмежену повторну спробу або покажіть базову рекомендацію. Наш валідатор навмисно суворий:
кодова огорожа Markdown не є JSON-об'єктом. Реальний API може підтримувати structured output;
навіть тоді перевірка бізнес-обмежень потрібна в застосунку.

Є відхилення через кандидата, неправильний title і порожній reason; valid з b02 прийнято.
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

# %% Основний код прикладу
responses = ['not json', '[]', json.dumps(fixtures['wrong_type']),
             json.dumps(fixtures['valid'], ensure_ascii=False)]
for response in responses:
    print(repr(response), '->', validate_response(response, allowed))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = diagram(['Parse', 'Схема', 'Каталог', 'Кандидати'], 'Валідатор: послідовність перевірок')
plt.show()
