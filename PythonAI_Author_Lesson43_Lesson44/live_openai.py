"""Необов'язковий live-режим: справжня модель OpenAI замість fixture_model.

Обов'язкова частина практикуму працює без мережі. Цей модуль потрібен лише для
кроків «Альтернатива з OPENAI_API_KEY». Ключ шукаємо в змінній середовища або в .env
поруч із пакетом 43–44 чи 41–42 (той самий ключ, що й на 41–42).
"""
import json
import os
from pathlib import Path

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

try:  # у скриптах беремо спільні функції з workshop.py; у ноутбуці вони вже визначені
    from PythonAI_Author_Lesson43_Lesson44.workshop import context_for, DOCS, retrieve
except ImportError:
    pass

MODEL = "gpt-4.1-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
USAGE = []  # журнал токенів усіх live-викликів цього процесу

try:
    _HERE = Path(__file__).resolve().parent
except NameError:  # Jupyter: __file__ немає
    _HERE = Path.cwd()
_ENV_CANDIDATES = [
    _HERE / ".env",
    _HERE / "PythonAI_Author_Lesson43_Lesson44" / ".env",
    _HERE.parent / "PythonAI_Author_Lesson41_Lesson42" / ".env",
    _HERE / "PythonAI_Author_Lesson41_Lesson42" / ".env",
    _HERE.parent / ".env",
]
_client = None


def _load_env():
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    for path in _ENV_CANDIDATES:
        if path.is_file():
            load_dotenv(path, override=False)


_load_env()
MODEL = os.getenv("OPENAI_MODEL", MODEL)
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", EMBEDDING_MODEL)


def live_ready():
    """True, якщо є ключ і встановлено пакет openai. Інакше пояснює, чого бракує."""
    _load_env()
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key or key == "replace-with-your-own-api-key":
        print("OPENAI_API_KEY не знайдено — live-крок пропущено. Офлайн-версія вже показала контракт.")
        return False
    try:
        import openai  # noqa: F401
    except ImportError:
        print("Пакет openai не встановлено: python -m pip install -r requirements-live.txt")
        return False
    return True


def require_key():
    """Для скриптів: без ключа спокійно завершуємо роботу з кодом 0."""
    if not live_ready():
        raise SystemExit(0)


def client():
    global _client
    if _client is None:
        from openai import OpenAI
        _client = OpenAI(timeout=30, max_retries=0)
    return _client


_ROLES = {"system": "system", "human": "user", "ai": "assistant"}


def to_input(value):
    """PromptValue / список повідомлень / рядок → input для Responses API."""
    if isinstance(value, str):
        return [{"role": "user", "content": value}]
    messages = value.to_messages() if hasattr(value, "to_messages") else value
    if isinstance(messages, BaseMessage):
        messages = [messages]
    return [{"role": _ROLES.get(m.type, "user"), "content": m.content} for m in messages]


def record_usage(response):
    usage = response.usage
    item = {"model": response.model,
            "input_tokens": usage.input_tokens if usage else None,
            "output_tokens": usage.output_tokens if usage else None}
    USAGE.append(item)
    return item


def call_model(value, json_mode=False, max_output_tokens=300):
    """Один виклик моделі. Повертає AIMessage, як і fixture_model."""
    extra = {"text": {"format": {"type": "json_object"}}} if json_mode else {}
    if MODEL.startswith("gpt-4"):  # reasoning-моделі не приймають temperature
        extra["temperature"] = 0
    response = client().responses.create(model=MODEL, input=to_input(value), store=False,
                                         max_output_tokens=max_output_tokens, **extra)
    usage = record_usage(response)
    return AIMessage(content=response.output_text, response_metadata=usage)


# Ті самі ролі, що й fixture_model: на вході PromptValue, на виході AIMessage.
live_model = RunnableLambda(call_model)
live_json_model = RunnableLambda(lambda value: call_model(value, json_mode=True))


def chain_with(model):
    """Той самий DocFlow-ланцюжок, що й make_chain(), але з довільним model-вузлом."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Працюйте лише за контекстом. Поверніть answer та sources у JSON."),
        ("human", "<context>{context}</context>\nПитання: {question}"),
    ])
    return ({"context": RunnableLambda(context_for), "question": RunnablePassthrough()}
            | prompt | model | JsonOutputParser())


def embed(texts):
    """Список рядків → список векторів (семантичні embeddings OpenAI)."""
    response = client().embeddings.create(model=EMBEDDING_MODEL, input=list(texts))
    USAGE.append({"model": response.model, "input_tokens": response.usage.prompt_tokens,
                  "output_tokens": 0})
    return [item.embedding for item in response.data]


def print_usage(title="Токени live-викликів"):
    total_in = sum(u["input_tokens"] or 0 for u in USAGE)
    total_out = sum(u["output_tokens"] or 0 for u in USAGE)
    print(f"{title}: викликів {len(USAGE)}, input {total_in}, output {total_out}")


def safe_parse(text):
    """JSON-текст моделі → об'єкт або None, без мовчазного «виправлення»."""
    try:
        return json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return None
