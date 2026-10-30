# file: prompt_lab.py
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

def ask(instructions, question):
    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=question,
        max_output_tokens=250,
    )
    return response.output_text, response.usage

message = "Магазин дорогий, але викладач пояснює дуже добре"
zero, usage_zero = ask(
    "Визнач тональність: Positive, Negative або Mixed. Поверни лише одну мітку.",
    message,
)
few, usage_few = ask(
    "Визнач тональність: Positive, Negative або Mixed. "
    "Приклади: 'дуже добре' → Positive; 'надто дорого' → Negative; "
    "'дорого, але якісно' → Mixed. Поверни лише мітку.",
    message,
)
print("Zero-shot:", zero, usage_zero)
print("Few-shot:", few, usage_few)
