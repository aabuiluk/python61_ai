# Карта практики

Пара 47: блоки 1–6 (80 хв). Пара 48: блоки 7–12 (80 хв).

1. 47 · Перехід з workflow: один запит, кілька етапів → examples/example_01.py → tasks/task_01.py → Є три фактичні результати, правильне джерело для строку 14 календарних днів і пояснення відмови або неоднозначності.
2. 47 · JSONL trace: токени, затримка, помилка → examples/example_02.py → tasks/task_02.py → Кожен рядок розбирається як JSON; ключів і текстів питань немає; usage підсумовано без подвійного рахунку result.
3. 47 · Звіт про запуски та межі метрик → examples/example_03.py → tasks/task_03.py → Таблиця не змішує різні етапи; приклад overlap=0.75 не названий faithfulness.
4. 47 · Golden cases: очікування до запуску → examples/example_04.py → tasks/task_04.py → Є 10 кейсів, очікувана ціна S300=690 грн, для експрес-доставки — refused. Новий набір окремо від базового.
5. 47 · LLM-as-judge та ручна перевірка → examples/example_05.py → tasks/task_05.py → Є власна оцінка й три реальні судження; відхилення judge від людини чесно зафіксовані.
6. 47 · JSONL, LangSmith та Monitoring: що бачимо → examples/example_06.py → tasks/task_06.py → Відрізняєте чотири інтерфейси: файл trace, UI додатка, Qdrant dashboard і optional LangSmith.
7. 48 · Десять PDF: extraction, chunking, provenance → examples/example_07.py → tasks/task_07.py → Знайдено рівно 10 PDF, кількість chunks пояснена, 7 одиниць перевірено у видимому джерелі.
8. 48 · OpenAI embeddings → Qdrant collection → examples/example_08.py → tasks/task_08.py → Кількість points стабільна; embedding етапів у trace під час cached build немає; база переживає закриття процесу.
9. 48 · Vector search: top-k, score та фільтр → examples/example_09.py → tasks/task_09.py → Є два набори retrieval, у filtered немає чужих PDF; висновок про ціну спирається на каталог.
10. 48 · RAG-відповідь, citations, hit і miss → examples/example_10.py → tasks/task_10.py → У UI видно джерела доставки; miss не має generate з тим самим run_id; невідомий товар не отримав вигаданої ціни або чесно позначений як fail.
11. 48 · HITL та перевірка набору кейсів → examples/example_11.py → tasks/task_11.py → Чернетка з sent=false; eval_report має 8 кейсів та посилання run_id; висновок не приховує помилок.
12. 48 · Локальний запуск, перевірка релізу й наступні кроки → examples/example_12.py → tasks/task_12.py → README відтворює запуск з кореня, результати перевірені за джерелами, секретів у здачі немає.