"""Пара 25 · готова програма: прогноз NORMAL / PNEUMONIA за рентгенівським знімком.

Без аргументів перевіряє всі знімки з assets/xray/png/ (правильна відповідь — у назві файлу).
Можна передати свої PNG/JPG:

    python Lesson25_04_predict_xray.py
    python Lesson25_04_predict_xray.py мій_знімок.png
    python Lesson25_04_predict_xray.py --dir test_data/xray           # 60 тестових знімків + метрики
    python Lesson25_04_predict_xray.py --model pneumonia_cnn.pth      # своя модель з Lesson25_02

Це навчальна модель на знімках 64×64, а не медичний висновок.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from pneumonia_model import CLASSES, MODELS, XRAY, binary_metrics, load_checkpoint, png_to_tensor, print_metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Прогноз пневмонії за знімком")
    parser.add_argument("images", nargs="*", help="шляхи до PNG/JPG")
    parser.add_argument("--dir", help="папка зі знімками NORMAL_*.png / PNEUMONIA_*.png")
    parser.add_argument("--model", default=str(MODELS / "pneumonia_cnn.pth"))
    args = parser.parse_args()

    model, mean, std = load_checkpoint(Path(args.model))
    folder = Path(args.dir) if args.dir else XRAY / "png"
    paths = [Path(p) for p in args.images] or sorted(
        p for p in folder.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    if not paths:
        raise SystemExit("Немає знімків: передайте шлях до PNG/JPG")

    ok = known = 0
    truths, guesses = [], []
    print(f"{'файл':<26}{'прогноз':<12}{'P(PNEUMONIA)':>14}")
    for path in paths:
        with torch.no_grad():
            probs = torch.softmax(model(png_to_tensor(path, mean, std)), dim=1)[0]
        guess = CLASSES[int(probs.argmax())]
        mark = ""
        truth = next((c for c in CLASSES if path.stem.upper().startswith(c)), None)
        if truth:
            known += 1
            ok += int(truth == guess)
            truths.append(CLASSES.index(truth))
            guesses.append(CLASSES.index(guess))
            mark = "  ✓" if truth == guess else f"  ✗ (правда {truth})"
        print(f"{path.name:<26}{guess:<12}{float(probs[1]):>14.2f}{mark}")
    if known:
        print(f"\nзбіг з назвою файлу: {ok}/{known}\n")
        print_metrics(binary_metrics(torch.tensor(truths), torch.tensor(guesses)))
    print("Навчальна модель 64×64. Рішення про діагноз приймає лікар.")


if __name__ == "__main__":
    main()
