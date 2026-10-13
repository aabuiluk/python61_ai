from sklearn.datasets import fetch_california_housing, load_breast_cancer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


def main() -> None:
    housing = fetch_california_housing(as_frame=True).frame
    X_h, y_h = housing.drop(columns=["MedHouseVal"]), housing["MedHouseVal"]
    X_train, X_test, y_train, y_test = train_test_split(X_h, y_h, test_size=0.2, random_state=42)

    gbr = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    gbr.fit(X_train, y_train)
    rf.fit(X_train, y_train)
    print("GBR R²:", round(r2_score(y_test, gbr.predict(X_test)), 3))
    print("RF R²:", round(r2_score(y_test, rf.predict(X_test)), 3))

    cancer = load_breast_cancer()
    X_c, y_c = cancer.data, cancer.target
    X_tr, X_te, y_tr, y_te = train_test_split(X_c, y_c, test_size=0.2, random_state=42)
    clf = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    pred = clf.predict(X_te)
    print("Confusion matrix:\n", confusion_matrix(y_te, pred))
    print("Accuracy:", round(accuracy_score(y_te, pred), 3))
    print("Precision:", round(precision_score(y_te, pred), 3))
    print("Recall:", round(recall_score(y_te, pred), 3))
    print("F1:", round(f1_score(y_te, pred), 3))


if __name__ == "__main__":
    main()
