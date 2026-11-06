"""**Завдання 7.** Класифікуйте три запити: SLA T101; повернення коштів T102; рецепт борщу.
Перевірте support/refund/unknown. Для refund поясніть роль локального правила; усі три запити мають бути справжніми API-викликами.

1. route_query по одному питанню. 2. Порівняйте enum. 3. Невдалу класифікацію збережіть, не підміняйте результат.

Готово, якщо: Три live-маршрути й записи usage; refund зберігає обов’язковий review.
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
    QUERIES = []  # TODO: три запити support/refund/unknown
    if len(QUERIES)!=3:
        raise NotImplementedError("Додайте три запити")
    routes = [route_query(api,q) for q in QUERIES]
    show(api,routes)
    # TODO: перевірте три маршрути.

if __name__=="__main__":
    main()
