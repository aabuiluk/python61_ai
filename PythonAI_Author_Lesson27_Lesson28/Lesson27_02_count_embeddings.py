"""Пара 27 · Від one-hot до embedding: проміжні подання слова без нейромережі.

1. One-hot: кожне слово — вектор довжини словника з однією одиницею. Косинус між будь-якими
   двома різними словами = 0, тобто one-hot не знає, що good ближче до great, ніж до battery.
2. Матриця співпоявлень (хто з ким стоїть у вікні ±2) на 15 відгуках TextMind.
3. PPMI + SVD на корпусі відгуків: щільні 100-вимірні вектори з тієї самої ідеї
   «слово визначає його оточення». Це count-based embedding — прямий предок GloVe.

    python Lesson27_02_count_embeddings.py
    python Lesson27_02_count_embeddings.py --vocab 3000
"""

from __future__ import annotations

import argparse

import numpy as np
from sklearn.utils.extmath import randomized_svd

from nlp_vectors import big_corpus, cosine, small_corpus, word_counts


def cooccurrence(sents: list[list[str]], vocab: list[str], window: int) -> np.ndarray:
    """m[a, b] — скільки разів слова a і b стоять у межах window слів в одному реченні.

    Усі речення склеєні в один масив id; для кожного зсуву d беремо пари (i, i + d)
    з одного речення і рахуємо їх bincount — так у сотні разів швидше, ніж цикл по словах.
    """
    index = {w: i for i, w in enumerate(vocab)}
    ids = np.array([index.get(w, -1) for s in sents for w in s])
    sent_no = np.repeat(np.arange(len(sents)), [len(s) for s in sents])
    n = len(vocab)
    flat = np.zeros(n * n, dtype=np.float64)
    for d in range(1, window + 1):
        a, b = ids[:-d], ids[d:]
        keep = (a >= 0) & (b >= 0) & (sent_no[:-d] == sent_no[d:])
        flat += np.bincount(a[keep] * n + b[keep], minlength=n * n)
    m = flat.reshape(n, n).astype(np.float32)
    return m + m.T


def ppmi(m: np.ndarray) -> np.ndarray:
    """Positive PMI: наскільки частіше пара трапляється разом, ніж випадково (log), відʼємне → 0."""
    total = m.sum()
    row = m.sum(axis=1, keepdims=True)
    col = m.sum(axis=0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(m * total / (row @ col))
    return np.nan_to_num(np.maximum(pmi, 0), neginf=0.0)


def neighbors(word: str, vectors: np.ndarray, vocab: list[str], topn: int = 5) -> str:
    unit = vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-9)
    sims = unit @ unit[vocab.index(word)]
    best = [i for i in np.argsort(-sims) if vocab[i] != word][:topn]
    return ", ".join(f"{vocab[i]} {sims[i]:.2f}" for i in best)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vocab", type=int, default=5000)
    parser.add_argument("--dim", type=int, default=100)
    args = parser.parse_args()

    small = small_corpus()
    vocab = sorted({w for s in small for w in s})
    print(f"=== 1. One-hot на корпусі TextMind: словник {len(vocab)} слів")
    eye = np.eye(len(vocab))
    oh = {w: eye[vocab.index(w)] for w in ("good", "great", "battery")}
    print("one-hot('good') — довжина", len(oh["good"]), ", одиниця на позиції", vocab.index("good"))
    print(f"cos(good, great) = {cosine(oh['good'], oh['great']):.2f}   cos(good, battery) = {cosine(oh['good'], oh['battery']):.2f}")

    print("\n=== 2. Співпоявлення у вікні ±2 (15 відгуків)")
    m = cooccurrence(small, vocab, window=2)
    for w in ("good", "great", "bad"):
        row = m[vocab.index(w)]
        top = [f"{vocab[i]}×{int(row[i])}" for i in np.argsort(-row)[:6] if row[i] > 0]
        print(f"{w:<7} поруч: {', '.join(top)}")
    print(f"cos(good, great) за рядками матриці = {cosine(m[vocab.index('good')], m[vocab.index('great')]):.2f}"
          " — вже не нуль: у них спільні сусіди")
    print(f"cos(good, bad) за рядками матриці = {cosine(m[vocab.index('good')], m[vocab.index('bad')]):.2f}"
          " — вже не нуль: у них спільні сусіди")

    print(f"\n=== 3. PPMI + SVD на корпусі відгуків ({args.vocab} найчастіших слів)")
    sents = big_corpus()
    vocab = [w for w, _ in word_counts(sents).most_common(args.vocab)]
    m = cooccurrence(sents, vocab, window=4)
    print(f"матриця співпоявлень {m.shape}, ненульових клітинок {np.count_nonzero(m) / m.size:.1%}")
    u, s, _ = randomized_svd(ppmi(m), n_components=args.dim, random_state=27)  # лише 100 перших компонент
    vectors = u[:, : args.dim] * np.sqrt(s[: args.dim])
    print(f"щільні вектори: {vectors.shape} — кожне слово тепер {args.dim} чисел замість {len(vocab)}")
    for w in ("good", "bad", "quality", "battery", "funny"):
        print(f"{w:<8} {neighbors(w, vectors, vocab)}")


if __name__ == "__main__":
    main()
