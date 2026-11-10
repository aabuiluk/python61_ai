"""Створіть таблицю по stage: кількість, середня duration_ms, кількість status=error. Окремо порівняйте дві фрази з запереченням і поясніть, чому overlap не перевіряє факт.
Готово, якщо: Таблиця не змішує різні етапи; приклад overlap=0.75 не названий faithfulness.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    trace=PACKAGE/'artifacts/trace.jsonl'
    rows=[json.loads(x) for x in trace.read_text(encoding='utf-8').splitlines()]
    for stage in sorted({r['stage'] for r in rows}):
        selected=[r for r in rows if r['stage']==stage]
        print(stage,len(selected),round(sum(r['duration_ms'] for r in selected)/len(selected),2))

if __name__=="__main__":
    main()
