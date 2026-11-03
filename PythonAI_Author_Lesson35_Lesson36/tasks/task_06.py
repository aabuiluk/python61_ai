"""**Завдання 6. Персональний фільтр і порожній сигнал.** Для запиту «fantasy magic school» поверніть до трьох книг, прибравши прочитану b03. Потім обробіть «quokka»: замість довільних кандидатів надрукуйте прохання уточнити інтерес.

Підказки
1. Використайте description_vectorizer.transform та description_X із контексту.
2. Перед cosine перевірте query.nnz; якщо нуль, повідомте про відсутність знайомих слів.
3. До фільтра score>0 додайте `~result.book_id.isin({'b03'})`.
4. Відомі слова не гарантують ідеальної поради: поясніть, які саме токени підняли кандидата.

Готово, якщо: Немає прочитаної b03; невідомий запит не породжує фальшиву рекомендацію.
"""

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson35_Lesson36.workshop import (
    books, cosine_similarity, customer_data, cutoff, DBSCAN, events, KMeans, np, OUTPUT_DIR, pd,
    plt, popularity, predict_rating, rating_matrix, recommend_user, StandardScaler, test,
    TfidfVectorizer, train, user_similarities,
)

# %% Початковий контекст
description_vectorizer = TfidfVectorizer()
description_X = description_vectorizer.fit_transform(books.description)

# %% Ваш код
# Завдання 6: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
