import pandas as pd

data = {
    "name": ["Anna", "Maksym", "Ira", "Bohdan", "Nazar"],
    "age": [19, 21, 20, 22, 19],
    "city": ["Lviv", "Kyiv", "Dnipro", "Odesa", "Lviv"],
}
df = pd.DataFrame(data)
print(df)
print(df.shape)


import pandas as pd

name = ["Anna", "Maksym", "Ira", "Bohdan", "Nazar", "Andrii", "Oleh"]
age = [19, 21, 20, 22, 19, 14, 16]
city = ["Lviv", "Kyiv", "Dnipro", "Odesa", "Lviv", "Odesa", "Lviv"]
data = {"name": name, "age": age, "city": city}
df = pd.DataFrame(data)
print(df)
print(df.shape)
print(df.columns)
print(df.head(3))

import pandas as pd

df = pd.DataFrame(
    {
        "movie": ["Dune", "Coco", "Interstellar", "Soul", "Avatar", "Inside Out"],
        "year": [2021, 2017, 2014, 2020, 2009, 2015],
        "rating": [8.1, 8.4, 8.7, 8.0, 7.9, 8.2],
    }
)

df1 = pd.DataFrame(
    {
        "movie": ["Data", "Coco1", "Interstellar", "Soul", "Avatar", "Inside Out"],
        "year": [2021, 2017, 2014, 2020, 2009, 2015],
        "rating": [1.1, 8.1, 8.7, 8.0, 7.9, 8.2],
    }
)
print(df.head(3))
print(df.tail(2))
print(df.sample(2, random_state=61))
print(df1.sample(2, random_state=61))

print("#################################")

import pandas as pd

df = pd.DataFrame(
    {
        "student": ["Anna", "Maksym", "Ira", "Bohdan"],
        "score": [95, 88, 91, 76],
        "hours": [8.5, 7.0, 8.0, 5.5],
    }
)
print(df.info())
print("#################################")
print(df.describe())
print("#################################")
print(df.isna().sum())

from pathlib import Path

df = pd.read_csv(Path(__file__).with_name("movies1.csv"))
print(df.isna().sum())