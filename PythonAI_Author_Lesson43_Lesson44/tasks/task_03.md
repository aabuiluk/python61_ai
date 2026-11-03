### Зараз виконайте завдання 3

Відкрийте `tasks/task_03.py`. Це копія `examples/live_03.py` з місцями `TODO`: допишіть їх і запустіть `python -m PythonAI_Author_Lesson43_Lesson44.tasks.task_03` з кореня репозиторію. Потрібен OPENAI_API_KEY.

**Завдання 3.** Запустіть той самий DocFlow-ланцюжок двічі: з `fixture_model` і з OpenAI. Порівняйте відповіді на трьох питаннях.

### Підказки

1. `chain_with(model)` уже складає context → prompt → model → parser.
2. Потрібен один рядок у циклі: `print("  OpenAI: ", openai_chain.invoke(question))`.

**Готово, якщо:** Для кожного з трьох питань надруковано дві відповіді. Ви записали, де вони відрізняються (текст, кількість джерел, відмова).
