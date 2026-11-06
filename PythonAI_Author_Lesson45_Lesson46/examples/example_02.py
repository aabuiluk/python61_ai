"""**Факт 2. Модель бачить тільки ту історію, яку застосунок передав у поточному запиті.**
Зберігаємо реальний RunnableWithMessageHistory із 44, а його модельний вузол викликає
OpenAI API. Сесія A отримує кодове слово, наступна репліка просить його повторити.
Новий session_id B не має цих повідомлень. Перевіряємо і поведінку моделі, і склад
сховища; лише правдоподібна відповідь не доводить ізоляцію.
InMemoryChatMessageHistory існує в RAM поточного процесу. Store=False в API не
підміняє локальне керування історією: потрібні messages, session_id та бюджет контексту.
За нових запусків скрипта починаємо з порожнього store.
Це місток до коду 44 на зафіксованій версії: RunnableWithMessageHistory та
InMemoryChatMessageHistory уже позначені deprecated у цій лінійці LangChain. Попередження
не є помилкою запуску. Для нових виробничих агентів перегляньте short-term memory та
LangGraph persistence; у 46 ми окремо зберігаємо стан workflow, а не покладаємось на RAM.
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
    store = {}
    def history_for(sid):
        return store.setdefault(sid,InMemoryChatMessageHistory())
    prompt = ChatPromptTemplate.from_messages([("system","Працюйте тільки з історією цієї розмови."),MessagesPlaceholder("history"),("human","{question}")])
    model = RunnableLambda(lambda value: AIMessage(content=api.text(value,stage="memory")))
    chat = RunnableWithMessageHistory(prompt | model,history_for,input_messages_key="question",history_messages_key="history")
    chat.invoke({"question":"Кодове слово нашої вправи — Клен."},config={"configurable":{"session_id":"A"}})
    answer = chat.invoke({"question":"Яке кодове слово я назвав?"},config={"configurable":{"session_id":"A"}})
    show(api,{"answer":answer.content,"messages_A":len(store["A"].messages)})

if __name__=="__main__":
    main()
