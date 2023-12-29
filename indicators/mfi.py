from ta.volume import MFIIndicator

class MFI:
    def __init__(self, df):
        mfi = MFIIndicator(df['high'], df['low'], df['close'], df['Volume'], window=14)
        df['mfi'] = mfi.money_flow_index()
        df['Buy Signal'] = (df['mfi'].shift() < df['mfi'])
        df['Sell Signal'] = (df['mfi'].shift() > df['mfi'])
        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]

        if latest_data['Buy Signal']:
            True
        elif latest_data['Sell Signal']:
            False
        else:
            None