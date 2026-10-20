"""**Завдання 9. Збережіть результат.** Отримайте top-3 для Olia, перевірте відсутність уже оцінених книг, запишіть у results/book_recommendations.csv. Прочитайте файл назад і звірте список ID. Окремо викличте рекомендацію для NewReader та поясніть reason.

Підказки
1. recommend_user уже розібрано в демонстрації; використайте його без нових формул.
2. seen визначайте за train, а не events.
3. Перетин set(result.book_id) & seen має бути порожнім.
4. OUTPUT_DIR.mkdir(parents=True,exist_ok=True); шлях OUTPUT_DIR/'book_recommendations.csv'.
5. to_csv(index=False,encoding='utf-8-sig'), потім pd.read_csv з тим самим кодуванням.

Готово, якщо: CSV існує, ID після читання збігаються, self-history відсутня, fallback підписано.
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

# %% Ваш код
# Завдання 9: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
