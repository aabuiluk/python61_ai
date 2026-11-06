"""**Завдання 12.** Запустіть повний live-workflow для SLA T102. Перевірте completed, SLA=24, validation.ok
та наявність tools у trace. Збережіть REPORT.md: question, model, call count, usage,
валідація, межі та відмінність від запиту про повернення. Не включайте ключ.

1. max_calls=8 не гарантує певної ціни, але обмежує виклики. 2. completed не означає, що відбулась зовнішня дія. 3. Файл звіту зберігайте в results/.

Готово, якщо: Повний live-цикл completed/T102/24, tool trace, usage та REPORT.md без ключа; refund-маршрут відмежовано.
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
    api = ClassroomAPI(max_calls=8)
    QUESTION = None  # TODO: SLA T102 з перевіркою tools
    if not QUESTION:
        raise NotImplementedError("Заповніть QUESTION")
    state,path = run_workflow(api,QUESTION)
    show(api,{"state":state,"path":str(path)})
    # TODO: перевірки completed, SLA, trace та власний REPORT.md.

if __name__=="__main__":
    main()
