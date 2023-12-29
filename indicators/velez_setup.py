class VelezSetup:
    def __init__(self, df) -> None:
        ema_8 = df['close'].rolling(window=8).mean()
        ema_20 = df['close'].rolling(window=20).mean()
        ema_200 = df['close'].rolling(window=200).mean()

        df['large_candle'] = df['High'] - df['Low'] > 1.5 * (df['High'].rolling(window=24).max() - df['Low'].rolling(window=24).min())
        df['emas_close'] = abs(ema_8 - ema_20) < 0.01 * df['Close']

        df['Buy_Signal'] = df['large_candle'] & df['emas_close'] & (ema_8 > ema_20) & (ema_20 > ema_200)
        df['Sell_Signal'] = df['large_candle'] & df['emas_close'] & (ema_8 < ema_20) & (ema_20 < ema_200)

        self.df = df

    def get_signal(self):
        latest_data = self.df.iloc[-1]
        if latest_data['Buy_Signal']:
            return True
        elif latest_data['Sell_Signal']:
            return False
        else:
            return None