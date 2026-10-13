"""Пара 29 · крок 2: що всередині RNN і чому зʼявився LSTM.

1. Формула RNN руками і перевірка, що nn.RNN рахує те саме.
2. Пастка padding: нулі в кінці запиту змінюють hidden state. Рішення — pack_padded_sequence.
3. Чому LSTM: градієнт від останнього слова до першого через 5, 20, 50 кроків.
4. Форми станів: RNN — h, LSTM — (h, c), GRU — h.

    python Lesson29_02_rnn_inside.py
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence

import supportflow as sf


def rnn_by_hand() -> None:
    print("1) h_t = tanh(W_ih·x_t + b_ih + W_hh·h_(t-1) + b_hh)")
    torch.manual_seed(0)
    rnn = nn.RNN(input_size=4, hidden_size=3, batch_first=True)
    x = torch.randn(1, 3, 4)  # 1 речення, 3 слова, по 4 числа
    h = torch.zeros(3)
    for t in range(3):
        h = torch.tanh(rnn.weight_ih_l0 @ x[0, t] + rnn.bias_ih_l0 + rnn.weight_hh_l0 @ h + rnn.bias_hh_l0)
        print(f"   крок {t + 1}: h = {[round(v, 3) for v in h.tolist()]}")
    out, h_n = rnn(x)
    assert torch.allclose(out[0, -1], h, atol=1e-6) and torch.allclose(h_n[0, 0], h, atol=1e-6)
    print(f"   nn.RNN: out {tuple(out.shape)} = усі h_t, h_n {tuple(h_n.shape)} = останній h. Збігається з ручним ✓")
    print("   Ті самі ваги на кожному кроці: модель однаково читає 3 слова і 300.\n")


def padding_trap() -> None:
    print("2) Пастка: <pad> теж проходить крізь RNN")
    _, vocab = sf.prepare(sf.load_pairs())
    torch.manual_seed(0)
    emb = nn.Embedding(len(vocab), 8, padding_idx=sf.PAD_ID)
    rnn = nn.RNN(8, 6, batch_first=True)
    tokens = sf.tokenize("reset my password")
    short = torch.tensor([vocab.encode(tokens)])
    padded = torch.tensor([vocab.encode(tokens, max_len=7)])
    _, h_short = rnn(emb(short))
    _, h_padded = rnn(emb(padded))
    packed = pack_padded_sequence(emb(padded), torch.tensor([len(tokens)]), batch_first=True)
    _, h_packed = rnn(packed)
    print(f"   {padded.tolist()[0]}")
    print(f"   без pad      h = {[round(v, 2) for v in h_short[0, 0].tolist()]}")
    print(f"   з 4 pad      h = {[round(v, 2) for v in h_padded[0, 0].tolist()]}   ← інший стан")
    print(f"   packed       h = {[round(v, 2) for v in h_packed[0, 0].tolist()]}   ← як без pad")
    print("   Embedding(padding_idx=0) дає нульовий вектор, але W_hh·h і bias все одно змінюють h.\n")


def gradient_through_time() -> None:
    print("3) Чому LSTM: скільки градієнта доходить до першого слова")
    print("   відношення |∂ y_останнє / ∂ x_перше| до |∂ y_останнє / ∂ x_останнє|, середнє з 5 запусків")

    def ratio(cell: type[nn.Module], steps: int, forget_bias: float | None = None) -> float:
        values = []
        for seed in range(5):
            torch.manual_seed(seed)
            model = cell(16, 64, batch_first=True)
            if forget_bias is not None:  # у LSTM bias ділиться на 4 ворота: input, forget, cell, output
                for name, p in model.named_parameters():
                    if "bias" in name:
                        p.data[64:128] = forget_bias / 2
            x = torch.randn(1, steps, 16, requires_grad=True)
            out, _ = model(x)
            out[0, -1].sum().backward()
            g = x.grad[0].norm(dim=1)
            values.append((g[0] / g[-1]).item())
        return sum(values) / len(values)

    sf.print_table(["кроків", "RNN", "LSTM", "LSTM, forget bias 1", "GRU"],
                   [[n, f"{ratio(nn.RNN, n):.0e}", f"{ratio(nn.LSTM, n):.0e}",
                     f"{ratio(nn.LSTM, n, 1.0):.0e}", f"{ratio(nn.GRU, n):.0e}"] for n in (5, 20, 50)],
                   [9, 10, 10, 22, 10])
    print("   RNN множить градієнт на W_hh на кожному кроці — він згасає експоненційно (vanishing gradient).")
    print("   LSTM має окрему «стрічку» c_t: forget gate близько 1 пропускає памʼять далі майже без втрат.\n")


def state_shapes() -> None:
    print("4) Що повертають рекурентні шари (batch 2, 5 слів, input 8, hidden 16)")
    x = torch.randn(2, 5, 8)
    for name, cell in sf.CELLS.items():
        out, state = cell(8, 16, batch_first=True)(x)
        shapes = " і ".join(str(tuple(s.shape)) for s in state) if isinstance(state, tuple) else str(tuple(state.shape))
        params = sum(p.numel() for p in cell(8, 16).parameters())
        print(f"   {name.upper():<5} out {tuple(out.shape)}  стан {shapes:<22} параметрів {params}")
    print("   LSTM: 4 набори ваг (ворота i, f, g, o), GRU — 3, RNN — 1. Звідси й різниця в параметрах.")


def main() -> None:
    rnn_by_hand()
    padding_trap()
    gradient_through_time()
    state_shapes()


if __name__ == "__main__":
    main()
