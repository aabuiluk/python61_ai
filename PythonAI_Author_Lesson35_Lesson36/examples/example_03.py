"""Приклад 3. 35.1 · Каталог і TF-IDF: перетворюємо автора на числа

## Починаємо з прозорого сигналу

**Факт 3. TF-IDF представляє книжку вектором слів із вибраного текстового поля.**

Схема: book_id і authors → словник токенів → TF-IDF-матриця → одна числова строка на книгу.

У нашому каталозі 12 навчальних записів: ідентифікатор, назва, автор і короткий опис. ID b01 не змінюється від сортування й не залежить від назви. Це важливо: дві різні книги можуть мати однакову назву, тому далі обираємо саме book_id.

Спочатку векторизуємо authors — це мінімум практикуму 7.3. Автори повторюються, тому Гобіт і Володар перснів матимуть спільний сигнал Tolkien. Метод не знає ні сюжету, ні жанру, доки ми не додамо відповідні поля.

TF — частота слова в одному документі; IDF зменшує відносну вагу слів, поширених у багатьох документах. За типовими параметрами TfidfVectorizer: idf = log((1+n)/(1+df)) + 1; потім рядок нормується за L2. Слово в усіх документах має IDF=1, а не нуль. Цей маленький каталог потрібен, щоб побачити механіку, а не довести якість великого сервісу.

Матриця розріджена: відсутнє слово займає нульову координату, а не записаний пробіл. toarray зручний для 12 книг, але не для мільйонів описів. fit_transform вчить словник; для нового тексту пізніше використаємо transform.

Є дві матриці та пояснення, які саме слова тепер впливають на результат.
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


# %% Основний код прикладу
author_vectorizer = TfidfVectorizer()
author_X = author_vectorizer.fit_transform(books.authors)
print(books[['book_id','title','authors']].to_string(index=False))
print('Форма:',author_X.shape)
print('Словник:',author_vectorizer.get_feature_names_out())
print('Перші два рядки:',author_X[:2].toarray())

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(8,3))
ax.imshow(author_X.toarray(),cmap='Blues',vmin=0,vmax=1,aspect='auto')
ax.set(xticks=range(author_X.shape[1]),xticklabels=author_vectorizer.get_feature_names_out(),
       yticks=range(len(books)),yticklabels=books.book_id,title='TF-IDF за автором: рядок на книгу')
ax.tick_params(axis='x',rotation=30)
fig.tight_layout()
plt.show()
