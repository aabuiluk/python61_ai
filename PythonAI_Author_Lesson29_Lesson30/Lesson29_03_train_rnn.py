"""Пара 29 · крок 3 · завдання 6.3.2: проста RNN генерує відповіді SupportFlow.

Параметри з аркуша 6.3: nn.RNN(input_size = розмір словника, hidden_size = 128, num_layers = 1),
nn.Linear на виході, CrossEntropyLoss, Adam(lr = 0.001), 10 епох.
input_size = розмір словника означає one-hot: кожне слово — вектор з однією одиницею.

Модель — seq2seq: encoder-RNN читає запит, decoder-RNN пише відповідь слово за словом.

    python Lesson29_03_train_rnn.py                  # 10 епох з аркуша, потім до 150
    python Lesson29_03_train_rnn.py --epochs 300     # довше
    python Lesson29_03_train_rnn.py --embedding      # nn.Embedding(…, 64) замість one-hot
"""

from __future__ import annotations

import argparse

import supportflow as sf

SHEET = dict(cell="rnn", hidden=128, one_hot=True)  # аркуш 6.3, завдання 2
QUERIES = ["How can I reset my password?", "Where is my order?", "I was charged twice."]


def show_answers(model, title: str) -> None:
    print(f"   {title}")
    for q in QUERIES:
        print(f"     {q:<30}→ {sf.answer(model, q) or '(порожньо)'}")


def save_plot(history: list[float]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(range(1, len(history) + 1), history)
    ax.axvline(10, color="gray", linestyle="--", label="10 епох з аркуша")
    ax.set(xlabel="епоха", ylabel="loss", yscale="log", title="RNN seq2seq · SupportFlow")
    ax.legend()
    fig.tight_layout()
    sf.RESULTS.mkdir(exist_ok=True)
    fig.savefig(sf.RESULTS / "rnn_loss.png", dpi=120)
    print(f"   графік: results/rnn_loss.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--embedding", action="store_true")
    parser.add_argument("--all", action="store_true", help="усі 30 пар замість 15")
    args = parser.parse_args()

    rows = sf.load_pairs(limit=None if args.all else 15)
    pairs, vocab = sf.prepare(rows)
    src, tgt_in, tgt_out = sf.make_tensors(pairs, vocab, vocab)
    sf.set_seed(0)
    config = dict(SHEET, one_hot=not args.embedding)
    model = sf.Seq2Seq(vocab, vocab, **config)
    kind = "nn.Embedding(…, 64)" if args.embedding else f"one-hot, input_size = {len(vocab)}"
    print(f"Модель: encoder nn.RNN + decoder nn.RNN + nn.Linear({128} → {len(vocab)}); вхід: {kind}")
    print(f"Параметрів: {sf.count_params(model):,}; пар: {len(pairs)}; batch 8\n".replace(",", " "))

    print("1) 10 епох, як в аркуші 6.3")
    first = sf.train(model, src, tgt_in, tgt_out, epochs=10, log_every=1)
    show_answers(model, "відповіді після 10 епох:")
    print("   Loss ще високий: 10 епох × 2 кроки Adam з lr 0.001 — це лише 20 оновлень ваг.\n")

    rest = max(0, args.epochs - 10)
    print(f"2) Ще {rest} епох (разом {args.epochs})")
    more = sf.train(model, src, tgt_in, tgt_out, epochs=rest, seed=1, log_every=25)
    history = first["history"] + more["history"]
    show_answers(model, f"відповіді після {args.epochs} епох:")
    train_eval = sf.evaluate(model, [(r["question"], r["answer"]) for r in rows])
    print(f"   дослівно правильних на навчальних запитах: {train_eval['exact']:.0%}"
          f"; час {first['seconds'] + more['seconds']:.1f} с")

    print("\n3) Перефразовані запити: слів passcode, parcel, late у словнику немає → <unk>")
    known = {r["answer"] for r in rows}
    items = [(q, ref) for q, ref in sf.load_paraphrases() if ref in known]
    result = sf.evaluate(model, items)
    for q, pred, ref in result["rows"]:
        print(f"     {'✓' if sf.tokenize(pred) == sf.tokenize(ref) else '✗'} {q:<34}→ {pred}")
    print(f"   правильно {result['exact']:.0%}. Модель вгадує лише за знайомими словами навколо <unk>:")
    print("   вона запамʼятала відповіді, а не вивчила мову. Як це виправити без нових даних — пара 30.")
    save_plot(history)
    sf.MODELS.mkdir(exist_ok=True)
    sf.save_model(model, sf.MODELS / "supportflow_rnn.pth")
    print("   модель: models/supportflow_rnn.pth")


if __name__ == "__main__":
    main()
