"""Word2Vec і KeyedVectors на чистому numpy — запасний варіант, коли gensim не встановився.

gensim поки не має збірки для Python 3.14. Тоді nlp_vectors.py бере класи звідси.
Інтерфейс той самий, що в gensim, тож код скриптів не змінюється:

    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=1)
    model.wv["good"], model.wv.most_similar("good"), model.wv.similarity("good", "great")

Навчання — Skip-gram або CBOW з negative sampling (як у gensim за замовчуванням),
але міні-батчами numpy замість коду на C. Тому воно в кілька разів повільніше
і числа трохи інші, ніж у gensim; ідея й результат — ті самі.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


class KeyedVectors:
    """Слова + матриця векторів: пошук сусідів, схожість, збереження у форматі word2vec."""

    def __init__(self, vector_size: int) -> None:
        self.vector_size = vector_size
        self.index_to_key: list[str] = []
        self.key_to_index: dict[str, int] = {}
        self.vectors = np.zeros((0, vector_size), dtype=np.float32)
        self._normed: np.ndarray | None = None

    # --- словник і доступ до векторів
    def add_vectors(self, keys: list[str], weights: np.ndarray) -> None:
        start = len(self.index_to_key)
        self.index_to_key.extend(keys)
        self.key_to_index.update({k: start + i for i, k in enumerate(keys)})
        self.vectors = np.vstack([self.vectors, np.asarray(weights, dtype=np.float32)])
        self._normed = None

    def __len__(self) -> int:
        return len(self.index_to_key)

    def __contains__(self, key: str) -> bool:
        return key in self.key_to_index

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.vectors[self.key_to_index[key]]
        return self.vectors[[self.key_to_index[k] for k in key]]

    def _unit(self) -> np.ndarray:
        if self._normed is None:
            norms = np.linalg.norm(self.vectors, axis=1, keepdims=True)
            self._normed = self.vectors / np.maximum(norms, 1e-12)
        return self._normed

    # --- схожість
    def similarity(self, a: str, b: str) -> float:
        unit = self._unit()
        return float(unit[self.key_to_index[a]] @ unit[self.key_to_index[b]])

    def most_similar(self, positive=None, negative=None, topn: int = 10) -> list[tuple[str, float]]:
        positive = [positive] if isinstance(positive, str) else list(positive or [])
        negative = [negative] if isinstance(negative, str) else list(negative or [])
        for word in positive + negative:
            if word not in self.key_to_index:
                raise KeyError(f"Key '{word}' not present")
        unit = self._unit()
        query = sum(unit[self.key_to_index[w]] for w in positive) - sum(unit[self.key_to_index[w]] for w in negative)
        query = query / max(np.linalg.norm(query), 1e-12)
        sims = unit @ query
        skip = {self.key_to_index[w] for w in positive + negative}
        best = np.argsort(-sims)[: topn + len(skip)]
        return [(self.index_to_key[i], float(sims[i])) for i in best if i not in skip][:topn]

    # --- оцінка на тестових наборах (як evaluate_* у gensim)
    def evaluate_word_pairs(self, path: str):
        from scipy.stats import pearsonr, spearmanr

        model, human, total = [], [], 0
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            a, b, score = line.lower().split("\t")[:3]
            total += 1
            if a in self.key_to_index and b in self.key_to_index:
                model.append(self.similarity(a, b))
                human.append(float(score))
        return pearsonr(model, human), spearmanr(model, human), 100 * (1 - len(model) / total)

    def evaluate_word_analogies(self, path: str):
        """a b c d: чи найближче до b − a + c саме d (слова a, b, c у відповідь не беремо)."""
        unit = self._unit()
        sections, current = [], None
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            if line.startswith(":"):
                current = {"section": line[1:].strip(), "correct": [], "incorrect": []}
                sections.append(current)
                continue
            words = line.lower().split()
            if len(words) != 4 or not all(w in self.key_to_index for w in words):
                continue
            a, b, c, d = (self.key_to_index[w] for w in words)
            sims = unit @ (unit[b] - unit[a] + unit[c])
            sims[[a, b, c]] = -np.inf
            guess = self.index_to_key[int(np.argmax(sims))]
            (current["correct"] if guess == words[3] else current["incorrect"]).append(tuple(words))
        correct = sum(len(s["correct"]) for s in sections)
        total = correct + sum(len(s["incorrect"]) for s in sections)
        sections.append({
            "section": "Total accuracy",
            "correct": [q for s in sections for q in s["correct"]],
            "incorrect": [q for s in sections for q in s["incorrect"]],
        })
        return (correct / total if total else 0.0), sections

    # --- файли
    @classmethod
    def load_word2vec_format(cls, path: str, binary: bool = True) -> "KeyedVectors":
        data = Path(path).read_bytes()
        end = data.index(b"\n")
        count, dim = (int(x) for x in data[:end].split())
        pos, words = end + 1, []
        vectors = np.empty((count, dim), dtype=np.float32)
        step = 4 * dim
        for i in range(count):
            space = data.index(b" ", pos)
            words.append(data[pos:space].decode("utf-8").strip())
            vectors[i] = np.frombuffer(data, dtype=np.float32, count=dim, offset=space + 1)
            pos = space + 1 + step
            if pos < len(data) and data[pos : pos + 1] == b"\n":
                pos += 1
        kv = cls(dim)
        kv.add_vectors(words, vectors)
        return kv

    def save_word2vec_format(self, path: str, binary: bool = True) -> None:
        with open(path, "wb") as fh:
            fh.write(f"{len(self)} {self.vector_size}\n".encode())
            for word, vec in zip(self.index_to_key, self.vectors.astype(np.float32)):
                fh.write(word.encode("utf-8") + b" " + vec.tobytes() + b"\n")


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -6, 6)))


class Word2Vec:
    """Word2Vec з negative sampling: sg=1 — Skip-gram, sg=0 — CBOW. Параметри як у gensim."""

    def __init__(self, sentences, vector_size: int = 100, window: int = 5, min_count: int = 5, sg: int = 0,
                 negative: int = 5, sample: float = 1e-3, alpha: float = 0.025, epochs: int = 5,
                 seed: int = 1, workers: int | None = None, batch: int = 1024) -> None:
        del workers  # тут один потік numpy
        self.vector_size, self.window, self.sg, self.negative = vector_size, window, sg, negative
        self.sample, self.alpha, self.epochs, self.batch = sample, alpha, epochs, batch
        self.rng = np.random.default_rng(seed)

        counts: dict[str, int] = {}
        for sent in sentences:
            for w in sent:
                counts[w] = counts.get(w, 0) + 1
        vocab = sorted((w for w, n in counts.items() if n >= min_count), key=lambda w: (-counts[w], w))
        self.counts = np.array([counts[w] for w in vocab], dtype=np.float64)
        n = len(vocab)
        self.wv = KeyedVectors(vector_size)
        self.wv.add_vectors(vocab, (self.rng.random((n, vector_size), dtype=np.float32) - 0.5) / vector_size)
        self.syn1neg = np.zeros((n, vector_size), dtype=np.float32)
        noise = self.counts**0.75
        self.noise_cdf = np.cumsum(noise / noise.sum())

        index = self.wv.key_to_index
        ids, sent_no = [], []
        for s, sent in enumerate(sentences):
            for w in sent:
                i = index.get(w)
                if i is not None:
                    ids.append(i)
                    sent_no.append(s)
        self.ids = np.array(ids, dtype=np.int64)
        self.sent_no = np.array(sent_no, dtype=np.int64)
        if len(self.ids) > 1:
            self.train()

    # --- підготовка прикладів однієї епохи
    def _epoch_tokens(self) -> tuple[np.ndarray, np.ndarray]:
        """Субсемплінг: дуже часті слова (the, a, and) частину разів пропускаємо."""
        if not self.sample:
            return self.ids, self.sent_no
        freq = self.counts / self.counts.sum()
        keep_p = np.minimum(1.0, (np.sqrt(freq / self.sample) + 1) * self.sample / freq)
        keep = self.rng.random(len(self.ids)) < keep_p[self.ids]
        return self.ids[keep], self.sent_no[keep]

    def _contexts(self, ids: np.ndarray, sent_no: np.ndarray) -> np.ndarray:
        """(N, 2·window) id сусідів кожного слова в межах речення і випадкового вікна; −1 — немає."""
        n = len(ids)
        reach = self.rng.integers(1, self.window + 1, n)  # як у word2vec: вікно від 1 до window
        ctx = np.full((n, 2 * self.window), -1, dtype=np.int64)
        col = 0
        for d in range(1, self.window + 1):
            for sign in (-1, 1):
                j = np.arange(n) + sign * d
                ok = (j >= 0) & (j < n) & (reach >= d)
                jj = np.clip(j, 0, n - 1)
                ok &= sent_no[jj] == sent_no
                ctx[:, col] = np.where(ok, ids[jj], -1)
                col += 1
        return ctx

    def _negatives(self, shape) -> np.ndarray:
        return np.searchsorted(self.noise_cdf, self.rng.random(shape))

    # --- навчання
    def train(self) -> None:
        w_in, w_out = self.wv.vectors, self.syn1neg
        plan = []
        for _ in range(self.epochs):
            ids, sent_no = self._epoch_tokens()
            ctx = self._contexts(ids, sent_no)
            if self.sg:
                center = np.repeat(ids, ctx.shape[1])
                other = ctx.ravel()
                keep = other >= 0
                plan.append((center[keep], other[keep]))
            else:
                has = (ctx >= 0).any(axis=1)
                plan.append((ids[has], ctx[has]))
        total = sum(len(p[0]) for p in plan)
        done = 0
        for center, other in plan:
            order = self.rng.permutation(len(center))
            for start in range(0, len(order), self.batch):
                k = order[start : start + self.batch]
                lr = max(self.alpha * (1 - done / total), self.alpha * 1e-4)
                done += len(k)
                if self.sg:
                    self._step_sg(w_in, w_out, center[k], other[k], lr)
                else:
                    self._step_cbow(w_in, w_out, center[k], other[k], lr)
        self.wv._normed = None

    def _neg_update(self, h: np.ndarray, target: np.ndarray, w_out: np.ndarray, lr: float) -> np.ndarray:
        """Справжнє слово → мітка 1, `negative` випадкових → 0. Повертає градієнт для h."""
        negs = self._negatives((len(target), self.negative))
        out_pos, out_neg = w_out[target], w_out[negs]
        g_pos = (1 - _sigmoid(np.einsum("bd,bd->b", h, out_pos))) * lr
        g_neg = -_sigmoid(np.einsum("bd,bkd->bk", h, out_neg)) * lr
        grad_h = g_pos[:, None] * out_pos + np.einsum("bk,bkd->bd", g_neg, out_neg)
        np.add.at(w_out, target, g_pos[:, None] * h)
        np.add.at(w_out, negs.ravel(), (g_neg[:, :, None] * h[:, None, :]).reshape(-1, h.shape[1]))
        return grad_h

    def _step_sg(self, w_in, w_out, center, context, lr) -> None:
        h = w_in[center]
        np.add.at(w_in, center, self._neg_update(h, context, w_out, lr))

    def _step_cbow(self, w_in, w_out, center, ctx, lr) -> None:
        mask = ctx >= 0
        count = mask.sum(axis=1, keepdims=True)
        h = (w_in[np.where(mask, ctx, 0)] * mask[:, :, None]).sum(axis=1) / count
        grad = self._neg_update(h, center, w_out, lr) / count
        rows = ctx[mask]
        np.add.at(w_in, rows, np.repeat(grad, mask.sum(axis=1), axis=0))

    def save(self, path: str) -> None:
        self.wv.save_word2vec_format(path, binary=True)
