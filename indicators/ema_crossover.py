class EmaCrossover:
    def __init__(self, df):
        df['EMA_8'] = df['close'].ewm(span=8, adjust=False).mean()
        df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

        df['Buy_Signal'] = (df['EMA_8'] > df['EMA_20']) & (df['EMA_8'].shift(1) < df['EMA_20'].shift(1))
        df['Sell_Signal'] = (df['EMA_8'] < df['EMA_20']) & (df['EMA_8'].shift(1) > df['EMA_20'].shift(1))
        print(df['EMA_8'])
        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]
        if latest_data['Buy_Signal']:
            return True
        elif latest_data['Sell_Signal']:
            return False
        else:
            return None
