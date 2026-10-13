"""
Пара 29 · Завдання 1 · Власний набір даних і словник.

Скрипт:
1. Створює my_qa.csv із запитаннями та відповідями кафе FoodExpress.
2. Завантажує дані через supportflow.
3. Створює словник токенів.
4. Знаходить 10 найчастіших слів без стоп-слів.
5. Створює тензори для навчання Seq2seq.
6. Перевіряє правильність результатів через assert.

Запуск:
    python pair29_task1.py

Залежності:
    pip install torch nltk
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import nltk
import torch

from nltk.corpus import stopwords

import supportflow as sf


# ============================================================
# 1. НАБІР ДАНИХ
# ============================================================

MY_QA = [
    ("menu", "What is on the menu today?", "Today we have pasta, soup and three salads."),
    ("menu", "Do you have vegan dishes?", "Yes. Every vegan dish has a green leaf icon."),

    ("order", "Where is my food?", "Your courier is on the way. Track it in the app."),
    ("order", "My food is cold.", "We are sorry. We will send a new meal for free."),
    ("order", "Can I change my order?", "Yes, within five minutes after you place it."),
    ("order", "Something is missing from my bag.", "Please send a photo and we will refund the item."),

    ("payment", "Can I pay with cash?", "Yes. Choose cash when you place the order."),
    ("payment", "I was charged twice.", "We will check the payment and refund the extra charge."),

    ("delivery", "How long does delivery take?", "Delivery takes thirty to forty minutes."),
    ("delivery", "Is delivery free?", "Delivery is free for orders over twenty dollars."),

    ("account", "How do I change my phone number?", "Open the profile and update the phone number."),

    ("hours", "When do you open?", "We open every day at nine in the morning."),
    ("hours", "Do you work at night?", "Yes. We deliver until two in the morning."),

    ("support", "I want to talk to a manager.", "A manager will call you in ten minutes."),
]


PATH = Path("my_qa.csv")


# ============================================================
# 2. СТВОРЕННЯ CSV
# ============================================================

def write_csv() -> None:
    """Створює CSV з оригінальними запитаннями та відповідями."""

    with PATH.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as fh:

        writer = csv.writer(fh)

        writer.writerow([
            "id",
            "topic",
            "question",
            "answer"
        ])

        for i, row in enumerate(MY_QA, start=1):
            writer.writerow([i, *row])

    print(f"CSV створено: {PATH.resolve()}")


# ============================================================
# 3. ЗАВАНТАЖЕННЯ СТОП-СЛІВ
# ============================================================

def get_stop_words() -> set[str]:
    """Повертає набір англійських стоп-слів."""

    try:
        words = stopwords.words("english")

    except LookupError:
        print("Завантаження англійських стоп-слів NLTK...")
        nltk.download("stopwords", quiet=True)
        words = stopwords.words("english")

    result = set(words)

    # Залишаємо заперечення, оскільки вони змінюють зміст.
    result.discard("not")
    result.discard("no")
    result.discard("nor")

    return result


# ============================================================
# 4. ПІДРАХУНОК НАЙЧАСТІШИХ СЛІВ
# ============================================================

def count_frequent_words(
    pairs,
    stop_words: set[str]
) -> Counter:

    """
    Підраховує частоти слів у запитаннях і відповідях.

    Стоп-слова не враховуються лише в статистиці.
    Оригінальні дані для Seq2seq залишаються незмінними.
    """

    counts = Counter(
        token.lower()
        for question, answer in pairs
        for token in question + answer
        if token.isalpha()
        and token.lower() not in stop_words
    )

    return counts


# ============================================================
# 5. ОСНОВНА ПРОГРАМА
# ============================================================

def main() -> None:

    # КРОК 1. Створюємо CSV
    write_csv()

    # КРОК 2. Завантажуємо запитання та відповіді
    rows = sf.load_pairs(PATH)

    # КРОК 3. Створюємо токенізовані пари та словник
    pairs, vocab = sf.prepare(rows)

    # КРОК 4. Отримуємо стоп-слова
    stop_words = get_stop_words()

    # КРОК 5. Рахуємо частоти без стоп-слів
    counts = count_frequent_words(
        pairs,
        stop_words
    )

    # КРОК 6. Знаходимо максимальні довжини
    max_q = max(
        len(question)
        for question, _ in pairs
    )

    max_a = max(
        len(answer)
        for _, answer in pairs
    )

    # КРОК 7. Створюємо тензори
    src, tgt_in, tgt_out = sf.make_tensors(
        pairs,
        vocab,
        vocab
    )

    # КРОК 8. Рахуємо частку PAD у вхідних даних
    pads = (
        (src == sf.PAD_ID)
        .float()
        .mean()
        .item()
    )

    # ========================================================
    # 6. ВИВЕДЕННЯ РЕЗУЛЬТАТІВ
    # ========================================================

    print("\n" + "=" * 60)
    print("СТАТИСТИКА НАБОРУ ДАНИХ")
    print("=" * 60)

    print(f"Кількість пар: {len(pairs)}")
    print(f"Розмір словника: {len(vocab)} токенів")

    print("\n10 НАЙЧАСТІШИХ СЛІВ БЕЗ СТОП-СЛІВ:")

    for i, (word, count) in enumerate(
        counts.most_common(10),
        start=1
    ):
        print(f"{i:2}. {word:15} — {count}")

    print("\nДОВЖИНИ ПОСЛІДОВНОСТЕЙ:")

    print(f"Максимальна довжина запитання: {max_q}")
    print(f"Максимальна довжина відповіді: {max_a}")
    print(f"Частка PAD у src: {pads:.0%}")

    print("\nРОЗМІРИ ТЕНЗОРІВ:")

    print(f"src.shape:     {tuple(src.shape)}")
    print(f"tgt_in.shape:  {tuple(tgt_in.shape)}")
    print(f"tgt_out.shape: {tuple(tgt_out.shape)}")

    # ========================================================
    # 7. ПЕРЕВІРКИ
    # ========================================================

    # Перевіряємо правильність кодування та декодування.
    for _, answer in pairs:
        assert vocab.decode(
            vocab.encode(answer, eos=True)
        ) == answer

    # Невідоме слово повинно отримувати UNK_ID.
    assert vocab.encode(["spaceship"]) == [
        sf.UNK_ID
    ]

    # Перевіряємо розміри тензорів.
    assert src.shape == (
        len(pairs),
        max_q
    )

    assert tgt_out.shape == (
        len(pairs),
        max_a + 1
    )

    # Перевіряємо спеціальні токени.
    assert vocab.itos[:4] == [
        "<pad>",
        "<unk>",
        "<sos>",
        "<eos>"
    ]

    # Кожна вхідна послідовність декодера
    # повинна починатися з SOS.
    assert torch.all(
        tgt_in[:, 0] == sf.SOS_ID
    )

    print("\nУсі assert пройдено ✓")

    # ========================================================
    # 8. ВИСНОВОК
    # ========================================================

    print("\nВИСНОВОК:")

    print(
        "Довга відповідь збільшує max_len і додає "
        "багато PAD до коротших відповідей."
    )

    print(
        "Можливе рішення — обмежувати довжину "
        "за 95-м перцентилем або розбивати "
        "надто довгі відповіді."
    )

    print(
        "Важливо: під час обрізання потрібно "
        "зберігати коректне завершення послідовності."
    )


# ============================================================
# 9. ТОЧКА ВХОДУ
# ============================================================

if __name__ == "__main__":
    main()