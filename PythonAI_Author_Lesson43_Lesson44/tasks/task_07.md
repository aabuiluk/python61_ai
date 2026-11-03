### Зараз виконайте завдання 7

Відкрийте `tasks/task_07.py`. Це копія `examples/live_07.py` з місцями `TODO`: допишіть їх і запустіть `python -m PythonAI_Author_Lesson43_Lesson44.tasks.task_07` з кореня репозиторію. Потрібен OPENAI_API_KEY.

**Завдання 7.** Допишіть chat-шаблон: додайте повідомлення human зі змінними `{context}` і `{question}`. Запитайте, коли працює магазин, і передайте знайдений контекст.

### Підказки

1. Формат рядка як у `examples/live_07.py`: `("human", "<context>{context}</context>\nПитання: {question}")`.
2. Після TODO 1 `chat.input_variables` має показати `['context', 'question']`.

**Готово, якщо:** Надруковано `['context', 'question']` і одне речення з «09:00» та «18:00».
