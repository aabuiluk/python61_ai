"""**Завдання 8.** Додайте ще два питання і запустіть їх одним `batch`. Надрукуйте відповіді та кількість викликів API.

Підказки:
1. Кожне питання — словник `{"question": "..."}`.
2. Кількість викликів: `len(USAGE)`.

Готово, якщо: Надруковано 3 відповіді і число 3. Ви пояснили, що `batch` — це 3 окремі запити, а не один дешевший.

Подивіться examples/live_08.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_model, require_key

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
