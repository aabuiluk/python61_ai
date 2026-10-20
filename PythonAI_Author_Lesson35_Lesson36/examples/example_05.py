"""Приклад 5. 35.3 · Рекомендація: ID, self-hit і чесний top-n

## Перетворюємо близькість на список

**Факт 5. Рекомендація потребує правил відбору: знайти ID, прибрати саму книгу й упорядкувати кандидатів.**

Схема: book_id → рядок схожості → без self і нульового сигналу → стабільне сортування → top-n.

Для b01 очікуємо іншу книгу Tolkien, а не повторення Гобіта. Якщо просто взяти найбільші числа, першою вийде сама b01. Тому self-hit прибираємо через ID, а не сліпо зрізом першого елемента: за однакових оцінок порядок може бути іншим.

Кількість n — верхня межа, а не обіцянка. За одного схожого автора список може містити лише одну книгу. Нульові оцінки не дають доказу схожості; повертати їх як «найкращі рекомендації» було б оманливо. Для однакових score застосуємо другий ключ book_id, щоб результат був відтворюваним.

Невідомий ID — помилка запиту; невідомий або порожній текст — відсутність сигналу. Ці ситуації слід розрізняти. Готова функція не повинна випадково брати чужий рядок, коли потрібної книги немає.

Є функція, перевірка self-hit та зрозумілий результат невідомого ID.
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
author_sim = cosine_similarity(author_X)

# %% Основний код прикладу
seed_id = 'b01'
seed_position = books.index[books.book_id == seed_id][0]
candidates = books[['book_id','title']].copy()
candidates['score'] = author_sim[seed_position]
candidates = candidates.loc[(candidates.book_id != seed_id) & (candidates.score > 0)]
print(candidates.sort_values(['score','book_id'],ascending=[False,True]).head(3).to_string(index=False))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(7,3))
shown = candidates.sort_values(['score','book_id'],ascending=[False,True]).head(3)
ax.bar(shown.book_id,shown.score,color='steelblue')
ax.set(ylim=(0,1.1),xlabel='Книга-кандидат',ylabel='Cosine',title='Лише позитивна близькість, без самої книги')
fig.tight_layout()
plt.show()
