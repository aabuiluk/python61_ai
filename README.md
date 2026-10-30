# Новий практикум 39–42 · реальний OpenAI API

[Почати роботу](PythonAI_Author_Lesson39_Lesson42_API/README.md) · [HTML](PythonAI_Author_Lesson39_Lesson42_API/practice.html) · [ZIP](PythonAI_Author_Lesson39_Lesson42_API.zip). 180 хв; 11 практичних завдань, власні запити, .env.example. Готових розв’язків вправ у цьому пакеті немає.

# python61_ai

## Пари 37–38 · Generative AI та Prompt Engineering · 240 хв

40 хв повторення рекомендацій 35–36, 100 хв Generative AI, 100 хв роботи з промптами.
10 завдань із підказками, окремі приклади й графічні пояснення.

- [Маршрут і пояснення](legacy/PythonAI_Author_Lesson37_Lesson38.md)
- [Ноутбук із виконаними прикладами та графіками](legacy/PythonAI_Author_Lesson37_Lesson38.ipynb)
- [Автономний HTML для офлайн-перегляду](legacy/PythonAI_Author_Lesson37_Lesson38.html)
- [Приклади](PythonAI_Author_Lesson37_Lesson38/examples), [завдання](PythonAI_Author_Lesson37_Lesson38/tasks), [залежності](PythonAI_Author_Lesson37_Lesson38/requirements.txt)

Обов'язкові вправи без API й ключів. Ручні fixture-відповіді допомагають перевірити JSON
та каталог; вони не є вимірюваннями живої LLM. Нових бібліотек не потрібно.

## Пари 35–36 · від сегментів до рекомендацій · 240 хв

40 хв повторення пар 33–34, 100 хв TF-IDF/cosine, 100 хв рекомендацій за оцінками читачів.
10 завдань із підказками; усі приклади мають окремий Matplotlib-блок.

- [Маршрут і пояснення](legacy/PythonAI_Author_Lesson35_Lesson36.md)
- [Ноутбук із виконаними прикладами та графіками](legacy/PythonAI_Author_Lesson35_Lesson36.ipynb)
- [Самодостатній HTML для завантаження й офлайн-перегляду](legacy/PythonAI_Author_Lesson35_Lesson36.html)
- [Приклади](PythonAI_Author_Lesson35_Lesson36/examples), [завдання](PythonAI_Author_Lesson35_Lesson36/tasks), [власний requirements](PythonAI_Author_Lesson35_Lesson36/requirements.txt)

Усі дані локальні. Нових бібліотек у спільному середовищі не потрібно.

## Пари 33–34 · версія 2 · 240 хвилин

Місток із пар 31–32 — 40 хв, K-Means — 100 хв, DBSCAN — 100 хв.
Одна історія про магазин, 10 коротких завдань із покроковими підказками.

- [Почати читання: Markdown](legacy/PythonAI_Author_Lesson33_Lesson34_v2.md)
- [Виконувати код: ноутбук із виводом і графіками](legacy/PythonAI_Author_Lesson33_Lesson34_v2.ipynb)
- [Офлайн HTML: завантажте файл і відкрийте у браузері](legacy/PythonAI_Author_Lesson33_Lesson34_v2.html)

Нових залежностей немає; використовуйте спільне середовище нижче.
Попередня версія та її скрипти залишаються доступними.

Матеріали курсу «Штучний інтелект з використанням Python» (група Python61): презентації, приклади, завдання і домашні роботи.

## Середовище

Один спільний venv у корені:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Скрипти запускайте з папки відповідної пари, наприклад:

```bash
cd PythonAI_Author_Lesson31_Lesson32
python Lesson32_05_wine_map.py
```

У папках лишилися власні `requirements.txt` — вони потрібні, якщо хочете поставити залежності лише для однієї пари.

## Пари

| Папка | Модуль | Теми |
|---|---|---|
| `PythonAI61_Lesson1_Lesson2` | 1. Вступ | AI / DS / ML, датасети, Jupyter |
| `PythonAI61_Lesson3_Lesson4` | 2. Обробка даних | NumPy, pandas |
| `PythonAI61_Lesson5_Lesson6` | 2 | статистика, розподіли, кореляція |
| `PythonAI61_Lesson7_Lesson8` | 2 | Matplotlib |
| `PythonAI61_Lesson9_Lesson10` | 3. Навчання з учителем | регресія з однією змінною, метрики |
| `PythonAI61_Lesson11_Lesson12` | 3 | градієнтний спуск, множинна регресія, scikit-learn |
| `PythonAI61_Lesson13_Lesson14` | 3 | препроцесинг і валідація, регуляризація, дерева |
| `PythonAI61_Lesson15_Lesson16` | 4. Нейронні мережі | персептрон, PyTorch |
| `PythonAI61_Lesson16_Lesson17_Lesson18` | 4 | autograd, dropout, MLP |
| `PythonAI61_Lesson17_Lesson18_Lesson19_Lesson20` | 4 | активації, градієнти, кейс серцевих захворювань |
| `PythonAI_Author_Lesson21_Lesson22_Lesson23` | 5. Комп'ютерний зір | CNN, згортка, MNIST |
| `PythonAI_Author_Lesson23_Lesson24` | 5 | CNN для цифр, BatchNorm |
| `PythonAI_Author_Lesson25_Lesson26` | 5–6 | архітектури CNN, пневмонія, NLTK |
| `PythonAI_Author_Lesson27_Lesson28` | 6. NLP | корпуси, Word2Vec, GloVe |
| `PythonAI_Author_Lesson29_Lesson30` | 6 | RNN, LSTM, Transformer, transfer learning |
| `PythonAI_Author_Lesson31_Lesson32` | 7. Навчання без учителя | SVD, PCA, зниження розмірності |
| `PythonAI_Author_Lesson33_Lesson34` | 7 | кластеризація: K-Means, DBSCAN, сегментація клієнтів |

У кожній папці починайте з `START.txt` або `README.txt`, якщо вони є.

Пари 31–32 за один раз, з повторенням пар 28–30: [PythonAI_Author_Lesson31_Lesson32.md](legacy/PythonAI_Author_Lesson31_Lesson32.md) — маршрут на 90 + 90 хвилин, усі команди запускаються з кореня репозиторію. Той самий маршрут ноутбуком з виводом і рисунками: [PythonAI_Author_Lesson31_Lesson32.ipynb](legacy/PythonAI_Author_Lesson31_Lesson32.ipynb).

Пари 33–34 за один раз, з повторенням пар 31–32: [PythonAI_Author_Lesson33_Lesson34.md](legacy/PythonAI_Author_Lesson33_Lesson34.md) і ноутбук [PythonAI_Author_Lesson33_Lesson34.ipynb](legacy/PythonAI_Author_Lesson33_Lesson34.ipynb) — так само з кореня репозиторію.


Пари 39–40 з повторенням 37–38: [повний практикум](PythonAI_Author_Lesson39_Lesson40.html), [ноутбук](PythonAI_Author_Lesson39_Lesson40.ipynb), [усі файли](PythonAI_Author_Lesson39_Lesson40.zip). 30 + 100 + 100 хв; пояснення, приклади, окремі схеми, 16 самостійних завдань. Тільки безкоштовні інструменти; офлайн-варіант не потребує сервісів.

Повнота програми 39–40: [карта тем і завдань](PythonAI_Author_Lesson39_Lesson40/COVERAGE.md). [Повні промпти для Gemini або ChatGPT](PythonAI_Author_Lesson39_Lesson40/PROMPTS.md).
