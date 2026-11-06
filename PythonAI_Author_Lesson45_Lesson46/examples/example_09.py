"""**Факт 9. Повтор через помилку мережі та виправлення змісту — різні механізми.**
SDK max_retries=0 прибирає приховані повтори транспорту. Бізнес-етап repair отримує
чернетку, перевірені джерела й конкретні reasons, виконує один новий модельний запит
і знову проходить validator. Якщо друга версія неправильна, workflow має rejected,
а не нескінченний цикл. Кількість repair і calls_used записуються в стан.
Щоб гарантовано побачити цей шлях, приклад починається з навмисно хибного числа
в локальній навчальній чернетці. Це дефектний вхід для досліду; виправлена відповідь
далі отримується справжнім OpenAI API, без підстановки готового результату.
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
    question = "Який SLA у заявки T101?"
    broken = {"answer":"Термін 99 годин","ticket_id":"T101","sla_hours":99,"needs_human":False,"sources":["ticket:T101","sla:urgent"]}
    check = validate(broken,question)
    fixed,final_check = repair_once(api,question,broken,check,"support")
    show(api,{"before":check,"after":fixed,"validation":final_check})

if __name__=="__main__":
    main()
