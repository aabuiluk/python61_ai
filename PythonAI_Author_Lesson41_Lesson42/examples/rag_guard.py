# file: rag_guard.py
from PythonAI_Author_Lesson41_Lesson42.examples.rag_live import retrieve

def retrieve_checked(question: str, k: int = 3):
    hits = retrieve(question, k)  # звірте сигнатуру з rag_live.py
    print('Знайдені фрагменти:', hits)
    return hits

# Для продуктивної системи додайте:
# - мінімальний поріг схожості;
# - контроль довжини контексту;
# - перевірку ID цитат;
# - обмеження кількості запитів.
