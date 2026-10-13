"""Пара 28 · готова програма: дослідник слів. Сусіди, схожість, аналогії — у Word2Vec і GloVe поруч.

Без аргументів показує демо. Моделі вже лежать у пакеті: models/reviews_w2v.bin (наш Word2Vec
на відгуках) і assets/glove/glove_100d.bin (GloVe 6B, 100 вимірів).

    python Lesson28_04_word_explorer.py
    python Lesson28_04_word_explorer.py good price funny            # сусіди слів
    python Lesson28_04_word_explorer.py --pair good great            # косинус пари
    python Lesson28_04_word_explorer.py --analogy king man woman     # king − man + woman = ?
    python Lesson28_04_word_explorer.py --eval                       # оцінка на test_data/
    python Lesson28_04_word_explorer.py --model my_w2v.bin good      # своя модель з Lesson27_03
"""

from __future__ import annotations

import argparse
from pathlib import Path

from nlp_vectors import GLOVE, TEST_DATA, W2V, load_vectors, print_neighbors


def analogy(name: str, kv, a: str, b: str, c: str) -> None:
    missing = [w for w in (a, b, c) if w not in kv.key_to_index]
    if missing:
        print(f"{name:<9} немає слів: {', '.join(missing)}")
        return
    best = kv.most_similar(positive=[a, c], negative=[b], topn=3)
    print(f"{name:<9} {a} − {b} + {c} ≈ " + ", ".join(f"{w} {s:.2f}" for w, s in best))


def evaluate(name: str, kv) -> None:
    _, spearman, oov = kv.evaluate_word_pairs(str(TEST_DATA / "wordsim353.tsv"))
    score, sections = kv.evaluate_word_analogies(str(TEST_DATA / "analogies.txt"))
    print(f"--- {name}: словник {len(kv)} слів")
    print(f"wordsim353: Spearman з оцінками людей {spearman.statistic:.2f}, немає слів для {oov:.0f}% пар")
    for sec in sections[:-1]:
        total = len(sec["correct"]) + len(sec["incorrect"])
        print(f"  аналогії {sec['section']:<26} {len(sec['correct']):>3} / {total}")
    print(f"  аналогії разом {score:.0%}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Дослідник слів: Word2Vec і GloVe")
    parser.add_argument("words", nargs="*")
    parser.add_argument("--pair", nargs=2, metavar=("A", "B"))
    parser.add_argument("--analogy", nargs=3, metavar=("A", "B", "C"))
    parser.add_argument("--eval", action="store_true")
    parser.add_argument("--model", default=str(W2V))
    args = parser.parse_args()

    models = {"Word2Vec": load_vectors(Path(args.model)), "GloVe": load_vectors(GLOVE)}
    demo = not (args.words or args.pair or args.analogy or args.eval)
    words = [w.lower() for w in args.words] or (["good", "quality", "battery", "funny"] if demo else [])
    pair = args.pair or (["good", "great"] if demo else None)
    triple = args.analogy or (["king", "man", "woman"] if demo else None)

    for name, kv in models.items():
        if words:
            print_neighbors(name, kv, words)
    if pair:
        a, b = (w.lower() for w in pair)
        for name, kv in models.items():
            ok = a in kv.key_to_index and b in kv.key_to_index
            print(f"{name:<9} cos({a}, {b}) = " + (f"{kv.similarity(a, b):.2f}" if ok else "немає слова"))
        print()
    if triple:
        for name, kv in models.items():
            analogy(name, kv, *(w.lower() for w in triple))
        print()
    if args.eval:
        for name, kv in models.items():
            evaluate(name, kv)
    if demo:
        print("Своє слово: python Lesson28_04_word_explorer.py price  ·  оцінка: --eval")


if __name__ == "__main__":
    main()
