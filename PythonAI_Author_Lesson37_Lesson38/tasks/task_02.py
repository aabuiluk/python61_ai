"""**Завдання 2. Знайдіть межу твердження.** Порівняйте Olia з Max за спільними книгами.
Надрукуйте їх cosine, кількість спільних оцінок та кількість пропусків Olia.
Напишіть одне обережне пояснення рекомендації b02 на основі Ira без вигадування смаків Olia.

Підказки
1. Виберіть Olia і Max; dropna(axis=1) залишить спільні колонки.
2. Для cosine передайте два двовимірні зрізи iloc[[0]] й iloc[[1]].
3. shape[1] дає кількість спільних книг, isna().sum() — число пропусків.
4. Назвіть джерело сигналу та обмеження маленької історії.

Готово, якщо: Пропуск збережено, є cosine для двох спільних книг і пояснення з названим обмеженням.
"""
from pathlib import Path
import sys

# Працює і з кореня репозиторію, і з папки examples/tasks.
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
from workshop import (
    np, pd, plt, json, re, books, fixtures, platforms, cosine_similarity,
    recommend, build_prompt, validate_response, evaluate_fixtures, diagram, OUTPUT_DIR,
)

# %% Початковий контекст
ratings = pd.DataFrame([[5, np.nan, 1], [5, 5, 1], [1, 2, 5]],
                       index=['Olia', 'Ira', 'Max'], columns=['b01', 'b02', 'b04'])

# %% Ваш код
# Завдання 2: напишіть власний код за умовою та підказками.
# Початкові змінні з контексту вже доступні.
common = ratings.loc[['Olia', 'Max']].dropna(axis=1)
similarity = cosine_similarity(common.iloc[[0]], common.iloc[[1]])[0, 0]
print('Спільні книги:', common.columns.tolist())
print('Cosine на спільних оцінках:', round(float(similarity), 3))
print('Ira оцінила b02:', ratings.loc['Ira', 'b02'])
