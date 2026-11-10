"""Запустіть UI з кореня, покажіть hit/miss, джерело зі сторінкою, trace і pending_approval. Закрийте UI, виконайте stats та переконайтеся, що індекс зберігся. Підготуйте README зі своїм середовищем і таблицею результатів.
Готово, якщо: README відтворює запуск з кореня, результати перевірені за джерелами, секретів у здачі немає.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    report_file=PACKAGE/'artifacts/eval_report.json'
    report=json.loads(report_file.read_text(encoding='utf-8'))
    expected_cases=None  # TODO: кількість базових кейсів
    if expected_cases is None:
        raise NotImplementedError('Вкажіть expected_cases')
    # TODO: кількість PDF, trace, eval cases, збереження індексу
    # TODO: README з фактичними результатами live-перевірки

if __name__=="__main__":
    main()
