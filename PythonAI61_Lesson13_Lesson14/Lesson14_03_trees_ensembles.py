from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


def main() -> None:
    df = fetch_california_housing(as_frame=True).frame
    X = df.drop(columns=["MedHouseVal"])
    y = df["MedHouseVal"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    tree = DecisionTreeRegressor(max_depth=5, random_state=42).fit(X_train, y_train)
    forest = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)
    print("Tree R²:", round(r2_score(y_test, tree.predict(X_test)), 3))
    print("Forest R²:", round(r2_score(y_test, forest.predict(X_test)), 3))


if __name__ == "__main__":
    main()
