"""Порівняйте top-k=1 і 4 для ціни L100. Потім застосуйте source=07_warranty.pdf. Випишіть, де є ціна 850 грн, а де її немає. Перевірте назву файлу кожного hit.
Готово, якщо: Є два набори retrieval, у filtered немає чужих PDF; висновок про ціну спирається на каталог.
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
    question=None  # TODO: питання про ціну L100
    if not question:
        raise NotImplementedError('Заповніть question')
    with session() as rag:
        # TODO: top-k 1 і 4, потім file-фільтр на гарантію
        pass

if __name__=="__main__":
    main()
