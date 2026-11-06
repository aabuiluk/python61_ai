### Зараз виконайте завдання 5

Після прикладу відкрийте `tasks/task_05.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_05.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

**Завдання 5.** Виконайте live-цикл для T102. Перевірте наявність lookup_ticket і get_sla у trace,
непорожні call_id та фінальний sla_hours=24. Перегляньте в runtime рядок function_call_output.

### Підказки

1. run_agent(api,question). 2. Перевірте множину tool names. 3. Перевірте validate на фінальному draft.

**Готово, якщо:** Є два реальні tool-виклики з call_id, observation і фінальний валідний SLA 24.

Окремі файли: `examples/example_05.py` і `tasks/task_05.py` у папці пакета.
