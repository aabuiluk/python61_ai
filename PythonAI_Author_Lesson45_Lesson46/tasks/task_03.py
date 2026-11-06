"""**Завдання 3.** Відкрийте Python-функцію get_sla і її JSON-схему. Збережіть перелік дозволених priority. Надішліть реальний запит пояснити різницю lookup_ticket і get_sla. Зіставте пояснення зі схемами.

1. TOOLS["get_sla"].args. 2. Literal задає три значення. 3. Пояснення моделі не є фактичним виконанням tool.

Готово, якщо: Є реальна @tool-схема, enum urgent/normal/low, strict=True та live-пояснення без твердження, що tool уже виконано.
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
    TOOL_NAME = None  # TODO: get_sla
    if TOOL_NAME not in TOOLS:
        raise NotImplementedError("Оберіть потрібний tool")
    schema = next(t for t in API_TOOLS if t["name"]==TOOL_NAME)
    show(api,{"schema":schema,"answer":api.text("Поясніть цю схему: "+json.dumps(schema),stage="tool_schema")})

if __name__=="__main__":
    main()
