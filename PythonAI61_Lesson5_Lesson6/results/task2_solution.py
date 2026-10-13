import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    base = rng.normal(loc=8, scale=2, size=120).clip(1, None)
    arr = np.concatenate([base, [24, 27, 31, 36, 41]])
    s = pd.Series(arr, name="order_size")

    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mad = (s - s.median()).abs().median()
    outside = ((s < lower) | (s > upper)).mean()

    print("mean:", round(s.mean(), 2))
    print("median:", round(s.median(), 2))
    print("std:", round(s.std(ddof=1), 2))
    print("IQR:", round(iqr, 2))
    print("MAD:", round(mad, 2))
    print("skew:", round(s.skew(), 2))
    print("kurtosis:", round(s.kurt(), 2))
    print("outside whiskers share:", round(outside, 3))


if __name__ == "__main__":
    main()
