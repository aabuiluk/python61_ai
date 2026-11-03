# Фреймворки на OpenAI · пари 43–44

Ті самі три правила магазину й той самий `retrieve()` з `workshop.py`, але в різних фреймворках.
Модель — `OPENAI_MODEL` (за замовчуванням `gpt-4.1-mini`), ключ — `OPENAI_API_KEY` з `.env`, як і в
`examples/live_NN.py`. Кожен скрипт робить 2–6 коротких запитів, тобто центи.

| Файл | Що показує | Встановлення (з папки пакета) |
|---|---|---|
| `langchain_demo.py` | ланцюжок `prompt \| ChatOpenAI \| parser` і виклик інструмента | `python -m pip install -r frameworks/requirements-langchain.txt` |
| `llamaindex_demo.py` | індекс документів, embeddings, відповідь з id джерела | `python -m pip install -r frameworks/requirements-llamaindex.txt` |
| `langgraph_demo.py` | граф станів retrieve → answer → validate з лімітом повторів | `python -m pip install -r frameworks/requirements-langgraph.txt` |
| `crewai_demo.py` | дві ролі (дослідник і редактор) виконують задачі по черзі | `python -m pip install -r frameworks/requirements-crewai.txt` |
| `autogen_demo.py` | агент AutoGen з інструментом пошуку | `python -m pip install -r frameworks/requirements-autogen.txt` |
| `semantic_kernel_demo.py` | агент Semantic Kernel з плагіном | окреме середовище Python 3.12, див. нижче |
| `agent_framework_demo.py` | Microsoft Agent Framework — наступник AutoGen і Semantic Kernel | `python -m pip install -r frameworks/requirements-agent-framework.txt` |

Запуск з папки `PythonAI_Author_Lesson43_Lesson44`: `python frameworks/langchain_demo.py`.

Ставте лише той фреймворк, який запускаєте. Якщо потрібні всі одразу, крім Semantic Kernel:
`python -m pip install -r frameworks/requirements-all.txt` (близько 1.4 ГБ). CrewAI і LlamaIndex можуть
понизити версію пакета `openai` до 2.x. Це нормально: приклади й завдання 41–44 з нею працюють.

**Semantic Kernel** поки не встановлюється на Python 3.14. Створіть для нього окреме середовище:

    python3.12 -m venv .venv-sk
    .venv-sk/bin/python -m pip install -r frameworks/requirements-semantic-kernel.txt
    .venv-sk/bin/python frameworks/semantic_kernel_demo.py

На Windows замість `.venv-sk/bin/python` — `.venv-sk\Scripts\python`.

Що порівнювати: у кожному фреймворку модель лише пропонує дію або текст. Пошук, перевірку джерел і
ліміт кроків задає наш код. Фреймворк змінює, як цей код записано, а не те, хто за нього відповідає.
