"""**Завдання 4.** Отримайте від моделі аргументи для normal і виконайте get_sla. Локально перевірте unknown_tool, зламаний JSON та зайвий ключ. Виведіть різні error-коди; негативні тести не потребують додаткових API-запитів.

1. Schema та prompt задають normal. 2. Перевірте observation data.hours=24. 3. Викличте dispatch напряму для помилкових аргументів.

Готово, якщо: Live-аргументи normal дали 24 години; три негативні кейси мають окремі error-коди.
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
    PRIORITY = None  # TODO: normal
    if PRIORITY not in SLA:
        raise NotImplementedError("Заповніть PRIORITY")
    api = ClassroomAPI()
    schema = {"type":"object","properties":{"priority":{"type":"string","enum":list(SLA)}},"required":["priority"],"additionalProperties":False}
    args = api.structured("Аргументи get_sla для "+PRIORITY,schema=schema,stage="arguments")
    show(api,{"observation":dispatch("get_sla",args)})
    # TODO: додайте три негативні локальні перевірки.

if __name__=="__main__":
    main()
