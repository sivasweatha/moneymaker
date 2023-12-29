class Fibonacci:
    def __init__(self, df):
        N = 20
        recent_data = df.tail(N)
        high, low = recent_data['high'].max(), df['low'].min()
        differences = high - low
        df['Fibonacci_38.2'] = high - 0.382 * differences
        df['Fibonacci_50.0'] = high - 0.5 * differences
        df['Fibonacci_61.8'] = high - 0.618 * differences

        df['Buy Signal'] = (df['close'] > df['Fibonacci_61.8']) & (df['close'].shift() < df['Fibonacci_61.8'])
        df['Sell Signal'] = (df['close'] < df['Fibonacci_38.2']) & (df['close'].shift() > df['Fibonacci_38.2'])
        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]

        if latest_data['Buy Signal']:
            True
        elif latest_data['Sell Signal']:
            False
        else:
            None