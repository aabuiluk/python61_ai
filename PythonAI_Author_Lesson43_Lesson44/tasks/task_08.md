**Завдання 8.** Побудуйте справжній LCEL prompt | RunnableLambda | StrOutputParser для питання
про самовивіз. Модельний fixture має повернути AIMessage з префіксом FIXTURE: та текстом
останнього human-повідомлення. Перевірте invoke і batch із двох різних питань.

Підказки: 1. Lambda отримує PromptValue. 2. Останнє повідомлення: to_messages()[-1].content. 3. Кінцевий результат — str.

Готово, якщо: Використано реальний |; вихід str; batch повертає два відповідні результати; жодного API-виклику.

Окремі файли: examples/example_08.py і tasks/task_08.py у папці пакета.
Промпти для Gemini та ChatGPT — у PROMPTS.md.
