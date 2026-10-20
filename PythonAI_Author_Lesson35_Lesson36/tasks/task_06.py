"""**Завдання 6. Персональний фільтр і порожній сигнал.** Для запиту «fantasy magic school» поверніть до трьох книг, прибравши прочитану b03. Потім обробіть «quokka»: замість довільних кандидатів надрукуйте прохання уточнити інтерес.

Підказки
1. Використайте description_vectorizer.transform та description_X із контексту.
2. Перед cosine перевірте query.nnz; якщо нуль, повідомте про відсутність знайомих слів.
3. До фільтра score>0 додайте `~result.book_id.isin({'b03'})`.
4. Відомі слова не гарантують ідеальної поради: поясніть, які саме токени підняли кандидата.

Готово, якщо: Немає прочитаної b03; невідомий запит не породжує фальшиву рекомендацію.
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

# %% Ваш код
# Завдання 6: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
