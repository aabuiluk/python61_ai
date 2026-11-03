"""Блок 10 · альтернатива з OPENAI_API_KEY (необов'язково).

`RunnableWithMessageHistory` зі справжньою моделлю: сесія A представляється, сесія B ставить те саме питання.

Офлайн-версія: examples/example_10.py. Без ключа скрипт друкує «пропущено».
"""
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_model, print_usage, require_key

require_key()

store = {}
def history_for(session_id):
    return store.setdefault(session_id, InMemoryChatMessageHistory())

prompt = ChatPromptTemplate.from_messages([("system", "Ви консультант магазину. Відповідайте коротко."),
                                           MessagesPlaceholder("history"), ("human", "{question}")])
chat = RunnableWithMessageHistory(prompt | live_model, history_for,
                                  input_messages_key="question", history_messages_key="history")

def ask(session, question):
    reply = chat.invoke({"question": question}, config={"configurable": {"session_id": session}})
    print(f"[{session}] {question} → {reply.content}")

ask("A", "Мене звати Олена, мене цікавить самовивіз у Львові.")
ask("A", "Як мене звати і що мене цікавить?")
ask("B", "Як мене звати?")
print({session: len(history.messages) for session, history in store.items()})
print_usage()
