from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime as dt
from time import sleep
yf.pdr_override()
class YahooFinance:
    onTicks = lambda ticks: None
    whenClose = lambda: None
    onClose = lambda: None
    waitForNextCandle = lambda self, minute, seconds, wait=300: (wait - (minute % 10) * 60 - seconds) % wait if (minute % 5 != 0) or (seconds != 0) else 0

    def getData(self, stock: str, interval='5m', tz='Asia/Kolkata', showDF=False):
        df = pdr.get_data_yahoo(stock, period='2d', interval=interval, progress=False)
        df['time'] = df.index
        df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'})
        df = df.drop(['Adj Close', 'Volume'], axis='columns')
        if not showDF:
            return df.to_dict(orient='records')
        else:
            return df

    def getHistorical(self, stock: str, period: str):
        ticker = yf.Ticker(stock)
        histdf = ticker.history(period)
        histdf = histdf.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'})
        histdf = histdf.drop(['Volume', 'Dividends', 'Stock Splits'], axis='columns')
        return histdf

    def subscribeFeeds(self, stock, interval):
        intervalToSecMap = {
                '5m': 300,
                '1m': 60,
                '1s': 1,
                '30m': 1800
            }
        while True:
            if self.whenClose():
                self.onClose()
                break
            lastCandle = self.getData(stock, interval)[-2]
            self.onTicks(lastCandle)
            now = dt.now()
            sleep(self.waitForNextCandle(now.minute, now.second, intervalToSecMap[interval]))