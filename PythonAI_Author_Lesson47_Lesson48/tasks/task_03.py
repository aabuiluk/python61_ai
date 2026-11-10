"""Створіть таблицю по stage: кількість, середня duration_ms, кількість status=error. Окремо порівняйте дві фрази з запереченням і поясніть, чому overlap не перевіряє факт.
Готово, якщо: Таблиця не змішує різні етапи; приклад overlap=0.75 не названий faithfulness.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Створіть таблицю по stage: кількість, середня duration_ms, кількість status=error. Окремо порівняйте дві фрази з запереченням і поясніть, чому overlap не перевіряє факт.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
