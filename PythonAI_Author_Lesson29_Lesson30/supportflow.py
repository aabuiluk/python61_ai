"""Спільний код пар 29–30: дані SupportFlow, словник, seq2seq-моделі, навчання, відповіді, метрики.

Дані — assets/supportflow_qa.csv (30 пар «запит → відповідь» служби підтримки),
GloVe з пари 28 — assets/glove/glove_100d.bin, готова модель — models/supportflow_bot.pth.
Інтернет не потрібен, GPU теж: усе вчиться на CPU за секунди.

Шлях даних у кожній моделі той самий:
    текст → токени → індекси → embedding → RNN / LSTM / GRU / Transformer → Linear → логіти → слово
"""

from __future__ import annotations

import csv
import math
import random
import re
import time
import warnings
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

HERE = Path(__file__).resolve().parent
QA_CSV = HERE / "assets" / "supportflow_qa.csv"
PARAPHRASES = HERE / "test_data" / "supportflow_paraphrases.csv"
GLOVE = HERE / "assets" / "glove" / "glove_100d.bin"
MODELS = HERE / "models"
BOT = MODELS / "supportflow_bot.pth"
RESULTS = HERE / "results"

# Спеціальні токени завжди мають ті самі індекси 0–3
PAD, UNK, SOS, EOS = "<pad>", "<unk>", "<sos>", "<eos>"
SPECIALS = [PAD, UNK, SOS, EOS]
PAD_ID, UNK_ID, SOS_ID, EOS_ID = 0, 1, 2, 3

WORD_RE = re.compile(r"[a-z]+")

torch.set_num_threads(max(1, min(4, torch.get_num_threads())))
warnings.filterwarnings("ignore", message=".*nested tensors.*")


# ---------------------------------------------------------------- текст і дані
def tokenize(text: str) -> list[str]:
    """Нижній регістр, без пунктуації й чисел: "Where's order #12?" → ['where', 's', 'order']."""
    return WORD_RE.findall(text.lower())


def load_pairs(path: Path = QA_CSV, limit: int | None = None) -> list[dict]:
    """Рядки CSV як словники: id, topic, question, answer."""
    if not path.is_file():
        raise SystemExit(f"Немає {path} — запускайте з папки пакета")
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows[:limit] if limit else rows


def load_paraphrases(path: Path = PARAPHRASES) -> list[tuple[str, str]]:
    """Перефразовані запити → еталонна відповідь з supportflow_qa.csv (за expected_id)."""
    answers = {row["id"]: row["answer"] for row in load_pairs()}
    with path.open(encoding="utf-8", newline="") as fh:
        return [(row["query"], answers[row["expected_id"]]) for row in csv.DictReader(fh)]


def set_seed(seed: int = 0) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


# ---------------------------------------------------------------- словник
class Vocab:
    """token ↔ index. Індекси 0–3 зайняті: <pad>, <unk>, <sos>, <eos>."""

    def __init__(self, words: list[str]) -> None:
        self.itos = list(SPECIALS) + [w for w in words if w not in SPECIALS]
        self.stoi = {w: i for i, w in enumerate(self.itos)}

    @classmethod
    def build(cls, token_lists: list[list[str]]) -> "Vocab":
        """Слова в порядку першої появи — так словник легко читати очима."""
        seen: dict[str, None] = {}
        for tokens in token_lists:
            for t in tokens:
                seen.setdefault(t, None)
        return cls(list(seen))

    def __len__(self) -> int:
        return len(self.itos)

    def __contains__(self, word: str) -> bool:
        return word in self.stoi

    def encode(self, tokens: list[str], max_len: int | None = None, sos: bool = False, eos: bool = False) -> list[int]:
        """Слова → індекси; невідоме слово → <unk>; доповнення <pad> до max_len (зайве обрізається)."""
        ids = [self.stoi.get(t, UNK_ID) for t in tokens]
        if sos:
            ids = [SOS_ID] + ids
        if eos:
            ids = ids + [EOS_ID]
        if max_len is not None:
            ids = ids[:max_len] + [PAD_ID] * (max_len - len(ids))
        return ids

    def decode(self, ids: list[int]) -> list[str]:
        """Індекси → слова до першого <eos>; <pad> і <sos> пропускаються."""
        words = []
        for i in ids:
            if i == EOS_ID:
                break
            if i not in (PAD_ID, SOS_ID):
                words.append(self.itos[i])
        return words


