import numpy as np

class Volume:
    def __init__(self, df):
        df['Volume Change'] = df['Volume'].pct_change(5)
        volume_threshold = 0.5

        df['Buy Signal'] = np.where((df['Volume Change'] > volume_threshold), 1, 0)
        df['Sell Signal'] = np.where((df['Volume Change'] > volume_threshold), -1, 0)

        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]

        if latest_data['Buy Signal']:
            return True
        elif latest_data['Sell Signal']:
            return False
        else:
            return None
