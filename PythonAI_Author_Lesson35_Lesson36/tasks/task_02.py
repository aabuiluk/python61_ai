"""**Завдання 2. Перевірте радіус.** Для eps=0.15 і eps=3.0 надрукуйте кількість кластерів та шуму. Закінчіть дві фрази: «Для content-based потрібні…», «Для collaborative потрібні…».

Підказки
1. Зберігайте customers_scaled і min_samples=4 незмінними.
2. Зробіть цикл за двома радіусами й викличте fit_predict.
3. Кластери рахуйте без -1: `len(set(labels) - {-1})`.
4. Шум: `(labels == -1).sum()`.
5. Обидва нові методи потребують іншої інформації, ніж середній чек і число замовлень.

Готово, якщо: Є два порівняння й названо джерело сигналу кожного типу рекомендацій.
"""

# Працює і з кореня репозиторію, і з папки examples/tasks.
from PythonAI_Author_Lesson35_Lesson36.workshop import (
    books, cosine_similarity, customer_data, cutoff, DBSCAN, events, KMeans, np, OUTPUT_DIR, pd,
    plt, popularity, predict_rating, rating_matrix, recommend_user, StandardScaler, test,
    TfidfVectorizer, train, user_similarities,
)

# %% Початковий контекст
customers = customer_data()
customers_scaled = StandardScaler().fit_transform(customers)
customer_db = DBSCAN(eps=0.35,min_samples=4).fit(customers_scaled)

# %% Ваш код
# Завдання 2: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
