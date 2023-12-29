import json
from . import all_indicators as indi
import pandas

class Indicators:
    def __init__(self, data: pandas.DataFrame, indicator_map: str ="indicators.json") -> None:
        self.indicator_map = indicator_map
        self.data = data

    def get_signal(self, indicators: list):
        output = {}
        indicator_map = self.get_indicator_map()
        for i in indicators:
            class_name = indicator_map[i]
            indicator_class = getattr(getattr(indi, i), class_name)(self.data)

            data = indicator_class.get_signal()
            output[i] = data
        return output

    def decide(self, indicators: list):
        signals = self.get_signal(indicators)
        values = list(signals.values())

        if all(element is True for element in values):
            return True
        elif all(element is False for element in values):
            return False
        elif all(element is None for element in values):
            return None
        else:
            return None


    def get_indicator_map(self):
        return json.load(open(self.indicator_map))