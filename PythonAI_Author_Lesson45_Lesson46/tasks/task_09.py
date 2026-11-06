"""**Завдання 9.** Створіть навмисно хибну чернетку T102 з SLA=5, виконайте один live-repair і перевірте
24. Перевірте calls_used=1. Якщо repair не пройшов, збережіть rejected та reasons, не запускайте нескінченний повтор.

1. Початкова помилка є локальним тестовим входом. 2. repair_once робить один запит. 3. Обов’язкова повторна validate.

Готово, якщо: Один реальний repair, повторна перевірка й SLA=24; лічильник викликів показано.
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
    BROKEN_SLA = None  # TODO: неправильне число для T102
    if type(BROKEN_SLA) is not int or BROKEN_SLA==24:
        raise NotImplementedError("Задайте навмисно неправильний SLA")
    question = "Який SLA у заявки T102?"
    broken = {"answer":"Навмисна помилка","ticket_id":"T102","sla_hours":BROKEN_SLA,"needs_human":False,"sources":["ticket:T102","sla:normal"]}
    fixed,check = repair_once(api,question,broken,validate(broken,question),"support")
    show(api,{"fixed":fixed,"check":check})

if __name__=="__main__":
    main()
