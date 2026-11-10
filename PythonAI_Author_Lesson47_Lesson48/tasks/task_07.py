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
    chunk_sizes=None  # TODO: два розміри з умови
    if not chunk_sizes:
        raise NotImplementedError('Заповніть chunk_sizes')
    for size in chunk_sizes:
        docs=read_documents(chunk_size=size,overlap=120)
        # TODO: перевірте 10 файлів, page, text і джерело числа 7

if __name__=="__main__":
    main()
