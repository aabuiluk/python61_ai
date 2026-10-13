"""Пара 4 · середній. Типи, пропуски, фільтр рядків."""

from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).with_name("Lesson4_01_movies.csv"))
print("missing per column:\n", df.isna().sum(), end="\n\n")

# rating приходить як float (бо є порожня клітинка). year — int.
print("year dtype:", df["year"].dtype, "rating dtype:", df["rating"].dtype)

sci = df[df["genre"] == "Science Fiction"]
print("\nScience Fiction:\n", sci[["title", "year", "rating"]])

recent = df.loc[df["year"] >= 2016, ["title", "year"]]
print("\nyear >= 2016:\n", recent)

print("\ndropna rating:\n", df.dropna(subset=["rating"])[["title", "rating"]])
print("OK")
