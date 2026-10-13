"""Спільний код пари 26: CNN для друкованих символів і нарізка картинки тексту на символи.

Алфавіт — великі латинські літери A–Z і цифри 0–9 (36 класів), як на бланках і табличках.
Кожен символ приводиться до 28×28 тією ж функцією normalize_glyph і в навчанні, і в розпізнаванні.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageFilter
from torch import nn

HERE = Path(__file__).resolve().parent
CHARS = HERE / "assets" / "chars"
TEXT_IMAGES = HERE / "assets" / "text_images"
MODELS = HERE / "models"
RESULTS = HERE / "results"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class CharCNN(nn.Module):
    """28×28 → 36 класів. Два згорткові блоки і два повнозвʼязні шари."""

    def __init__(self, n_classes: int = len(ALPHABET)) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 28 → 14
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),  # 14 → 7
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, n_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(self.features(x))


def load_checkpoint(path: Path) -> CharCNN:
    blob = torch.load(path, map_location="cpu")
    model = CharCNN(len(blob["alphabet"]))
    model.load_state_dict(blob["model_state"])
    model.eval()
    return model


def normalize_glyph(ink: np.ndarray) -> np.ndarray:
    """Вирізаний символ (світле чорнило на темному, будь-який розмір) → 28×28 uint8.

    Обрізаємо поля, вписуємо в 20×20 зі збереженням пропорцій, ставимо в центр.
    """
    ink = np.asarray(ink, dtype=np.float32)
    mask = ink > 0.2 * ink.max() if ink.max() > 0 else ink > 0
    if not mask.any():
        return np.zeros((28, 28), dtype=np.uint8)
    rows = np.where(mask.any(1))[0]
    cols = np.where(mask.any(0))[0]
    crop = ink[rows[0] : rows[-1] + 1, cols[0] : cols[-1] + 1]
    crop = 255.0 * crop / crop.max()
    h, w = crop.shape
    scale = 20.0 / max(h, w)
    new_w, new_h = max(1, round(w * scale)), max(1, round(h * scale))
    small = Image.fromarray(crop.astype(np.uint8)).resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("L", (28, 28), 0)
    canvas.paste(small, ((28 - new_w) // 2, (28 - new_h) // 2))
    return np.array(canvas, dtype=np.uint8)


def to_ink(path: Path) -> np.ndarray:
    """Картинка тексту → масив «чорнила» 0..255 (текст світлий, фон 0)."""
    img = Image.open(path).convert("L").filter(ImageFilter.MedianFilter(3))  # медіана прибирає поодинокі плями
    gray = np.array(img, dtype=np.float32)
    if np.median(gray) > 127:  # темний текст на світлому папері
        gray = 255.0 - gray
    threshold = otsu_threshold(gray)
    return np.where(gray > threshold, gray, 0.0)


def otsu_threshold(gray: np.ndarray) -> float:
    """Поріг, що найкраще ділить гістограму на «фон» і «чорнило» (метод Оцу)."""
    hist, edges = np.histogram(gray, bins=256, range=(0, 256))
    total = hist.sum()
    best, best_t = -1.0, 127.0
    cum, cum_mean = 0, 0.0
    all_mean = (hist * np.arange(256)).sum()
    for t in range(256):
        cum += hist[t]
        cum_mean += t * hist[t]
        if cum == 0 or cum == total:
            continue
        w0, w1 = cum / total, 1 - cum / total
        m0, m1 = cum_mean / cum, (all_mean - cum_mean) / (total - cum)
        between = w0 * w1 * (m0 - m1) ** 2
        if between > best:
            best, best_t = between, edges[t + 1]
    return float(best_t)


def runs(profile: np.ndarray, floor: float = 0.0) -> list[tuple[int, int]]:
    """Індекси [start, end) суцільних ділянок, де profile > floor."""
    on = np.concatenate([[False], profile > floor, [False]])
    edges = np.flatnonzero(on[1:] != on[:-1])
    return list(zip(edges[::2], edges[1::2]))


def space_threshold(gaps: list[int]) -> float:
    """Проміжки всередині слова дрібні, між словами — помітно більші.

    Сортуємо проміжки й шукаємо найбільший стрибок; якщо він менший ніж у 1.6 раза,
    у рядку одне слово і пробілів немає.
    """
    if len(gaps) < 2:
        return float("inf")
    ordered = sorted(gaps)
    ratios = [(ordered[i + 1] / max(ordered[i], 1), i) for i in range(len(ordered) - 1)]
    best, i = max(ratios)
    return (ordered[i] + ordered[i + 1]) / 2 if best >= 1.6 else float("inf")


def segment(ink: np.ndarray) -> list[list[tuple[np.ndarray, bool]]]:
    """Розрізати картинку на рядки, а рядки — на символи.

    Повертає список рядків; кожен рядок — список (glyph 28×28, space_before).
    Рядки шукаємо за горизонтальною проєкцією, символи — за вертикальною,
    пробіли — за ширшими за звичайні проміжками між символами.
    """
    lines = []
    rows = ink.sum(axis=1)
    for top, bottom in runs(rows, floor=0.02 * rows.max()):
        if bottom - top < 4:  # пил і шум
            continue
        line = ink[top:bottom]
        boxes = [
            (left, right)
            for left, right in runs(line.sum(axis=0))
            if line[:, left:right].sum() >= 255 * 6  # відкидаємо крихти, менші за кілька пікселів
        ]
        if not boxes:
            continue
        gaps = [boxes[i + 1][0] - boxes[i][1] for i in range(len(boxes) - 1)]
        cut = space_threshold(gaps)
        glyphs = [
            (normalize_glyph(line[:, left:right]), i > 0 and gaps[i - 1] > cut)
            for i, (left, right) in enumerate(boxes)
        ]
        lines.append(glyphs)
    return lines


LOOKALIKE_TO_LETTER = {"0": "O", "1": "I", "5": "S", "8": "B", "2": "Z"}
LOOKALIKE_TO_DIGIT = {v: k for k, v in LOOKALIKE_TO_LETTER.items()}


def fix_lookalikes(word: str) -> str:
    """O/0, I/1, S/5 часто однакові на вигляд. Якщо слово переважно з літер — цифри-двійники стають літерами, і навпаки."""
    letters = sum(c.isalpha() for c in word)
    digits = sum(c.isdigit() for c in word)
    if letters > digits:
        return "".join(LOOKALIKE_TO_LETTER.get(c, c) for c in word)
    if digits > letters:
        return "".join(LOOKALIKE_TO_DIGIT.get(c, c) for c in word)
    return word


def read_image(model: CharCNN, path: Path, fix: bool = True) -> str:
    """Повний OCR: картинка → рядки тексту."""
    out_lines = []
    for glyphs in segment(to_ink(path)):
        batch = torch.from_numpy(np.stack([g for g, _ in glyphs])).float().unsqueeze(1) / 255.0
        with torch.no_grad():
            idx = model(batch).argmax(1).tolist()
        text = ""
        for (_, space), i in zip(glyphs, idx):
            text += (" " if space else "") + ALPHABET[i]
        if fix:
            text = " ".join(fix_lookalikes(w) for w in text.split(" "))
        out_lines.append(text)
    return "\n".join(out_lines)


def edit_distance(a: str, b: str) -> int:
    """Відстань Левенштейна: скільки вставок / видалень / замін перетворюють a на b."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