def make_tensors(pairs: list[tuple[list[str], list[str]]], src_vocab: Vocab, tgt_vocab: Vocab):
    """Пари токенів → три тензори однакової ширини.

    src      (N, max_q)    запит
    tgt_in   (N, max_a+1)  <sos> + відповідь   — вхід декодера (teacher forcing)
    tgt_out  (N, max_a+1)  відповідь + <eos>   — що декодер має передбачити
    """
    max_q = max(len(q) for q, _ in pairs)
    max_a = max(len(a) for _, a in pairs) + 1
    src = torch.tensor([src_vocab.encode(q, max_q) for q, _ in pairs])
    tgt_in = torch.tensor([tgt_vocab.encode(a, max_a, sos=True) for _, a in pairs])
    tgt_out = torch.tensor([tgt_vocab.encode(a, max_a, eos=True) for _, a in pairs])
    return src, tgt_in, tgt_out


def prepare(rows: list[dict]):
    """Рядки CSV → (пари токенів, спільний словник). Один словник для запитів і відповідей."""
    pairs = [(tokenize(r["question"]), tokenize(r["answer"])) for r in rows]
    vocab = Vocab.build([q for q, _ in pairs] + [a for _, a in pairs])
    return pairs, vocab


# ---------------------------------------------------------------- GloVe з пари 28
def load_glove(path: Path = GLOVE) -> tuple[list[str], np.ndarray]:
    """Формат word2vec binary: рядок «N D», далі для кожного слова: слово, пробіл, D чисел float32."""
    if not path.is_file():
        raise SystemExit(f"Немає {path} — запускайте з папки пакета")
    with path.open("rb") as fh:
        n, dim = map(int, fh.readline().split())
        words, vectors = [], np.empty((n, dim), dtype=np.float32)
        for i in range(n):
            word = bytearray()
            while (ch := fh.read(1)) != b" ":
                if ch != b"\n":
                    word += ch
            words.append(word.decode("utf-8"))
            vectors[i] = np.frombuffer(fh.read(4 * dim), dtype=np.float32)
    return words, vectors


def save_glove(path: Path, words: list[str], vectors: np.ndarray) -> None:
    with path.open("wb") as fh:
        fh.write(f"{len(words)} {vectors.shape[1]}\n".encode())
        for w, v in zip(words, vectors.astype(np.float32)):
            fh.write(w.encode("utf-8") + b" " + v.tobytes() + b"\n")


def glove_vocab(extra_words: list[str] = (), path: Path = GLOVE) -> tuple[Vocab, torch.Tensor]:
    """Словник = усі слова GloVe (+ слова даних, яких у GloVe немає). Ваги — вектори GloVe.

    Слова поза GloVe і спецтокени отримують малі випадкові вектори, <pad> — нулі.
    Це і є transfer learning: шар embedding приходить уже навченим на 6 млрд слів.
    """
    words, vectors = load_glove(path)
    known = set(words)
    missing = list(dict.fromkeys(w for w in extra_words if w not in known))
    vocab = Vocab(words + missing)
    gen = torch.Generator().manual_seed(0)
    weights = torch.randn(len(vocab), vectors.shape[1], generator=gen) * 0.1
    weights[len(SPECIALS):len(SPECIALS) + len(words)] = torch.from_numpy(vectors)
    weights[PAD_ID] = 0
    return vocab, weights


# ---------------------------------------------------------------- моделі
CELLS = {"rnn": nn.RNN, "lstm": nn.LSTM, "gru": nn.GRU}


