"""LlamaIndex + OpenAI: індекс документів, embeddings і відповідь з джерелами.

Встановлення: python -m pip install -r PythonAI_Author_Lesson43_Lesson44/frameworks/requirements-llamaindex.txt
Запуск з кореня репозиторію: python -m PythonAI_Author_Lesson43_Lesson44.frameworks.llamaindex_demo
"""
import json
from PythonAI_Author_Lesson43_Lesson44.workshop import DOCS, retrieve, validate_answer
from PythonAI_Author_Lesson43_Lesson44.live_openai import EMBEDDING_MODEL, MODEL, require_key

require_key()  # читає OPENAI_API_KEY з .env; без ключа скрипт завершується

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

Settings.llm = OpenAI(model=MODEL, temperature=0)
Settings.embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL)

# Ті самі три правила магазину стають документами з id у метаданих
documents = [Document(text=d["text"], doc_id=d["id"], metadata={"id": d["id"]}) for d in DOCS]
index = VectorStoreIndex.from_documents(documents)  # embeddings рахуються тут
engine = index.as_query_engine(similarity_top_k=1)

for question in ["Скільки треба платити, щоб посилку привезли в інше місто?", "Коли працює магазин?"]:
    response = engine.query(question)
    sources = [(n.node.metadata["id"], round(n.score or 0, 3)) for n in response.source_nodes]
    print(question)
    print("  відповідь:", str(response).strip())
    print("  джерела:  ", sources)
