"""**Завдання 10.** Перевірте ізоляцію пам'яті: у сесії A представтесь і запитайте своє ім'я, у сесії B запитайте ім'я без представлення.

Підказки:
1. Функція `ask(session, question)` уже готова, потрібні лише два виклики.
2. Кількість повідомлень у кожній сесії друкує останній рядок.

Готово, якщо: Сесія A називає ваше ім'я, сесія B — ні. У `store` у сесії A 4 повідомлення, у B — 2.

Подивіться examples/live_10.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from PythonAI_Author_Lesson43_Lesson44.live_openai import live_model, require_key

require_key()

# %% Ваш код: допишіть місця TODO
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

ask("A", "Мене звати Олена.")  # можна вказати своє ім'я
# TODO 1: у сесії A запитайте «Як мене звати?»
# TODO 2: у сесії B запитайте «Як мене звати?»
print({session: len(history.messages) for session, history in store.items()})
