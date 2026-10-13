import pandas as pd

data = {'Імʼя': ['Олексій', 'Марія', 'Іван', 'Анна', 'Петро'],
        'Вік': [25, 30, 22, 27, 35],
        'Місто': ['Київ', 'Львів', 'Харків', 'Одеса', 'Дніпро']}
df = pd.DataFrame(data)
print(df)
print('shape:', df.shape)
print('columns:', list(df.columns))
print(df.head(3))
