
from typing import Union, Dict, List, Any, Optional
from interfaces.trendInterface import TrendInterface
import pandas as pd

class Trend(TrendInterface):
    def __init__(self, data: dict) -> None:
        self.data = data

    def findAllEma(self, periods: int, showDF: bool = False) -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        df = pd.DataFrame(self.data)
        df = df.sort_index()
        df['ema'] = df['close'].ewm(span=periods, adjust=False).mean()
        if showDF:
            return df
        else:
            return df.to_dict(orient='records')

    def findAllTrend(self, showDF=False)  -> Union[pd.DataFrame, List[Dict[str, Any]]]:
        df = self.findAllEma(20, showDF=True)
        df['uptrend'] = df['ema'] < df['close']
        df['downtrend'] = df['ema'] > df['close']
        df['uptrend'] = df['uptrend'].astype(bool)
        df['downtrend'] = df['downtrend'].astype(bool)
        if showDF:
            return df
        else:
            return df.to_dict(orient='records')

    def isSideways(self) -> bool:
        df = self.findAllTrend(showDF=True)
        last_five = df.iloc[-5:]
        downtrend = last_five['downtrend']
        uptrend = last_five['uptrend']
        if not downtrend.all() and not uptrend.all() and not downtrend.eq(False).all() and not uptrend.eq(False).all():
            return True
        else:
            return False

    def isUptrend(self) -> bool:
        df = self.findAllTrend()
        return df[-2]['uptrend']

    def getTrend(self) -> Optional[bool]:
        if self.isSideways() == True:
            return None
        return True if self.isUptrend() else False