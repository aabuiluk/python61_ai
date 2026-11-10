"""Після блоку 1 відкрийте trace.jsonl в IDE. Знайдіть один run_id і його generate. Напишіть перевірку, що кожен рядок має run_id/stage/status, а API-ключ відсутній. Додайте підрахунок токенів.
Готово, якщо: Кожен рядок розбирається як JSON; ключів і текстів питань немає; usage підсумовано без подвійного рахунку result.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Після блоку 1 відкрийте trace.jsonl в IDE. Знайдіть один run_id і його generate. Напишіть перевірку, що кожен рядок має run_id/stage/status, а API-ключ відсутній. Додайте підрахунок токенів.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
