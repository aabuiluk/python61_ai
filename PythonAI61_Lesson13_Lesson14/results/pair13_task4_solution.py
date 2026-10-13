from sklearn.datasets import fetch_california_housing
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


def main() -> None:
    df = fetch_california_housing(as_frame=True).frame
    X = df.drop(columns=["MedHouseVal"])
    y = df["MedHouseVal"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for depth in (3, 8, None):
        tree = DecisionTreeRegressor(max_depth=depth, random_state=42).fit(X_train, y_train)
        train_r2 = r2_score(y_train, tree.predict(X_train))
        test_r2 = r2_score(y_test, tree.predict(X_test))
        print(f"depth={depth}: train={train_r2:.3f} test={test_r2:.3f}")


if __name__ == "__main__":
    main()
