import json
import csv
from pathlib import Path
CATALOG = [
    {"id": "b01", "title": "Python старт", "price": 320, "topic": "python"},
    {"id": "b02", "title": "Практика Python", "price": 450, "topic": "python"},
    {"id": "b03", "title": "Основи даних", "price": 390, "topic": "data"},
]
SOURCE = "[S1] Книга b01 коштує 320 грн. [S2] Повернення можливе протягом 14 днів."
def validate(raw):
    try:
        obj = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return False
    if not isinstance(obj, dict) or set(obj) != {"book_id", "price"}:
        return False
    return any(obj["book_id"] == b["id"] and type(obj["price"]) is int
               and obj["price"] == b["price"] for b in CATALOG)
def chunks(text, size=12, overlap=3):
    if type(size) is not int or type(overlap) is not int or not 0 <= overlap < size:
        raise ValueError("Потрібно: size > overlap >= 0")
    words = text.split()
    result = []
    start = 0
    while start < len(words):
        result.append(" ".join(words[start:start+size]))
        if start+size >= len(words):
            break
        start += size-overlap
    return result
