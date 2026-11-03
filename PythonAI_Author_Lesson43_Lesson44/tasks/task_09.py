"""**Завдання 9.** Перевірте три питання справжньою моделлю: доставка Україною, «Марсіанський телепорт» і доставка в Польщу. Для кожного надрукуйте результат `validate_answer` і чи збігається answer дослівно з джерелом.

Підказки:
1. Додайте два рядки в список `questions`.
2. Дослівний збіг: `result["answer"] in [d["text"] for d in docs]`.

Готово, якщо: Для трьох питань є `контракт` і `дослівно`. Ви знайшли випадок, де контракт `True`, а факт сумнівний (Польща).

Подивіться examples/live_09.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from PythonAI_Author_Lesson43_Lesson44.live_openai import (
    chain_with, live_json_model, print_usage, require_key,
)
from PythonAI_Author_Lesson43_Lesson44.workshop import retrieve, validate_answer

require_key()

# %% Ваш код: допишіть місця TODO
chain = chain_with(live_json_model)
questions = ["Доставка Україною"]  # TODO 1: додайте «Марсіанський телепорт» і «Скільки коштує доставка у Польщу?»
for question in questions:
    docs = retrieve(question)
    result = chain.invoke(question)
    print(question, "→", result)
    print("   контракт:", validate_answer(result, docs))
    # TODO 2: надрукуйте, чи result["answer"] дослівно є серед текстів docs
print_usage()
