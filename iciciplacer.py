from argparse import ArgumentParser
from candle import Candle
from strategy import Strategy
from trend import Trend
from orderdecider import OrderDecider
from vendors.tradingviewPaperTrader import PaperTrade
from env import paperTradeCookie, iciciApiKey, iciciApiSecret
from maps import stockCodes
from datetime import datetime as dt
from datetime import timedelta as td
from breeze_connect import BreezeConnect

class IciciPlacer:
    def __init__(self, exchange, interval, session_token, stock):
        self.exchange, self.interval, self.session_token, self.stock = exchange, interval, session_token, stock
        self.breeze = BreezeConnect(iciciApiKey)
        self.breeze.generate_session(api_secret=iciciApiSecret, session_token=self.session_token)
        self.pt = PaperTrade(paperTradeCookie)
        self.prevDayData = self.breeze.get_historical_data(interval=self.interval,
                                    from_date= (dt.utcnow() - td(days=5)).strftime("%Y-%m-%dT07:00:00.000Z"),
                                    to_date= dt.now().strftime("%Y-%m-%dT07:00:00.000Z"),
                                    stock_code=stockCodes[self.stock]['icici'],
                                    exchange_code=self.exchange,
                                    product_type="cash")
        self.prevDayData['Success'] = [{k: float(v) for k, v in d.items() if k in Candle.__init__.__code__.co_varnames} for d in self.prevDayData['Success']]
        self.dayCandle = self.prevDayData['Success'][-1]
        self.dayCandle = {k: float(v) for k, v in self.dayCandle.items() if k in Candle.__init__.__code__.co_varnames}
        self.prevDayCandle = Candle(**self.dayCandle)
        self.trend = Trend(self.prevDayData['Success'])
        self.strategy = Strategy(self.prevDayCandle)
        self.stockToken = self.breeze.get_stock_token_value(self.exchange, stockCodes[self.stock]['icici'])[0]
        self.breeze.ws_connect()
        self.breeze.on_ticks = self.on_ticks
        self.breeze.subscribe_feeds(stock_token=self.stockToken,interval=self.interval)

    def on_ticks(self, cur_candle):
        print("next candle comes")
        cur_candle = {k: float(v) for k, v in cur_candle.items() if k in Candle.__init__.__code__.co_varnames}
        self.candle = Candle(**cur_candle)
        decider = OrderDecider(self.candle, self.trend, self.strategy)
        order = decider.decide()
        if order:
            status = self.pt.checkList(key="symbol", item=stockCodes[self.stock]['tvPaperTrader'], orders=self.pt.getOrders())
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
            status = self.pt.checkList(key="symbol", item=stockCodes[self.stock]['tvPaperTrader'], orders=self.pt.getOrders())
            id = status['parent'] if status and self.pt.checkList(key="id", item=status['parent'], orders=self.pt.getOrders()) else None
            if id:
                self.pt.cancel(id)
        print(cur_candle)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("stock", type=str, help="Stock symbol")
    parser.add_argument("-i", "--interval", type=str, help="Interval", default="30minute", metavar="", action="store")
    parser.add_argument("-e", "--exchange", type=str, help="Exchange Code", default="NSE", metavar="", action="store")
    parser.add_argument("sessiontoken", type=str, help="Session Token")
    args = parser.parse_args()
    return args

args = parse_args()

iciciplacer = IciciPlacer(args.exchange, args.interval, args.sessiontoken, args.stock)