"""**Завдання 4.** Отримайте відповідь про самовивіз у Львові напряму через OpenAI SDK, без LangChain. Надрукуйте відповідь і кількість токенів.

Підказки:
1. Подивіться, як у `examples/live_04.py` збирається повідомлення user: `f"<context>{context}</context>\nПитання: {question}"`.
2. Токени лежать у `response.usage.input_tokens` і `response.usage.output_tokens`.

Готово, якщо: Надруковано JSON з `answer` і `sources: ["pickup_lviv"]` та два числа токенів.

Подивіться examples/live_04.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

# %% Ваш код: допишіть місця TODO
question = "Самовивіз у Львові"
context = context_for(question)
response = client().responses.create(
    model=MODEL, store=False, max_output_tokens=200,
    text={"format": {"type": "json_object"}},
    input=[
        {"role": "system", "content": "Працюйте лише за контекстом. Поверніть answer та sources у JSON."},
        # TODO 1: додайте повідомлення {"role": "user", "content": ...} з context і question
    ])
record_usage(response)
print("Відповідь:", json.loads(response.output_text))
# TODO 2: надрукуйте response.usage.input_tokens і response.usage.output_tokens
