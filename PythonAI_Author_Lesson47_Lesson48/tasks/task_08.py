"""Запустіть build двічі, потім stats. Запишіть points і dimensions. Другий build має cached=true, а points не збільшується. У Docker dashboard відкрийте collection → points → payload; без Docker перегляньте payload через наступний search.
Готово, якщо: Кількість points стабільна; embedding етапів у trace під час cached build немає; база переживає закриття процесу.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    docs=read_documents()
    confirm_live=False  # TODO: після конфігурації .env погодьте один build
    if not confirm_live:
        raise NotImplementedError('Підготуйте .env та встановіть confirm_live=True')
    with session() as rag:
        # TODO: два build, порівняння points і cached; перегляд trace
        pass

if __name__=="__main__":
    main()
