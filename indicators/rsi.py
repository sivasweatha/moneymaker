from ta.momentum import RSIIndicator

class RSI:
    def __init__(self, df):
        rsi = RSIIndicator(df['close'], window=14)
        df['rsi'] = rsi.rsi()
        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]
        if latest_data['rsi'] < 30:
            return True
        elif latest_data['rsi'] > 70:
            return False
        else:
            return None
