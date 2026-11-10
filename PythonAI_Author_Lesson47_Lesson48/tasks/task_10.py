"""У Streamlit запитайте про доставку (90 грн; безкоштовно від 3000), потім про ноутбук X999. Через CLI виконайте ask із --source does_not_exist.pdf. Порівняйте generate у trace для hit та порожнього retrieval.
Готово, якщо: У UI видно джерела доставки; miss не має generate з тим самим run_id; невідомий товар не отримав вигаданої ціни або чесно позначений як fail.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: У Streamlit запитайте про доставку (90 грн; безкоштовно від 3000), потім про ноутбук X999. Через CLI виконайте ask із --source does_not_exist.pdf. Порівняйте generate у trace для hit та порожнього retrieval.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
