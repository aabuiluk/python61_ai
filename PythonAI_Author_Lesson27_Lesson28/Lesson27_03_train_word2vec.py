"""Пара 27 · Word2Vec: спершу параметри аркуша на 15 відгуках, потім справжній корпус.

1. Завдання 6.2.2: Word2Vec(vector_size=100, window=5, min_count=1, sg=1) на корпусі TextMind,
   вектор слова good. На 15 реченнях сусіди випадкові — це видно в таблиці.
2. Ті самі параметри, але min_count=5, на 73 тисячах речень відгуків (movie_reviews +
   product_reviews з NLTK). Порівнюємо Skip-gram (sg=1) і CBOW (sg=0): час, сусіди,
   кореляція з людськими оцінками схожості (test_data/wordsim353.tsv).
3. Зберігаємо вектори Skip-gram у файл (готова модель пакета — models/reviews_w2v.bin).

    python Lesson27_03_train_word2vec.py
    python Lesson27_03_train_word2vec.py --epochs 3          # швидше на слабкому ноутбуці
    python Lesson27_03_train_word2vec.py --out my_w2v.bin    # своя модель для Lesson28_*
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
from nlp_vectors import BACKEND, HERE, SHEET_W2V, Word2Vec, TEST_DATA, big_corpus, print_neighbors, small_corpus

PROBE = ["good", "bad", "quality", "battery", "funny"]


def wordsim(kv) -> tuple[float, float]:
    """Spearman між косинусом моделі й оцінками людей; частка пар, для яких є обидва слова."""
    pearson, spearman, oov = kv.evaluate_word_pairs(str(TEST_DATA / "wordsim353.tsv"))
    return float(spearman.statistic if hasattr(spearman, "statistic") else spearman[0]), 1 - oov / 100


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=10 if BACKEND == "gensim" else 1)
    parser.add_argument("--min-count", type=int, default=5)
    parser.add_argument("--out", default="reviews_w2v.bin")
    args = parser.parse_args()

    if BACKEND == "numpy":
        print("gensim не встановлено (Python 3.14?) — навчаємо Word2Vec на numpy: повільніше, 1 епоха, лише Skip-gram.")
        print("Швидша повна версія: Python 3.10–3.13 і pip install gensim.\n")
    print("=== 1. Аркуш 6.2: 15 відгуків TextMind")
    small = small_corpus()
    print(f"речень {len(small)}, середня довжина {np.mean([len(s) for s in small]):.1f} слова")
    print("перше речення:", small[0])
    tiny = Word2Vec(small, **SHEET_W2V, seed=27, workers=1, epochs=args.epochs)
    vec = tiny.wv["good"]
    print(f"model.wv['good'].shape = {vec.shape}, перші 5 чисел: {np.round(vec[:5], 3)}")
    print(f"model.wv['good'].shape = {vec.shape}, перші 50 чисел: {np.round(vec[:50], 3)}")
    print_neighbors("Word2Vec на 15 реченнях (сусіди майже випадкові)", tiny.wv, ["good", "bad", "quality"], 3)

    print("=== 2. Справжній корпус: відгуки з NLTK")
    t0 = time.time()
    sents = big_corpus()
    words = sum(len(s) for s in sents)
    print(f"речень {len(sents)}, слів {words}, завантаження {time.time() - t0:.0f} с\n")

    params = dict(SHEET_W2V, min_count=args.min_count)
    models = {}
    variants = ((1, "Skip-gram (sg=1)"), (0, "CBOW (sg=0)")) if BACKEND == "gensim" else ((1, "Skip-gram (sg=1)"),)
    for sg, name in variants:
        t0 = time.time()
        model = Word2Vec(sents, **dict(params, sg=sg), seed=27, workers=4, epochs=args.epochs)
        spent = time.time() - t0
        rho, covered = wordsim(model.wv)
        models[sg] = model
        print(f"{name}: словник {len(model.wv)} слів, навчання {spent:.0f} с, wordsim353 Spearman {rho:.2f}"
              f" (є слова для {covered:.0%} пар)")
        print_neighbors(name, model.wv, PROBE)

    out = Path(args.out)
    if not out.is_absolute():
        out = HERE / out
    out.parent.mkdir(parents=True, exist_ok=True)
    models[1].wv.save_word2vec_format(str(out), binary=True)
    print(f"Вектори Skip-gram збережено: {out.relative_to(HERE)} ({out.stat().st_size // 1024} КБ)")
    print("Повна модель (щоб довчати): model.save('reviews.model'); для пошуку схожих слів досить векторів.")


if __name__ == "__main__":
    main()
