"""Пара 28 · Завдання 6.2.3–6.2.4: таблиця сусідів, PCA 100D → 2D, порівняння Word2Vec і GloVe.

1. most_similar для good, bad, quality у нашому Word2Vec і в готовому GloVe → results/neighbors.csv
2. 20 найчастіших змістовних слів корпусу → матриця (20, 100) → PCA → scatter з підписами
   → results/word2vec_visualization.png (і glove_visualization.png для порівняння)
3. Які пари слів схожі в обох моделях одразу.

    python Lesson28_02_similarity_pca.py
    python Lesson28_02_similarity_pca.py --model my_w2v.bin      # своя модель з Lesson27_03
    python Lesson28_02_similarity_pca.py --words good bad price service
"""

from __future__ import annotations

import argparse
import csv
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from sklearn.decomposition import PCA  # noqa: E402

from nlp_vectors import GLOVE, HERE, RESULTS, W2V, big_corpus, load_vectors, stopword_set, word_counts  # noqa: E402


def scatter(kv, words: list[str], title: str, out: Path) -> None:
    x = np.stack([kv[w] for w in words])
    pca = PCA(n_components=2, random_state=28)
    xy = pca.fit_transform(x)
    plt.figure(figsize=(8, 6))
    plt.scatter(xy[:, 0], xy[:, 1], s=25)
    for (px, py), w in zip(xy, words):
        plt.annotate(w, (px, py), xytext=(4, 3), textcoords="offset points", fontsize=10)
    share = pca.explained_variance_ratio_.sum()
    plt.title(f"{title}: {x.shape} → 2D, PCA зберегла {share:.0%} дисперсії")
    plt.tight_layout()
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"{out.relative_to(HERE)}  матриця {x.shape}, дві компоненти пояснюють {share:.0%} дисперсії")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=str(W2V))
    parser.add_argument("--words", nargs="+", default=["good", "bad", "quality"])
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()

    models = {"Word2Vec": load_vectors(Path(args.model)), "GloVe": load_vectors(GLOVE)}
    RESULTS.mkdir(exist_ok=True)

    print("=== 1. Завдання 6.2.3: таблиця сусідів")
    rows = []
    for name, kv in models.items():
        print(f"--- {name}")
        print(f"{'цільове слово':<15}{'близькі слова':<36}косинусна схожість")
        for w in args.words:
            if w not in kv.key_to_index:
                print(f"{w:<15}немає у словнику")
                continue
            near = kv.most_similar(w, topn=3)
            print(f"{w:<15}{', '.join(n for n, _ in near):<36}{', '.join(f'{s:.2f}' for _, s in near)}")
            rows += [[name, w, n, round(s, 3)] for n, s in near]
        print()
    with (RESULTS / "neighbors.csv").open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows([["model", "word", "neighbor", "cosine"], *rows])
    print("таблиця:", (RESULTS / "neighbors.csv").relative_to(HERE), "\n")

    print(f"=== 2. Завдання 6.2.4: {args.top} найчастіших слів → PCA")
    stops = stopword_set() | {"s", "t", "film", "movie", "one"}
    common = [w for w, _ in word_counts(big_corpus()).most_common(500)
              if w not in stops and all(w in kv.key_to_index for kv in models.values())][: args.top]
    print("слова:", ", ".join(common))
    scatter(models["Word2Vec"], common, "Word2Vec", RESULTS / "word2vec_visualization.png")
    scatter(models["GloVe"], common, "GloVe", RESULTS / "glove_visualization.png")

    print("\n=== 3. Пари, схожі в обох моделях")
    pairs = []
    for a, b in combinations(common, 2):
        s1, s2 = (float(kv.similarity(a, b)) for kv in models.values())
        pairs.append((min(s1, s2), a, b, s1, s2))
    print(f"{'пара':<24}{'Word2Vec':>9}{'GloVe':>8}")
    for _, a, b, s1, s2 in sorted(pairs, reverse=True)[:8]:
        print(f"{a + ' – ' + b:<24}{s1:>9.2f}{s2:>8.2f}")


if __name__ == "__main__":
    main()
