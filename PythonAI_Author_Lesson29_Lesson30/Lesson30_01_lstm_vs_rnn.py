"""Пара 30 · крок 1 · завдання 6.3.3: LSTM проти RNN (і GRU) на тих самих даних.

Однакові умови: 30 пар SupportFlow, Embedding 64, hidden 128, Adam 0.001, однакові епохи й seed.
Різниця лише в рекурентній комірці. Метрики:
  loss         — наскільки добре модель вивчила навчальні відповіді;
  train exact  — частка навчальних запитів з дослівно правильною відповіддю;
  нові exact   — те саме на 15 перефразованих запитах з test_data/ (слів у них модель не бачила);
  нові F1      — частка спільних слів з еталонною відповіддю (часткова правильність).

    python Lesson30_01_lstm_vs_rnn.py
    python Lesson30_01_lstm_vs_rnn.py --seeds 5 --epochs 200
"""

from __future__ import annotations

import argparse
from statistics import mean

import supportflow as sf

QUERIES = ["i cannot remember my passcode", "my package is late", "i want my cash back",
           "how can i change my home address", "the application is too slow"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--seeds", type=int, default=3)
    args = parser.parse_args()

    rows = sf.load_pairs()
    pairs, vocab = sf.prepare(rows)
    src, tgt_in, tgt_out = sf.make_tensors(pairs, vocab, vocab)
    train_items = [(r["question"], r["answer"]) for r in rows]
    para = sf.load_paraphrases()
    print(f"{len(pairs)} пар, словник {len(vocab)}, {args.epochs} епох, seed 0…{args.seeds - 1}\n")

    table, keep = [], {}
    for cell in ("rnn", "lstm", "gru"):
        runs = []
        for seed in range(args.seeds):
            sf.set_seed(seed)
            model = sf.Seq2Seq(vocab, vocab, cell)
            fit = sf.train(model, src, tgt_in, tgt_out, epochs=args.epochs, seed=seed)
            runs.append((fit, sf.evaluate(model, train_items), sf.evaluate(model, para)))
            if seed == 0:
                keep[cell] = model
        table.append([cell.upper(), f"{sf.count_params(model):,}".replace(",", " "),
                      f"{mean(f['seconds'] for f, _, _ in runs):.1f} с",
                      f"{mean(f['history'][-1] for f, _, _ in runs):.3f}",
                      f"{mean(t['exact'] for _, t, _ in runs):.0%}",
                      f"{mean(p['exact'] for _, _, p in runs):.0%}",
                      f"{mean(p['f1'] for _, _, p in runs):.2f}"])
        print(f"   {cell.upper()} готово")

    print()
    sf.print_table(["модель", "параметрів", "час", "loss", "train exact", "нові exact", "нові F1"], table,
                   [8, 12, 8, 8, 13, 12, 9])

    print("\n5 запитів, яких немає в базі (seed 0)")
    for q in QUERIES:
        print(f"   {q}")
        for cell, model in keep.items():
            print(f"     {cell.upper():<5}→ {sf.answer(model, q)}")

    ratio = sf.count_params(keep["lstm"]) / sf.count_params(keep["rnn"])
    print("\nНа навчальних запитах усі три моделі запамʼятовують відповіді дослівно — тут їх не розрізнити.")
    print(f"Різницю видно на нових формулюваннях і в ціні: у LSTM в {ratio:.1f} раза більше параметрів, ніж у RNN.")
    print("Запити тут по 4–7 слів, тож довга памʼять LSTM ще не головна перевага. Вона важить на довгих текстах")
    print("(Lesson29_02, розділ 3). Числа скачуть від seed до seed — порівнюйте середнє, а не один запуск.")
    sf.MODELS.mkdir(exist_ok=True)
    sf.save_model(keep["lstm"], sf.MODELS / "supportflow_lstm.pth")
    print("Модель LSTM: models/supportflow_lstm.pth (назва з домашнього 6.3)")


if __name__ == "__main__":
    main()
