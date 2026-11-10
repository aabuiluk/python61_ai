"""Виконайте три реальні запити до того самого контексту: строк повернення, вартість ноутбука та неоднозначне «А якщо пізніше?». Для кожного збережіть status і run_id у власну таблицю. Звірте факти з PDF.
Готово, якщо: Є три фактичні результати, правильне джерело для строку 14 календарних днів і пояснення відмови або неоднозначності.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Виконайте три реальні запити до того самого контексту: строк повернення, вартість ноутбука та неоднозначне «А якщо пізніше?». Для кожного збережіть status і run_id у власну таблицю. Звірте факти з PDF.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
