### Зараз виконайте завдання 4

Відкрийте `tasks/task_04.py`. Це копія `examples/live_04.py` з місцями `TODO`: допишіть їх і запустіть `python tasks/task_04.py` з папки пакета. Потрібен OPENAI_API_KEY.

**Завдання 4.** Отримайте відповідь про самовивіз у Львові напряму через OpenAI SDK, без LangChain. Надрукуйте відповідь і кількість токенів.

### Підказки

1. Подивіться, як у `examples/live_04.py` збирається повідомлення user: `f"<context>{context}</context>\nПитання: {question}"`.
2. Токени лежать у `response.usage.input_tokens` і `response.usage.output_tokens`.

**Готово, якщо:** Надруковано JSON з `answer` і `sources: ["pickup_lviv"]` та два числа токенів.
