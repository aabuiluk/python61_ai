"""Пара 27 · Корпуси в NLP: що всередині, скільки слів, закон Ципфа, корпус як список списків.

1. Три корпуси NLTK різного типу: Brown (жанри), movie_reviews (pos / neg), product_reviews (товари).
2. Частоти слів і закон Ципфа: результат у results/zipf.png.
3. Завдання 6.2.1: 15 відгуків TextMind → нижній регістр, без пунктуації → список списків,
   кількість речень і середня довжина.

    python Lesson27_01_corpus_explore.py
    python Lesson27_01_corpus_explore.py --no-plot
"""

from __future__ import annotations

import argparse

import numpy as np

from nlp_vectors import CORPUS, RESULTS, clean_tokens, small_corpus, stopword_set, word_counts


def describe(name: str, sents: list[list[str]], note: str) -> None:
    counts = word_counts(sents)
    total = sum(counts.values())
    once = sum(1 for n in counts.values() if n == 1)
    print(f"{name:<18}{len(sents):>8}{total:>11}{len(counts):>9}{once / len(counts):>9.0%}   {note}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()

    from nltk.corpus import brown, movie_reviews, product_reviews_1

    lower = lambda reader, **kw: [[w.lower() for w in s if w.isalpha()] for s in reader.sents(**kw)]  # noqa: E731
    print("=== 1. Корпуси NLTK")
    print(f"{'корпус':<18}{'речень':>8}{'слів':>11}{'словник':>9}{'1 раз':>9}")
    news = lower(brown, categories="news")
    describe("brown / news", news, "газети 1961 року")
    describe("brown / romance", lower(brown, categories="romance"), "любовні романи")
    reviews = lower(movie_reviews)
    describe("movie_reviews", reviews, "2000 відгуків на фільми, 1000 pos + 1000 neg")
    describe("product_reviews_1", lower(product_reviews_1), "відгуки на 5 товарів")
    print("\nЖанри Brown:", ", ".join(brown.categories()))
    print("Мітки movie_reviews:", movie_reviews.categories(), "· файл:", movie_reviews.fileids("pos")[0])
    print("Один відгук на товар з позначеними властивостями:")
    review = product_reviews_1.reviews("Canon_G3.txt")[0]
    for line in review.review_lines[:2]:
        print("  ", " ".join(line.sent[:14]), "→", line.features)

    print("\n=== 2. Частоти й закон Ципфа (movie_reviews)")
    counts = word_counts(reviews)
    stops = stopword_set()
    print("топ-10 усіх слів:      ", ", ".join(w for w, _ in counts.most_common(10)))
    content = [w for w, _ in counts.most_common(200) if w not in stops]
    print("топ-10 без стоп-слів:  ", ", ".join(content[:10]))
    freqs = np.array(sorted(counts.values(), reverse=True))
    for rank in (1, 10, 100, 1000):
        print(f"ранг {rank:>5}: частота {freqs[rank - 1]:>6}, ранг × частота = {rank * freqs[rank - 1]}")
    if not args.no_plot:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        ranks = np.arange(1, len(freqs) + 1)
        plt.figure(figsize=(6, 4))
        plt.loglog(ranks, freqs, label="movie_reviews")
        plt.loglog(ranks, freqs[0] / ranks, "--", label="частота ~ 1 / ранг")
        plt.xlabel("ранг слова")
        plt.ylabel("частота")
        plt.legend()
        plt.title("Закон Ципфа")
        RESULTS.mkdir(exist_ok=True)
        plt.tight_layout()
        plt.savefig(RESULTS / "zipf.png", dpi=120)
        print("графік:", RESULTS / "zipf.png")

    print("\n=== 3. Завдання 6.2.1: корпус TextMind")
    raw = (CORPUS / "textmind_reviews.txt").read_text(encoding="utf-8").splitlines()
    print("сирий рядок:   ", raw[0])
    print("після очищення:", clean_tokens(raw[0]))
    corpus = small_corpus()
    lengths = [len(s) for s in corpus]
    print(f"речень: {len(corpus)}, середня довжина: {np.mean(lengths):.1f} слова, від {min(lengths)} до {max(lengths)}")
    print("тип:", type(corpus).__name__, "of", type(corpus[0]).__name__, "— кожен підсписок = одне речення")


if __name__ == "__main__":
    main()
