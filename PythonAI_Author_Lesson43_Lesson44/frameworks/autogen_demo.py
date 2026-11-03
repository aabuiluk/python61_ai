"""AutoGen (AgentChat) + OpenAI: агент з інструментом відповідає на питання.

Встановлення: python -m pip install -r frameworks/requirements-autogen.txt
Запуск з папки пакета: python frameworks/autogen_demo.py
Нові проєкти Microsoft радить будувати на Agent Framework: див. agent_framework_demo.py.
"""
import asyncio
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import DOCS, retrieve, validate_answer
from live_openai import MODEL, EMBEDDING_MODEL, require_key

require_key()  # читає OPENAI_API_KEY з .env; без ключа скрипт завершується

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


def search_knowledge(question: str) -> str:
    """Пошук у правилах магазину. Повертає фрагменти з id."""
    return json.dumps(retrieve(question, 1), ensure_ascii=False)


async def main():
    model_client = OpenAIChatCompletionClient(model=MODEL, temperature=0)
    agent = AssistantAgent("shop_assistant", model_client=model_client, tools=[search_knowledge],
                           system_message="Ви консультант магазину. Відповідайте лише за результатами search_knowledge.",
                           reflect_on_tool_use=True)
    result = await agent.run(task="Скільки коштує доставка Україною?")
    for message in result.messages:
        print(f"{type(message).__name__}: {message.content}")
    await model_client.close()


asyncio.run(main())
