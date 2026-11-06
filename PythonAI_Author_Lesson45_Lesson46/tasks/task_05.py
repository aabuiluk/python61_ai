"""**Завдання 5.** Виконайте live-цикл для T102. Перевірте наявність lookup_ticket і get_sla у trace,
непорожні call_id та фінальний sla_hours=24. Перегляньте в runtime рядок function_call_output.

1. run_agent(api,question). 2. Перевірте множину tool names. 3. Перевірте validate на фінальному draft.

Готово, якщо: Є два реальні tool-виклики з call_id, observation і фінальний валідний SLA 24.
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
    QUESTION = None  # TODO: запит про SLA T102 з вимогою перевірити ticket і policy
    if not QUESTION:
        raise NotImplementedError("Заповніть QUESTION")
    api = ClassroomAPI()
    result = run_agent(api,QUESTION)
    show(api,result)
    # TODO: перевірте tool names, call_id та validate.

if __name__=="__main__":
    main()