class TokenInput(nn.Module):
    """Індекси → вектори: або навчений шар nn.Embedding, або one-hot (як в аркуші 6.3: input_size = розмір словника)."""

    def __init__(self, vocab_size: int, emb_dim: int, one_hot: bool = False,
                 weights: torch.Tensor | None = None, freeze: bool = False) -> None:
        super().__init__()
        self.vocab_size, self.one_hot = vocab_size, one_hot
        if one_hot:
            self.embedding = None
            self.dim = vocab_size
        else:
            self.embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=PAD_ID)
            if weights is not None:
                self.embedding.weight.data.copy_(weights)
            self.embedding.weight.requires_grad = not freeze
            self.dim = emb_dim

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        if self.one_hot:
            return nn.functional.one_hot(ids, self.vocab_size).float()
        return self.embedding(ids)


class Seq2Seq(nn.Module):
    """Encoder–decoder на RNN / LSTM / GRU, за бажання з увагою (attention) декодера на слова запиту.

    Encoder читає запит і стискає його в hidden state.
    Decoder стартує з цього стану і пише відповідь слово за словом.
    """

    def __init__(self, src_vocab: Vocab, tgt_vocab: Vocab, cell: str = "lstm", hidden: int = 128,
                 emb_dim: int = 64, one_hot: bool = False, attention: bool = False,
                 src_weights: torch.Tensor | None = None, freeze: bool = False, pack: bool = True) -> None:
        super().__init__()
        self.src_vocab, self.tgt_vocab = src_vocab, tgt_vocab
        self.cell, self.attention, self.pack = cell, attention, pack
        src_dim = src_weights.shape[1] if src_weights is not None else emb_dim
        self.config = dict(cell=cell, hidden=hidden, emb_dim=emb_dim, one_hot=one_hot,
                           attention=attention, glove=src_weights is not None, freeze=freeze)
        self.src_in = TokenInput(len(src_vocab), src_dim, one_hot, src_weights, freeze)
        self.tgt_in = TokenInput(len(tgt_vocab), emb_dim, one_hot)
        rnn = CELLS[cell]
        self.encoder = rnn(self.src_in.dim, hidden, num_layers=1, batch_first=True)
        self.decoder = rnn(self.tgt_in.dim, hidden, num_layers=1, batch_first=True)
        self.out = nn.Linear(hidden * 2 if attention else hidden, len(tgt_vocab))
        self.last_attention: torch.Tensor | None = None

    def encode(self, src: torch.Tensor):
        x = self.src_in(src)
        if not self.pack:  # <pad> теж проходить крізь RNN і псує hidden state
            return self.encoder(x)
        lengths = (src != PAD_ID).sum(1).clamp(min=1).cpu()
        packed = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        out, state = self.encoder(packed)
        out, _ = pad_packed_sequence(out, batch_first=True, total_length=src.size(1))
        return out, state

    def decode(self, tgt_in: torch.Tensor, state, enc_out: torch.Tensor, src_mask: torch.Tensor):
        dec_out, state = self.decoder(self.tgt_in(tgt_in), state)
        if self.attention:  # dot-product attention: на які слова запиту дивитися зараз
            scores = dec_out @ enc_out.transpose(1, 2)
            scores = scores.masked_fill(~src_mask[:, None, :], -1e9)
            weights = scores.softmax(-1)
            dec_out = torch.cat([dec_out, weights @ enc_out], dim=-1)
            self.last_attention = weights
        return self.out(dec_out), state

    def forward(self, src: torch.Tensor, tgt_in: torch.Tensor) -> torch.Tensor:
        enc_out, state = self.encode(src)
        logits, _ = self.decode(tgt_in, state, enc_out, src != PAD_ID)
        return logits

    @torch.no_grad()
    def generate(self, src: torch.Tensor, max_len: int = 20) -> list[list[int]]:
        """Жадібна генерація: щоразу беремо найімовірніше слово і подаємо його на наступний крок."""
        self.eval()
        enc_out, state = self.encode(src)
        mask = src != PAD_ID
        token = torch.full((src.size(0), 1), SOS_ID)
        result, attn = [], []
        for _ in range(max_len):
            logits, state = self.decode(token, state, enc_out, mask)
            token = logits.argmax(-1)
            result.append(token)
            if self.attention:
                attn.append(self.last_attention)
        if self.attention:
            self.last_attention = torch.cat(attn, dim=1)
        return torch.cat(result, dim=1).tolist()


