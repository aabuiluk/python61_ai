# file: agent_live.py
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from rag_live import retrieve

load_dotenv()
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Демонстраційний каталог українського магазину, ціни в гривнях.
PRODUCTS = {"lamp": {"name": "Настільна лампа", "price_uah": 850, "stock": 7},
            "chair": {"name": "Офісний стілець", "price_uah": 3200, "stock": 3}}

def get_product_info(product: str) -> dict:
    return PRODUCTS.get(product.lower(), {"error": "Товар не знайдено"})

def search_knowledge(query: str) -> dict:
    return {"matches": retrieve(query, k=3)}

TOOLS = [
    {"type": "function", "function": {
        "name": "get_product_info",
        "description": "Знайти ціну у гривнях і залишок товару за кодом lamp або chair",
        "parameters": {"type": "object", "properties": {
            "product": {"type": "string", "enum": ["lamp", "chair"]}},
            "required": ["product"], "additionalProperties": False}}},
    {"type": "function", "function": {
        "name": "search_knowledge",
        "description": "Знайти інформацію у правилах українського магазину",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string"}},
            "required": ["query"], "additionalProperties": False}}},
]
FUNCTIONS = {"get_product_info": get_product_info,
             "search_knowledge": search_knowledge}

def run_agent(question: str, max_steps: int = 4) -> str:
    messages = [
        {"role": "system", "content": (
            "Ти консультант українського магазину. Факти отримуй через інструменти. "
            "Не вигадуй ціни, залишки, години роботи чи джерела.")},
        {"role": "user", "content": question},
    ]
    for _ in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS,
            tool_choice="auto", temperature=0,
        )
        msg = response.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content or "Модель повернула порожню відповідь"
        for call in msg.tool_calls:
            name = call.function.name
            if name not in FUNCTIONS:
                result = {"error": "Невідомий інструмент"}
            else:
                try:
                    args = json.loads(call.function.arguments)
                    if not isinstance(args, dict):
                        raise ValueError("Аргументи повинні бути об'єктом")
                    if name == "get_product_info":
                        if set(args) != {"product"} or args["product"] not in PRODUCTS:
                            raise ValueError("Недопустимий код товару")
                    elif name == "search_knowledge":
                        if set(args) != {"query"} or not isinstance(args["query"], str) or len(args["query"]) > 500:
                            raise ValueError("Недопустимий запит")
                    result = FUNCTIONS[name](**args)
                except (ValueError, TypeError) as exc:
                    result = {"error": str(exc)}
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(result, ensure_ascii=False)})
    return "Досягнуто ліміту кроків агента"

if __name__ == "__main__":
    print(run_agent("Скільки коштує настільна лампа?"))
    print(run_agent("Коли працює магазин?"))

