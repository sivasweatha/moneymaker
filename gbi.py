import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf

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

def findGbi(data):
    dfJson = data.to_dict("records")

    gbis = []
    i = len(dfJson) - 1
    while i >= 0:
        candle = dfJson.pop(i)
        if (i != 0):
            if(
                (candle['Color'] == "red") and
                (candle['Close'] < dfJson[i-1]['Open']) and
                (dfJson[i-1]['Color'] == "green") and
                (dfJson[i-2]['Color'] == "red")
            ):
                gbis.append({'candle1': dfJson[i-2]["Time"],
                            'candle2': dfJson[i-1]["Time"],
                            'candle3': candle["Time"]
                })
        i = i - 1
    return gbis

print(findGbi(getData(stock)))
