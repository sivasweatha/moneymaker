from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime as dt
from time import sleep
from maps import marketHoursMap, stockCodes, stockExchangeMap
yf.pdr_override()

class YahooFinance:
    onTicks = lambda ticks: None
    def duration(self, stock: str) -> bool:
        current_time = dt.now().hour * 100 + dt.now().minute
        exchange = stockExchangeMap[stock]
        open = marketHoursMap.get(exchange, {}).get("open")
        close = marketHoursMap.get(exchange, {}).get("close")
        if open > close:
            return current_time >= open or current_time <= close
        else:
            return open <= current_time <= close
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
        while True:
            print("Waiting for next candle.")
            self.sleepUntilNextCandle(interval)
            print("Getting data from yfinance.", end="", flush=True)
            data = self.getData(stockCodes[stock]['yfinance'], interval)
            lastCandle = data[-2]
            print(u'\u2713')
            print(lastCandle)
            self.onTicks(lastCandle, data)
            print("Checking if time is within trading hours.", end="", flush=True)
            if not self.duration(stock):
                print("\nMarket closed.")
                self.onClose()
                break
            print(u'\u2713')

    def sleepUntilNextCandle(self, interval):
        time_value = int(interval[:-1]) * 60
        now = dt.now()
        sleep(self.waitForNextCandle(now.minute, now.second, time_value))