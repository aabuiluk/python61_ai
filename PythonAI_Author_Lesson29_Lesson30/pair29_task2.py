"""Пара 29 · завдання 2 · еталон: RNN з аркуша — one-hot чи Embedding, скільки епох, ignore_index.

Запуск з папки пакета:  python pair29_task2.py      (~10 с)
"""

from __future__ import annotations

import supportflow as sf

CHECKPOINTS = (10, 50, 100, 200)


def run(vocab, src, tgt_in, tgt_out, items, **kw):
    ignore_pad = kw.pop("ignore_pad", True)
    sf.set_seed(0)
    model = sf.Seq2Seq(vocab, vocab, cell="rnn", hidden=128, **kw)
    fit = sf.train(model, src, tgt_in, tgt_out, epochs=max(CHECKPOINTS), ignore_pad=ignore_pad)
    return model, fit, sf.evaluate(model, items)["exact"]


def main() -> None:
    rows = sf.load_pairs(limit=15)
    pairs, vocab = sf.prepare(rows)
    src, tgt_in, tgt_out = sf.make_tensors(pairs, vocab, vocab)
    items = [(r["question"], r["answer"]) for r in rows]

    table = []
    variants = {"one-hot (аркуш)": dict(one_hot=True),
                "Embedding 32": dict(one_hot=False, emb_dim=32),
                "Embedding 32, без ignore_index": dict(one_hot=False, emb_dim=32, ignore_pad=False)}
    results = {}
    for name, kw in variants.items():
        model, fit, exact = run(vocab, src, tgt_in, tgt_out, items, **kw)
        results[name] = (model, fit)
        h = fit["history"]
        table.append([name, sf.count_params(model)] + [f"{h[e - 1]:.3f}" for e in CHECKPOINTS]
                     + [f"{fit['seconds']:.1f} с", f"{exact:.0%}"])
    sf.print_table(["модель", "параметрів"] + [f"loss@{e}" for e in CHECKPOINTS] + ["час", "exact"], table,
                   [32, 12, 10, 10, 10, 10, 8, 7])

    model = results["Embedding 32, без ignore_index"][0]
    print("\nвідповіді моделі без ignore_index:")
    for q in ("How can I reset my password?", "Where is my order?"):
        print(f"   {q:<30}→ {sf.answer(model, q)}")
    pad_share = (tgt_out == sf.PAD_ID).float().mean().item()
    with_pad = results["Embedding 32, без ignore_index"][1]["history"]
    without = results["Embedding 32"][1]["history"]
    print(f"\n3) {pad_share:.0%} позицій tgt_out — це <pad>. loss@100: {without[99]:.3f} з ignore_index і "
          f"{with_pad[99]:.3f} без нього.")
    print("   Без ignore_index loss — середнє по всіх позиціях разом з <pad>: на початку модель витрачає сили,")
    print("   щоб навчитися ставити <pad> після <eos>, а потім отримує за них майже нульову помилку.")
    print("   Це дві різні формули, тому порівнювати ці числа нечесно — порівнюйте відповіді й exact.")
    print("   Відповіді однакові, бо generate зупиняється на <eos> і до <pad> не доходить.")
    print("\nВисновок")
    print("   • 10 епох з аркуша замало: loss ледь рушив, відповіді — набір частих слів. Потрібно 100–200 епох.")
    print("   • Embedding 32 має менше параметрів, ніж one-hot: вхідна матриця RNN 32×128 замість 104×128.")
    print("   • На 10 000 слів one-hot дає 10 000 входів на кожен крок: 1,28 млн ваг лише на вхід encoder-RNN.")
    print("     Embedding росте лише в таблиці векторів, а RNN лишається тією самою.")


if __name__ == "__main__":
    main()
