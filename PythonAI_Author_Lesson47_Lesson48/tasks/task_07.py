"""Запустіть inspect з кореня. Відкрийте 03_stock.pdf і знайдіть 7 L100. Порівняйте кількість chunks при chunk_size=500 та 850. Перевірте page і непорожній text для всіх фрагментів.
Готово, якщо: Знайдено рівно 10 PDF, кількість chunks пояснена, 7 одиниць перевірено у видимому джерелі.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime import PACKAGE, session, read_documents, validate_answer
import json
import time
import uuid

def main():
    # TODO: Запустіть inspect з кореня. Відкрийте 03_stock.pdf і знайдіть 7 L100. Порівняйте кількість chunks при chunk_size=500 та 850. Перевірте page і непорожній text для всіх фрагментів.
    raise NotImplementedError("Виконайте завдання; підказки у відповідному .md")

if __name__=="__main__":
    main()
