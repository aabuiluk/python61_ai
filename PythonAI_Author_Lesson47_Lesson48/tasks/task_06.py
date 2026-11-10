"""Складіть порівняння JSONL / LangSmith / Vertex Monitoring за чотирма ознаками: де зберігаються дані, які метрики бачимо, що потрібно налаштувати, чого інструмент не доводить. Необов’язково надішліть один очищений trace у LangSmith.
Готово, якщо: Відрізняєте чотири інтерфейси: файл trace, UI додатка, Qdrant dashboard і optional LangSmith.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    comparison={}
    # TODO: JSONL / LangSmith / Vertex Monitoring, чотири ознаки за умовою
    if len(comparison)!=3:
        raise NotImplementedError('Заповніть порівняння трьох інструментів')
    print(json.dumps(comparison,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
