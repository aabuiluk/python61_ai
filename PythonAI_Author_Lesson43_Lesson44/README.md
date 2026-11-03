# Пари 43–44 з переходом 41–42

Почніть із PythonAI_Author_Lesson43_Lesson44.html, .md або .ipynb у цій папці чи її батьківському каталозі.

30 + 100 + 100 хв; 12 блоків. У кожному блоці:

- `examples/example_NN.py` — офлайн-приклад на `fixture_model`, без мережі;
- `examples/live_NN.py` — той самий крок зі справжньою моделлю OpenAI;
- `tasks/task_NN.py` — завдання на OpenAI: копія live-прикладу з 1–2 місцями `TODO`.

Встановлення з кореня репозиторію:

    python -m pip install -r PythonAI_Author_Lesson43_Lesson44/requirements.txt -r PythonAI_Author_Lesson43_Lesson44/requirements-live.txt

Ключ: якщо є `PythonAI_Author_Lesson41_Lesson42/.env`, його буде знайдено автоматично. Інакше скопіюйте
`.env.example` у `.env` у цій папці. Запуск з кореня репозиторію: `python -m PythonAI_Author_Lesson43_Lesson44.examples.live_01`, `python -m PythonAI_Author_Lesson43_Lesson44.tasks.task_01`.

`frameworks/` — окремі приклади LangChain, LlamaIndex, LangGraph, CrewAI, AutoGen, Semantic Kernel і
Microsoft Agent Framework на OpenAI. Що встановити — у `frameworks/README.md`.

Графіка відокремлена `# %%`; закрийте вікно графіка для завершення скрипта.
PROMPTS.md: однакові промпти для Gemini та ChatGPT. COVERAGE.md: відповідність програмі.
