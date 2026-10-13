"""Пара 28 · GloVe своїми руками на numpy: глобальна матриця співпоявлень → вектори.

Ідея GloVe (Pennington et al., 2014): для кожної пари слів (i, j), що траплялись разом X_ij разів,
підбираємо вектори так, щоб  w_i · w̃_j + b_i + b̃_j ≈ log X_ij.
Похибка зважена f(X_ij) = min(1, (X_ij / 100) ** 0.75): рідкі пари важать менше, часті не домінують.
Оптимізатор — AdaGrad, як в оригіналі; тут кожен крок бере всю матрицю одразу. Фінальний вектор слова = w + w̃.

Порівняння: Word2Vec вчиться на кожному вікні окремо (локально), GloVe — один раз
рахує всю матрицю співпоявлень корпусу (глобально) і вчиться на ній.

    python Lesson28_01_glove_from_scratch.py
    python Lesson28_01_glove_from_scratch.py --steps 100 --vocab 2000    # швидше
"""

from __future__ import annotations

import argparse
import time

import numpy as np

from Lesson27_02_count_embeddings import cooccurrence, neighbors
from nlp_vectors import GLOVE, big_corpus, load_vectors, print_neighbors, word_counts

PROBE = ["good", "bad", "quality", "battery", "funny"]


def train_glove(m: np.ndarray, dim: int, steps: int, lr: float = 0.1, seed: int = 28) -> np.ndarray:
    """Повний батч: уся матриця X за крок. Для словника в кілька тисяч слів це кілька матричних множень."""
    rng = np.random.default_rng(seed)
    n = m.shape[0]
    weight = np.minimum(1.0, (m / 100) ** 0.75).astype(np.float32)  # f(X); для X = 0 вага 0
    log_x = np.log(np.maximum(m, 1)).astype(np.float32)
    w = ((rng.random((n, dim)) - 0.5) / dim).astype(np.float32)  # вектори слів
    wc = ((rng.random((n, dim)) - 0.5) / dim).astype(np.float32)  # вектори контексту
    b, bc = np.zeros(n, np.float32), np.zeros(n, np.float32)
    params = [w, wc, b, bc]
    sq = [np.ones_like(p) for p in params]  # суми квадратів градієнтів для AdaGrad
    pairs = np.count_nonzero(m)
    for step in range(1, steps + 1):
        diff = w @ wc.T + b[:, None] + bc[None, :] - log_x
        g = weight * diff
        grads = [g @ wc, g.T @ w, g.sum(axis=1), g.sum(axis=0)]
        for p, s, grad in zip(params, sq, grads):
            s += grad**2
            p -= lr * grad / np.sqrt(s)
        if step == 1 or step % 50 == 0:
            print(f"крок {step:>3}: середня зважена похибка {float((g * diff).sum()) / 2 / pairs:.4f}")
    vectors = w + wc
    return vectors - vectors.mean(axis=0)  # прибираємо спільний для всіх слів напрямок


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vocab", type=int, default=4000)
    parser.add_argument("--dim", type=int, default=50)
    parser.add_argument("--steps", type=int, default=250)
    args = parser.parse_args()

    sents = big_corpus()
    vocab = [w for w, _ in word_counts(sents).most_common(args.vocab)]
    t0 = time.time()
    m = cooccurrence(sents, vocab, window=5)
    print(f"матриця X {m.shape}: {np.count_nonzero(m)} ненульових пар, {time.time() - t0:.0f} с")
    i, j = vocab.index("good"), vocab.index("movie")
    print(f"X[good, movie] = {m[i, j]:.0f} → ціль log X = {np.log(m[i, j]):.2f}\n")

    t0 = time.time()
    vectors = train_glove(m, args.dim, args.steps)
    print(f"навчання {time.time() - t0:.0f} с, вектори {vectors.shape}\n")
    print("--- наш GloVe (1,4 млн слів відгуків)")
    for w in PROBE:
        print(f"{w:<10}  {neighbors(w, vectors, vocab)}")
    print()
    print_neighbors("готовий GloVe 6B (6 млрд слів Wikipedia + новини)", load_vectors(GLOVE), PROBE)


if __name__ == "__main__":
    main()
