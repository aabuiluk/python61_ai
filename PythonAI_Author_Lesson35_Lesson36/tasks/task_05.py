"""**Завдання 5. Напишіть recommend_book(book_id, n=3).** Поверніть DataFrame з book_id, title і score, без самої книги та нульової близькості. Невідомий ID має давати зрозумілий ValueError, n<=0 — також. Перевірте b03 і невідомий b99.

Підказки
1. Знайдіть позиції за `books.index[books.book_id == book_id]` і перевірте len.
2. Демо вже показує фільтр, потрібні лише параметри функції та перевірки.
3. Відсортуйте score за спаданням, book_id за зростанням.
4. Візьміть head(n), не доповнюйте нулями короткий результат.
5. Викличте функцію в try/except ValueError для b99 і надрукуйте повідомлення.

Готово, якщо: Є функція, перевірка self-hit та зрозумілий результат невідомого ID.
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
author_vectorizer = TfidfVectorizer()
author_X = author_vectorizer.fit_transform(books.authors)
author_sim = cosine_similarity(author_X)

# %% Ваш код
# Завдання 5: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
