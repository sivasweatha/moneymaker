from interfaces.candleInterface import CandleInterface

class Candle(CandleInterface):
    open: float
    high: float
    low: float
    close: float
    color: str
    time: str
    def __init__(self, open: float, high: float, low: float, close: float,  time="") -> bool: # pragma: no cover
        self.open, self.high, self.low, self.close = open, high, low, close
        if self.isRed():
            self.color = 'red'
        elif self.isGreen():
            self.color = 'green'
        else:
            self.color = 'doji'

    def isRed(self):
        if self.close < self.open :
            self.color = 'red'
            return True
        return False

    def isGreen(self):
        if self.close > self.open :
            self.color = 'green'
            return True
        return False

    def isDoji(self):
        if self.close == self.open:
            self.color = 'doji'
            return True
        return False