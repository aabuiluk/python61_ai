"""**Завдання 3. Змініть текстове поле.** Побудуйте окремий TF-IDF на authors + пробіл + title. Надрукуйте кількість колонок до й після зміни. Поясніть, чому додавання назви змінює поняття схожості.

Підказки
1. Початкову модель авторів збережіть без змін.
2. Тексти: `books['authors'] + ' ' + books['title']`.
3. Створіть новий TfidfVectorizer і викличте fit_transform.
4. shape[1] — число ознак, а не книжок.
5. Назви українською токенізуються, але без лематизації споріднені форми слів можуть лишитися різними ознаками.

Готово, якщо: Є дві матриці та пояснення, які саме слова тепер впливають на результат.
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


# %% Ваш код
# Завдання 3: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
