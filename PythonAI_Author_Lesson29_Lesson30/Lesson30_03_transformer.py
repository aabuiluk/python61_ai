"""Пара 30 · крок 3 · завдання 6.3.4: Transformer проти seq2seq на RNN / LSTM.

1. Маленький Transformer (nn.Transformer) з нуля на тих самих 30 парах — чесне порівняння з LSTM.
2. distilGPT2 з бібліотеки transformers: переднавчений, але не під службу підтримки.
3. --finetune: донавчання distilGPT2 на 30 парах (~10 с на CPU) — transfer learning трансформера.
4. Таблиця порівняння архітектур.

Пункти 2–3 потребують `pip install transformers` і інтернету при першому запуску
(distilGPT2 ≈ 350 МБ, далі береться з кешу ~/.cache/huggingface). Без них скрипт робить 1 і 4.

    python Lesson30_03_transformer.py
    python Lesson30_03_transformer.py --finetune
    python Lesson30_03_transformer.py --skip-local --finetune     # лише distilGPT2
"""

from __future__ import annotations

import argparse
import time
from statistics import mean

import torch

import supportflow as sf

SHEET_QUERIES = ["I forgot my password", "My order is delayed", "How do I get a refund?"]
PROMPT = "Customer: {}\nSupport agent:"


def local_comparison(seeds: int) -> None:
    print(f"1) З нуля на 30 парах: LSTM seq2seq проти Transformer, seed 0…{seeds - 1}")
    rows = sf.load_pairs()
    pairs, vocab = sf.prepare(rows)
    src, tgt_in, tgt_out = sf.make_tensors(pairs, vocab, vocab)
    train_items = [(r["question"], r["answer"]) for r in rows]
    para = sf.load_paraphrases()
    table, models = [], {}
    for name, make, epochs in [("LSTM", lambda: sf.Seq2Seq(vocab, vocab, "lstm"), 150),
                               ("Transformer", lambda: sf.TransformerSeq2Seq(vocab, vocab), 200)]:
        runs = []
        for seed in range(seeds):
            sf.set_seed(seed)
            model = make()
            fit = sf.train(model, src, tgt_in, tgt_out, epochs=epochs, seed=seed)
            start = time.perf_counter()
            new = sf.evaluate(model, para)
            gen_ms = (time.perf_counter() - start) / len(para) * 1000
            runs.append((fit["seconds"], sf.evaluate(model, train_items)["exact"], new["exact"], new["f1"], gen_ms))
            models.setdefault(name, model)
        table.append([name, f"{sf.count_params(model):,}".replace(",", " "), epochs,
                      f"{mean(r[0] for r in runs):.1f} с", f"{mean(r[1] for r in runs):.0%}",
                      f"{mean(r[2] for r in runs):.0%}", f"{mean(r[3] for r in runs):.2f}",
                      f"{mean(r[4] for r in runs):.0f} мс"])
    sf.print_table(["модель", "параметрів", "епох", "навчання", "train exact", "нові exact", "нові F1",
                    "відповідь"], table, [13, 12, 6, 10, 13, 12, 9, 10])
    for q in SHEET_QUERIES:
        print(f"   {q}")
        for name, model in models.items():
            print(f"     {name:<12}→ {sf.answer(model, q)}")
    print("   Transformer з нуля на 30 парах не кращий за LSTM: увазі потрібно багато даних, щоб навчитися,")
    print("   куди дивитися. Сила трансформерів — у переднавчанні на мільярдах слів. Це наступний пункт.\n")


def load_gpt():
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from transformers.utils import logging
    except ImportError:
        print("   transformers не встановлено. Для пунктів 2–3:  python -m pip install transformers")
        return None
    logging.set_verbosity_error()
    try:
        tok = AutoTokenizer.from_pretrained("distilgpt2")
        model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    except OSError as err:
        print(f"   Не вдалося завантажити distilgpt2 (потрібен інтернет при першому запуску): {err}")
        return None
    tok.pad_token = tok.eos_token
    return tok, model


def gpt_answer(tok, model, query: str) -> tuple[str, float]:
    from transformers import GenerationConfig

    prompt = PROMPT.format(query)
    ids = tok(prompt, return_tensors="pt")
    cfg = GenerationConfig(max_new_tokens=25, do_sample=False, pad_token_id=tok.eos_token_id,
                           eos_token_id=tok.eos_token_id)
    start = time.perf_counter()
    with torch.no_grad():
        out = model.generate(**ids, generation_config=cfg)
    text = tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
    return text.strip().replace("\n", " ⏎ "), (time.perf_counter() - start) * 1000


