"""**Факт 6. Кожний новий крок агента має бюджет і видимий результат попередньої дії.**
ReAct у практикумі — чергування рішення про дію, її виконання та observation.
Не вимагаємо прихованої траси міркувань. Для T103 lookup_ticket поверне low, отже
get_sla має отримати low й повернути 72 години. Бюджети max_rounds і max_tools — різні:
одна відповідь моделі може запропонувати кілька tools. Перед виконанням усієї партії
перевіряємо, чи не буде перевищено загальну межу.
Якщо модель не завершила цикл, повертаємо явну помилку budget_exhausted. Не додаємо
нескінченних повторів або «успішного» fallback із вигаданим текстом. Помилки tools є
структурованими observation, помилки API — окремими діагностичними статусами.
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
    api = ClassroomAPI(max_calls=4)
    result = run_agent(api,"Перевір SLA заявки T103 через ticket і policy.",max_rounds=4,max_tools=4)
    show(api,{"result":result,"remaining_calls":api.max_calls-api.calls_used})

if __name__=="__main__":
    main()
