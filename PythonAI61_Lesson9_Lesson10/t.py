from sklearn.linear_model import LinearRegression

# X — години навчання
X = [[1], [2], [3], [4], [5]]
# y — оцінка
y = [50, 60, 70, 80, 90]

model = LinearRegression()
model.fit(X, y)
result = model.predict([[8]])
print(result)  # -> [100.]
# -> приблизно 100
# assert abs(result[0] - 100.0) < 1.0


from sklearn.linear_model import LinearRegression

# X — відстань, км
X = [[1], [2], [3], [4], [5]]
# y — час доставки, хв
y = [15, 25, 35, 45, 55]

model = LinearRegression()
model.fit(X, y)
mins = model.predict([[3.5]])
print(mins)  # -> [30.]
# -> приблизно 30 хв на 3.5 км
# assert abs(mins[0] - 30.0) < 1.0
