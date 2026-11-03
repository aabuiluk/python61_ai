"""Semantic Kernel + OpenAI: агент з плагіном, функцію якого модель викликає сама.

Semantic Kernel поки не встановлюється на Python 3.14. Потрібне окреме середовище 3.10–3.13,
див. frameworks/README.md (розділ про .venv-312).
"""
import asyncio
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import DOCS, retrieve, validate_answer
from live_openai import MODEL, EMBEDDING_MODEL, require_key

require_key()  # читає OPENAI_API_KEY з .env; без ключа скрипт завершується

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function


class ShopPlugin:
    @kernel_function(description="Пошук у правилах магазину. Повертає фрагменти з id.")
    def search_knowledge(self, question: str) -> str:
        return json.dumps(retrieve(question, 1), ensure_ascii=False)


async def main():
    agent = ChatCompletionAgent(service=OpenAIChatCompletion(ai_model_id=MODEL), name="ShopAssistant",
                                instructions="Ви консультант магазину. Відповідайте лише за результатами search_knowledge.",
                                plugins=[ShopPlugin()])
    response = await agent.get_response(messages="Скільки коштує доставка Україною?")
    print("Відповідь:", response.content)


asyncio.run(main())
