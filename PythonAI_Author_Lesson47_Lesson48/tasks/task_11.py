"""Створіть одну чернетку в UI, знайдіть approval-файл і sent=false. Запустіть eval. Для одного невдалого або складного кейсу знайдіть trace та PDF і поясніть причину. За бажанням порівняйте judge.
Готово, якщо: Чернетка з sent=false; eval_report має 8 кейсів та посилання run_id; висновок не приховує помилок.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Створіть одну чернетку в UI, знайдіть approval-файл і sent=false. Запустіть eval. Для одного невдалого або складного кейсу знайдіть trace та PDF і поясніть причину. За бажанням порівняйте judge.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
