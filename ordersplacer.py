from argparse import ArgumentParser
from candle import Candle
from strategy import Strategy
from trend import Trend
from vendors.yahoo import YahooFinance
from orderdecider import OrderDecider
from vendors.tradingviewPaperTrader import PaperTrade
from env import paperTradeCookie
from maps import stockCodes, stockClosingMap, ordersClosingMap
from datetime import datetime as dt
from datetime import timedelta as td
import time

parser = ArgumentParser()
parser.add_argument("stock", type=str, help="Stock symbol")
args = parser.parse_args()
stock = args.stock
print(args)

def writeToTxt(savedData):
    now = dt.now()
    fileName = f"./logs/log-{stock}-{now.strftime('%Y.%m.%d')}.txt"
    with open(fileName, "a") as outfile:
        outfile.write(savedData)

pt = PaperTrade(paperTradeCookie)
yahoo = YahooFinance()

now = dt.now()
waitFor = yahoo.waitForNextCandle(now.minute, now.second)
time.sleep(waitFor)

prevDayData = yahoo.getHistorical(stock=stockCodes[stock]['yfinance'], period='2d')
dayCandle = prevDayData.iloc[0]
prevDayCandle = Candle(**dayCandle)
strategy = Strategy(prevDayCandle)

while stockClosingMap.get(stock) >= dt.now().hour * 100 + dt.now().minute:
# while stockClosingMap.get(stock) <= dt.now().hour * 100 + dt.now().minute:
    print("next candle comes")
    data = yahoo.getData(stock=stockCodes[stock]['yfinance'])
    cur_candle = data[-2]
    candle = Candle(**cur_candle)
    trend = Trend(data)
    decider = OrderDecider(candle, trend, strategy)
    order = decider.decide()
    if ordersClosingMap.get(stock) >= dt.now().hour * 100 + dt.now().minute:
    # if ordersClosingMap.get(stock) <= dt.now().hour * 100 + dt.now().minute:
        if order:
            status = pt.checkList(key="symbol", item=stock, orders=pt.getOrders())
            id = status['parent'] if status and pt.checkList(key="id", item=status['parent'], orders=pt.getOrders()) else None
            exp = dt.now() + td(days=1)
            exp = round(exp.timestamp())
            orderKwargs = dict(symbol=stockCodes[stock]['tvPaperTrader'], side=order['side'], type="limit", qty=10, price=order['entry'], exp=exp, tp=order['target'], sl=order['stoploss'])
            if id:
                order = pt.modify(id, **{k: v for k, v in orderKwargs.items() if k in pt.modify.__code__.co_varnames})
                order.update({'message': 'modified'})
            else:
                order = pt.place(**orderKwargs)
                order.update({'message': 'placed'})
            print(order)
            print(f"Order {order['message']}")
            writeToTxt('\n' + str(order))
        else:
            status = pt.checkList(key="symbol", item=stock, orders=pt.getOrders())
            id = status['parent'] if status and pt.checkList(key="id", item=status['parent'], orders=pt.getOrders()) else None
            if id:
                cancel = pt.cancel(id)
                writeToTxt('\n' + str(cancel))
    else:
        status = pt.checkList(key="symbol", item=stock, orders=pt.getOrders())
        id = status['parent'] if status and pt.checkList(key="id", item=status['parent'], orders=pt.getOrders()) else None
        if id:
            cancel = pt.cancel(id)
            writeToTxt('\n' + str(cancel))
    now = dt.now()
    waitFor = yahoo.waitForNextCandle(now.minute, now.second)
    time.sleep(waitFor)