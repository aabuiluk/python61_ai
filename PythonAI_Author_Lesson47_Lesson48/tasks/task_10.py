"""У Streamlit запитайте про доставку (90 грн; безкоштовно від 3000), потім про ноутбук X999. Через CLI виконайте ask із --source does_not_exist.pdf. Порівняйте generate у trace для hit та порожнього retrieval.
Готово, якщо: У UI видно джерела доставки; miss не має generate з тим самим run_id; невідомий товар не отримав вигаданої ціни або чесно позначений як fail.
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
    questions=None  # TODO: доставка та невідомий ноутбук
    if not questions:
        raise NotImplementedError('Заповніть questions')
    with session() as rag:
        # TODO: live ask для обох питань, перевірка sources/status/run_id
        # TODO: детермінований miss із неіснуючим source-файлом
        pass

if __name__=="__main__":
    main()
