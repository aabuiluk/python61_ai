"""Блок 1 · альтернатива з OPENAI_API_KEY (необов'язково).

TF-IDF шукає однакові слова. Embeddings порівнюють зміст. Перевірте питання, у якому немає слова «доставка».

Офлайн-версія: examples/example_01.py. Без ключа скрипт друкує «пропущено».
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workshop import *
from live_openai import *

require_key()

import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

def embed_retrieve(question, k=2):
    doc_vectors = embed([d["text"] for d in DOCS])
    [q] = embed([question])
    scored = sorted(((cosine(q, v), d["id"]) for v, d in zip(doc_vectors, DOCS)), reverse=True)
    return [{"id": doc_id, "score": round(score, 3)} for score, doc_id in scored[:k]]

question = "Скільки треба платити, щоб посилку привезли в інше місто?"
print("TF-IDF:    ", retrieve(question, k=2))
print("Embeddings:", embed_retrieve(question))
print("Марсіанський телепорт:", embed_retrieve("Марсіанський телепорт", k=1))
print_usage()
