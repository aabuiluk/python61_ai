"""LangChain + OpenAI: ланцюжок prompt | model | parser і виклик інструмента.

Встановлення: python -m pip install -r frameworks/requirements-langchain.txt
Запуск з папки пакета: python frameworks/langchain_demo.py
"""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import DOCS, retrieve, validate_answer
from live_openai import MODEL, EMBEDDING_MODEL, require_key

require_key()  # читає OPENAI_API_KEY з .env; без ключа скрипт завершується

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=MODEL, temperature=0)

# 1. Ланцюжок: той самий DocFlow, але model-вузол — готовий конектор ChatOpenAI
prompt = ChatPromptTemplate.from_messages([
    ("system", "Працюйте лише за контекстом. Поверніть answer та sources у JSON."),
    ("human", "<context>{context}</context>\nПитання: {question}")])
chain = prompt | llm.bind(response_format={"type": "json_object"}) | JsonOutputParser()
question = "Доставка Україною"
context = json.dumps(retrieve(question), ensure_ascii=False)
print("Ланцюжок:", chain.invoke({"context": context, "question": question}))


# 2. Інструмент: модель лише просить виклик, виконує його наш код
@tool
def search_knowledge(question: str) -> str:
    """Пошук у правилах магазину. Повертає фрагменти з id."""
    return json.dumps(retrieve(question, 1), ensure_ascii=False)


llm_with_tools = llm.bind_tools([search_knowledge])
messages = [HumanMessage("Коли працює магазин? Шукай у правилах.")]
reply = llm_with_tools.invoke(messages)
messages.append(reply)
for call in reply.tool_calls:
    print("Модель просить:", call["name"], call["args"])
    messages.append(ToolMessage(search_knowledge.invoke(call["args"]), tool_call_id=call["id"]))
if reply.tool_calls:
    reply = llm_with_tools.invoke(messages)
print("Відповідь:", reply.content)
