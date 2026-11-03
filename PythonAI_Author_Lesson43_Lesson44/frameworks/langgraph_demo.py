"""LangGraph + OpenAI: явний граф станів retrieve → answer → validate з лімітом повторів.

Встановлення: python -m pip install -r frameworks/requirements-langgraph.txt
Запуск з папки пакета: python frameworks/langgraph_demo.py
"""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import DOCS, retrieve, validate_answer
from live_openai import MODEL, EMBEDDING_MODEL, require_key

require_key()  # читає OPENAI_API_KEY з .env; без ключа скрипт завершується

from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

llm = ChatOpenAI(model=MODEL, temperature=0).bind(response_format={"type": "json_object"})
MAX_ATTEMPTS = 2


class State(TypedDict, total=False):
    question: str
    docs: list
    answer: dict
    attempts: int
    valid: bool


def retrieve_node(state):
    return {"docs": retrieve(state["question"]), "attempts": 0}


def answer_node(state):
    context = json.dumps(state["docs"], ensure_ascii=False)
    message = llm.invoke([
        ("system", "Працюйте лише за контекстом. Поверніть JSON з ключами answer і sources (список id)."),
        ("human", f"<context>{context}</context>\nПитання: {state['question']}")])
    return {"answer": json.loads(message.content), "attempts": state["attempts"] + 1}


def validate_node(state):
    return {"valid": validate_answer(state["answer"], state["docs"])}


def route(state):
    # Рішення «повторити чи зупинитись» приймає програма, а не модель
    return END if state["valid"] or state["attempts"] >= MAX_ATTEMPTS else "answer"


graph = StateGraph(State)
graph.add_node("retrieve", retrieve_node)
graph.add_node("answer", answer_node)
graph.add_node("validate", validate_node)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "answer")
graph.add_edge("answer", "validate")
graph.add_conditional_edges("validate", route)
app = graph.compile()

for question in ["Самовивіз у Львові", "Марсіанський телепорт"]:
    state = app.invoke({"question": question})
    print(f"{question} → {state['answer']} | valid={state['valid']} | спроб: {state['attempts']}")
