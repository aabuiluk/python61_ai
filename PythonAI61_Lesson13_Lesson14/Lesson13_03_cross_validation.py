from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def main() -> None:
    df = fetch_california_housing(as_frame=True).frame
    X = df.drop(columns=["MedHouseVal"])
    y = df["MedHouseVal"]
    pipe = Pipeline([("scaler", StandardScaler()), ("reg", LinearRegression())])

    cv_scores = cross_val_score(pipe, X, y, cv=5, scoring="r2")
    print("CV mean:", round(cv_scores.mean(), 3), "std:", round(cv_scores.std(), 3))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)
    print("single split R²:", round(r2_score(y_test, pipe.predict(X_test)), 3))


if __name__ == "__main__":
    main()
