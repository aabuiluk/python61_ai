from sklearn.linear_model import LinearRegression
X = [[50], [50], [80], [80], [65]]   # площа, кімнати
y = [95, 120, 150, 180, 135]                        # ціна, тис.
m = LinearRegression().fit(X, y)
print("ваги:", m.coef_.round(2), " зсув:", round(m.intercept_, 1))
# -> дві ваги: ~1.5 за м² площі, ~13 за кожну кімнату


from sklearn.linear_model import LinearRegression
X = [[50, 1], [50, 3], [80, 2], [80, 4], [65, 3]]   # площа, кімнати
y = [95, 120, 150, 180, 135]                        # ціна, тис.
m = LinearRegression().fit(X, y)
print("ваги:", m.coef_.round(2), " зсув:", round(m.intercept_, 1))
# -> дві ваги: ~1.5 за м² площі, ~13 за кожну кімнату