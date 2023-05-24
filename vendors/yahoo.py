from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime as dt
from time import sleep
from maps import ordersClosingMap, stockCodes
yf.pdr_override()

class YahooFinance:
    onTicks = lambda ticks: None
    whenClose = lambda self, stock: ordersClosingMap.get(stock) <= dt.now().hour * 100 + dt.now().minute
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
        self.sleepUntilNextCandle(interval)
        while True:
            print(self.whenClose(stock))
            if self.whenClose(stock):
                self.onClose()
                break
            data = self.getData(stockCodes[stock]['yfinance'], interval)
            lastCandle = data[-2]
            self.onTicks(lastCandle, data)
            self.sleepUntilNextCandle(interval)

    def sleepUntilNextCandle(self, interval):
        time_value = int(interval[:-1]) * 60
        now = dt.now()
        sleep(self.waitForNextCandle(now.minute, now.second, time_value))