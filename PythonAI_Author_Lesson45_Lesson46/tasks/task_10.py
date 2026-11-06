"""**Завдання 10.** Створіть live-пропозицію повернення за T101. Перевірте paused_for_human, revision=1,
існування файла та external_action_executed=false. Прочитайте JSON заново з диска й звірте request_id.

1. run_workflow робить реальні запити. 2. Файл має бути в results/. 3. Пока не викликайте approve.

Готово, якщо: Два або більше live-виклики, файл стану з паузою, ревізією та відсутністю зовнішньої дії.
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
    QUESTION = None  # TODO: пропозиція повернення за T101
    if not QUESTION:
        raise NotImplementedError("Заповніть QUESTION")
    state,path = run_workflow(api,QUESTION)
    show(api,{"state":state,"path":str(path)})
    # TODO: прочитайте файл і перевірте pause/revision/external_action_executed.

if __name__=="__main__":
    main()
