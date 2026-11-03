"""**Завдання 7. Виміряйте порожнечі.** Порахуйте кількість відомих і невідомих клітинок, частку заповнення. Виведіть книги, які Оля вже оцінила, і книги каталогу, яких вона ще не оцінила. Перевірте, що b02 у її історії train відсутня.

Підказки
1. matrix = rating_matrix(train); notna().sum().sum() рахує відомі.
2. matrix.size — загальне число клітинок у pivot, а не число подій.
3. Для Олі використайте `train.loc[train.user_id == 'Olia','book_id']`.
4. Кандидати — set(books.book_id) мінус seen; це включає також книги без жодних оцінок.
5. Не підміняйте train повною events: b02 для Олі є майбутньою перевіркою.

Готово, якщо: Підрахунок узгоджений із train, невідомі оцінки не стали нульовими цілями.
"""

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson35_Lesson36.workshop import (
    books, cosine_similarity, customer_data, cutoff, DBSCAN, events, KMeans, np, OUTPUT_DIR, pd,
    plt, popularity, predict_rating, rating_matrix, recommend_user, StandardScaler, test,
    TfidfVectorizer, train, user_similarities,
)

# %% Початковий контекст


# %% Ваш код
# Завдання 7: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
