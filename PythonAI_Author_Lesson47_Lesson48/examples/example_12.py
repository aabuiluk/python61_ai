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
    print('package:',PACKAGE)
    print('PDF:',len(list((PACKAGE/'data/pdf').glob('*.pdf'))))
    print('trace:',(PACKAGE/'artifacts/trace.jsonl').exists())
    print('eval:',(PACKAGE/'artifacts/eval_report.json').exists())
    print('Не публікуйте .env або artifacts. Команда UI — у README.')

if __name__=="__main__":
    main()
