import pandas as pd
import datetime as dt
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

# end = dt.datetime.now()
# start = end - dt.timedelta(minutes=500)

stock = ['TATAPOWER.NS']

#calculate 20 period sma
ma = 20
df = pdr.get_data_yahoo(stock, period='200m', interval='5m')
df['20 SMA'] = df['Close'].rolling(window=ma).mean()
df = df.iloc[ma:]

df['red'] = df['Close'] < df['Open']
df['green'] = df['Close'] > df['Open']


df['rbi'] = ((df['red'] == True) & (df['Open'] > df['Close'].shift(1))).all()

# if()

# elif((df['green'] == True) and (df['Open'] < df['Close'].shift(1))):
#     print("green bar ignored")

print(df)

# print(df.to_csv("su.csv"))