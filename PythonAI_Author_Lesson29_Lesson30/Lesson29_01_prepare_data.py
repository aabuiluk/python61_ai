"""Пара 29 · крок 1 · завдання 6.3.1: дані для мовної моделі SupportFlow.

Текст → нижній регістр без пунктуації → токени → словник token-to-index → максимальні довжини → padding.

    python Lesson29_01_prepare_data.py           # 15 пар, як в аркуші 6.3
    python Lesson29_01_prepare_data.py --all     # усі 30 пар (обсяг домашнього 6.3)
"""

from __future__ import annotations

import argparse
import json

import supportflow as sf


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="усі 30 пар замість 15")
    args = parser.parse_args()
    rows = sf.load_pairs(limit=None if args.all else 15)

    print(f"1) {len(rows)} пар запит → відповідь (assets/supportflow_qa.csv)")
    for r in rows[:3]:
        print(f"   {r['question']!r} → {r['answer']!r}")
        print(f"   {sf.tokenize(r['question'])} → {sf.tokenize(r['answer'])}")

    pairs, vocab = sf.prepare(rows)
    print(f"\n2) Словник: {len(vocab)} токенів, з них 4 спеціальні")
    print("   " + ", ".join(f"{w}={i}" for i, w in enumerate(vocab.itos[:16])) + ", …")

    max_q = max(len(q) for q, _ in pairs)
    max_a = max(len(a) for _, a in pairs)
    longest = max(pairs, key=lambda p: len(p[1]))
    print(f"\n3) Максимальна довжина: запит {max_q} токенів, відповідь {max_a} токенів")
    print(f"   найдовша відповідь: {' '.join(longest[1])!r}")

    q, a = pairs[0]
    print("\n4) Кодування одного прикладу")
    print(f"   {'запит':<13}{q}")
    print(f"   {'індекси':<13}{vocab.encode(q, max_q)}      ← доповнено <pad>=0 до {max_q}")
    print(f"   {'вхід decoder':<13}{vocab.encode(a, max_a + 1, sos=True)}")
    print(f"   {'ціль decoder':<13}{vocab.encode(a, max_a + 1, eos=True)}")
    print(f"   {'назад':<13}{vocab.decode(vocab.encode(a, max_a + 1, eos=True))}")
    new = sf.tokenize("How can I reset my passcode?")
    print(f"   {'нове слово':<13}{new} → {vocab.encode(new)}   ← passcode → <unk>=1")

    src, tgt_in, tgt_out = sf.make_tensors(pairs, vocab, vocab)
    print(f"\n5) Тензори для навчання: src {tuple(src.shape)}, tgt_in {tuple(tgt_in.shape)}, tgt_out {tuple(tgt_out.shape)}")
    pads = (src == sf.PAD_ID).float().mean().item()
    print(f"   {pads:.0%} клітинок src — це <pad>. Їх не можна рахувати в loss і не варто пускати в RNN.")

    assert vocab.decode(vocab.encode(a, eos=True)) == a
    assert src.shape[1] == max_q and tgt_out.shape[1] == max_a + 1
    sf.RESULTS.mkdir(exist_ok=True)
    out = sf.RESULTS / "vocab.json"
    out.write_text(json.dumps({"max_q": max_q, "max_a": max_a, "itos": vocab.itos}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
    print(f"\nСловник збережено: {out.relative_to(sf.HERE)}")


if __name__ == "__main__":
    main()
