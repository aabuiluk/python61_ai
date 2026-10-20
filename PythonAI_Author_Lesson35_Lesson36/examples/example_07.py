"""Приклад 7. 36.1 · Оцінки читачів: пропуск не є нуль зірок

## Інший сигнал для тієї самої книгарні

**Факт 7. У матриці явних рейтингів порожня клітинка означає невідому оцінку, а не погану книгу.**

Схема: user_id, book_id, rating → pivot → читачі × книги → маска відомих оцінок.

У локальній таблиці є оцінки 1..5 та час події. Для уроку вже відокремлено історію train до 1 лютого 2026 та майбутні test-події після цього моменту. Уся побудова сусідів і рекомендацій працює тільки з train. Майбутні оцінки побачимо лише наприкінці для перевірки.

Довгий формат зручний для збереження: один рядок — оцінка однієї книги одним читачем. Pivot робить матрицю, де рядки — читачі, колонки — book_id. На місці невідомого зберігаємо NaN. Повторні оцінки однієї пари потрібно обробити за явним правилом: наприклад, брати останню за часом; наші дані повторів не мають, а функція перевіряє це.

Для простого cosine користувачів створимо технічну копію fillna(0). Оригінальна матриця лишається з NaN, щоб відрізняти невідоме від реальної низької оцінки. Ця навчальна схожість не центрує рейтинги та чутлива до повноти історії й щедрості читача; це спрощений baseline, а не універсальна модель смаку.

Покупка, перегляд і оцінка — різні типи сигналів. Відсутність покупки теж не доводить нелюбов; не змішуйте implicit-події зі шкалою явних зірок без окремого пояснення.

Підрахунок узгоджений із train, невідомі оцінки не стали нульовими цілями.
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


# %% Основний код прикладу
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
print(matrix.to_string())
print('Відомих оцінок:',int(matrix.notna().sum().sum()))
print('Схожість на Olia:',similarities.loc['Olia'].round(3).to_dict())

# %% Графічне пояснення — Matplotlib (окремо від алгоритму)
fig, ax = plt.subplots(figsize=(8,3))
cmap = plt.get_cmap('YlGnBu').copy()
cmap.set_bad('lightgray')
image = ax.imshow(np.ma.masked_invalid(matrix.to_numpy()),vmin=1,vmax=5,cmap=cmap,aspect='auto')
ax.set(xticks=range(len(matrix.columns)),xticklabels=matrix.columns,
       yticks=range(len(matrix.index)),yticklabels=matrix.index,title='Сіре — невідома оцінка, не 0 зірок')
fig.colorbar(image,ax=ax,label='Відомий рейтинг')
fig.tight_layout()
plt.show()
