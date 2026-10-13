"""Пара 28 · Приклад задачі: тональність відгуку (pos / neg) через embeddings.

Відгук → середнє векторів його слів (100 чисел) → LogisticRegression.
Порівнюємо три способи перетворити текст на числа на тих самих 2000 відгуках movie_reviews:
TF-IDF (мішок слів), наш Word2Vec, готовий GloVe. Потім класифікуємо нові відгуки TextMind
з test_data/reviews_new.csv і ваш власний текст.

    python Lesson28_03_review_sentiment.py
    python Lesson28_03_review_sentiment.py --text "The battery is awful but the screen is great"
"""

from __future__ import annotations

import argparse
import csv

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from nlp_vectors import GLOVE, TEST_DATA, W2V, WORD_RE, clean_tokens, load_vectors, stopword_set


def load_reviews() -> tuple[list[list[str]], np.ndarray]:
    from nltk.corpus import movie_reviews

    docs, labels = [], []
    for label in ("neg", "pos"):
        for fid in movie_reviews.fileids(label):
            docs.append([w.lower() for w in movie_reviews.words(fid) if WORD_RE.fullmatch(w.lower())])
            labels.append(int(label == "pos"))
    return docs, np.array(labels)


def average(kv, docs: list[list[str]], stops: set[str]) -> np.ndarray:
    """Середній вектор слів документа; слова без вектора і стоп-слова пропускаємо."""
    out = np.zeros((len(docs), kv.vector_size), dtype=np.float32)
    for i, doc in enumerate(docs):
        known = [w for w in doc if w in kv.key_to_index and w not in stops]
        if known:
            out[i] = kv[known].mean(axis=0)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text")
    args = parser.parse_args()

    docs, y = load_reviews()
    stops = stopword_set()
    idx_train, idx_test = train_test_split(np.arange(len(docs)), test_size=0.25, stratify=y, random_state=28)
    print(f"movie_reviews: {len(docs)} відгуків, train {len(idx_train)}, test {len(idx_test)}\n")

    tfidf = TfidfVectorizer(min_df=3, stop_words=list(stops))
    x_tfidf = tfidf.fit_transform([" ".join(d) for d in docs])
    kvs = {"Word2Vec": load_vectors(W2V), "GloVe": load_vectors(GLOVE)}
    features = {
        "TF-IDF": x_tfidf,
        "Word2Vec avg": average(kvs["Word2Vec"], docs, stops),
        "GloVe avg": average(kvs["GloVe"], docs, stops),
    }
    print(f"{'ознаки':<14}{'розмір':>14}{'accuracy test':>15}")
    classifiers = {}
    for name, x in features.items():
        clf = LogisticRegression(max_iter=2000, C=1.0 if name == "TF-IDF" else 10.0)
        clf.fit(x[idx_train], y[idx_train])
        acc = clf.score(x[idx_test], y[idx_test])
        classifiers[name] = clf
        print(f"{name:<14}{str(x.shape):>14}{acc:>15.3f}")

    with (TEST_DATA / "reviews_new.csv").open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    texts = [r["text"] for r in rows] + ([args.text] if args.text else [])
    truth = [r["label"] for r in rows] + (["?"] if args.text else [])
    token_docs = [clean_tokens(t) for t in texts]
    preds = {
        "TF-IDF": classifiers["TF-IDF"].predict_proba(tfidf.transform([" ".join(d) for d in token_docs]))[:, 1],
        "W2V": classifiers["Word2Vec avg"].predict_proba(average(kvs["Word2Vec"], token_docs, stops))[:, 1],
        "GloVe": classifiers["GloVe avg"].predict_proba(average(kvs["GloVe"], token_docs, stops))[:, 1],
    }
    print(f"\n=== Нові відгуки TextMind (P(pos); ✓ — збіг з міткою)")
    print(f"{'TF-IDF':>8}{'W2V':>7}{'GloVe':>7}  мітка  текст")
    hits = dict.fromkeys(preds, 0)
    for i, text in enumerate(texts):
        cells = []
        for name, p in preds.items():
            guess = "pos" if p[i] >= 0.5 else "neg"
            ok = guess == truth[i]
            hits[name] += int(ok)
            cells.append(f"{p[i]:.2f}{'✓' if ok else ' ' if truth[i] == '?' else '✗'}")
        print(f"{cells[0]:>8}{cells[1]:>7}{cells[2]:>7}  {truth[i]:<5}  {text[:60]}")
    n = len(rows)
    print("\nвгадано з", n, ":", ", ".join(f"{k} {min(v, n)}" for k, v in hits.items()))
    print("Корпус для навчання — відгуки на фільми, а перевіряємо на відгуках про товари: це інший домен.")


if __name__ == "__main__":
    main()
