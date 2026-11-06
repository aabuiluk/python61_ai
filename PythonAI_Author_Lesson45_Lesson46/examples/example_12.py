"""**Факт 12. Завершення workflow доводиться станом, перевірками та журналом викликів.**
Підсумок: route → tools/draft → validate → до одного repair → completed або
paused_for_human/rejected. Клієнт моделі є залежністю ClassroomAPI, а не копією SDK-коду
в кожному вузлі. Це дозволяє тестувати транспорт локально, не підміняючи live-режим
навчальних прикладів. Дані про model, status, usage та latency потрапляють у usage.jsonl.
Ключі не записуються, текст заявки не потрібний у транспортному журналі.
Ви маєте показати живий tool trace і файл review, а локальні негативні тести позначити
окремо. Зелений транспортний тест не є фактично виконаним живим запитом.
Exit ticket: хто виконав дію; як перевірено факт; де межа повторів; який статус очікує людину?
Де перечитати: блоки 5, 8, 9, 10–11.
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
    api = ClassroomAPI(max_calls=8)
    state,path = run_workflow(api,"Який SLA у заявки T101? Перевірте через інструменти.")
    show(api,{"state":state,"saved_to":str(path)})

if __name__=="__main__":
    main()
