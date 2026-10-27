Після пояснення та `examples/example_06.py` виконайте цю вправу у `tasks/task_06.py`.

**Завдання 6.** Напишіть dispatch(request) з allowlist для lookup_book.
Перевірте b02, b99 і недозволену дію delete_all. Складіть журнал request → observation
для двох дозволених пошуків. Після None відповідь має повідомити, що запис відсутній.

## Підказки
1. Перевірте набір ключів і назву action. 2. Пошук зробіть через next(..., None).
3. Для delete_all перехопіть ValueError; не реалізуйте цю дію.

Готово, якщо: b02 → 450; b99 → None; delete_all заблокована; журнал містить реальні результати Python.

Окремі файли: `examples/example_06.py` і `tasks/task_06.py` у папці пакета.

Промпт можна виконати в Gemini або ChatGPT; повний текст і обидва маршрути — у PROMPTS.md, блок 6.
