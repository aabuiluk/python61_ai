"""Викличте judge для двох відповідей: 14 і 30 календарних днів. Запишіть власну оцінку перед API, порівняйте relevant/supported і reason. Додайте суперечливий фрагмент тільки до локальної копії контексту.
Готово, якщо: Є власна оцінка й три реальні судження; відхилення judge від людини чесно зафіксовані.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Викличте judge для двох відповідей: 14 і 30 календарних днів. Запишіть власну оцінку перед API, порівняйте relevant/supported і reason. Додайте суперечливий фрагмент тільки до локальної копії контексту.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
