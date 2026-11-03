"""**Завдання 1.** Перепишіть питання про самовивіз без слів «самовивіз» і «Львів». Порівняйте TF-IDF і embeddings. Потім додайте поріг: результати зі score нижче `threshold` не повертаються.

Підказки:
1. Почніть з `examples/live_01.py` — код майже такий самий.
2. Поріг — це один рядок: залиште в `scored` тільки пари, де `score >= threshold`.
3. Якщо телепорт усе ще знаходиться, підніміть поріг (0.3 → 0.35 → 0.4).

Готово, якщо: TF-IDF не знаходить `pickup_lviv`, embeddings знаходять. «Марсіанський телепорт» з вашим порогом дає `[]`.

Подивіться examples/live_01.py — там той самий код без TODO. Потрібен OPENAI_API_KEY (див. README.md).
"""
from PythonAI_Author_Lesson43_Lesson44.live_openai import embed, print_usage, require_key
from PythonAI_Author_Lesson43_Lesson44.workshop import DOCS, retrieve

require_key()

# %% Ваш код: допишіть місця TODO
import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

def embed_retrieve(question, k=1, threshold=0.0):
    doc_vectors = embed([d["text"] for d in DOCS])
    [q] = embed([question])
    scored = sorted(((cosine(q, v), d["id"]) for v, d in zip(doc_vectors, DOCS)), reverse=True)
    # TODO 2: залиште в scored тільки пари, де score >= threshold
    return [{"id": doc_id, "score": round(score, 3)} for score, doc_id in scored[:k]]

question = "Скільки коштує самовивіз у Львові?"  # TODO 1: перепишіть без слів «самовивіз» і «Львів»
print("TF-IDF:    ", retrieve(question, k=1))
print("Embeddings:", embed_retrieve(question, threshold=0.3))
print("Телепорт:  ", embed_retrieve("Марсіанський телепорт", threshold=0.3))
print_usage()
