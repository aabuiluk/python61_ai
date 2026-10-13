"""Пара 26 · NLTK на розпізнаному тексті: токенізація, стоп-слова, стемінг, лематизація, частоти.

Бере results/ocr_*.txt (після Lesson26_02_read_text_image.py). Якщо їх немає —
еталонні тексти assets/text_images/*.txt. Можна передати свій текст через --text.

Словники NLTK (stopwords, wordnet, punkt_tab) уже лежать у nltk_data/ — інтернет не потрібен.

    python Lesson26_03_nltk_pipeline.py
    python Lesson26_03_nltk_pipeline.py --text "The batteries were charging slowly"
    python Lesson26_03_nltk_pipeline.py --truth          # еталонні тексти замість OCR
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

from ocr_model import HERE, RESULTS, TEXT_IMAGES

nltk.data.path.insert(0, str(HERE / "nltk_data"))


def tokenize(text: str) -> list[str]:
    try:
        return nltk.word_tokenize(text)
    except LookupError:  # немає punkt_tab — простий регулярний вираз
        return RegexpTokenizer(r"[A-Za-z0-9']+|[^\sA-Za-z0-9]").tokenize(text)


def stopword_set() -> set[str]:
    try:
        from nltk.corpus import stopwords

        return set(stopwords.words("english"))
    except LookupError:
        return {"the", "a", "an", "and", "or", "is", "was", "are", "were", "it", "to", "of", "in", "on", "for", "but"}


def lemmatize(lemmatizer: WordNetLemmatizer | None, word: str) -> str:
    if lemmatizer is None:
        return word
    as_verb = lemmatizer.lemmatize(word, pos="v")
    return as_verb if as_verb != word else lemmatizer.lemmatize(word, pos="n")


def in_wordnet(word: str) -> bool | None:
    """Чи є слово (або його лема) у WordNet; None, якщо WordNet недоступний."""
    try:
        from nltk.corpus import wordnet

        return bool(wordnet.synsets(word)) or word in stopword_set()
    except LookupError:
        return None


def load_texts(use_truth: bool, text: str | None) -> list[tuple[str, str]]:
    if text:
        return [("--text", text)]
    ocr = sorted(RESULTS.glob("ocr_*.txt"))
    if ocr and not use_truth:
        return [(p.name, p.read_text(encoding="utf-8")) for p in ocr]
    if not use_truth:
        print("results/ocr_*.txt ще немає — беру еталонні тексти (спершу запустіть Lesson26_02)\n")
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(TEXT_IMAGES.glob("*.txt"))]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text")
    parser.add_argument("--truth", action="store_true")
    args = parser.parse_args()

    stops = stopword_set()
    stemmer = PorterStemmer()
    try:
        lemmatizer = WordNetLemmatizer()
        lemmatizer.lemmatize("tests")
    except LookupError:
        print("WordNet не знайдено — лематизацію пропущено")
        lemmatizer = None

    freq: Counter[str] = Counter()
    for name, text in load_texts(args.truth, args.text):
        tokens = tokenize(text.lower())
        words = [t for t in tokens if t.isalpha()]
        content = [w for w in words if w not in stops]
        print(f"=== {name}")
        print(f"токенів {len(tokens)}, слів {len(words)}, без стоп-слів {len(content)}")
        print(f"{'слово':<14}{'стем (Porter)':<16}{'лема (WordNet)':<16}{'у WordNet':<10}")
        unknown = []
        for i, w in enumerate(content):
            known = in_wordnet(w)
            if known is False:
                unknown.append(w)
            if i < 12:
                mark = {True: "так", False: "НІ", None: "?"}[known]
                print(f"{w:<14}{stemmer.stem(w):<16}{lemmatize(lemmatizer, w):<16}{mark:<10}")
        if unknown:
            print("невідомі слова (часто це помилки OCR):", ", ".join(unknown))
        print()
        freq.update(lemmatize(lemmatizer, w) for w in content)

    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / "word_freq.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["lemma", "count"])
        writer.writerows(freq.most_common())
    print("Топ-10 лем:", ", ".join(f"{w}×{n}" for w, n in freq.most_common(10)))
    print("Частоти:", out)


if __name__ == "__main__":
    main()
