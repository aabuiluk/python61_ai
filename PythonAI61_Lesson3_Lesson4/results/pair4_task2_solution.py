from pathlib import Path
import pandas as pd

# requires movies.csv (provided in lesson pack)
df = pd.read_csv(Path(__file__).with_name('movies.csv'))
print(df.head())
print('shape:', df.shape)
print(df.dtypes)
print(df.isnull().sum())
