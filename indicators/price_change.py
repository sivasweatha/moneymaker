import numpy as np

class PriceChange:
    def __init__(self, df):
        df['Price Change'] = df['close'].pct_change(5)
        price_threshold = 0.02

        df['Buy Signal'] = np.where((df['Price Change'] > price_threshold), 1, 0)
        df['Sell Signal'] = np.where((df['Price Change'] < -price_threshold), -1, 0)

        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]

        if latest_data['Buy Signal']:
            return True
        elif latest_data['Sell Signal']:
            return False
        else:
            return None