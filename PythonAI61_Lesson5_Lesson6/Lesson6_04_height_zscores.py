from pathlib import Path

import pandas as pd


DATA = Path(__file__).with_name("Lesson6_02_heights.csv")


def main() -> None:
    df = pd.read_csv(DATA)
    mean = df["height"].mean()
    std = df["height"].std(ddof=1)
    df["height_z"] = (df["height"] - mean) / std

    print("percentiles:")
    print(df["height"].quantile([0.05, 0.25, 0.5, 0.75, 0.95]), end="\n\n")
    print("z outliers:", int((df["height_z"].abs() > 3).sum()))
    print(df.head())


if __name__ == "__main__":
    main()
