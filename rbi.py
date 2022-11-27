import pandas as pd
import datetime as dt
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf
import re

yf.pdr_override()

stock = ['AAPL']

def getData(stocks=[], interval='5m', period='200m'):
    df = pdr.get_data_yahoo(stocks, period=period, interval=interval)
    df: pd.DataFrame = df.drop('Adj Close', axis='columns').drop('Volume', axis='columns')

    df['Time'] = df.index
    df['Time'] = df['Time'].dt.tz_convert('America/New_York')
    df['Time'] = df['Time'].dt.strftime('%d/%m %H:%M:%S')

    df["Color"] = df.apply(
        lambda d: "red"if d.Close < d.Open else
        ("green"if d.Close > d.Open
        else "doji"),
        axis=1,
    )
    return df

dfJson = getData(stock, '5m', '200m').to_dict("records")

gbis = []
i = len(dfJson) - 1
while i >= 0:
    candle = dfJson.pop(i)
    if((['Color'] == "green") and (candle['Open'] < dfJson[i-1]['Close'])):
        gbis.append({candle1: dfJson[i-2]["Time"], candle2: dfJson[i-i]["Time"], candle3: candle["Time"]})
    i = i - 1
print(gbis)