class PositionalEncoding(nn.Module):
    """Синусоїди з «Attention Is All You Need»: без них увага не знає порядку слів."""

    def __init__(self, dim: int, max_len: int = 64) -> None:
        super().__init__()
        pos = torch.arange(max_len)[:, None]
        div = torch.exp(torch.arange(0, dim, 2) * (-math.log(10000.0) / dim))
        pe = torch.zeros(max_len, dim)
        pe[:, 0::2], pe[:, 1::2] = torch.sin(pos * div), torch.cos(pos * div)
        self.register_buffer("pe", pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[: x.size(1)]


class TransformerSeq2Seq(nn.Module):
    """Той самий контракт, що в Seq2Seq, але без рекурентності: encoder і decoder на self-attention."""

    def __init__(self, src_vocab: Vocab, tgt_vocab: Vocab, d_model: int = 64, nhead: int = 4,
                 layers: int = 2, ff: int = 128, dropout: float = 0.1) -> None:
        super().__init__()
        self.src_vocab, self.tgt_vocab = src_vocab, tgt_vocab
        self.config = dict(cell="transformer", d_model=d_model, nhead=nhead, layers=layers, ff=ff)
        self.src_emb = nn.Embedding(len(src_vocab), d_model, padding_idx=PAD_ID)
        self.tgt_emb = nn.Embedding(len(tgt_vocab), d_model, padding_idx=PAD_ID)
        self.pos = PositionalEncoding(d_model)
        self.scale = math.sqrt(d_model)
        self.transformer = nn.Transformer(d_model, nhead, layers, layers, ff, dropout, batch_first=True)
        self.out = nn.Linear(d_model, len(tgt_vocab))

    def forward(self, src: torch.Tensor, tgt_in: torch.Tensor) -> torch.Tensor:
        size = tgt_in.size(1)  # True = «цю позицію не видно»: декодер не підглядає в майбутні слова
        causal = torch.triu(torch.ones(size, size, dtype=torch.bool), diagonal=1)
        h = self.transformer(
            self.pos(self.src_emb(src) * self.scale),
            self.pos(self.tgt_emb(tgt_in) * self.scale),
            tgt_mask=causal,
            src_key_padding_mask=src == PAD_ID,
            tgt_key_padding_mask=tgt_in == PAD_ID,
            memory_key_padding_mask=src == PAD_ID,
        )
        return self.out(h)

    @torch.no_grad()
    def generate(self, src: torch.Tensor, max_len: int = 20) -> list[list[int]]:
        self.eval()
        tgt = torch.full((src.size(0), 1), SOS_ID)
        for _ in range(max_len):
            nxt = self(src, tgt)[:, -1].argmax(-1, keepdim=True)
            tgt = torch.cat([tgt, nxt], dim=1)
        return tgt[:, 1:].tolist()


# ---------------------------------------------------------------- навчання і відповіді
def train(model: nn.Module, src: torch.Tensor, tgt_in: torch.Tensor, tgt_out: torch.Tensor,
          epochs: int = 10, lr: float = 1e-3, batch_size: int = 8, seed: int = 0,
          ignore_pad: bool = True, log_every: int = 0) -> dict:
    """Adam + CrossEntropyLoss по всіх позиціях відповіді. Повертає історію loss і час навчання."""
    torch.manual_seed(seed)
    loss_fn = nn.CrossEntropyLoss(ignore_index=PAD_ID if ignore_pad else -100)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=lr)
    history, start = [], time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        order, total = torch.randperm(len(src)), 0.0
        for i in range(0, len(src), batch_size):
            idx = order[i:i + batch_size]
            logits = model(src[idx], tgt_in[idx])
            loss = loss_fn(logits.reshape(-1, logits.size(-1)), tgt_out[idx].reshape(-1))
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
            total += loss.item() * len(idx)
        history.append(total / len(src))
        if log_every and (epoch % log_every == 0 or epoch == 1):
            print(f"     епоха {epoch:>4}   loss {history[-1]:.3f}")
    return {"history": history, "seconds": time.perf_counter() - start}


