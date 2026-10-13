import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def main() -> None:
    df = fetch_california_housing(as_frame=True).frame.copy()
    df["Category"] = np.where(df["HouseAge"] > 30, "Old", "New")
    df.loc[df.sample(frac=0.05, random_state=42).index, "MedInc"] = np.nan

    X = df[["MedInc", "HouseAge", "AveRooms", "Category"]]
    y = df["MedHouseVal"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    prep = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer()), ("scaler", StandardScaler())]), ["MedInc", "HouseAge", "AveRooms"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["Category"]),
        ]
    )
    model = Pipeline([("prep", prep), ("reg", LinearRegression())]).fit(X_train, y_train)
    print("R²:", round(r2_score(y_test, model.predict(X_test)), 3))


if __name__ == "__main__":
    main()
