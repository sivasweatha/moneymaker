from interfaces.strategyInterface import StrategyInterface
from candle import Candle

class Strategy(StrategyInterface):
    def __init__(self, dayCandle: Candle):
        self.dayCandle = dayCandle

    def CPR(self):
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