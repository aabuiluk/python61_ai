"""**Факт 4. Аргументи моделі проходять перевірку до Python-виклику.**
Зовнішній рядок спочатку читаємо json.loads, потім перевіряємо object, точний набір
ключів, типи та дозволені значення. Не використовуємо eval або getattr для довільних
назв. Dispatcher має allowlist із двох tools і повертає ok/data або ok/error.
Невідомий tool, зайвий ключ, число замість рядка й відсутня заявка — різні негативні кейси.
Приклад робить реальний API-запит на JSON-аргументи, після чого Python виконує dispatch.
Це ще не повний function-calling протокол: у ньому також є call_id та function_call_output,
які розберемо далі. Зберігайте цю різницю в назві свого результату.
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
    schema = {"type":"object","properties":{"priority":{"type":"string","enum":["urgent","normal","low"]}},"required":["priority"],"additionalProperties":False}
    args = api.structured("Поверніть аргументи get_sla для priority urgent.",schema=schema,stage="arguments")
    observation = dispatch("get_sla",args)
    show(api,{"arguments":args,"observation":observation})

if __name__=="__main__":
    main()
