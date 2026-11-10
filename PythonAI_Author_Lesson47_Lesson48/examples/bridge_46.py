"""Після прикладу відкрийте tasks/bridge_46.py. Перевірте інформаційне питання, запит на чернетку та заборонену дію send_email. Покажіть answered / pending_approval / refused. Відкрийте artifacts/bridge_approval_UUID.json і перевірте sent=false; порівняйте run_id з bridge-подіями в artifacts/trace.jsonl.
20 хв. Критерій: Є два live workflow-запуски і одна локальна відмова до API. Чернетка збережена, sent=false. Жоден лист не надіслано. Названо, які stage/status зручно досліджувати далі у парі 47.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    from bridge_runtime import bridge46
    result=bridge46('Підготуй пояснення правил повернення.',action='draft_email')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
