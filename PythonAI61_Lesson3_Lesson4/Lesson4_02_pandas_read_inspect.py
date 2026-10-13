"""Пара 4 · легко. Прочитати CSV і подивитись типи колонок."""

from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).with_name("Lesson4_01_movies.csv"))
print(df.head(), end="\n\n")
print("shape:", df.shape)
print("columns:", df.columns.tolist())
print(df.dtypes)
print("OK")
