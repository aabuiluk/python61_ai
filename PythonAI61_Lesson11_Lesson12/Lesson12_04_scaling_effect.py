"""Пара 12 · з StandardScaler і без: коефіцієнти й R²."""

from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

df = fetch_california_housing(as_frame=True).frame
X = df[["MedInc", "HouseAge", "AveRooms", "AveBedrms"]]
y = df["MedHouseVal"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

raw = LinearRegression().fit(X_train, y_train)
scaled = Pipeline([("scaler", StandardScaler()), ("reg", LinearRegression())]).fit(X_train, y_train)

print("raw   R²", round(r2_score(y_test, raw.predict(X_test)), 3), "coef", [round(float(c), 3) for c in raw.coef_])
reg = scaled.named_steps["reg"]
print("scale R²", round(r2_score(y_test, scaled.predict(X_test)), 3), "coef", [round(float(c), 3) for c in reg.coef_])
