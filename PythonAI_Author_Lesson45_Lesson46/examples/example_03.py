"""**Факт 3. Tool — це Python-функція, опис її призначення та схема аргументів.**
runtime.py оголошує lookup_ticket і get_sla через справжній декоратор @tool із
langchain-core. Docstring пояснює, коли дія доречна, а type hints задають типи.
convert_to_openai_function переносить цей контракт у function tool для Responses API.
Назва й схема не надають моделі прямого доступу до Python: виконання відбудеться
тільки через наш dispatcher. Strict schema допомагає формі аргументів, але не гарантує,
що запит до обраного інструмента доречний або що заявка існує.
У прикладі надсилаємо моделі самі схеми та просимо пояснити вибір. У наступних блоках
виконаємо справжні function calls. Два read-only tools не змінюють заявки.
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
    print(json.dumps(API_TOOLS,ensure_ascii=False,indent=2))
    answer = api.text("Доступні схеми: "+json.dumps(API_TOOLS)+". Одним реченням поясніть: який tool спочатку потрібен для SLA T101 і чому?",stage="tool_schema")
    show(api,{"answer":answer})

if __name__=="__main__":
    main()
