"""Пара 31 · крок 4: навіщо саме TruncatedSVD — розріджені таблиці й текст.

TF-IDF запитів SupportFlow (пари 29–30) → розріджена матриця → TruncatedSVD → «теми» (LSA).
TruncatedSVD не центрує дані, тому нулі лишаються нулями.

    python Lesson31_04_svd_text.py
    python Lesson31_04_svd_text.py "i lost my password"
"""

from __future__ import annotations

import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import dimred as dr


def same_topic_share(vectors, topics: list[str]) -> float:
    """Частка рядків, у яких найближчий сусід (косинус) має ту саму тему."""
    sim = cosine_similarity(vectors)
    np.fill_diagonal(sim, -1)
    nearest = sim.argmax(axis=1)
    return float(np.mean([topics[i] == topics[j] for i, j in enumerate(nearest)]))


def main() -> None:
    rows = dr.load_questions()
    texts = [f"{r['question']} {r['answer']}" for r in rows]
    topics = [r["topic"] for r in rows]

    tfidf = TfidfVectorizer(stop_words="english")
    x = tfidf.fit_transform(texts)
    words = tfidf.get_feature_names_out()
    density = x.nnz / (x.shape[0] * x.shape[1])
    print(f"1) TF-IDF: {x.shape[0]} текстів × {x.shape[1]} слів, ненульових клітинок {x.nnz} ({density:.1%})")
    centered = x.toarray() - x.toarray().mean(axis=0)
    print(f"   якщо відняти середнє стовпців (як робить PCA), ненульових стане {np.count_nonzero(centered)} "
          f"({np.count_nonzero(centered) / centered.size:.0%})")
    print("   на 100 000 документів × 50 000 слів така матриця не влізе в памʼять. TruncatedSVD її не центрує.")

    svd = TruncatedSVD(n_components=10, random_state=dr.SEED)
    z = svd.fit_transform(x)
    print(f"\n2) TruncatedSVD: {x.shape} → {z.shape}. Кожна компонента — «тема», суміш слів")
    for i in range(3):
        top = np.argsort(-np.abs(svd.components_[i]))[:5]
        print(f"   компонента {i + 1}: " + ", ".join(words[j] for j in top))

    print("\n3) Найближчий сусід має ту саму тему (12 тем, 30 текстів)")
    print(f"   TF-IDF, {x.shape[1]} чисел на текст: {same_topic_share(x, topics):.0%}")
    for k in (2, 5, 10):
        print(f"   SVD, k={k:<2} {' ' * 14}{same_topic_share(z[:, :k], topics):.0%}")
    print("   10 чисел замість 107 — і майже та сама якість. Двох чисел для 12 тем замало.")

    queries = sys.argv[1:] or ["i lost my password", "when will my parcel arrive"]
    print("\n4) Пошук у стиснутому просторі (10 вимірів)")
    for q in queries:
        qz = svd.transform(tfidf.transform([q]))
        best = int(cosine_similarity(qz, z)[0].argmax())
        print(f"   {q!r} → [{topics[best]}] {rows[best]['question']}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(z[:, 0], z[:, 1], s=30, color=dr.COLORS[0])
    for (px, py), topic in zip(z[:, :2], topics):
        ax.annotate(topic, (px, py), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_title("SVD Projection · запити SupportFlow")
    ax.set_xlabel("SVD-1")
    ax.set_ylabel("SVD-2")
    ax.grid(alpha=0.25)
    print(f"\nКарта текстів: {dr.rel(dr.save(fig, 'svd_text_map.png'))}")
    print("Той самий прийом на парі 28 робив PCA над векторами слів. Тут SVD працює прямо з таблицею частот.")


if __name__ == "__main__":
    main()
