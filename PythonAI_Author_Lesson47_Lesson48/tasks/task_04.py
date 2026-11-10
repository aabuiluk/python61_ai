"""Додайте два власні кейси у копію набору: точне питання про ціну S300 та питання про невідому експрес-доставку. До запуску визначте expected_status і expected_files. Перевірте у PDF.
Готово, якщо: Є 10 кейсів, очікувана ціна S300=690 грн, для експрес-доставки — refused. Новий набір окремо від базового.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Додайте два власні кейси у копію набору: точне питання про ціну S300 та питання про невідому експрес-доставку. До запуску визначте expected_status і expected_files. Перевірте у PDF.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
