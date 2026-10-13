"""Пара 30 · крок 2: transfer learning — шар embedding з GloVe (пара 28) у seq2seq-моделі (пара 29).

30 навчальних пар замало, щоб модель дізналася, що cash ≈ money, а remember ≈ forgot.
GloVe це вже знає: його навчили на 6 млрд слів. Беремо готові вектори і порівнюємо 4 варіанти LSTM:

  з нуля           — свій словник із 30 пар, випадковий embedding; нове слово → <unk>
  GloVe, заморожено — словник 25 тис. слів GloVe, ваги embedding не змінюються (freeze)
  GloVe, донавчання — ті самі ваги, але оптимізатор їх теж змінює (fine-tune)
  freeze → unfreeze — спочатку вчимо решту моделі, потім обережно (lr 0.0001) донавчаємо embedding

    python Lesson30_02_transfer_glove.py
    python Lesson30_02_transfer_glove.py --seeds 5
    python Lesson30_02_transfer_glove.py --save      # навчити й зберегти models/supportflow_bot.pth
"""

from __future__ import annotations

import argparse
from statistics import mean, pstdev

import supportflow as sf

EPOCHS = 150


def build(variant: str, vocab: sf.Vocab, glove: tuple[sf.Vocab, object]):
    if variant == "з нуля":
        return sf.Seq2Seq(vocab, vocab, "lstm")
    gv, weights = glove
    return sf.Seq2Seq(gv, vocab, "lstm", src_weights=weights, freeze=variant != "GloVe, донавчання")


def fit(variant: str, model, pairs, vocab, seed: int) -> float:
    src, tgt_in, tgt_out = sf.make_tensors(pairs, model.src_vocab, vocab)
    if variant != "freeze → unfreeze":
        return sf.train(model, src, tgt_in, tgt_out, epochs=EPOCHS, seed=seed)["seconds"]
    first = sf.train(model, src, tgt_in, tgt_out, epochs=100, seed=seed)
    model.src_in.embedding.weight.requires_grad = True  # unfreeze
    second = sf.train(model, src, tgt_in, tgt_out, epochs=EPOCHS - 100, lr=1e-4, seed=seed)
    return first["seconds"] + second["seconds"]


def save_bot(pairs, vocab, glove) -> None:
    sf.set_seed(0)
    model = build("GloVe, заморожено", vocab, glove)
    fit("GloVe, заморожено", model, pairs, vocab, seed=0)
    sf.MODELS.mkdir(exist_ok=True)
    sf.save_model(model, sf.BOT)
    result = sf.evaluate(model, sf.load_paraphrases())
    print(f"Збережено {sf.BOT.relative_to(sf.HERE)}: нові запити exact {result['exact']:.0%}, F1 {result['f1']:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()

    rows = sf.load_pairs()
    pairs, vocab = sf.prepare(rows)
    glove = sf.glove_vocab([t for q, _ in pairs for t in q])
    para = sf.load_paraphrases()
    if args.save:
        save_bot(pairs, vocab, glove)
        return

    print("1) Чого модель «з нуля» не бачила ніколи, а GloVe знає")
    unseen = sorted({t for q, _ in para for t in sf.tokenize(q)} - set(vocab.itos))
    print(f"   {len(unseen)} слів нових запитів немає в 30 навчальних парах: {', '.join(unseen)}")
    print(f"   у GloVe є {sum(w in glove[0] for w in unseen)} з них")
    gv, weights = glove
    unit = weights / weights.norm(dim=1, keepdim=True).clamp(min=1e-12)
    from Lesson28_05_words_to_sequences import STOP

    STOP = STOP | {"they", "we", "not", "no", "very", "too", "cannot", "will", "please", "yes"}
    train_words = sorted({t for q, _ in pairs for t in q} - STOP)
    train_unit = unit[[gv.stoi[w] for w in train_words]]
    nearest = []
    for w in (w for w in unseen if w not in STOP):
        sims = train_unit @ unit[gv.stoi[w]]
        j = int(sims.argmax())
        nearest.append((float(sims[j]), w, train_words[j]))
    nearest.sort(reverse=True)
    print("   найближче змістовне навчальне слово за GloVe: " + ", ".join(f"{w} → {t} {c:.2f}" for c, w, t in nearest[:8]))
    print("   найслабші: " + ", ".join(f"{w} → {t} {c:.2f}" for c, w, t in nearest[-3:]) + "\n")

    print(f"2) Чотири варіанти LSTM, {EPOCHS} епох, seed 0…{args.seeds - 1}")
    variants = ["з нуля", "GloVe, заморожено", "GloVe, донавчання", "freeze → unfreeze"]
    table, best = [], {}
    for variant in variants:
        exact, f1, secs = [], [], []
        for seed in range(args.seeds):
            sf.set_seed(seed)
            model = build(variant, vocab, glove)
            secs.append(fit(variant, model, pairs, vocab, seed))
            result = sf.evaluate(model, para)
            exact.append(result["exact"])
            f1.append(result["f1"])
            if seed == 0:
                best[variant] = result
        trainable = f"{sf.count_params(build(variant, vocab, glove), trainable=True):,}"
        if variant == "freeze → unfreeze":
            trainable += f" → {sf.count_params(model):,}"
        table.append([variant, f"{mean(exact):.0%} ± {pstdev(exact):.0%}", f"{mean(f1):.2f}",
                      trainable.replace(",", " "), f"{mean(secs):.1f} с"])
        print(f"   {variant} готово")

    from Lesson28_05_words_to_sequences import Glove, make_search

    search = make_search(Glove(), rows)
    hits = sum(search(q)[0]["answer"] == ref for q, ref in para) / len(para)
    table.append(["пошуковик з пари 28", f"{hits:.0%}", "—", "0", "0 с"])
    print()
    sf.print_table(["варіант", "нові exact", "нові F1", "навчається параметрів", "час"], table,
                   [22, 13, 10, 26, 8])

    print("\n3) Відповіді на нові запити (seed 0)")
    scratch, frozen = best["з нуля"]["rows"], best["GloVe, заморожено"]["rows"]
    for (q, a, ref), (_, b, _) in zip(scratch, frozen):
        mark = lambda pred: "✓" if sf.tokenize(pred) == sf.tokenize(ref) else "✗"
        print(f"   {q}")
        print(f"     з нуля {mark(a)} {a}")
        print(f"     GloVe  {mark(b)} {b}")

    print("\nВисновки")
    print("   • Готовий embedding — найдешевший transfer learning: та сама модель, ті самі 30 пар, а нових запитів")
    print("     розуміє більше, бо в GloVe нові слова стоять поруч зі знайомими: cash → money, mail → email.")
    print("     Але поруч бувають і антоніми (fast → slow, rejected → accept): GloVe знає, що слова вживають")
    print("     в однакових контекстах, а не що вони означають одне й те саме — як good і bad на парі 27.")
    print("   • Заморожений GloVe не гірший за донавчений. Донавчання змінює лише вектори 77 слів із навчальних")
    print("     запитів, а їхні синоніми лишаються на старих місцях — сусідство password і passcode розходиться.")
    print("     Мало даних → freeze. Багато даних → freeze → unfreeze з малим lr.")
    print("   • Пошуковик з пари 28 тут сильний, бо відповіді фіксовані. Генерація потрібна, коли відповідь треба")
    print("     скласти, а не вибрати. У справжніх системах їх поєднують (RAG — модуль 9).")


if __name__ == "__main__":
    main()
