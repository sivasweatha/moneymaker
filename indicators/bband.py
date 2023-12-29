from ta.volatility import BollingerBands as bband

class BollingerBands:
    def __init__(self, df):
        bb = bband(df['close'], window=20, window_dev=2)
        df['bb_high'] = bb.bollinger_hband()
        df['bb_low'] = bb.bollinger_lband()
        self.data = df

    def get_signal(self):
        latest_data = self.data.iloc[-1]
        if latest_data['close'] < latest_data['bb_low']:
            return True
        elif latest_data['close'] > latest_data['bb_high']:
            return False
        else:
            return None