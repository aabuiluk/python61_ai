"""**Завдання 1. Новий покупець.** Для рядка [850, 6] знайдіть сегмент та відстань до найближчого центру. Порівняйте із [5000, 1]. Скажіть, чи доводять ці два числа, яку книжку покупець хоче прочитати.

Підказки
1. Створіть масив двох рядків через np.array.
2. Перетворіть його customer_scaler.transform; не навчайте новий scaler.
3. customer_km.predict дасть дві мітки, customer_km.transform — відстані до трьох центрів.
4. Для мінімуму в кожному рядку використайте `.min(axis=1)`.
5. Висновок має назвати, якої інформації про інтереси нам бракує.

Готово, якщо: Є два призначення, дві відстані й пояснення різниці між сегментом та особистою рекомендацією.
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
customers = customer_data()
customer_scaler = StandardScaler().fit(customers)
customers_scaled = customer_scaler.transform(customers)
customer_km = KMeans(n_clusters=3,n_init=10,random_state=42).fit(customers_scaled)

# %% Ваш код
# Завдання 1: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
