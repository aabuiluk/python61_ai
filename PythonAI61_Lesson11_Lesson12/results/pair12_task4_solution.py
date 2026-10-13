from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def main() -> None:
    data = fetch_california_housing(as_frame=True)
    X = data.frame.drop(columns=["MedHouseVal"])
    y = data.frame["MedHouseVal"]

    model = Pipeline([("scaler", StandardScaler()), ("reg", LinearRegression())])
    scores = cross_val_score(model, X, y, cv=5, scoring="r2")
    print("R² mean:", round(scores.mean(), 3))
    print("R² std:", round(scores.std(), 3))
    print("folds:", [round(value, 3) for value in scores])


if __name__ == "__main__":
    main()
