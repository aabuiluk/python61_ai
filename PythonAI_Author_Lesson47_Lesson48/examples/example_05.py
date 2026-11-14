"""Викличте judge для двох відповідей: 14 і 30 календарних днів. Запишіть власну оцінку перед API, порівняйте relevant/supported і reason. Додайте суперечливий фрагмент тільки до локальної копії контексту.
Готово, якщо: Є власна оцінка й три реальні судження; відхилення judge від людини чесно зафіксовані.
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
        print(rag.judge('Який строк повернення?',docs,'Зверніться протягом 14 календарних днів від отримання.'))

if __name__=="__main__":
    main()
