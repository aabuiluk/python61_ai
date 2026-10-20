"""Приклад 9. 36.3 · Список для читача: unseen, cold start і CSV

## Прогноз ще треба перетворити на рекомендацію

**Факт 9. Хороший список виключає вже оцінене й чесно позначає fallback, коли персонального сигналу немає.**

Схема: історія читача → unseen → прогноз для кандидатів → сортування → CSV; немає історії → популярність.

Із каталогу прибираємо книги, вже оцінені цим читачем у train. Для решти обчислюємо прогноз, пропускаємо None, сортуємо й беремо top-n. Невідомий користувач не має рядка схожості: це cold start. Йому можна запропонувати популярність або попросити інтерес і використати content-based із пари 35.

Наш fallback спочатку сортує за кількістю оцінок, потім за середньою оцінкою та ID. Це прозоре неперсональне правило, не «штучний смак» нового користувача. Воно має popularity bias: маловідомі книги майже не отримують шансів. Поле reason у результаті показує, яке правило спрацювало.

Можливий ще один cold start: нова книга без жодного рейтингу. Collaborative не має для неї оцінок, але content-based може використати її опис. Якщо отримали менше n кандидатів, повертаємо коротший список, не домішуючи довільні нулі.

Результат практикуму — book_recommendations.csv, а не лише красивий print. UTF-8 із BOM зручно відкривається в багатьох табличних редакторах. Перед записом створимо папку results; шлях будуємо від пакета, щоб запуск з іншого каталогу не загубив файл.

CSV існує, ID після читання збігаються, self-history відсутня, fallback підписано.
"""
from pathlib import Path
import sys

# Працює і з кореня репозиторію, і з папки examples/tasks.
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
from workshop import (
    np, pd, plt, KMeans, DBSCAN, StandardScaler, TfidfVectorizer,
    cosine_similarity, books, events, train, test, cutoff, customer_data,
    rating_matrix, user_similarities, predict_rating, popularity,
    recommend_user, OUTPUT_DIR,
)

# %% Початковий контекст
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

# %% Основний код прикладу
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

print('Для Olia:')
print(recommend_user(train,books,'Olia',n=3).round(3).to_string(index=False))
print('Для нового читача:')
print(recommend_user(train,books,'NewReader',n=3).to_string(index=False))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
shown = recommend_user(train,books,'Olia',n=3)
fig, ax = plt.subplots(figsize=(7,3))
ax.bar(shown.book_id,shown.score,color='purple')
ax.set(ylabel='Прогноз рейтингу',ylim=(0,5.5),xlabel='Непрочитана книга',title='Top-3 для Олі за сусідами')
fig.tight_layout()
plt.show()
