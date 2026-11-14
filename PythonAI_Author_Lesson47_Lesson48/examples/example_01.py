"""Виконайте три реальні запити до того самого контексту: строк повернення, вартість ноутбука та неоднозначне «А якщо пізніше?». Для кожного збережіть status і run_id у власну таблицю. Звірте факти з PDF.
Готово, якщо: Є три фактичні результати, правильне джерело для строку 14 календарних днів і пояснення відмови або неоднозначності.
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
    docs=[d for d in read_documents() if d['file']=='06_returns.pdf']
    with session() as rag:
        run_id=str(uuid.uuid4())
        print(rag.generate('Який строк повернення?',docs,run_id))
        print('run_id:',run_id)

if __name__=="__main__":
    main()
