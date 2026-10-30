# file: rag_live.py
import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Вигадані навчальні дані українського магазину. Це не реальні тарифи.
chunks = [
    {"id": "DOC-1", "text": "Магазин працює з понеділка до суботи з 09:00 до 19:00."},
    {"id": "DOC-2", "text": "Самовивіз замовлень доступний у Києві на вулиці Хрещатик, 10."},
    {"id": "DOC-3", "text": "Повернення товару належної якості можливе протягом 14 днів за умов законодавства України."},
    {"id": "DOC-4", "text": "Підтримка покупців відповідає на запити в робочі години магазину."},
]

vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
matrix = vectorizer.fit_transform([c["text"] for c in chunks])

def retrieve(question: str, k: int = 2):
    query_vector = vectorizer.transform([question])
    similarities = cosine_similarity(query_vector, matrix)[0]
    indices = np.argsort(similarities)[::-1][:k]
    return [chunks[int(i)] | {"score": float(similarities[i])}
            for i in indices if similarities[i] > 0]

def rag_answer(question: str):
    matches = retrieve(question)
    if not matches:
        return "Немає релевантних джерел.", []
    context = "\n".join(f'[{m["id"]}] {m["text"]}' for m in matches)
    response = client.responses.create(
        model=MODEL,
        instructions=("Відповідай українською ТІЛЬКИ за фрагментами. "
                      "Для кожного факту зазначай [DOC-ID]. Якщо даних немає, "
                      "напиши 'Немає даних у джерелах'. Не вигадуй факти."),
        input=f"ДЖЕРЕЛА:\n{context}\n\nПИТАННЯ: {question}",
        max_output_tokens=250,
    )
    return response.output_text, matches

if __name__ == "__main__":
    answer, matches = rag_answer("Коли працює магазин?")
    print("Відповідь:", answer)
    print("Знайдені джерела:", matches)

