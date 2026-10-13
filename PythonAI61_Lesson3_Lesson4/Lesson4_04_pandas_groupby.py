"""Пара 4 · складніше. groupby, агрегації, нова колонка."""

from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).with_name("Lesson4_01_movies.csv"))
df["decade"] = (df["year"] // 10) * 10

by_genre = (
    df.dropna(subset=["rating"])
    .groupby("genre", as_index=False)
    .agg(n=("title", "size"), mean_rating=("rating", "mean"), min_year=("year", "min"))
    .sort_values("mean_rating", ascending=False)
)
print(by_genre.to_string(index=False), end="\n\n")
print("value_counts genre:\n", df["genre"].value_counts())
print("\nby decade:\n", df.groupby("decade")["title"].count())
print("OK")
