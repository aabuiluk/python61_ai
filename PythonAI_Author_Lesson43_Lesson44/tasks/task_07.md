**Завдання 7.** Створіть chat-шаблон: system задає відповідь тільки за джерелом; human містить
context і question. Підставте pickup_lviv та питання про вартість самовивозу.
Перевірте типи повідомлень і поведінку за відсутності question.

Підказки: 1. ChatPromptTemplate.from_messages. 2. invoke(...).to_messages(). 3. Пропущене question має спричинити KeyError до моделі.

Готово, якщо: Два повідомлення system/human, context підставлено; відсутнє question відхилено до виклику моделі.

Окремі файли: examples/example_07.py і tasks/task_07.py у папці пакета.
Промпти для Gemini та ChatGPT — у PROMPTS.md.
