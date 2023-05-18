from argparse import ArgumentParser
from candle import Candle
from emastrategy import Strategy
from trend import Trend
from orderdecider import OrderDecider
from vendors.tradingviewPaperTrader import PaperTrade
from env import paperTradeCookie, iciciApiKey, iciciApiSecret
from maps import stockCodes, stockClosingMap, ordersClosingMap
from datetime import datetime as dt
from datetime import timedelta as td
from breeze_connect import BreezeConnect

parser = ArgumentParser()
parser.add_argument("stock", type=str, help="Stock symbol")
parser.add_argument("-i", "--interval", type=str, help="Interval", default="30minute", metavar="", action="store")
parser.add_argument("-e", "--exchange", type=str, help="Exchange Code", default="NSE", metavar="", action="store")
parser.add_argument("sessiontoken", type=str, help="Session Token")
args = parser.parse_args()
stock = args.stock
exchange = args.exchange
interval = args.interval
session_token=args.sessiontoken

breeze = BreezeConnect(iciciApiKey)
breeze.generate_session(api_secret=iciciApiSecret, session_token=session_token)

stockToken = breeze.get_stock_token_value(exchange, stockCodes[stock]['icici'])[0]
# print(breeze.get_stock_token_value(exchange, stock)[0])
print(exchange, interval, stockToken, stock)
breeze.ws_connect()
# print(args)


def writeToTxt(savedData):
    now = dt.now()
    fileName = f"./logs/log-{stock}-{now.strftime('%Y.%m.%d')}.txt"
    with open(fileName, "a") as outfile:
        outfile.write(savedData)

pt = PaperTrade(paperTradeCookie)

prevDayData = breeze.get_historical_data(interval=interval,
                            from_date= (dt.utcnow() - td(days=5)).strftime("%Y-%m-%dT07:00:00.000Z"),
                            to_date= dt.now().strftime("%Y-%m-%dT07:00:00.000Z"),
                            stock_code=stockCodes[stock]['icici'],
                            exchange_code=exchange,
                            product_type="cash")
prevDayData['Success'] = [{k: float(v) for k, v in d.items() if k in Candle.__init__.__code__.co_varnames} for d in prevDayData['Success']]
dayCandle = prevDayData['Success'][-1]
dayCandle = {k: float(v) for k, v in dayCandle.items() if k in Candle.__init__.__code__.co_varnames}
prevDayCandle = Candle(**dayCandle)
trend = Trend(prevDayData['Success'])
strategy = Strategy(prevDayCandle)

def on_ticks(cur_candle):
    print("next candle comes")
    cur_candle = {k: float(v) for k, v in cur_candle.items() if k in Candle.__init__.__code__.co_varnames}
    candle = Candle(**cur_candle)
    decider = OrderDecider(candle, trend, strategy)
    order = decider.decide()
    if order:
        status = pt.checkList(key="symbol", item=stockCodes[stock]['tvPaperTrader'], orders=pt.getOrders())
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
        status = pt.checkList(key="symbol", item=stockCodes[stock]['tvPaperTrader'], orders=pt.getOrders())
        id = status['parent'] if status and pt.checkList(key="id", item=status['parent'], orders=pt.getOrders()) else None
        if id:
            cancel = pt.cancel(id)
            writeToTxt('\n' + str(cancel))
    print(cur_candle)

breeze.on_ticks = on_ticks
breeze.subscribe_feeds(stock_token=stockToken,interval=interval)