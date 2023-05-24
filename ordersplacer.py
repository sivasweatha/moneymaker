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

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("stock", type=str, help="Stock symbol")
    parser.add_argument("interval", type=str, help="Interval")
    args = parser.parse_args()
    print(f"Given Stock: {args.stock}")
    print(f"Given Interval: {args.interval}")
    return args

args = parse_args()
pt = PaperTrade(paperTradeCookie)
yahoo = YahooFinance()
prevDayData = yahoo.getHistorical(stock=stockCodes[args.stock]['yfinance'], period='2d')
dayCandle = prevDayData.iloc[0]
prevDayCandle = Candle(**dayCandle)
strategy = Strategy(prevDayCandle)

def onTicks(cur_candle, data):
    print("next candle comes")
    candle = Candle(**cur_candle)
    trend = Trend(data)
    decider = OrderDecider(candle, trend, strategy)
    order = decider.decide()

    if order:
        status = pt.checkList(key="symbol", item=args.stock, orders=pt.getOrders())
        id = status['parent'] if status and pt.checkList(key="id", item=status['parent'], orders=pt.getOrders()) else None
        exp = dt.now() + td(days=1)
        exp = round(exp.timestamp())
        orderKwargs = dict(symbol=stockCodes[args.stock]['tvPaperTrader'], side=order['side'], type="limit", qty=10, price=order['entry'], exp=exp, tp=order['target'], sl=order['stoploss'])
        if id:
            order = pt.modify(id, **{k: v for k, v in orderKwargs.items() if k in pt.modify.__code__.co_varnames})
            order.update({'message': 'modified'})
        else:
            order = pt.place(**orderKwargs)
            order.update({'message': 'placed'})
        print(order)
        print(f"Order {order['message']}")
    else:
        status = pt.checkList(key="symbol", item=args.stock, orders=pt.getOrders())
        id = status['parent'] if status and pt.checkList(key="id", item=status['parent'], orders=pt.getOrders()) else None
        if id:
            pt.cancel(id)

def onClose():
    status = pt.checkList(key="symbol", item=args.stock, orders=pt.getOrders())
    id = status['parent'] if status and pt.checkList(key="id", item=status['parent'], orders=pt.getOrders()) else None
    if id:
        pt.cancel(id)

yahoo.onTicks = onTicks
yahoo.onClose = onClose
yahoo.subscribeFeeds(stock=stockCodes[args.stock]['yfinance'], interval=args.interval)