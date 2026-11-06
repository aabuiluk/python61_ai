"""**Завдання 11.** Згенеруйте live-чернетку T103 для повернення, відхиліть її через resume(...,"reject").
Перевірте status=rejected і revision=2. Повторний approve цього самого файла має завершитися ClassroomError без нового API-виклику.

1. Спершу має бути paused_for_human. 2. Збережіть calls_used до review. 3. Повторний виклик обгорніть try/except.

Готово, якщо: Є live-походження чернетки, відхилення з revision=2 і заблокований повторний approve без додаткового API-запиту.
"""
from pathlib import Path
import sys
REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPOSITORY))
from pathlib import Path
import json
from PythonAI_Author_Lesson45_Lesson46.runtime import (ClassroomAPI, ClassroomError, API_TOOLS, TOOLS, TICKETS, SLA,
    ANSWER_SCHEMA, ROUTE_SCHEMA, dispatch, validate, run_agent, route_query,
    draft_for, repair_once, run_workflow, resume, show)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

def main():
    api = ClassroomAPI()
    state,path = run_workflow(api,"Підготуй пропозицію повернення коштів за T103")
    DECISION = None  # TODO: reject
    if DECISION not in {"approve","edit","reject"}:
        raise NotImplementedError("Оберіть рішення")
    reviewed = resume(path,DECISION)
    show(api,reviewed)
    # TODO: перевірте revision та заблокуйте повторний review.

if __name__=="__main__":
    main()
