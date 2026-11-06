"""**Факт 1. Модельний вузол LCEL можна замінити, зберігши контракт входу й виходу.**
У 43–44 ви відокремлювали prompt від моделі. Тепер ChatPromptTemplate формує повідомлення,
RunnableLambda передає їх у ClassroomAPI.text, а StrOutputParser повертає рядок.
Усередині виконується client.responses.create; це живий API-виклик, не симуляція.
Ключ читається з локального .env пакета. Виводимо текст, фактичну модель та usage.
Перевірте призначення кожного шару: шаблон не надсилає запит сам по собі, lambda тут
викликає клієнт, parser не доводить істинність тексту. Перенесення бізнес-перевірок
залишається вашою відповідальністю.
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
    prompt = ChatPromptTemplate.from_messages([("system","Поясніть початківцю одним реченням."),("human","{question}")])
    chain = prompt | RunnableLambda(api.text) | StrOutputParser()
    answer = chain.invoke({"question":"Навіщо parser після моделі?"})
    show(api,{"answer":answer})

if __name__=="__main__":
    main()
