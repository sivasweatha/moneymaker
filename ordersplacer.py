from argparse import ArgumentParser
from candle import Candle
from strategy import Strategy
from trend import Trend
from vendors.yahoo import YahooFinance
from orderdecider import OrderDecider
from vendors.tradingviewPaperTrader import PaperTrade
from env import paperTradeCookie
from maps import stockCodes
from datetime import datetime as dt
from datetime import timedelta as td

class OrderPlacer:
    def __init__(self, stock, interval) -> None:
        self.stock, self.interval = stock, interval
        self.pt = PaperTrade(paperTradeCookie)
        self.yahoo = YahooFinance()
        self.prevDayData = self.yahoo.getHistorical(stock=stockCodes[stock]['yfinance'], period='2d')
        self.dayCandle = self.prevDayData.iloc[0]
        self.prevDayCandle = Candle(**self.dayCandle)
        self.strategy = Strategy(self.prevDayCandle)

    def start(self):
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
            print("Now, placing/modifying order through vendor.")
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
            print(order)
            print(f"Order {order['message']}")
        else:
            status = self.pt.checkList(key="symbol", item=self.stock, orders=self.pt.getOrders())
            id = status['parent'] if status and self.pt.checkList(key="id", item=status['parent'], orders=self.pt.getOrders()) else None
            if id:
                self.pt.cancel(id)

    def onClose(self):
        status = self.pt.checkList(key="symbol", item=self.stock, orders=self.pt.getOrders())
        id = status['parent'] if status and self.pt.checkList(key="id", item=status['parent'], orders=self.pt.getOrders()) else None
        if id:
            self.pt.cancel(id)

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