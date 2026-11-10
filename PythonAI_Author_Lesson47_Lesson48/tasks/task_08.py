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
    # TODO: Запустіть build двічі, потім stats. Запишіть points і dimensions. Другий build має cached=true, а points не збільшується. У Docker dashboard відкрийте collection → points → payload; без Docker перегляньте payload через наступний search.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
