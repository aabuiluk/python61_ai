import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


def main() -> None:
    df = fetch_california_housing(as_frame=True).frame
    print(df.shape)
    print(df.describe().T[["mean", "std"]].head())

    X = df[["MedInc", "HouseAge", "AveRooms", "AveBedrms"]]
    y = df["MedHouseVal"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression().fit(X_train, y_train)
    print("R²:", round(r2_score(y_test, model.predict(X_test)), 3))


if __name__ == "__main__":
    main()
