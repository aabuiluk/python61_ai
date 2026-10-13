from __future__ import annotations

import numpy as np

from nlp_vectors import GLOVE, W2V, load_vectors

ANALOGIES = [
    "france paris japan tokyo",
    "germany berlin italy rome",
    "good better bad worse",
    "big bigger small smaller",
    "phone screen laptop keyboard",
    "camera photos headphones sound",
]

result = model.wv.most_similar(
    positive=["paris", "italy"],
    negative=["france"],
    topn=5
)
print(result)