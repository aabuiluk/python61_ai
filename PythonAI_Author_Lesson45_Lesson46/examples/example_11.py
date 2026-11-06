"""**Факт 11. Рішення людини також має правила переходу та повторну валідацію.**
Після paused_for_human можна approve, edit або reject. Edit змінює текст answer,
не довільні id чи SLA. Перед фінальним статусом знову виконується validate. Ревізія
збільшується; повторне рішення для того самого завершеного файла відхиляється.
Це локальна послідовна демонстрація, а не готовий сервіс із транзакційним блокуванням.
Для справжньої команди review потрібні авторизація, журнал рецензента й захист від
одночасного схвалення. Тут усі приклади працюють тільки з навчальними файлами.
Схвалення затверджує чернетку, але не запускає платіж чи надсилання повідомлення.
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
    state,path = run_workflow(api,"Підготуй пропозицію повернення коштів за T102")
    reviewed = resume(path,"edit",edited_answer="Пропозицію передано на розгляд; повернення коштів ще не виконувалось.")
    show(api,{"reviewed":reviewed})

if __name__=="__main__":
    main()
