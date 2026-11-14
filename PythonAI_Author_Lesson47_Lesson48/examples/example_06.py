"""Складіть порівняння JSONL / LangSmith / Vertex Monitoring за чотирма ознаками: де зберігаються дані, які метрики бачимо, що потрібно налаштувати, чого інструмент не доводить. Необов’язково надішліть один очищений trace у LangSmith.
Готово, якщо: Відрізняєте чотири інтерфейси: файл trace, UI додатка, Qdrant dashboard і optional LangSmith.
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
    rows=[json.loads(x) for x in (PACKAGE/'artifacts/trace.jsonl').read_text(encoding='utf-8').splitlines()]
    print('runs:',len({r['run_id'] for r in rows}))
    print('stages:',sorted({r['stage'] for r in rows}))
    print('JSONL локально; dashboard Streamlit у парі 48; LangSmith — окрема необов’язкова інтеграція.')

if __name__=="__main__":
    main()
