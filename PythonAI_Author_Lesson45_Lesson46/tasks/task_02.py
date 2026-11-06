"""**Завдання 2.** Виконайте дві live-репліки в A й одну в B. В A використайте слово «Липа», у B попросіть повторити слово, якого B не отримувала. Перевірте довжини історій 4 та 2 і відсутність повідомлень A у B.

1. Новий store. 2. Три invoke з двома session_id. 3. Не перевіряйте ізоляцію тільки за відповіддю моделі: перегляньте повідомлення.

Готово, якщо: Три реальні запити; A має 4 повідомлення, B — 2; історія B не містить приватної репліки A.
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
    store = {}
    def history_for(sid):
        return store.setdefault(sid,InMemoryChatMessageHistory())
    prompt = ChatPromptTemplate.from_messages([("system","Відповідайте тільки з історії цієї сесії."),MessagesPlaceholder("history"),("human","{question}")])
    model = RunnableLambda(lambda value: AIMessage(content=api.text(value,stage="memory")))
    chat = RunnableWithMessageHistory(prompt | model,history_for,input_messages_key="question",history_messages_key="history")
    QUERIES = []  # TODO: три пари (session_id, question) для A/A/B
    if len(QUERIES)!=3:
        raise NotImplementedError("Заповніть QUERIES")
    for sid,question in QUERIES:
        answer = chat.invoke({"question":question},config={"configurable":{"session_id":sid}})
    show(api,{"answer":answer.content,"lengths":{k:len(v.messages) for k,v in store.items()}})
    # TODO: перевірте 4/2 повідомлення та відсутність приватного тексту A в B.

if __name__=="__main__":
    main()
