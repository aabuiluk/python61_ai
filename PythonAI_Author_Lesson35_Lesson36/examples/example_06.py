"""Приклад 6. 35.4 · Новий читач: опис інтересу та нульовий вектор

## Порадити можна й без історії оцінок

**Факт 6. Текст інтересу можна порівняти з описами книг через той самий навчений словник.**

Схема: описи → fit TF-IDF; інтерес читача → transform → cosine до описів → без уже прочитаного.

Новий читач написав «python machine learning». Авторський вектор тут не допомагає: у запиті немає Tolkien чи Geron. Для цієї окремої моделі використаємо description. Англійські ключові слова в локальних описах написані спеціально для вправи, щоб не додавати морфологічний аналіз української.

Для запиту не викликаємо новий fit: словник і ваги мають залишитися сумісними з векторами каталогу. Запит transform дає один рядок із тими самими колонками. cosine_similarity(query,description_X) повертає 1×12 оцінок.

Якщо всі слова невідомі словнику, query.nnz дорівнює 0. Повертати top із нулів не варто: немає сигналу. У такому разі можна попросити уточнити інтерес або явно запропонувати неперсональний список. Також прибираємо вже прочитані книги: цей фільтр потрібен незалежно від методу.

Content-based не розуміє синоніми автоматично: «coding» та «python» не стануть близькими без спільних токенів чи додаткового представлення. Новий текст або книга поза словником потребують перевірки, а при оновленні словника треба перерахувати всі вектори каталогу.

Немає прочитаної b03; невідомий запит не породжує фальшиву рекомендацію.
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
description_vectorizer = TfidfVectorizer()
description_X = description_vectorizer.fit_transform(books.description)

# %% Основний код прикладу
query = description_vectorizer.transform(['python machine learning'])
scores = cosine_similarity(query,description_X)[0]
ranking = books[['book_id','title']].assign(score=scores)
print(ranking.loc[ranking.score > 0].sort_values(['score','book_id'],ascending=[False,True]).head(3).to_string(index=False))
print('Невідомі слова, ненульових координат:',description_vectorizer.transform(['quokka']).nnz)

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(7,3))
shown = ranking.sort_values(['score','book_id'],ascending=[False,True]).head(5)
ax.bar(shown.book_id,shown.score,color='teal')
ax.set(ylim=(0,1.1),xlabel='Книга',ylabel='Cosine до запиту',title='Інтерес: python machine learning')
fig.tight_layout()
plt.show()
