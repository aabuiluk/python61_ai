from pathlib import Path

import pandas as pd


DATA = Path(__file__).with_name("Lesson6_01_ratings.csv")


def main() -> None:
    df = pd.read_csv(DATA)
    freq = df["rating"].value_counts().sort_index()
    rel = (freq / freq.sum()).round(3)
    cum = rel.cumsum().round(3)

    print(pd.DataFrame({"freq": freq, "rel": rel, "cum": cum}), end="\n\n")
    print("mode:", df["rating"].mode().tolist())
    print("median:", df["rating"].median())
    print("mean:", round(df["rating"].mean(), 2))


if __name__ == "__main__":
    main()
