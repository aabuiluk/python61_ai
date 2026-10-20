"""Локальні навчальні дані й допоміжні функції рекомендацій."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Навчальний каталог: назви відомі, короткі описи написано для цієї вправи.
# Англійські ключові слова дозволяють зосередитися на TF-IDF, без лематизації.
books = pd.DataFrame([
    ('b01', 'Гобіт', 'Tolkien', 'fantasy dragon journey friendship'),
    ('b02', 'Володар перснів', 'Tolkien', 'fantasy ring journey friendship'),
    ('b03', 'Гаррі Поттер і філософський камінь', 'Rowling', 'fantasy magic school friendship'),
    ('b04', 'Гаррі Поттер і таємна кімната', 'Rowling', 'fantasy magic school mystery'),
    ('b05', 'Чарівник Земномор’я', 'LeGuin', 'fantasy wizard island journey'),
    ('b06', 'Гробниці Атуану', 'LeGuin', 'fantasy island tomb journey'),
    ('b07', 'Фундація', 'Asimov', 'science space empire future'),
    ('b08', 'Я, робот', 'Asimov', 'science robot future ethics'),
    ('b09', 'Убивство у Східному експресі', 'Christie', 'detective train crime mystery'),
    ('b10', 'Смерть на Нілі', 'Christie', 'detective river crime mystery'),
    ('b11', 'Прикладне машинне навчання', 'Geron', 'python machine learning models'),
    ('b12', 'Навчальний довідник моделей', 'Workshop', 'python machine learning practice'),
], columns=['book_id', 'title', 'authors', 'description'])

# Вигадані оцінки 1..5. Відсутній рядок — невідома оцінка, не нуль зірок.
history = {
    'Olia': [('b01',5),('b03',4),('b09',1),('b05',4)],
    'Ira': [('b01',5),('b03',4),('b09',1),('b02',5),('b04',4),('b06',3)],
    'Max': [('b01',1),('b03',1),('b09',4),('b07',5),('b08',5),('b10',5)],
    'Taras': [('b01',4),('b03',5),('b09',2),('b02',4),('b04',5),('b05',4)],
    'Nadia': [('b01',2),('b03',2),('b09',3),('b02',2),('b05',5),('b06',5)],
    'Lena': [('b01',5),('b03',4),('b09',1),('b04',4),('b05',3)],
}
rows = []
for user_no, (user, items) in enumerate(history.items()):
    for day, (book, rating) in enumerate(items):
        timestamp = pd.Timestamp('2026-01-01') + pd.Timedelta(days=day*4+user_no)
        rows.append((user, book, rating, timestamp))
# Майбутні оцінки після спільного cutoff; модель до них доступу не матиме.
for offset, (user, book, rating) in enumerate([
    ('Olia','b02',5), ('Ira','b05',4), ('Max','b02',1),
    ('Taras','b06',4), ('Nadia','b04',2), ('Lena','b02',5),
]):
    rows.append((user,book,rating,pd.Timestamp('2026-03-01')+pd.Timedelta(days=offset)))
events = pd.DataFrame(rows, columns=['user_id','book_id','rating','timestamp'])
events = events.sort_values(['timestamp','user_id','book_id']).reset_index(drop=True)
cutoff = pd.Timestamp('2026-02-01')
train = events.loc[events.timestamp < cutoff].copy()
test = events.loc[events.timestamp >= cutoff].copy()

assert books.book_id.is_unique
assert not events.duplicated(['user_id','book_id']).any()
assert events.rating.between(1,5).all()
assert set(events.book_id) <= set(books.book_id)
assert train.timestamp.max() < test.timestamp.min()


def customer_data():
    """Дві фізично зрозумілі ознаки й один нетиповий клієнт; seed фіксовано."""
    rng = np.random.default_rng(42)
    groups = [rng.normal(c,[50,0.6],size=(25,2))
              for c in ([350,2],[1800,12],[900,6])]
    return np.vstack(groups + [np.array([[5000,1]])])


def rating_matrix(table):
    """NaN зберігається в матриці явних оцінок."""
    if table.duplicated(['user_id','book_id']).any():
        raise ValueError('Спочатку узгодьте політику повторних оцінок')
    return table.pivot(index='user_id',columns='book_id',values='rating')


def user_similarities(matrix):
    """Нуль — лише технічне заповнення для cosine; оригінальні NaN збережені."""
    return pd.DataFrame(cosine_similarity(matrix.fillna(0)),
                        index=matrix.index, columns=matrix.index)


def predict_rating(matrix, similarities, user, book):
    """Середнє оцінок тільки тих інших користувачів, хто оцінив цю книжку."""
    if user not in matrix.index or book not in matrix.columns:
        return None
    known = matrix[book].dropna().drop(index=user, errors='ignore')
    weights = similarities.loc[user].reindex(known.index)
    positive = weights > 0
    known, weights = known[positive], weights[positive]
    if weights.sum() <= 0:
        return None
    return float(np.dot(weights.to_numpy(), known.to_numpy()) / weights.sum())


def popularity(table, catalog, seen=(), n=3):
    """Fallback: спочатку кількість оцінок, потім середній рейтинг та стабільний ID."""
    stats = table.groupby('book_id').rating.agg(['count','mean']).reset_index()
    stats = stats.loc[~stats.book_id.isin(set(seen))]
    stats = stats.sort_values(['count','mean','book_id'],ascending=[False,False,True])
    return stats.head(n).merge(catalog[['book_id','title']],on='book_id',how='left')


def recommend_user(table, catalog, user, n=3):
    """Приклад складання списку; жодних невідомих оцінок у знаменнику."""
    matrix = rating_matrix(table)
    if user not in matrix.index:
        result = popularity(table,catalog,n=n)
        return result.assign(reason='популярність: немає історії')
    similarities = user_similarities(matrix)
    seen = set(table.loc[table.user_id == user,'book_id'])
    candidates = []
    for book in catalog.book_id:
        if book in seen:
            continue
        score = predict_rating(matrix,similarities,user,book)
        if score is not None:
            candidates.append((book,score))
    if not candidates:
        return popularity(table,catalog,seen,n).assign(reason='популярність: немає сигналу')
    result = pd.DataFrame(candidates,columns=['book_id','score'])
    result = result.sort_values(['score','book_id'],ascending=[False,True]).head(n)
    return result.merge(catalog[['book_id','title']],on='book_id').assign(reason='оцінки сусідів')


# У .py результати поряд із пакетом; у самодостатньому ноутбуці — поряд із ним.
OUTPUT_DIR = (Path(__file__).resolve().parent / 'results'
              if '__file__' in globals() else Path.cwd() / 'results_35_36')
