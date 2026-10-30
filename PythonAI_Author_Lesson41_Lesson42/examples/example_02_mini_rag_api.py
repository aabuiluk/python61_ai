"""Розібраний навчальний приклад; API викликається тільки при запуску."""
import sys
from pathlib import Path
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))
from api_client import send

def run():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    documents = [
        {'id': 'hours', 'text': 'Бібліотека відкрита з 09:00 до 18:00.'},
        {'id': 'ticket', 'text': 'Читацький квиток бібліотеки коштує 20 гривень.'}]
    question = 'Скільки коштує читацький квиток?'
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([d['text'] for d in documents])
    scores = cosine_similarity(vectorizer.transform([question]), matrix)[0]
    selected = [documents[i] for i in scores.argsort()[::-1][:1] if scores[i] > 0]
    if not selected:
        print('Немає даних у джерелі')
        return None
    import json
    response = send({'instructions': 'Відповідай лише за контекстом і вкажи ID документа.',
                     'input': json.dumps({'question': question, 'context': selected}, ensure_ascii=False)})
    print('retrieved:', [d['id'] for d in selected])
    print(response.output_text)
    print('status:', response.status, 'usage:', response.usage)
    return response

if __name__ == "__main__":
    run()
