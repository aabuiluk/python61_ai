"""Запустіть build двічі, потім stats. Запишіть points і dimensions. Другий build має cached=true, а points не збільшується. У Docker dashboard відкрийте collection → points → payload; без Docker перегляньте payload через наступний search.
Готово, якщо: Кількість points стабільна; embedding етапів у trace під час cached build немає; база переживає закриття процесу.
"""
from pathlib import Path
import sys
REPOSITORY = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPOSITORY))
from PythonAI_Author_Lesson47_Lesson48.runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    with session() as rag:
        print(rag.index(read_documents()))
        print(rag.stats())

if __name__=="__main__":
    main()
