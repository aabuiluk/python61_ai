"""**Факт 8. Послідовність generate → validate має явний контракт на межі кожного кроку.**
Чернетка містить answer, ticket_id, sla_hours, needs_human, sources. Structured Output
контролює форму JSON, але Python звіряє SLA з локальною таблицею, перевіряє id та джерела.
Validator повертає ok і список reasons. Неправильне число не виправляється мовчазно.
Текст answer може ще потребувати змістовного перегляду: правильні структуровані поля
не гарантують відсутність суперечностей у вільному реченні. Для зовнішніх дій додавайте
предметні перевірки та review; у цій вправі ніяких зовнішніх змін немає.
Використайте результати перевірки як дані наступного вузла, а не просто print у консолі.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pathlib import Path
import json
from runtime import (ClassroomAPI, ClassroomError, API_TOOLS, TOOLS, TICKETS, SLA,
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
    question = "Який SLA у заявки T102?"
    draft = draft_for(api,question,"support")
    check = validate(draft,question,"support")
    show(api,{"draft":draft,"validation":check})

if __name__=="__main__":
    main()
