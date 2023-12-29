from ta.momentum import WilliamsRIndicator

class Williams_R:
    def __init__(self, df):
        williams_r = WilliamsRIndicator(high=df['high'], low=df['low'], close=df['close'], lbp=14)
        df['Williams %R'] = williams_r.williams_r()
        df['Buy Signal'] = (df['Williams %R'].shift() < -80) & (df['Williams %R'] > -80)
        df['Sell Signal'] = (df['Williams %R'].shift() > -20) & (df['Williams %R'] < -20)
        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]
        if latest_data['Buy Signal']:
            return True
        elif latest_data['Sell Signal']:
            return False
        else:
            return None