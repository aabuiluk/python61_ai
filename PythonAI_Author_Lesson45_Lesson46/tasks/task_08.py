"""**Завдання 8.** Отримайте live-чернетку для T103 та перевірте SLA=72. У копії чернетки локально змініть
sla_hours на 1, а потім sources на невідомий id. Перевірте wrong_sla й unknown_or_duplicate_source.

1. Не змінюйте оригінальний live-вивід. 2. Робіть копії словника. 3. Негативні перевірки без мережі.

Готово, якщо: Є live-чернетка T103/72, валідний контракт і два незалежні негативні кейси.
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
    QUESTION = None  # TODO: T103
    if not QUESTION:
        raise NotImplementedError("Заповніть QUESTION")
    draft = draft_for(api,QUESTION,"support")
    show(api,{"draft":draft,"check":validate(draft,QUESTION)})
    # TODO: дві локальні копії з помилками SLA та source.

if __name__=="__main__":
    main()
