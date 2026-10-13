"""Пара 28 → 29 · передумова: що вміють вектори слів і де вони зупиняються.

1. Сусіди слів служби підтримки в GloVe — повторення пари 28.
2. Бот-пошуковик: середній вектор GloVe запиту → найближчий запит із бази → його відповідь.
3. Межа: середній вектор не бачить порядку слів. Саме тому далі — RNN, LSTM і Transformer.

    python Lesson28_05_words_to_sequences.py
    python Lesson28_05_words_to_sequences.py "my parcel is lost"     # свій запит до пошуковика
"""

from __future__ import annotations

import sys

import numpy as np

import supportflow as sf

# Короткі службові слова майже не несуть змісту, але сильно зсувають середній вектор
STOP = set("a an the i my me you your is are am was do does did can could how what when where which "
           "to of in on for it its and or be have has with at from this that there any".split())


class Glove:
    def __init__(self) -> None:
        words, vectors = sf.load_glove()
        self.index = {w: i for i, w in enumerate(words)}
        self.words = words
        self.unit = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    def neighbors(self, word: str, topn: int = 5) -> list[tuple[str, float]]:
        sims = self.unit @ self.unit[self.index[word]]
        best = np.argsort(-sims)[1:topn + 1]
        return [(self.words[i], float(sims[i])) for i in best]

    def sentence(self, text: str, stop: set[str] = STOP) -> np.ndarray:
        """Середній вектор слів речення (без службових слів і слів, яких GloVe не знає)."""
        rows = [self.unit[self.index[w]] for w in sf.tokenize(text) if w in self.index and w not in stop]
        return np.mean(rows, axis=0) if rows else np.zeros(self.unit.shape[1], dtype=np.float32)


def make_search(glove: Glove, rows: list[dict]):
    """Пошуковик: запит → найближчий за косинусом запит із бази → (рядок бази, схожість)."""
    base = np.vstack([glove.sentence(r["question"]) for r in rows])
    base /= np.linalg.norm(base, axis=1, keepdims=True) + 1e-12

    def search(query: str) -> tuple[dict, float]:
        v = glove.sentence(query)
        sims = base @ v / (np.linalg.norm(v) + 1e-12)
        best = int(np.argmax(sims))
        return rows[best], float(sims[best])

    return search


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


def main() -> None:
    glove = Glove()
    print(f"GloVe: {len(glove.words)} слів по 100 чисел\n")

    print("1) Сусіди слів служби підтримки")
    for word in ("password", "order", "refund", "delivery", "late"):
        print(f"   {word:<10}" + ", ".join(f"{w} {s:.2f}" for w, s in glove.neighbors(word)))

    print("\n2) Бот-пошуковик: найближчий запит з бази SupportFlow")
    search = make_search(glove, sf.load_pairs())

    queries = sys.argv[1:] or [q for q, _ in sf.load_paraphrases()]
    hits = 0
    paraphrases = dict(sf.load_paraphrases())
    for q in queries:
        row, sim = search(q)
        ok = paraphrases.get(q) == row["answer"]
        hits += ok
        mark = "" if q not in paraphrases else ("✓" if ok else "✗")
        print(f"   {q:<36}→ {row['question']:<36} {sim:.2f} {mark}")
    if not sys.argv[1:]:
        print(f"   Влучань: {hits} з {len(queries)}. Жодного з цих запитів немає в базі дослівно.")

    print("\n3) Межа середнього вектора: порядок слів зникає")
    for a, b in [("you can cancel it", "can you cancel it"),
                 ("the order is not delayed", "not the order is delayed"),
                 ("refund before delivery", "delivery before refund")]:
        va, vb = glove.sentence(a, stop=set()), glove.sentence(b, stop=set())
        print(f"   cos({a!r}, {b!r}) = {cosine(va, vb):.3f}")
    print("\n   Зміст різний, вектор однаковий. Відповідь теж треба писати слово за словом у правильному порядку.")
    print("   Тому на парі 29 текст стає послідовністю індексів, а модель читає її крок за кроком.")


if __name__ == "__main__":
    main()
