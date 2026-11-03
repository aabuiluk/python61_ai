"""**Завдання 8.** Додайте ще два питання і запустіть їх одним `batch`. Надрукуйте відповіді та кількість викликів API.

Підказки:
1. Кожне питання — словник `{"question": "..."}`.
2. Кількість викликів: `len(USAGE)`.

Готово, якщо: Надруковано 3 відповіді і число 3. Ви пояснили, що `batch` — це 3 окремі запити, а не один дешевший.

Подивіться examples/live_08.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

# %% Ваш код: допишіть місця TODO
prompt = ChatPromptTemplate.from_messages([("system", "Відповідайте одним коротким реченням."),
                                           ("human", "{question}")])
chain = prompt | live_model | StrOutputParser()
questions = [{"question": "Що таке RAG?"}]  # TODO 1: додайте ще два питання
answers = chain.batch(questions)
for item, answer in zip(questions, answers):
    print(item["question"], "→", answer)
# TODO 2: надрукуйте кількість викликів API: len(USAGE)
