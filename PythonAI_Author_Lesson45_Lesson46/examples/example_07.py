"""**Факт 7. Класифікація моделі обирає маршрут, але не скасовує обов’язкову перевірку людиною.**
Router повертає route з enum support/refund/unknown та коротку reason. Після JSON
код перевіряє enum. Запити про повернення чи компенсацію мають локальну політику review:
навіть помилковий route від LLM не може перетворити їх на автоматичну дію.
Короткий reason допомагає пояснити вибір, але не є прихованим chain-of-thought.
Для складної предметної області словникового правила недостатньо: тут воно явно
обмежене навчальними формулюваннями українською та refund англійською.
Зміна маршруту впливає на наступні кроки, тому журналюємо route окремим stage.
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
    routed = route_query(api,"Підготуй пропозицію повернення коштів за T102")
    show(api,routed)

if __name__=="__main__":
    main()
