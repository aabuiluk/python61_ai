import pandas as pd

products = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'Назва': ['A', 'B', 'C', 'D', 'E'], 'Ціна': [10, 20, 15, 30, 25]})
sales = pd.DataFrame({'ID': [1, 2, 3, 4, 5], 'Кількість': [5, 3, 8, 2, 6]})
df = products.merge(sales, on='ID')
df['Сума'] = df['Ціна'] * df['Кількість']
print(df)
