# file: rag_guard.py
from rag_live import retrieve

def retrieve_checked(question: str, k: int = 3):
    hits = retrieve(question, k)  # звірте сигнатуру з rag_live.py
    print('Знайдені фрагменти:', hits)
    return hits

# Для продуктивної системи додайте:
# - мінімальний поріг схожості;
# - контроль довжини контексту;
# - перевірку ID цитат;
# - обмеження кількості запитів.
