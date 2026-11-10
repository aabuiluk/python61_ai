### Зараз виконайте завдання 8

Після прикладу відкрийте `tasks/task_08.py`, допишіть TODO і запустіть. Для порівняння — `examples/example_08.py`. Це live-код із виданим ключем OpenAI. У ноутбуці використайте наступну комірку.

Запустіть build двічі, потім stats. Запишіть points і dimensions. Другий build має cached=true, а points не збільшується. У Docker dashboard відкрийте collection → points → payload; без Docker перегляньте payload через наступний search.

### Підказки

Запускайте CLI після зупинки Streamlit. Якщо corpus/model mismatch — нова назва QDRANT_COLLECTION і повторний build. Ключ не копіюйте у звіт.

**Готово, якщо:** Кількість points стабільна; embedding етапів у trace під час cached build немає; база переживає закриття процесу.

Окремі файли: `examples/example_08.py` і `tasks/task_08.py` у папці пакета.
