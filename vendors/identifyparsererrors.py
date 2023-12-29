import pandas as pd

df1 = pd.read_csv('./data.csv')

from dateutil.parser import parse, ParserError

error_rows = []

for index, value in df1['time'].items():
    try:
        parse(value)
    except ParserError:
        error_rows.append(index)
print(df1.loc[error_rows])