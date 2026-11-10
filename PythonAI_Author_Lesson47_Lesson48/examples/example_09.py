"""Порівняйте top-k=1 і 4 для ціни L100. Потім застосуйте source=07_warranty.pdf. Випишіть, де є ціна 850 грн, а де її немає. Перевірте назву файлу кожного hit.
Готово, якщо: Є два набори retrieval, у filtered немає чужих PDF; висновок про ціну спирається на каталог.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    with session() as rag:
        hits=rag.search('Скільки ламп L100 є на складі?',top_k=3)
        for hit in hits:
            print(hit['source_id'],round(hit['score'],3),hit['text'])

if __name__=="__main__":
    main()
