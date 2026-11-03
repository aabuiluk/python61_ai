"""**Завдання 5. Напишіть recommend_book(book_id, n=3).** Поверніть DataFrame з book_id, title і score, без самої книги та нульової близькості. Невідомий ID має давати зрозумілий ValueError, n<=0 — також. Перевірте b03 і невідомий b99.

Підказки
1. Знайдіть позиції за `books.index[books.book_id == book_id]` і перевірте len.
2. Демо вже показує фільтр, потрібні лише параметри функції та перевірки.
3. Відсортуйте score за спаданням, book_id за зростанням.
4. Візьміть head(n), не доповнюйте нулями короткий результат.
5. Викличте функцію в try/except ValueError для b99 і надрукуйте повідомлення.

Готово, якщо: Є функція, перевірка self-hit та зрозумілий результат невідомого ID.
"""

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson35_Lesson36.workshop import (
    books, cosine_similarity, customer_data, cutoff, DBSCAN, events, KMeans, np, OUTPUT_DIR, pd,
    plt, popularity, predict_rating, rating_matrix, recommend_user, StandardScaler, test,
    TfidfVectorizer, train, user_similarities,
)

# %% Початковий контекст
author_vectorizer = TfidfVectorizer()
author_X = author_vectorizer.fit_transform(books.authors)
author_sim = cosine_similarity(author_X)

# %% Ваш код
# Завдання 5: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