def answer(model: nn.Module, question: str, max_len: int = 20) -> str:
    tokens = tokenize(question)
    src = torch.tensor([model.src_vocab.encode(tokens)]) if tokens else torch.tensor([[UNK_ID]])
    return " ".join(model.tgt_vocab.decode(model.generate(src, max_len)[0]))


def token_f1(pred: str, ref: str) -> float:
    """Збіг слів відповіді з еталоном: 1.0 — ті самі слова, 0 — жодного спільного."""
    p, r = tokenize(pred), tokenize(ref)
    common = sum(min(p.count(w), r.count(w)) for w in set(p))
    if not p or not r or not common:
        return 0.0
    precision, recall = common / len(p), common / len(r)
    return 2 * precision * recall / (precision + recall)


def evaluate(model: nn.Module, items: list[tuple[str, str]]) -> dict:
    """items — (запит, еталонна відповідь). exact — частка дослівно правильних відповідей."""
    rows = [(q, answer(model, q), ref) for q, ref in items]
    exact = sum(tokenize(p) == tokenize(r) for _, p, r in rows) / len(rows)
    f1 = sum(token_f1(p, r) for _, p, r in rows) / len(rows)
    return {"exact": exact, "f1": f1, "rows": rows}


def count_params(model: nn.Module, trainable: bool = False) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad or not trainable)


def print_table(headers: list[str], rows: list[list], widths: list[int] | None = None, indent: str = "   ") -> None:
    widths = widths or [max(len(str(x)) for x in col) + 2 for col in zip(headers, *rows)]
    for row in [headers, ["-" * (w - 2) for w in widths], *rows]:
        print(indent + "".join(f"{str(x):<{w}}" for x, w in zip(row, widths)).rstrip())


# ---------------------------------------------------------------- збереження
def save_model(model: nn.Module, path: Path) -> None:
    """Зберігаємо конфіг, словники й ваги. Заморожений GloVe не зберігаємо — він уже лежить в assets/."""
    state = {k: v for k, v in model.state_dict().items()
             if not (model.config.get("freeze") and k == "src_in.embedding.weight")}
    torch.save({"config": model.config, "src": model.src_vocab.itos, "tgt": model.tgt_vocab.itos,
                "state": state}, path)


def load_model(path: Path = BOT) -> nn.Module:
    if not path.is_file():
        raise SystemExit(f"Немає {path} — запускайте з папки пакета")
    ckpt = torch.load(path, map_location="cpu", weights_only=True)
    cfg = dict(ckpt["config"])
    src, tgt = Vocab(ckpt["src"]), Vocab(ckpt["tgt"])
    if cfg.pop("cell") == "transformer":
        model = TransformerSeq2Seq(src, tgt, **cfg)
    else:
        cfg["cell"] = ckpt["config"]["cell"]
        weights = None
        if cfg.pop("glove"):
            words = ckpt["src"][len(SPECIALS):]
            vocab, weights = glove_vocab(words)
            if vocab.itos != src.itos:
                raise SystemExit("Словник моделі не збігається з assets/glove — перенавчіть модель")
        model = Seq2Seq(src, tgt, src_weights=weights, **cfg)
    model.load_state_dict(ckpt["state"], strict=False)
    model.eval()
    return model
