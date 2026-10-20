"""Приклад 10. 36.4 · Перевірка без майбутнього та завершений звіт

## Чи справді список корисний

**Факт 10. Якість перевіряють на майбутніх подіях, яких не було ані в сусідах, ані в статистиках популярності.**

Схема: спільний cutoff → train для всіх перетворень → майбутні test → покриття й MAE → обережний висновок.

Часовий поділ у цьому пакеті зроблено до рекомендацій. Окреме «останнє читання кожної людини» без загального часу може залишити майбутні оцінки інших людей у train. Тому тут усі train-події передують усім test-подіям.

MAE — середня абсолютна помилка прогнозованих зірок. Для 5 зірок і прогнозу 4.5 помилка 0.5. Якщо модель не змогла дати прогноз, повідомляємо покриття — частку тестових подій із прогнозом. Не підміняємо відсутні прогнози нулями та не приховуємо пропущені випадки.

Порівняємо з простим baseline: середній рейтинг кожної книги за train. Обидві MAE рахуємо на тих самих тестових подіях, де доступні обидва прогнози. Шість штучних тестових оцінок — лише демонстрація протоколу, а не доказ переваги методу.

Малий MAE не гарантує доброго top-3: список може повторювати прочитане, бути одноманітним чи показувати лише хіти. Окремо перевіряйте ранжування, новизну, різноманітність і продуктову користь. Якщо частина смаків не представлена, потрібні нові сигнали, а не лише ще одна формула.

Сьогодні ми використовували memory-based сусідів. Surprise.SVD або навчання таблиць embedding — інший, model-based шлях, він не є тим самим матричним SVD із пари 31. Ці розширення не потрібні для проходження й не додають прихованих залежностей.

Є часовий поділ, покриття та обидві MAE на тих самих рядках; висновок не перебільшує результат.
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

# %% Основний код прикладу
print('Train:',len(train),'Test:',len(test))
print('Останній train:',train.timestamp.max(),'Перший test:',test.timestamp.min())
print('Тестові події:')
print(test[['user_id','book_id','rating','timestamp']].to_string(index=False))
assert train.timestamp.max() < test.timestamp.min()

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(8,3))
ax.scatter(train.timestamp,np.zeros(len(train)),label='Train',marker='|',s=100)
ax.scatter(test.timestamp,np.ones(len(test)),label='Test',marker='|',s=100)
ax.axvline(cutoff,color='red',linestyle='--',label='Спільний cutoff')
ax.set(yticks=[0,1],yticklabels=['Train','Test'],xlabel='Час події',title='Усі навчальні події раніше за тестові')
ax.legend()
fig.autofmt_xdate()
fig.tight_layout()
plt.show()
