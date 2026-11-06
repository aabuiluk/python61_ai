"""**Завдання 6.** Запустіть T101 з max_rounds=4, max_tools=4. Перевірте SLA=4 і бюджет api.calls_used<=4.
Окремо без мережі перевірте, що max_rounds=0 відхиляється. Поясніть різницю бюджету tools та модельних викликів.

1. Невалідні межі відхиляються до запиту. 2. Не провокуйте зайві платні помилки для тесту. 3. Перегляньте rounds і tool_count.

Готово, якщо: Live-цикл дав SLA 4, бюджети дотримані, нульовий max_rounds відхилено локально.
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
    api = ClassroomAPI(max_calls=4)
    QUESTION = None  # TODO: T101, ticket -> policy
    if not QUESTION:
        raise NotImplementedError("Заповніть QUESTION")
    result = run_agent(api,QUESTION,max_rounds=4,max_tools=4)
    show(api,result)
    # TODO: assert для SLA й бюджету.

if __name__=="__main__":
    main()
