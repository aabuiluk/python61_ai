"""**Завдання 4. Порахуйте cosine руками й кодом.** Для a=[1,1,0], b=[1,0,1] знайдіть добуток, довжини та cosine. Звірте зі sklearn. Потім виведіть близькість b01 до b02 і b03 за автором та поясніть різницю.

Підказки
1. Перетворіть списки на np.array з float.
2. Чисельник: np.dot(a,b); довжина: np.linalg.norm(a).
3. Для перевірки sklearn очікує двовимірні масиви: `cosine_similarity([a],[b])[0,0]`.
4. Побудуйте author_sim, якщо запускаєте завдання окремо.
5. Індекси рядків для b01,b02,b03 у навчальному каталозі — 0,1,2; у загальному коді шукайте ID явно.

Готово, якщо: Є ручний розрахунок 0.5 та пояснення, чому спільний автор дає інший результат, ніж різний.
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

# %% Ваш код
# Завдання 4: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
