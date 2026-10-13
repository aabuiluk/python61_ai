# python61_ai

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

У кожній папці починайте з `START.txt` або `README.txt`, якщо вони є.
