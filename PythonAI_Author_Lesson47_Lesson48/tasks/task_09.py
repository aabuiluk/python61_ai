"""Порівняйте top-k=1 і 4 для ціни L100. Потім застосуйте source=07_warranty.pdf. Випишіть, де є ціна 850 грн, а де її немає. Перевірте назву файлу кожного hit.
Готово, якщо: Є два набори retrieval, у filtered немає чужих PDF; висновок про ціну спирається на каталог.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Порівняйте top-k=1 і 4 для ціни L100. Потім застосуйте source=07_warranty.pdf. Випишіть, де є ціна 850 грн, а де її немає. Перевірте назву файлу кожного hit.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
