import sys
from argparse import ArgumentParser
from datetime import datetime as dt
from datetime import timedelta as td
import requests
try:
    from lib.candle import Candle
    from lib.strategy import Strategy
    from lib.trend import Trend
    from vendors.yahoo import YahooFinance
    from lib.orderdecider import OrderDecider
    from vendors.tradingviewPaperTrader import PaperTrade
    from env import paperTradeCookie
    from lib.maps import stockCodes, stockExchangeMap, marketHoursMap
except ImportError as e:
    print(f"Failed to import a required module: {e}")
    sys.exit()

class OrderPlacer:
    def __init__(self, stock, interval):
        self.stock = stock
        self.interval = interval
        self.yahoo = YahooFinance()
        self.pt = PaperTrade(paperTradeCookie)

    def duration(self, stock: str) -> bool:
        current_time = dt.now().hour * 100 + dt.now().minute
        exchange = stockExchangeMap[stock]
        open = marketHoursMap.get(exchange, {}).get("open")
        close = marketHoursMap.get(exchange, {}).get("close")
        if open > close:
            return current_time >= open or current_time <= close
        else:
            return open <= current_time <= close

    def check_stock_mappings(self):
        try:
            stockExchangeMap[self.stock]
        except KeyError:
            print("Please check values in maps.json for this symbol.")
            sys.exit()

    def check_trading_hours(self):
        print("Checking if time is within trading hours.", end="", flush=True)
        if not self.duration(self.stock):
            print("\nMarket is currently closed for this stock's exchange.")
            sys.exit()
        print(u'\u2713')

    def check_tradingview_cookie(self):
        print("Checking TradingView Cookie.", end="", flush=True)
        try:
            if not self.pt.checkCookieValidity():
                raise ValueError()
        except ValueError:
            print("\nThere is an issue with TradingView and/or your TradingView cookie.")
            sys.exit()
        except requests.exceptions.SSLError:
            print("\nThere is an SSL Certification error. Please contact adminstrator: moneymaker@ulagellam.com.")
            sys.exit()
        print(u'\u2713')

    def download_strategy_data(self):
        print("Downloading data for strategy.", end="", flush=True)
        try:
            self.prevDayData = self.yahoo.getHistorical(stock=stockCodes[self.stock]['yfinance'], period='2d')
            self.dayCandle = self.prevDayData.iloc[0]
            self.prevDayCandle = Candle(**self.dayCandle)
            self.strategy = Strategy(self.prevDayCandle)
        except KeyError:
            print("\nPlease check the symbol and interval values in maps.json, might be an issue with the internet access.")
            sys.exit()
        print(u'\u2713')

    def start(self):
        self.check_stock_mappings()
        self.check_trading_hours()
        self.check_tradingview_cookie()
        self.download_strategy_data()
        self.yahoo.duration = self.duration
        self.yahoo.onTicks = self.onTicks
        self.yahoo.onClose = self.onClose
        self.yahoo.subscribeFeeds(stock=self.stock, interval=self.interval)

    def onTicks(self, cur_candle, data):
        print("New candle has arrived.")
        candle = Candle(**cur_candle)
        trend = Trend(data)
        decider = OrderDecider(candle, trend, self.strategy)
        print("Analyzed candle data.")
        order = decider.decide()
        if order:
            print("Now, placing/modifying order through vendor.", end="", flush=True)
            status = self.pt.checkList(key="symbol", item=self.stock, orders=self.pt.getOrders())
            id = status['parent'] if status and self.pt.checkList(key="id", item=status['parent'], orders=self.pt.getOrders()) else None
            exp = dt.now() + td(days=1)
            exp = round(exp.timestamp())
            orderKwargs = dict(symbol=stockCodes[self.stock]['tvPaperTrader'], side=order['side'], type="limit", qty=10, price=order['entry'], exp=exp, tp=order['target'], sl=order['stoploss'])
            if id:
                order = self.pt.modify(id, **{k: v for k, v in orderKwargs.items() if k in self.pt.modify.__code__.co_varnames})
                order.update({'message': 'modified'})
            else:
                order = self.pt.place(**orderKwargs)
                order.update({'message': 'placed'})
            print(u'\u2713')
            print(order)
            print(f"Order {order['message']}")
        else:
            print("Not placing orders.")
            status = self.pt.checkList(key="symbol", item=self.stock, orders=self.pt.getOrders())
            id = status['parent'] if status and self.pt.checkList(key="id", item=status['parent'], orders=self.pt.getOrders()) else None
            if id:
                self.pt.cancel(id)

    def onClose(self):
        status = self.pt.checkList(key="symbol", item=self.stock, orders=self.pt.getOrders())
        id = status['parent'] if status and self.pt.checkList(key="id", item=status['parent'], orders=self.pt.getOrders()) else None
        if id:
            self.pt.cancel(id)

if __name__ == "__main__":
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument("stock", type=str, help="Stock symbol")
        parser.add_argument("interval", type=str, help="Interval")
        args = parser.parse_args()
        print(f"Stock: {args.stock}. Interval: {args.interval}.")
        return args

    args = parse_args()

    orderplacer = OrderPlacer(args.stock, args.interval)
    orderplacer.start()