"""Приклад 8. 36.2 · Прогноз рейтингу: хто саме має право голосу

## Голосують лише сусіди, які оцінили кандидата

**Факт 8. Зважений прогноз ділиться на суму ваг тільки тих інших читачів, чиї оцінки кандидата відомі.**

Схема: кандидат → відомі рейтинги інших → ваги схожості → sum(w*r)/sum(w).

Нехай Іра має вагу 0.8 й поставила 5, Тарас має 0.2 й поставив 3, а третій читач із вагою 0.9 книгу не оцінив. Прогноз: (0.8×5+0.2×3)/(0.8+0.2)=4.6. Третій не входить ні в чисельник, ні в знаменник. Інакше невідоме непомітно перетвориться на негативний голос.

Самого користувача прибираємо зі списку сусідів. За нашими позитивними шкалами cosine невід'ємний, тому беремо лише ваги >0. Якщо жодного голосу немає або сума ваг нульова, повернемо None — прогнозу немає. Не видаємо його за 0 зірок і не ділимо на нуль.

Це простий user-based baseline: середнє рейтингів сусідів без центрування. Люди можуть по-різному користуватися шкалою; зважений результат не є відкаліброваною впевненістю. Якщо ваги додатні, прогноз лежить між мінімальною та максимальною оцінками використаних сусідів.

Прогноз використовує тільки наявні оцінки кандидата та вирівняні ваги.
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
def rating_matrix(table):
    """NaN зберігається в матриці явних оцінок."""
    if table.duplicated(['user_id','book_id']).any():
        raise ValueError('Спочатку узгодьте політику повторних оцінок')
    return table.pivot(index='user_id',columns='book_id',values='rating')

def user_similarities(matrix):
    """Нуль — лише технічне заповнення для cosine; оригінальні NaN збережені."""
    return pd.DataFrame(cosine_similarity(matrix.fillna(0)),
                        index=matrix.index, columns=matrix.index)

matrix = rating_matrix(train)
similarities = user_similarities(matrix)

# %% Основний код прикладу
def predict_rating(matrix, similarities, user, book):
    """Середнє оцінок тільки тих інших користувачів, хто оцінив цю книжку."""
    if user not in matrix.index or book not in matrix.columns:
        return None
    known = matrix[book].dropna().drop(index=user, errors='ignore')
    weights = similarities.loc[user].reindex(known.index)
    positive = weights > 0
    known, weights = known[positive], weights[positive]
    if weights.sum() <= 0:
        return None
    return float(np.dot(weights.to_numpy(), known.to_numpy()) / weights.sum())

print('Прогноз Olia/b02:',predict_rating(matrix,similarities,'Olia','b02'))
print('Книга без оцінок b12:',predict_rating(matrix,similarities,'Olia','b12'))

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
known_votes = matrix['b02'].dropna().drop(index='Olia',errors='ignore')
vote_weights = similarities.loc['Olia'].reindex(known_votes.index)
fig, axes = plt.subplots(1,2,figsize=(9,3))
axes[0].bar(known_votes.index,known_votes.values)
axes[0].set(ylabel='Оцінка b02',ylim=(0,5.5),title='Хто прочитав кандидата')
axes[1].bar(vote_weights.index,vote_weights.values,color='coral')
axes[1].set(ylabel='Вага cosine',ylim=(0,1.1),title='Сила їхніх голосів для Олі')
fig.tight_layout()
plt.show()
