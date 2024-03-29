from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep
from lib.maps import stockCodes
import requests
yf.pdr_override()

class YahooFinance:
    onTicks = lambda ticks: None
    duration = lambda: None
    onClose = lambda: None
    waitForNextCandle = lambda self, minute, seconds, wait=300: (wait - (minute % 10) * 60 - seconds) % wait if (minute % 5 != 0) or (seconds != 0) else 0

    def getData(self, stock: str, interval='5m', showDF=False):
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

    def download(self, stock:str, days:int, interval:str):
        today = dt.today()
        start = today - td(days=days)
        start = start.date()
        end = today - td(days=1)
        end = end.date()
        data = yf.download(tickers=stock, start=start, end=end, interval=interval, prepost=False, repair=True, progress=False, group_by="ticker")
        data = data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'})
        data = data.drop(['Volume', 'Adj Close'], axis='columns')
        data['time'] = data.index
        data['time'] = data['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        return data

    def subscribeFeeds(self, stock, interval):
        while True:
            print("Waiting for next candle.")
            self.sleepUntilNextCandle(interval)
            print("Getting data from yfinance.", end="", flush=True)
            data = self.getData(stockCodes[stock]['yfinance'], interval)
            lastCandle = data[-2]
            print(u'\u2713')
            self.onTicks(lastCandle, data)
            print("Checking if time is within trading hours.", end="", flush=True)
            if not self.duration(stock):
                print("\nMarket closed.")
                self.onClose()
                break
            print(u'\u2713')

    def sleepUntilNextCandle(self, interval: str) -> None:
        time_value = int(interval[:-1]) * 60
        now = dt.now()
        sleep(self.waitForNextCandle(now.minute, now.second, time_value))

    def wait_for_interval(self, interval_str, offset_minutes=15):
        interval_minutes = int(interval_str[:-1])

        now = dt.now()
        minutes = (now.minute - offset_minutes) % interval_minutes
        seconds = now.second

        wait_minutes = interval_minutes - minutes if minutes < interval_minutes else 0
        wait_seconds = 60 - seconds if seconds > 0 else 0

        wait_time = wait_minutes * 60 + wait_seconds
        print(wait_time)
        sleep(wait_time)

    def searchStock(self, stock: str):

        search_url = "https://query2.finance.yahoo.com/v1/finance/search"
        query_params = {
            "q": stock,
            "lang": "en-US",
            "region": "US",
            "quotesCount": 6,
            "newsCount": 2,
            "listsCount": 2,
            "enableFuzzyQuery": False,
            "quotesQueryId": "tss_match_phrase_query",
            "multiQuoteQueryId": "multi_quote_single_token_query",
            "newsQueryId": "news_cie_vespa",
            "enableCb": True,
            "enableNavLinks": True,
            "enableEnhancedTrivialQuery": True,
            "enableResearchReports": True,
            "enableCulturalAssets": True,
            "enableLogoUrl": True,
            "researchReportsCount": 2
        }

        headers = {'user-agent': 'curl/7.55.1', 'accept': 'application/json'}
        response = requests.get(search_url, params=query_params, headers=headers)
        data = response.json()
        if "quotes" in data and len(data["quotes"]) > 0:
            return data["quotes"]
        else:
            return "No search results found."