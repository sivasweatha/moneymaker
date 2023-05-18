from candle import Candle
from trend import Trend
from strategy import Strategy
from vendors.yahoo import YahooFinance

class OrderDecider:
    entry_price: float = None
    side: str = None
    def __init__(self, candle: Candle, trend: Trend, strategy: Strategy):
        self.candle = candle
        self.trend = trend
        self.strategy = strategy
        self.ema20 = trend.findAllEma(20)[-2]['ema']
        self.upTrend = trend.getTrend()
        self.pivot = strategy.CPR()
    def decide(self):
        order = {}
        order['entry'] = self.get_entry_price()
        if order['entry']:
            order['side'] = self.get_side()
            order['target'] = self.get_target_price(entry_price=order['entry'], side=order['side'])
            order['stoploss'] = self.get_stop_loss_price(entry_price=order['entry'], side=order['side'])
            return order
        return None

    def set_entry_and_side(self):
        if self.upTrend == True:
            # if self.candle.close == self.ema20:
                self.entry_price = self.ema20
                self.side = "buy"
        elif self.upTrend == False:
            self.entry_price = self.ema20
            self.side = "sell"
        else:
            self.entry_price = None

    def get_entry_price(self) -> float:
        if not self.entry_price:
            self.set_entry_and_side()
        return self.entry_price

    def get_side(self) -> str:
        if not self.side:
            self.set_entry_and_side()
        return self.side

    def get_target_price(self, entry_price: float, side: str) -> float:
        target_price = None
        if 'buy' in side:
            ranges = {key: value for key, value in self.pivot.items() if key not in ['s1', 's2']}
            if ranges:
                pivot_ranges_above_price = [value for value in ranges.values() if value > entry_price]
                if pivot_ranges_above_price:
                    target_price = min(pivot_ranges_above_price)
        elif 'sell' in side:
            ranges = {key: value for key, value in self.pivot.items() if key not in ['r1', 'r2']}
            if ranges:
                pivot_ranges_below_price = [value for value in ranges.values() if value < entry_price]
                if pivot_ranges_below_price:
                    target_price = max(pivot_ranges_below_price)
        return target_price

    def get_stop_loss_price(self, entry_price: float, side: str) -> float:
        stoploss_price = None
        if 'buy' in side:
            ranges = [range for range in self.pivot.values() if range < entry_price]
            if ranges:
                stoploss_price = max(ranges)
        elif 'sell' in side:
            ranges = [range for range in self.pivot.values() if range > entry_price]
            if ranges:
                stoploss_price = min(ranges)
        return stoploss_price

if __name__ == "__main__":
    yahoo = YahooFinance()

    data = yahoo.getData(stock="HDFCBANK.NS")
    t = Trend(data)
    cur_candle = data[-2]
    c = Candle(**cur_candle)

    data = yahoo.getHistorical(stock="HDFCBANK.NS", period='2d')
    prev_day = data.iloc[0]
    candle = Candle(**prev_day)
    s = Strategy(candle)

    od = OrderDecider(c, t, s)
    print(od.get_entry_price())

    print(od.decide())

    pivot = s.CPR()
    print(pivot)
    side = input("Name a side: ")
    entry_price = float(input("Price? :"))