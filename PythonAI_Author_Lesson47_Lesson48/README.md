# Пари 47–48 · готовий магазин із Qdrant RAG

Теорія → приклад → практика; 20 + 20 + 80 + 80 = 200 хв. Спочатку tasks/bridge_45.py (20 хв) і tasks/bridge_46.py (20 хв), потім основні 47–48. Почніть з PythonAI_Author_Lesson47_Lesson48.html або .ipynb. Методичка лежить у корені та в цій єдиній папці. Студентські tasks містять TODO; готові приклади — examples, завершений RAG-додаток — app.py/runtime.py.

## Запуск із кореня python61_ai

Python 3.11+. Активуйте спільне .venv і виконайте:

```bash
python -m pip install -r requirements-47-48.txt
python PythonAI_Author_Lesson47_Lesson48/runtime.py inspect
```

Скопіюйте PythonAI_Author_Lesson47_Lesson48/.env.example у .env у цій самій папці. Вставте справжній OPENAI_API_KEY. QDRANT_URL лишіть порожнім. Нове .venv всередині пакета не потрібне. Для Jupyter додатково: python -m pip install jupyterlab ipykernel; виберіть ядро свого .venv.

```bash
python PythonAI_Author_Lesson47_Lesson48/runtime.py build
python PythonAI_Author_Lesson47_Lesson48/runtime.py stats
python PythonAI_Author_Lesson47_Lesson48/runtime.py search "Скільки ламп L100 є на складі?" --top-k 4
python PythonAI_Author_Lesson47_Lesson48/runtime.py ask "Яка вартість доставки Україною?"
python PythonAI_Author_Lesson47_Lesson48/runtime.py ask "Скільки коштує ноутбук X999?"
python PythonAI_Author_Lesson47_Lesson48/runtime.py ask "Яка доставка?" --source does_not_exist.pdf
python PythonAI_Author_Lesson47_Lesson48/runtime.py ask "Підготуй пояснення правил повернення." --draft
python PythonAI_Author_Lesson47_Lesson48/runtime.py eval
python PythonAI_Author_Lesson47_Lesson48/runtime.py trace
python -m streamlit run PythonAI_Author_Lesson47_Lesson48/app.py
```

UI: http://localhost:8501. Якщо порт зайнятий, додайте --server.port 8502. Перед CLI зупиніть Streamlit (Ctrl+C), і навпаки: Qdrant Local має одного власника сховища. Після закриття індекс зберігається у PythonAI_Author_Lesson47_Lesson48/artifacts/qdrant.

## Де і що перевіряти

1. Inspect у терміналі: files=10, chunks>10, перший source_id, page і текст. Відкрийте data/pdf/03_stock.pdf: L100 — 7 одиниць на дату знімка.
2. Build/stats: points дорівнює кількості chunks, dimensions відповідає embeddings. Повторний build має cached=true та ті самі points.
3. Search: source_id, score, file, page, text. Для ціни потрібен каталог; для доставки — 04_delivery.pdf. Score не є ймовірністю істини.
4. UI: кнопки перевірки PDF, індексації та статистики зліва. Після питання видно status, sources, run_id. Нижче кожен hit і кнопка PDF; відкрийте й звірте факт вручну.
5. Trace: artifacts/trace.jsonl або розділ UI. Знайдіть run_id; дивіться embedding/retrieve/generate/result, токени та duration_ms. Порожній retrieval не має generate. Порожня колекція не має embeddings.
6. Невідомий ноутбук: очікується refused без вигаданої ціни. Якщо не так — записуйте fail. Детермінований miss — --source does_not_exist.pdf.
7. HITL: checkbox у UI або --draft. Для answered з’явиться pending_approval та artifacts/approval_UUID.json з sent=false. Реального надсилання немає.
8. Eval: artifacts/eval_report.json, 8 кейсів. Status accuracy та retrieval hit@k не доводять правильності фактів. Перевірте PDF і текст відповіді вручну. --judge додає платний оцінювач.

## Qdrant Server і dashboard (додатково)

Встановіть Docker Desktop і запустіть його. Named volume однаковий для Windows/macOS:

```bash
docker volume create store47_qdrant
docker run -d --name store47-qdrant -p 127.0.0.1:6333:6333 -v store47_qdrant:/qdrant/storage qdrant/qdrant:v1.20.0
```

У .env задайте QDRANT_URL=http://localhost:6333, перезапустіть Python/Streamlit, виконайте build у серверну базу. Dashboard: http://localhost:6333/dashboard → Collections → store_47_48 → Points → payload. Перевірте file/page/text/embedding_model. Локальна база в artifacts і Docker volume — різні сховища. Для повторного старту контейнера: docker start store47-qdrant. Основний маршрут без Docker теж використовує справжню Qdrant, але dashboard не має.

## Дані, версії та помилки

Десять PDF — вигадані українські правила магазину. Індексація не змінює ваги LLM. PDF-фрагменти та питання надсилаються в OpenAI; vectors/retrieval локальні. API-запити платні. Ключ не друкується і не потрапляє у trace. Artifacts, чернетки, .env і локальна база виключені з ZIP/Git.

Changed corpus/model: задайте нову QDRANT_COLLECTION (наприклад store_47_48_v2), повторіть build. Старий індекс зберігається. Connection refused: перевірте Docker/QDRANT_URL. Locked storage: закрийте інший Python/Streamlit-процес. 401: перевірте ключ у .env; 429: баланс/ліміт API; model not found: OPENAI_MODEL; incomplete: коротше питання або перевірка output budget. Безкоштовного fake fallback немає.

Приклад: python PythonAI_Author_Lesson47_Lesson48/examples/example_01.py. Завдання: python PythonAI_Author_Lesson47_Lesson48/tasks/task_01.py. Якщо ZIP розпаковано окремо, збережіть структуру каталогів. Транспортні тести: python -m pytest PythonAI_Author_Lesson47_Lesson48/tests -q (жодних платних викликів).

Необов’язковий LangSmith: python -m pip install langsmith; ключ LANGSMITH_API_KEY у .env. python PythonAI_Author_Lesson47_Lesson48/examples/langsmith_optional.py — лише попередній перегляд; --send передає тільки очищені метадані одного run. Його UI не є Qdrant dashboard.
