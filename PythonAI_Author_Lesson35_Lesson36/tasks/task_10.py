"""**Завдання 10. Порівняйте з baseline.** Для кожного рядка test отримайте прогноз із матриці, побудованої тільки на train, та середній рейтинг книги за train. На спільно покритих рядках обчисліть обидві MAE. Повідомте покриття й напишіть чотири речення: який сигнал у кожного методу, що робити з новим читачем, чому MAE замало, що перевіряти на реальних даних.

Підказки
1. Побудуйте matrix і similarities заново саме з train.
2. Середні baseline: `train.groupby('book_id').rating.mean()`.
3. Перебирайте test.itertuples(index=False), використовуйте row.user_id, row.book_id, row.rating.
4. Якщо predict_rating дав None або середнього для книги немає, не включайте рядок в обидві MAE.
5. Для спільного DataFrame: abs(prediction-rating).mean(); покриття = число цих рядків / len(test).
6. Якщо спільних рядків немає, явно повідомте про неможливість порівняння.

Готово, якщо: Є часовий поділ, покриття та обидві MAE на тих самих рядках; висновок не перебільшує результат.
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
# Завдання 10: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
