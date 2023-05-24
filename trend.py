import json
from interfaces.trendInterface import TrendInterface
import pandas as pd
import numpy as np

class Trend(TrendInterface):
    data: dict

    def __init__(self, data: list) -> bool:
        self.data = data

    def findAllEma(self, periods, showDF = False):
        df = pd.DataFrame(self.data)
        df = df.sort_index()
        df['ema'] = df['close'].ewm(span=periods, adjust=False).mean()
        if showDF:
            return df
        else:
            return df.to_dict(orient='records')

    def findAllTrend(self, showDF=False):
        df = self.findAllEma(20, showDF=True)
        df['uptrend'] = df['ema'] < df['close']
        df['downtrend'] = df['ema'] > df['close']
        df['uptrend'] = df['uptrend'].astype(bool)
        df['downtrend'] = df['downtrend'].astype(bool)
        if showDF:
            return df
        else:
            return df.to_dict(orient='records')

    def isSideways(self):
        df = self.findAllTrend(showDF=True)
        last_five = df.iloc[-5:]
        downtrend = last_five['downtrend']
        uptrend = last_five['uptrend']
        if not downtrend.all() and not uptrend.all() and not downtrend.eq(False).all() and not uptrend.eq(False).all():
            return True
        else:
            return False

    def isUptrend(self):
        df = self.findAllTrend()
        return df[-2]['uptrend']

    def getTrend(self):
        if self.isSideways() == True:
            return None
        return True if self.isUptrend() else False

if __name__ == "__main__":
    from vendors.yahoo import YahooFinance
    yahoo = YahooFinance()
    data = yahoo.getData(stock="HDFCBANK.NS")
    # print(data)
    t = Trend(data)
    # print(t.findAllEma(20, showDF=False))
    f = open("ema-aapl-2.txt", "a")
    json.dump(t.findAllEma(20, showDF=False), f, indent=4)
    # print(t.isUptrend())
    # print(t.getTrend())
    # print(t.isSideways())