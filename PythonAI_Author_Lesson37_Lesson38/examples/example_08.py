"""Приклад 8. 38.2 · Чотири способи сформулювати запит

## Приклади в промпті задають зразок поведінки

**Факт 8. Instruction, role, conversational і few-shot промпти можна поєднати в одному запиті.**

Схема: інструкція + роль + діалоговий контекст + приклади → новий запит → перевірка.

Instruction каже, що зробити: «поверни один жанр». Role задає перспективу або тон:
«ти редактор навчального каталогу». Conversational використовує репліки й уточнення;
коли запит «щось цікаве», корисне уточнення — «який жанр і для якого віку?». В API зазвичай
передають структуру повідомлень; наш список словників — лише навчальне представлення діалогу.

Few-shot додає кілька прикладів input/output. Вони мають відповідати потрібним міткам і формату.
Якщо всі приклади — fantasy, ви не показали, як обробляти science або невідомий жанр.
Приклади допомагають задавати шаблон, але не змінюють ваги моделі й не гарантують узагальнення.

Промпт для тесту не повинен містити правильну відповідь саме тестового кейсу під виглядом прикладу.
Залиште окремий новий запит і порівняйте варіанти на однаковому наборі кейсів.
У цьому блоці Python тільки друкує промпти; не називайте довжину рядків якістю класифікації.

Є три приклади, unknown, окремий тест і пояснення різниці few-shot та fine-tuning.
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
few_shot = ('Поверни один жанр: fantasy, science, detective або unknown.\n'
            'Опис: dragon magic -> fantasy\n'
            'Опис: robot space -> science\n'
            'Опис: train crime -> detective\n'
            'Опис: friendship school magic ->')
dialogue = [{'role': 'user', 'content': 'Порадь щось цікаве'},
            {'role': 'assistant', 'content': 'Який жанр вас цікавить?'},
            {'role': 'user', 'content': 'Наукова фантастика про роботів'}]
print(few_shot)
print(json.dumps(dialogue, ensure_ascii=False, indent=2))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = diagram(['Інструкція', 'Приклади', 'Новий вхід', 'Мітка'], 'Few-shot: приклади у вході, без навчання ваг')
plt.show()
