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
    docs=read_documents()
    print('PDF:',len({d['file'] for d in docs}),'chunks:',len(docs))
    stock=[d for d in docs if d['file']=='03_stock.pdf']
    print(stock[0]['source_id'],stock[0]['text'])

if __name__=="__main__":
    main()
