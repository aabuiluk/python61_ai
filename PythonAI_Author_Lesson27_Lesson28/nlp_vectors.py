"""Спільний код пар 27–28: корпуси, очищення тексту, завантаження векторів, косинус.

Корпуси й словники NLTK лежать у nltk_data/ пакета, GloVe — в assets/glove/,
наша модель Word2Vec — у models/. Інтернет не потрібен.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import nltk
import numpy as np

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "assets" / "corpus"
GLOVE = HERE / "assets" / "glove" / "glove_100d.bin"
MODELS = HERE / "models"
W2V = MODELS / "reviews_w2v.bin"
RESULTS = HERE / "results"
TEST_DATA = HERE / "test_data"

nltk.data.path.insert(0, str(HERE / "nltk_data"))

try:  # gensim швидший (код на C), але для Python 3.14 його ще немає
    from gensim.models import KeyedVectors, Word2Vec

    BACKEND = "gensim"
except ImportError:
    from word_vectors import KeyedVectors, Word2Vec

    BACKEND = "numpy"

# Параметри Word2Vec з практичного завдання 6.2
SHEET_W2V = dict(vector_size=100, window=5, min_count=1, sg=1)

WORD_RE = re.compile(r"[a-z]+(?:'[a-z]+)?")


def clean_tokens(text: str) -> list[str]:
    """Нижній регістр, без пунктуації й чисел: "Good, isn't it?" → ['good', "isn't", 'it']."""
    return WORD_RE.findall(text.lower())


def stopword_set() -> set[str]:
    from nltk.corpus import stopwords

    return set(stopwords.words("english"))


def small_corpus() -> list[list[str]]:
    """15 відгуків TextMind з assets/corpus/textmind_reviews.txt — один рядок = одне речення."""
    lines = (CORPUS / "textmind_reviews.txt").read_text(encoding="utf-8").splitlines()
    return [clean_tokens(line) for line in lines if line.strip()]


def big_corpus() -> list[list[str]]:
    """Відгуки на фільми (movie_reviews) + відгуки на товари (product_reviews_1/2) з NLTK.

    Близько 72 тисяч речень і 1,6 мільйона слів. Кожне речення — список слів без пунктуації.
    """
    from nltk.corpus import movie_reviews, product_reviews_1, product_reviews_2

    sents: list[list[str]] = []
    for reader in (movie_reviews, product_reviews_1, product_reviews_2):
        for sent in reader.sents():
            words = [w for w in (t.lower() for t in sent) if WORD_RE.fullmatch(w)]
            if len(words) > 1:
                sents.append(words)
    return sents


def word_counts(sents: list[list[str]]) -> Counter[str]:
    return Counter(w for s in sents for w in s)


def load_vectors(path: Path):
    """KeyedVectors у форматі word2vec binary (так зберігаємо і GloVe, і нашу модель)."""
    if not path.is_file():
        raise SystemExit(f"Немає {path.relative_to(HERE)} — запускайте з папки пакета")
    return KeyedVectors.load_word2vec_format(str(path), binary=True)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """cos = a·b / (|a|·|b|): 1 — той самий напрямок, 0 — перпендикулярні."""
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def print_neighbors(name: str, kv, words: list[str], topn: int = 5) -> None:
    print(f"--- {name}")
    print(f"{'слово':<10}  найближчі слова (косинусна схожість)")
    for w in words:
        if w not in kv.key_to_index:
            print(f"{w:<10}  немає у словнику моделі")
            continue
        near = ", ".join(f"{n} {s:.2f}" for n, s in kv.most_similar(w, topn=topn))
        print(f"{w:<10}  {near}")
    print()
