import pandas as pd

data = {'Імʼя': ['А', 'Б', 'В', 'Г', 'Д'], 'Вік': [25, 32, 28, 40, 22], 'Відділ': ['IT', 'HR', 'IT', 'HR', 'IT'], 'Зарплата': [70000, 45000, 55000, 42000, 80000]}
df = pd.DataFrame(data)
print(df[df['Зарплата'] > 50000])
print(df.sort_values('Вік'))
print(df.sort_values('Зарплата', ascending=False))
