"""**Завдання 3. Змініть текстове поле.** Побудуйте окремий TF-IDF на authors + пробіл + title. Надрукуйте кількість колонок до й після зміни. Поясніть, чому додавання назви змінює поняття схожості.

Підказки
1. Початкову модель авторів збережіть без змін.
2. Тексти: `books['authors'] + ' ' + books['title']`.
3. Створіть новий TfidfVectorizer і викличте fit_transform.
4. shape[1] — число ознак, а не книжок.
5. Назви українською токенізуються, але без лематизації споріднені форми слів можуть лишитися різними ознаками.

Готово, якщо: Є дві матриці та пояснення, які саме слова тепер впливають на результат.
"""

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson35_Lesson36.workshop import (
    books, cosine_similarity, customer_data, cutoff, DBSCAN, events, KMeans, np, OUTPUT_DIR, pd,
    plt, popularity, predict_rating, rating_matrix, recommend_user, StandardScaler, test,
    TfidfVectorizer, train, user_similarities,
)

# %% Початковий контекст


# %% Ваш код
# Завдання 3: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
