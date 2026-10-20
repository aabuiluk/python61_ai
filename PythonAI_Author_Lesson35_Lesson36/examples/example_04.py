"""Приклад 4. 35.2 · Cosine: вимірюємо спільний напрямок

## Чому спільні слова дають схожість

**Факт 4. Cosine порівнює напрямки ненульових векторів, а не кількість покупок чи якість книжки.**

Схема: два TF-IDF-вектори → скалярний добуток / добуток довжин → оцінка близькості.

Для двох векторів a і b формула: sum(a*b)/(norm(a)*norm(b)). Наприклад [1,0] та [2,0] мають однаковий напрямок, cosine=1, хоча друга довжина більша. [1,0] і [0,1] не мають спільного напрямку, cosine=0.

Для невід'ємних TF-IDF-ознак близькість від 0 до 1. Загалом cosine для довільних дійсних векторів може бути від -1 до 1. Оцінка 0.8 не означає 80% імовірності, що книга сподобається: це близькість у нашому представленні.

Матриця cosine авторів має форму 12×12: рядок — запитана книга, колонка — кандидат. Діагональ для ненульового рядка дорівнює 1: книга найбільше схожа сама на себе. Під час рекомендації її потрібно явно прибрати. Нульовий вектор математично не має визначеного кута; sklearn повертає для нього нульові подібності — такий результат потребує пояснення, а не вигаданого рейтингу.

У великому каталозі не обов'язково зберігати повну квадратну матрицю. Можна порівнювати один запит зі всіма або шукати лише найближчих кандидатів. Сьогодні квадратна матриця маленька й корисна для наочності.

Є ручний розрахунок 0.5 та пояснення, чому спільний автор дає інший результат, ніж різний.
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

# %% Основний код прикладу
author_sim = cosine_similarity(author_X)
print(pd.DataFrame(author_sim,index=books.book_id,columns=books.book_id).round(2))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(6,4))
picture = ax.imshow(author_sim,vmin=0,vmax=1,cmap='Blues')
ax.set(xticks=range(len(books)),xticklabels=books.book_id,
       yticks=range(len(books)),yticklabels=books.book_id,title='Cosine: однаковий автор → спільний сигнал')
ax.tick_params(axis='x',rotation=90)
fig.colorbar(picture,ax=ax)
fig.tight_layout()
plt.show()
