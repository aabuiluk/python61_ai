"""CrewAI + OpenAI: дві ролі (дослідник і редактор) виконують задачі по черзі.

CrewAI поки не встановлюється на Python 3.14. Потрібне окреме середовище 3.10–3.13,
див. frameworks/README.md (розділ про .venv-312).
"""
import os
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")  # не надсилати телеметрію
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import DOCS, retrieve, validate_answer
from live_openai import MODEL, EMBEDDING_MODEL, require_key

require_key()  # читає OPENAI_API_KEY з .env; без ключа скрипт завершується

import logging
logging.getLogger("crewai").setLevel(logging.ERROR)  # прибрати службові попередження
from crewai import LLM, Agent, Crew, Process, Task
from crewai.tools import tool


@tool("search_knowledge")
def search_knowledge(question: str) -> str:
    """Пошук у правилах магазину. Повертає фрагменти з id."""
    return json.dumps(retrieve(question, 2), ensure_ascii=False)


llm = LLM(model=f"openai/{MODEL}", temperature=0)
researcher = Agent(role="Дослідник", goal="Знайти правила магазину для питання клієнта",
                   backstory="Ви шукаєте лише в базі правил і завжди називаєте id фрагмента.",
                   tools=[search_knowledge], llm=llm, verbose=False)
writer = Agent(role="Редактор", goal="Написати коротку відповідь клієнту лише за знайденими правилами",
               backstory="Ви не додаєте фактів, яких немає у джерелах.", llm=llm, verbose=False)

find = Task(description="Знайдіть правила для питання: {question}",
            expected_output="Фрагменти правил з id", agent=researcher)
answer = Task(description="Напишіть відповідь клієнту одним реченням і вкажіть id джерела.",
              expected_output="Одне речення та id джерела", agent=writer, context=[find])

crew = Crew(agents=[researcher, writer], tasks=[find, answer], process=Process.sequential, verbose=False)
result = crew.kickoff(inputs={"question": "Скільки коштує доставка Україною?"})
print("Результат дослідника:", find.output.raw if find.output else None)
print("Відповідь редактора: ", result.raw)