def gpt_as_is(tok, model) -> None:
    print(f"2) distilGPT2 як є: {sum(p.numel() for p in model.parameters()) / 1e6:.0f} млн параметрів, "
          "навчений на текстах з інтернету (OpenWebText)")
    model.eval()
    for q in SHEET_QUERIES:
        text, ms = gpt_answer(tok, model, q)
        print(f"   {q:<24}→ {text[:90] or '(порожньо)'}   ({ms:.0f} мс)")
    print("   Мову модель знає, але задачі «відповідай клієнту» її ніхто не вчив: вона продовжує текст,")
    print("   найчастіше повторюючи шаблон Customer / Support.\n")


def gpt_finetune(tok, model, epochs: int) -> None:
    print(f"3) Transfer learning: донавчаємо distilGPT2 на 30 парах, {epochs} епох")
    rows = sf.load_pairs()
    texts = [PROMPT.format(r["question"]) + f" {r['answer']}{tok.eos_token}" for r in rows]
    enc = tok(texts, return_tensors="pt", padding=True)
    labels = enc["input_ids"].clone()
    labels[enc["attention_mask"] == 0] = -100  # як ignore_index=0 у нашому CrossEntropyLoss
    torch.manual_seed(0)
    opt = torch.optim.AdamW(model.parameters(), lr=5e-5)
    start = time.perf_counter()
    model.train()
    for epoch in range(1, epochs + 1):
        total = 0.0
        for idx in torch.randperm(len(texts)).split(8):
            out = model(input_ids=enc["input_ids"][idx], attention_mask=enc["attention_mask"][idx],
                        labels=labels[idx])
            opt.zero_grad()
            out.loss.backward()
            opt.step()
            total += out.loss.item() * len(idx)
        if epoch in (1, epochs) or epoch % 4 == 0:
            print(f"     епоха {epoch:>3}   loss {total / len(texts):.3f}")
    model.eval()
    print(f"   навчання {time.perf_counter() - start:.0f} с")
    rows_out = [(q, gpt_answer(tok, model, q)[0].split(" ⏎ ")[0], ref) for q, ref in sf.load_paraphrases()]
    for q, a, _ in rows_out[:6]:
        print(f"   {q:<34}→ {a}")
    f1 = mean(sf.token_f1(a, ref) for _, a, ref in rows_out)
    print(f"   нові запити: F1 {f1:.2f}. Відповіді складені заново, а не вибрані з 30 завчених: про passcode —")
    print("   по суті, про parcel — ні. F1 таке не розрізняє, тому генерацію оцінює людина (таблиця з ДЗ 6.3).\n")


def architecture_table() -> None:
    print("4) Порівняння архітектур")
    sf.print_table(
        ["критерій", "Seq2Seq RNN / LSTM", "Transformer"],
        [["як читає текст", "слово за словом", "усі слова одночасно"],
         ["контекст", "стискається в один hidden state", "увага бачить кожне слово"],
         ["довгі тексти", "RNN забуває; LSTM краще", "до межі вікна (1024 у GPT-2)"],
         ["навчання на GPU", "погано паралелиться", "паралелиться повністю"],
         ["даних треба", "мало вистачає (наші 30 пар)", "багато; або готова модель"],
         ["розмір", "сотні тисяч параметрів", "мільйони й мільярди"],
         ["час відповіді на CPU", "~1 мс", "десятки–сотні мс"],
         ["де трапляється", "сенсори, ряди, малі моделі", "GPT, BERT, переклад, чат-боти"]],
        [22, 34, 32])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finetune", action="store_true")
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--skip-local", action="store_true")
    args = parser.parse_args()
    if not args.skip_local:
        local_comparison(args.seeds)
    gpt = load_gpt()
    if gpt:
        gpt_as_is(*gpt)
        if args.finetune:
            gpt_finetune(*gpt, args.epochs)
        else:
            print("   Донавчання: python Lesson30_03_transformer.py --skip-local --finetune\n")
    else:
        print()
    architecture_table()


if __name__ == "__main__":
    main()
