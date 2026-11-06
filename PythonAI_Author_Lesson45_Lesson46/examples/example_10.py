"""**Факт 10. Пауза для людини — збережений стан, з якого можна продовжити пізніше.**
Для запиту про повернення коштів workflow виконує live-router і live-draft, перевіряє
контракт і записує JSON зі status=paused_for_human. Є request_id, revision, question,
route, draft, validation, trace, model і calls_used. Так людина бачить не лише кнопку
«ок», а перевірювану пропозицію та її походження.
Модель не отримує tool виплати. Навіть якщо текст користувача наказує «вже поверни»,
локальна політика зберігає паузу. external_action_executed=false явно позначає, що
зовнішньої дії не було. Зберігайте файл до рішення: стан має пережити завершення скрипта.
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
    state,path = run_workflow(api,"Підготуй пропозицію повернення коштів за T102")
    show(api,{"state":state,"review_file":str(path)})

if __name__=="__main__":
    main()
