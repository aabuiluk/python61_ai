from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA = Path(__file__).with_name("transactions.csv")


def main() -> None:
    df = pd.read_csv(DATA)
    clean = df.dropna(subset=["amount"]).copy()
    amount = clean["amount"]

    print("== HEAD ==")
    print(df.head(), end="\n\n")
    print("== MISSING ==")
    print(df.isna().sum(), end="\n\n")
    print("== SUMMARY ==")
    print(amount.describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.95]), end="\n\n")
    print("median:", amount.median())
    print("mode:", amount.mode().tolist())
    print("variance:", round(amount.var(ddof=1), 2))
    print("std:", round(amount.std(ddof=1), 2))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    amount.plot(kind="hist", bins=8, ax=axes[0], title="Amount histogram")
    amount.plot(kind="box", ax=axes[1], title="Amount boxplot")
    plt.tight_layout()
    plt.savefig(Path(__file__).with_suffix('.png'), dpi=120, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
