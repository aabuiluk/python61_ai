"""Пара 29 · крок 4: увага (attention) — серце трансформера.

1. Навчена увага seq2seq: на які слова запиту дивиться кожне слово відповіді.
2. softmax(Q·Kᵀ / √d)·V своєю функцією і перевірка проти torch.
3. Маска причинності: декодер не бачить майбутніх слів.
4. Без позиційного кодування увага не знає порядку слів.
5. Шар TransformerEncoderLayer: форми, параметри, чому він паралельний.

    python Lesson29_04_attention.py
"""

from __future__ import annotations

import math

import torch
from torch import nn

import supportflow as sf


def attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: torch.Tensor | None = None):
    """Scaled dot-product attention. mask: True там, куди дивитися НЕ можна."""
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.size(-1))
    if mask is not None:
        scores = scores.masked_fill(mask, float("-inf"))
    weights = scores.softmax(dim=-1)
    return weights @ v, weights


def glove_matrix(words: list[str]) -> torch.Tensor:
    vocab, weights = sf.glove_vocab()
    return torch.stack([weights[vocab.stoi[w]] for w in words])


def learned_attention() -> None:
    print("1) Куди дивиться навчена модель: LSTM seq2seq + attention на 30 парах SupportFlow (~3 с)")
    rows = sf.load_pairs()
    pairs, vocab = sf.prepare(rows)
    src, tgt_in, tgt_out = sf.make_tensors(pairs, vocab, vocab)
    sf.set_seed(0)
    model = sf.Seq2Seq(vocab, vocab, "lstm", attention=True)
    sf.train(model, src, tgt_in, tgt_out, epochs=150)
    for i, q in enumerate(["How can I reset my password?", "My order is delayed.", "I was charged twice."]):
        tokens = sf.tokenize(q)
        out = vocab.decode(model.generate(torch.tensor([vocab.encode(tokens)]))[0])
        weights = model.last_attention[0, :len(out)]
        print(f"   {q} → {' '.join(out)}")
        if i == 0:
            print("   " + " " * 10 + "".join(f"{t:>9}" for t in tokens))
            for word, row in zip(out, weights):
                print(f"   {word:<10}" + "".join(f"{p:>9.2f}" for p in row.tolist()))
        else:
            share = weights.mean(0)
            top = share.argsort(descending=True)[:2].tolist()
            print("   найбільше уваги: " + ", ".join(f"{tokens[j]} {share[j]:.0%}" for j in top))
    print("   Ніхто не казав моделі, що password — головне слово. Вона знайшла це сама, бо так менший loss.")
    print("   Рядок таблиці — розподіл уваги одного слова відповіді по словах запиту (сума 1).\n")


def check_against_torch() -> None:
    print("2) Своя функція = torch.nn.functional.scaled_dot_product_attention")
    torch.manual_seed(0)
    q, k, v = torch.randn(1, 5, 16), torch.randn(1, 5, 16), torch.randn(1, 5, 16)
    mine, _ = attention(q, k, v)
    ref = nn.functional.scaled_dot_product_attention(q, k, v)
    assert torch.allclose(mine, ref, atol=1e-5)
    print(f"   різниця {float((mine - ref).abs().max()):.1e} ✓  (Q, K, V: {tuple(q.shape)})\n")


def causal_mask() -> None:
    print("3) Маска причинності: слово t бачить лише слова 1…t")
    words = "sorry for the delay".split()
    x = glove_matrix(words)
    mask = torch.triu(torch.ones(4, 4, dtype=torch.bool), diagonal=1)
    _, w = attention(x, x, x, mask)
    print("   " + " " * 8 + "".join(f"{t:>8}" for t in words))
    for word, row in zip(words, w):
        print(f"   {word:<8}" + "".join(f"{p:>8.2f}" for p in row.tolist()))
    assert torch.all(w[mask] == 0)
    print("   Над діагоналлю нулі. Так GPT і декодер трансформера вчаться передбачати наступне слово.\n")


def order_blindness() -> None:
    print("4) Без позиційного кодування порядок слів не важить")
    words = "you can cancel it".split()
    perm = [2, 0, 3, 1]
    x = glove_matrix(words)
    out, _ = attention(x, x, x)
    out_shuffled, _ = attention(x[perm], x[perm], x[perm])
    same = torch.allclose(out[perm], out_shuffled, atol=1e-5)
    print(f"   перемішали слова → виходи просто переставились: {same}")
    pe = sf.PositionalEncoding(100)
    xp, xs = pe(x[None])[0], pe(x[perm][None])[0]
    out_p, _ = attention(xp, xp, xp)
    out_ps, _ = attention(xs, xs, xs)
    print(f"   з позиційним кодуванням те саме: {torch.allclose(out_p[perm], out_ps, atol=1e-5)}")
    print("   Тому трансформер додає до кожного слова вектор його позиції (синусоїди або навчений).\n")


def encoder_layer() -> None:
    print("5) Шар TransformerEncoderLayer (d_model 64, 4 голови) проти LSTM того ж розміру")
    layer = nn.TransformerEncoderLayer(d_model=64, nhead=4, dim_feedforward=128, batch_first=True)
    lstm = nn.LSTM(64, 64, batch_first=True)
    x = torch.randn(2, 9, 64)
    print(f"   вхід {tuple(x.shape)} → вихід {tuple(layer(x).shape)}: форма та сама, кожне слово «бачило» всі")
    sf.print_table(["шар", "параметрів", "кроків по послідовності з 9 слів"],
                   [["TransformerEncoderLayer", sf.count_params(layer), "1: усі позиції разом"],
                    ["LSTM", sf.count_params(lstm), "9: слово за словом"]], [26, 13, 32])
    print("   Паралельність — головна причина, чому великі мовні моделі — трансформери, а не LSTM.")
    print("   distilGPT2 з пари 30: 6 таких шарів-декодерів з маскою причинності, 82 млн параметрів.")


def main() -> None:
    learned_attention()
    check_against_torch()
    causal_mask()
    order_blindness()
    encoder_layer()


if __name__ == "__main__":
    main()
