"""Microsoft Agent Framework + OpenAI: наступник AutoGen і Semantic Kernel.

Встановлення: python -m pip install -r PythonAI_Author_Lesson43_Lesson44/frameworks/requirements-agent-framework.txt
Запуск з кореня репозиторію: python -m PythonAI_Author_Lesson43_Lesson44.frameworks.agent_framework_demo
"""
import asyncio
import json
from PythonAI_Author_Lesson43_Lesson44.workshop import DOCS, retrieve, validate_answer
from PythonAI_Author_Lesson43_Lesson44.live_openai import EMBEDDING_MODEL, MODEL, require_key

require_key()  # читає OPENAI_API_KEY з .env; без ключа скрипт завершується

from agent_framework.openai import OpenAIChatClient


def search_knowledge(question: str) -> str:
    """Пошук у правилах магазину. Повертає фрагменти з id."""
    return json.dumps(retrieve(question, 1), ensure_ascii=False)


async def main():
    agent = OpenAIChatClient(model=MODEL).as_agent(
        name="ShopAssistant",
        instructions="Ви консультант магазину. Відповідайте лише за результатами search_knowledge.",
        tools=[search_knowledge])
    result = await agent.run("Скільки коштує доставка Україною?")
    print("Відповідь:", result.text)


asyncio.run(main())
