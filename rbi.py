import pandas as pd
import datetime as dt
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf
import re

yf.pdr_override()

# end = dt.datetime.now()
# start = end - dt.timedelta(minutes=500)

stock = ['AAPL']


#calculate 20 period sma
# ma = 20
df = pdr.get_data_yahoo(stock, period='50m', interval='5m')
# df['20 SMA'] = df['Close'].rolling(window=ma).mean()
# df = df.iloc[ma:]
df = df.drop('Adj Close', axis='columns').drop('Volume', axis='columns')
df['Time'] = df.index
df['Time'] = df['Time'].dt.tz_convert('America/New_York')
df['Time'] = df['Time'].dt.strftime('%d/%m %H:%M:%S')
# if (df['Close'] < df['Open'] == True).all():
#     df['color'] = "red"
# elif (df['Close'] > df['Open'] == True).all():
#     df["color"] = "green"
df["Color"] = df.apply(
    lambda d: "red"if d.Close < d.Open else
    ("green"if d.Close > d.Open
    else "doji"),
    axis=1,
)

# print(df.values.tolist())

# Convert To Json Function
def convertToJson(data):
    # Creating an array
    records = []
    # While loop over every data lines (not header line)
    i = 1
    while i <= len(data) - 1:
        # Creating a json object
        record = {}
        # Spliting every space to get data
        values = data[i].split("  ")
        # Another while loop to loop over every col and set values
        j = 0
        while j <= len(df.columns) - 1:
            record[df.columns[j]] = values[j]
            j = j + 1
        # Pushing json object into array
        records.append(record)
        i = i + 1
    return records

i = 0
dfTxt = df.to_string(header=True, index=False).replace('    ', '  ')
dfTxt = dfTxt.split("\n")
dfJson =convertToJson(dfTxt)
# print(dfTxt)
while i <= len(dfJson):
    print(dfJson.pop(i))
    # if((dfJson[i]['green'] == True) and (dfJson[i]['Open'] < dfJson[i-1]['Close'])):
    #     print("green bar ignored")
# green red green
# i = i + 1