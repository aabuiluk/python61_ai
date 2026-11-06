"""**Завдання 1.** Змініть питання на різницю chain та agent. Запустіть реальний LCEL і збережіть текст відповіді разом із model та usage. Перевірте, що відбувся один API-виклик.

1. Скопіюйте структуру прикладу. 2. Замініть question. 3. Перевірте api.calls_used та api.records, не друкуйте ключ.

Готово, якщо: Є непорожня live-відповідь, один API-виклик і запис фактичних model/usage.
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
    QUESTION = None  # TODO: власне питання про chain та agent
    if not QUESTION:
        raise NotImplementedError("Заповніть QUESTION")
    api = ClassroomAPI()
    prompt = ChatPromptTemplate.from_messages([("system","Одне речення українською."),("human","{question}")])
    chain = prompt | RunnableLambda(api.text) | StrOutputParser()
    show(api,{"answer":chain.invoke({"question":QUESTION})})

if __name__=="__main__":
    main()
