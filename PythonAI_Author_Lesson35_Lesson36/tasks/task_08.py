"""**Завдання 8. Перевірте знаменник самостійно.** Для кандидата b06 зберіть рейтинги інших читачів, що оцінили його, і їхні ваги схожості з Олею. Порахуйте прогноз через dot та суму ваг. Порівняйте з predict_rating. Надрукуйте також суму ваг усіх інших читачів і поясніть, чому її не можна брати знаменником.

Підказки
1. `matrix['b06'].dropna()` лишає тільки відомі оцінки; приберіть Olia через drop(errors='ignore').
2. `similarities.loc['Olia'].reindex(rated.index)` вирівнює ваги й оцінки за іменами, а не випадковим порядком.
3. Залиште positive = weights > 0 в обох об'єктах.
4. Перевірте weights.sum() перед діленням.
5. Відомий прогноз — np.dot(weights, rated)/weights.sum(); порівняння через np.isclose.

Готово, якщо: Прогноз використовує тільки наявні оцінки кандидата та вирівняні ваги.
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

# %% Ваш код
# Завдання 8: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
