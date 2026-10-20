"""**Завдання 7. Виміряйте порожнечі.** Порахуйте кількість відомих і невідомих клітинок, частку заповнення. Виведіть книги, які Оля вже оцінила, і книги каталогу, яких вона ще не оцінила. Перевірте, що b02 у її історії train відсутня.

Підказки
1. matrix = rating_matrix(train); notna().sum().sum() рахує відомі.
2. matrix.size — загальне число клітинок у pivot, а не число подій.
3. Для Олі використайте `train.loc[train.user_id == 'Olia','book_id']`.
4. Кандидати — set(books.book_id) мінус seen; це включає також книги без жодних оцінок.
5. Не підміняйте train повною events: b02 для Олі є майбутньою перевіркою.

Готово, якщо: Підрахунок узгоджений із train, невідомі оцінки не стали нульовими цілями.
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
# Завдання 7: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
