"""**Завдання 3.** Запустіть той самий DocFlow-ланцюжок двічі: з `fixture_model` і з OpenAI. Порівняйте відповіді на трьох питаннях.

Підказки:
1. `chain_with(model)` уже складає context → prompt → model → parser.
2. Потрібен один рядок у циклі: `print("  OpenAI: ", openai_chain.invoke(question))`.

Готово, якщо: Для кожного з трьох питань надруковано дві відповіді. Ви записали, де вони відрізняються (текст, кількість джерел, відмова).

Подивіться examples/live_03.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from langchain_core.runnables import RunnableLambda
from PythonAI_Author_Lesson43_Lesson44.live_openai import (
    chain_with, live_json_model, print_usage, require_key,
)
from PythonAI_Author_Lesson43_Lesson44.workshop import fixture_model

require_key()

# %% Ваш код: допишіть місця TODO
questions = ["Доставка Україною", "Самовивіз у Львові", "Марсіанський телепорт"]
fixture_chain = chain_with(RunnableLambda(fixture_model))
openai_chain = chain_with(live_json_model)
for question in questions:
    print(question)
    print("  fixture:", fixture_chain.invoke(question))
    # TODO: надрукуйте відповідь openai_chain на це саме питання
print_usage()
