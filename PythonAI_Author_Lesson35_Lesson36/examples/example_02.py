"""Приклад 2. 34 · DBSCAN: нетипова точка та межа старої задачі

## Кого можна залишити поза групами

**Факт 2. DBSCAN може позначити рідкісне оточення як шум, але не пояснює читацький смак.**

Схема: радіус eps → сусіди → ядра й межові → групи або -1 → перевірка змісту ознак.

Ядрова точка має в радіусі eps принаймні min_samples точок, включно із собою у scikit-learn. Межова має замало власних сусідів, але лежить біля ядра. Інші точки можуть отримати -1. Це шум за поточними параметрами, а не шахрайство чи помилка даних.

На тих самих масштабованих покупцях DBSCAN не отримує кількість груп наперед. Ми задаємо щільність через eps і min_samples. Малий радіус може розсипати хмари, великий — склеїти. Номери кластерів двох алгоритмів не слід порівнювати як однакові назви.

Тепер змінимо саму задачу. Пара 35 відповідає «Яка книга схожа за змістом на цю?», навіть без рейтингів. Пара 36 — «Що оцінили люди зі схожою історією?» Один метод порівнює ознаки речей, інший використовує спільні реакції людей. Жоден із них не вгадує вподобання з самого номера сегмента.

Є два порівняння й названо джерело сигналу кожного типу рекомендацій.
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
customers_scaled = StandardScaler().fit_transform(customers)
customer_db = DBSCAN(eps=0.35,min_samples=4).fit(customers_scaled)

# %% Основний код прикладу
print('Груп:',len(set(customer_db.labels_) - {-1}))
print('Шум:',int((customer_db.labels_ == -1).sum()))
print('Чи є predict:',hasattr(customer_db,'predict'))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(7,3))
for label in sorted(set(customer_db.labels_)):
    mask = customer_db.labels_ == label
    ax.scatter(customers[mask,0],customers[mask,1],marker='x' if label == -1 else 'o',
               label='Шум' if label == -1 else f'Група {label}')
ax.set(xlabel='Середній чек, грн',ylabel='Замовлень на місяць',title='Групи за щільністю')
ax.legend()
fig.tight_layout()
plt.show()
