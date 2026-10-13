"""Пара 30 · готова програма: чат-бот SupportFlow на seq2seq LSTM + GloVe.

Модель уже навчена: models/supportflow_bot.pth (LSTM, embedding — заморожений GloVe з пари 28).
Без аргументів показує демо: запити з бази і нові формулювання, яких модель не бачила.

    python Lesson30_04_supportflow_bot.py
    python Lesson30_04_supportflow_bot.py "my parcel is lost" "how do i pay"
    python Lesson30_04_supportflow_bot.py --chat                 # діалог, вихід — порожній рядок
    python Lesson30_04_supportflow_bot.py --model models/supportflow_lstm.pth    # модель з Lesson30_01
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import supportflow as sf

DEMO = ["How can I reset my password?", "My order is delayed.", "i cannot remember my passcode",
        "what is the shipping price", "they took money from me two times", "my parcel is lost",
        "can you tell me a joke"]


def reply(model, train_words: set[str], query: str) -> None:
    start = time.perf_counter()
    text = sf.answer(model, query)
    ms = (time.perf_counter() - start) * 1000
    new = [w for w in sf.tokenize(query) if w not in train_words]
    print(f"Клієнт: {query}")
    print(f"Бот:    {text}   ({ms:.0f} мс)")
    if new:
        known = [w for w in new if w in model.src_vocab]
        print(f"        слів поза навчальними запитами: {', '.join(new)}; модель має для них вектори: {', '.join(known) or '—'}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("queries", nargs="*")
    parser.add_argument("--chat", action="store_true")
    parser.add_argument("--model", type=Path, default=sf.BOT)
    args = parser.parse_args()

    model = sf.load_model(args.model)
    pairs, _ = sf.prepare(sf.load_pairs())
    train_words = {t for q, _ in pairs for t in q}
    cfg = model.config
    print(f"Модель: {cfg['cell'].upper()}{' + GloVe' if cfg.get('glove') else ''}, "
          f"параметрів {sf.count_params(model):,}, словник запитів {len(model.src_vocab):,}, "
          f"відповідей {len(model.tgt_vocab)}\n".replace(",", " "))
    if args.chat:
        while query := input("Клієнт: ").strip():
            print(f"Бот:    {sf.answer(model, query)}\n")
        return
    for q in args.queries or DEMO:
        reply(model, train_words, q)
    if not args.queries:
        print("Дві останні відповіді хибні. «parcel is lost» — такої теми в 30 парах немає, а «joke» — взагалі не")
        print("про підтримку. Модель не вміє сказати «не знаю»: вона завжди складе відповідь зі слів, які бачила.")
        print("Це межа маленької seq2seq-моделі; великі моделі вчать відмовляти окремо.")


if __name__ == "__main__":
    main()
