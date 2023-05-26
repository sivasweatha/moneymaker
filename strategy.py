from interfaces.strategyInterface import StrategyInterface
from candle import Candle

class Strategy(StrategyInterface):
    def __init__(self, dayCandle: Candle = {}, curCandle: Candle = {}, prevCandle: Candle = {}, prev2Candle: Candle = {}) -> None:
        self.dayCandle = dayCandle
        self.curCandle, self.prevCandle, self.prev2Candle = curCandle, prevCandle, prev2Candle

    def CPR(self) -> dict:
        pivot = {}
        high = self.dayCandle.high
        low = self.dayCandle.low
        close = self.dayCandle.close

        pivot["p"] = (high + low + close) / 3
        pivot["bCPR"] = (high + low) / 2
        pivot["tCPR"] = (pivot["p"] - pivot["bCPR"]) + pivot["p"]

        pivot["r1"] = (2 * pivot["p"]) - low
        pivot["s1"] = (2 * pivot["p"]) - high
        pivot["r2"] = pivot["p"] + (pivot["r1"] - pivot["s1"])
        pivot["s2"] = pivot["p"] - (pivot["r1"] - pivot["s1"])
        pivot["r3"] = high + 2 * (pivot["p"] - low)
        pivot["s3"] = low - 2 * (high - pivot["p"])
        pivot["r4"] = pivot["r3"] + (pivot["r2"] - pivot["r1"])
        pivot["s4"] = abs(pivot["s1"] - (pivot["s2"] + pivot["s3"]))

        pivot["prevHigh"] = high
        pivot["prevLow"] = low

        return pivot

    def isBull180(self) -> bool:
        curCandle, prevCandle = self.curCandle, self.prevCandle
        if (
            (curCandle.color == "green") and
            (prevCandle.color == "red") and
            (curCandle.close >= prevCandle.open) and
            ()
        ):
            return True
        return False

    def isBear180(self) -> bool:
        curCandle, prevCandle = self.curCandle, self.prevCandle
        if (
            (curCandle.color == "red") and
            (prevCandle.color == "green") and
            (curCandle.close <= prevCandle.open)
        ):
            return True
        return False

    def isGbi(self) -> bool:
        curCandle, prevCandle, prev2Candle = self.curCandle, self.prevCandle, self.prev2Candle
        if (
            (prev2Candle.color == "red") and
            (prevCandle.color == "green") and
            (curCandle.color == "red") and
            (curCandle.close <= prevCandle.open)
        ):
            return True
        return False

    def isRbi(self) -> bool:
        curCandle, prevCandle, prev2Candle = self.curCandle, self.prevCandle, self.prev2Candle
        if (
            (prev2Candle.color == "green") and
            (prevCandle.color == "red") and
            (curCandle.color == "green") and
            (curCandle.close >= prevCandle.open)
        ):
            return True
        return False