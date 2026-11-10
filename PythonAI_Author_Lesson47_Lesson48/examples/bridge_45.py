"""Після прикладу відкрийте tasks/bridge_45.py. Зробіть реальний запит про повернення й окремий — про доставку. Для кожного покажіть tool name/topic, call_id, джерела та відповідь. Локально перевірте відхилення невідомого tool і зайвого JSON-поля; негативні перевірки не повинні викликати API.
20 хв. Критерій: У терміналі є два справжні результати: повернення — 14 календарних днів, стандартна доставка — 90 грн / безкоштовно від 3000 грн. Джерела перевірені у 06_returns.pdf та 04_delivery.pdf. Два некоректні виклики відхилено Python-кодом.
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
    from PythonAI_Author_Lesson47_Lesson48.bridge_runtime import bridge45
    result=bridge45('Який строк повернення невикористаного товару?')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
