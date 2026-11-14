"""Створіть одну чернетку в UI, знайдіть approval-файл і sent=false. Запустіть eval. Для одного невдалого або складного кейсу знайдіть trace та PDF і поясніть причину. За бажанням порівняйте judge.
Готово, якщо: Чернетка з sent=false; eval_report має 8 кейсів та посилання run_id; висновок не приховує помилок.
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
    question=None  # TODO: запит на підготовку чернетки про повернення
    if not question:
        raise NotImplementedError('Заповніть question')
    with session() as rag:
        # TODO: ask із external_action=True; перевірте approval-файл і sent
        # TODO: evaluate базових кейсів і ручний розбір одного результату
        pass

if __name__=="__main__":
    main()
