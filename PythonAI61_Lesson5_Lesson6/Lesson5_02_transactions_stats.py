from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA = Path(__file__).with_name("transactions1.csv")


def main() -> None:
    df = pd.read_csv(DATA)
    clean = df.dropna(subset=["amount"]).copy()
    amount = clean["amount"]

    print("== SUMMARY ==")
    print("mean:", amount.mean())
    print("median:", amount.median())
    print("std:", amount.std())
    print("size:", amount.size)




if __name__ == "__main__":
    main()
