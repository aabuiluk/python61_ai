"""**Факт 5. Результат tool повертається моделі з тим самим call_id.**
Responses API може повернути output item type=function_call замість фінального тексту.
У ньому є name, arguments та call_id. Застосунок виконує dispatch, додає попередні output
items у діалог і надсилає function_call_output з відповідним call_id. Без цього модель
не отримала підтвердженого observation, навіть якщо ви надрукували результат у консолі.
runtime.run_agent реалізує саме цей цикл; історія передається явним input, store=False.
Перевіряємо response.status перед використанням output; incomplete не приймаємо за успіх.
У trace видно фактичні виклики й observation, а не вигадані «думки» моделі.
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
    result = run_agent(api,"Який SLA у заявки T101? Спочатку перевір заявку, потім SLA.")
    show(api,result)

if __name__=="__main__":
    main()
