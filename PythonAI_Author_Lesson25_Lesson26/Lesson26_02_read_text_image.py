"""Пара 26 · готова програма: розпізнавання друкованого тексту з картинки (OCR).

Кроки: картинка → «чорнило» (поріг Оцу) → рядки → символи → CharCNN → текст.
Без аргументів читає всі assets/text_images/*.png і порівнює з еталоном *.txt
(CER — частка помилкових символів). Результат пише в results/ocr_<імʼя>.txt.

    python Lesson26_02_read_text_image.py
    python Lesson26_02_read_text_image.py моя_табличка.png
    python Lesson26_02_read_text_image.py --dir test_data/ocr       # 10 тестових картинок
    python Lesson26_02_read_text_image.py --no-fix            # без виправлення O/0, I/1, S/5
    python Lesson26_02_read_text_image.py --model ocr_char_cnn.pth   # своя модель з Lesson26_01
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ocr_model import MODELS, RESULTS, TEXT_IMAGES, edit_distance, load_checkpoint, read_image


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR друкованого тексту")
    parser.add_argument("images", nargs="*")
    parser.add_argument("--model", default=str(MODELS / "ocr_char_cnn.pth"))
    parser.add_argument("--dir", help="папка з картинками (поруч *.txt з еталоном — необовʼязково)")
    parser.add_argument("--no-fix", action="store_true")
    args = parser.parse_args()

    model = load_checkpoint(Path(args.model))
    folder = Path(args.dir) if args.dir else TEXT_IMAGES
    paths = [Path(p) for p in args.images] or sorted(folder.glob("*.png"))
    RESULTS.mkdir(exist_ok=True)
    errors = chars = 0
    for path in paths:
        text = read_image(model, path, fix=not args.no_fix)
        (RESULTS / f"ocr_{path.stem}.txt").write_text(text + "\n", encoding="utf-8")
        print(f"=== {path.name}")
        print(text)
        truth_path = path.with_suffix(".txt")
        if truth_path.is_file():
            truth = truth_path.read_text(encoding="utf-8").strip()
            dist = edit_distance(text, truth)
            errors += dist
            chars += len(truth)
            print(f"--- CER {dist / max(1, len(truth)):.3f}  ({dist} правок на {len(truth)} символів)")

            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            from nltk.stem import WordNetLemmatizer

            # 1. Нормалізуємо register
            text = text.lower()

            # 2. Розбиваємо text на tokens
            tokens = word_tokenize(text)

            # 3. Беремо stop-word list
            stop_words = set(stopwords.words("english"))

            # 4. Для sentiment залишаємо negation
            stop_words.discard("not")

            # 5. Залишаємо alphabetic tokens і прибираємо stop words
            filtered = [
                token
                for token in tokens
                if token.isalpha() and token not in stop_words
            ]

            # 6. Lemmatization
            lemmatizer = WordNetLemmatizer()

            lemmas = [
                lemmatizer.lemmatize(token)
                for token in filtered
            ]

            print(f" {lemmas}")
        print()
    if chars:
        print(f"Разом CER {errors / chars:.3f}. Тексти збережено в {RESULTS}/ocr_*.txt")
        print("Далі: python Lesson26_03_nltk_pipeline.py")


if __name__ == "__main__":
    main()
