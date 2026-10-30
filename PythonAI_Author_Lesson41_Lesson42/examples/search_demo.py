# file: search_demo.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = ['Розклад занять: субота 17:00',
        'Оплата товару здійснюється щомісяця',
        'Домашнє завдання потрібно здати до п’ятниці']
query = 'Коли потрібно здати домашнє завдання?'
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(docs)
q = vectorizer.transform([query])
scores = cosine_similarity(q, X).ravel()
for idx in scores.argsort()[::-1][:2]:
    print(idx, round(float(scores[idx]), 3), docs[idx])
