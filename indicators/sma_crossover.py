class SmaCrossover:
    def __init__(self, df):
        df['SMA_8'] = df['close'].rolling(window=8).mean()
        df['SMA_20'] = df['close'].rolling(window=20).mean()

        df['Buy_Signal'] = (df['SMA_8'] > df['SMA_20']) & (df['SMA_8'].shift(1) < df['SMA_20'].shift(1))
        df['Sell_Signal'] = (df['SMA_8'] < df['SMA_20']) & (df['SMA_8'].shift(1) > df['SMA_20'].shift(1))
        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]
        if latest_data['Buy_Signal']:
            return True
        elif latest_data['Sell_Signal']:
            return False
        else:
            return None
