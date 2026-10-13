import pandas as pd

data = {'Імʼя': ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Є', 'Ж'], 'Курс': [1, 1, 2, 2, 3, 3, 1, 2], 'Оцінка': [85, 72, 90, 68, 78, 95, 88, 76]}
df = pd.DataFrame(data)
print(df.groupby('Курс')['Оцінка'].agg(['mean', 'min', 'max']))
