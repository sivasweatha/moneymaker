from interfaces.candleInterface import CandleInterface
from config import Config

class Candle(CandleInterface):
    def __init__(self, open: float, high: float, low: float, close: float) -> None:
        self.open, self.high, self.low, self.close = open, high, low, close
        if self.isRed():
            self.color = 'red'
        elif self.isGreen():
            self.color = 'green'
        else:
            self.color = 'doji'
        self.cf = Config(open, high, low, close)
        z = self.zeroValidation([self.cf.greenTopTail, self.cf.redTopTail, self.cf.greenBottomTail, self.cf.redBottomTail])
        if z:
            self.cf = False

    def isRed(self) -> bool:
        if self.close < self.open :
            self.color = 'red'
            return True
        return False

    def isGreen(self) -> bool:
        if self.close > self.open :
            self.color = 'green'
            return True
        return False

    def isDoji(self) -> bool:
        if self.close == self.open:
            self.color = 'doji'
            return True
        return False

    def zeroValidation(self, arr: list) -> bool:
        for z in arr:
            if z == 0:
                return True
        return False

    def isBt(self) -> bool:
        open, close = self.open, self.close
        if not self.cf:
            return False
        else:
            self.cf.deltaFinder()

        if self.cf.body <= 5:
            if (close > open) or (close == open):
                if (
                    (self.cf.deltaGTGB <= 1.3) and
                    (self.cf.deltaGBGB <= 1)
                ):
                    return True
            elif open > close:
                if (
                    (self.cf.deltaRTRB <= 1.3) and
                    (self.cf.deltaRBRB <= 1)
                ):
                    return True
        return False

    def isTt(self) -> bool:
        open, close = self.open, self.close
        if not self.cf:
            return False
        else:
            self.cf.deltaFinder()

        if self.cf.body <= 5:
            if (close > open) or (close == open):
                if (
                    (round(self.cf.deltaGBGT) <= 1.3) and
                    (round(self.cf.deltaGTGT) <= 1)
                ):
                    return True
            elif open > close:
                if (
                    (round(self.cf.deltaRBRT) <= 1.3) and
                    (round(self.cf.deltaRTRT) <= 1)
                ):
                    return True
        return False