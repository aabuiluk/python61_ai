import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


def main() -> None:
    data = fetch_california_housing(as_frame=True)
    df = data.frame
    features = ["MedInc", "HouseAge", "AveRooms", "AveBedrms"]
    X = df[features]
    y = df["MedHouseVal"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression().fit(X_train, y_train)
    pred = model.predict(X_test)

    coef_table = pd.DataFrame({"feature": features, "coef": model.coef_}).sort_values("coef", key=lambda s: s.abs(), ascending=False)
    print("R²:", round(r2_score(y_test, pred), 3))
    print(coef_table)


if __name__ == "__main__":
    main()
