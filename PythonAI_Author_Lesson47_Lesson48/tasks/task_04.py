"""Додайте два власні кейси у копію набору: точне питання про ціну S300 та питання про невідому експрес-доставку. До запуску визначте expected_status і expected_files. Перевірте у PDF.
Готово, якщо: Є 10 кейсів, очікувана ціна S300=690 грн, для експрес-доставки — refused. Новий набір окремо від базового.
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
    cases=json.loads((PACKAGE/'data/eval_cases.json').read_text(encoding='utf-8'))
    new_cases=[]  # TODO: ціна S300 та експрес-доставка, з очікуваннями
    if len(new_cases)!=2:
        raise NotImplementedError('Додайте два власні кейси')
    # TODO: запишіть окремий artifacts/my_cases.json; не змінюйте базовий набір

if __name__=="__main__":
    main()
