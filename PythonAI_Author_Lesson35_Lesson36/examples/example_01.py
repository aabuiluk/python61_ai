"""Приклад 1. 33 · Від сегмента покупців до особистої рекомендації

## Що вже вміє наш магазин

На попередній зустрічі ми знаходили групи схожих покупців. Сьогодні магазин ставить точніше питання: «Яку книжку показати Олі наступною?» Група допомагає описати людей, але ще не визначає конкретну книжку для конкретної людини.

**Факт 1. Кластеризація повертає групу об'єкта, а рекомендація — впорядкований список інших об'єктів для нього.**

Схема: витрати й замовлення → масштабування → K-Means → сегмент → нове питання про книжку.

У повторенні маємо 76 синтетичних покупців, дві ознаки: середній чек і кількість замовлень за місяць. K-Means призначає кожному найближчий центр і пересуває центр у середнє своєї групи. k=3 — наше рішення. Номер групи не є рейтингом людини.

Гривні чисельно більші за кількість замовлень, тому спершу StandardScaler. Для нового покупця застосовуємо той самий transform і predict, а не fit на одному рядку. Навіть віддалений покупець отримає найближчий центр. Ця межа підводить до DBSCAN у наступному блоці.

У самих двох ознаках немає інформації про книжкові вподобання. Не можна чесно вивести «любить фентезі» з великого чека. Для рекомендацій знадобиться інший сигнал: зміст книжок або історія оцінок.

Є два призначення, дві відстані й пояснення різниці між сегментом та особистою рекомендацією.
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

# %% Основний код прикладу
print('Розміри сегментів:',pd.Series(customer_km.labels_).value_counts().sort_index().to_dict())

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(7,3))
ax.scatter(customers[:,0],customers[:,1],c=customer_km.labels_,cmap='tab10',s=20)
ax.set(xlabel='Середній чек, грн',ylabel='Замовлень на місяць',title='Сегмент ще не є рекомендацією книги')
fig.tight_layout()
plt.show()
