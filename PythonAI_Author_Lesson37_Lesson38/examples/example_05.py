"""Приклад 5. 37.3 · Де живе хмарна AI-платформа

## SDK — лише одна частина застосунку

**Факт 5. Хмарний GenAI-застосунок поєднує дані, права доступу, модельний endpoint і перевірку відповіді.**

Схема: користувач → backend → дозволений контекст → model endpoint → валідатор → відповідь.

Програма називає Google Vertex AI, Azure OpenAI Service та Amazon Bedrock. Це керовані хмарні
можливості доступу до моделей. У поточній документації Google старий маршрут Vertex AI GenAI
перенаправляється до Gemini Enterprise Agent Platform, а Azure — до Microsoft Foundry.
У навчанні зберігаємо назви програми й читаємо актуальну сторінку за посиланням унизу.

Модель — не вся платформа. Backend обирає контекст, автентифікує користувача, викликає дозволену
модель, обробляє timeout і перевіряє результат. У Google потрібен контекст project/location та IAM;
в Azure маршрутизація може спиратися на deployment; у Bedrock — на region, модель і права IAM.
Конкретні способи авторизації залежать від endpoint і режиму доступу.

Не обирайте платформу за одним показником. Порівняйте потрібну модель, регіональну доступність,
обробку даних, інтеграцію з наявною інфраструктурою та результати власного тесту.
Тарифи й доступність тут не зафіксовані: їх перевіряють перед підключенням. Секрети лишаються
на backend, не в ноутбуці чи студентському Git. Ця вправа створює план, без реєстрації ресурсу.

Є повний маршрут, резервна поведінка, обґрунтування й два відкриті питання без секретів.
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


# %% Основний код прикладу
print(platforms.to_string(index=False))
request_plan = {'context_source': 'approved catalog', 'auth': 'server identity',
                'timeout_seconds': 30, 'validate': True, 'log': 'metadata only'}
print(json.dumps(request_plan, ensure_ascii=False, indent=2))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = diagram(['Backend', 'IAM', 'Endpoint', 'Перевірка'], 'Хмарний запит: концептуальна схема')
plt.show()
