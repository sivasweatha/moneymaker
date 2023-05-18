import json
import yfinance as yf
import pandas as pd

class EMAStrategy:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.df = self.get_data()
        self.df['EMA20'] = self.df['Close'].ewm(span=20).mean()
        self.qty = 100

    def get_data(self):
        ticker = yf.Ticker(self.symbol)
        df = ticker.history(start=self.start_date, end=self.end_date, period="5m")
        df = df.drop(['Volume', 'Dividends', 'Stock Splits'], axis='columns')
        return df

    def backtest(self, capital):
        self.capital = capital

        orders = []
        position = 0  # 0: flat, 1: long, -1: short

        for i in range(1, len(self.df)):
            side = ''
            if self.df['Close'][i] > self.df['EMA20'][i] and self.df['Close'][i-1] <= self.df['EMA20'][i-1]:

                if position == 0 or position == -1:
                    stop_loss_price = self.df['EMA20'][i] - 2
                    target_price = self.df['EMA20'][i] + 4
                    side = 'buy'
                    position = 1

            elif self.df['Close'][i] < self.df['EMA20'][i] and self.df['Close'][i-1] >= self.df['EMA20'][i-1]:

                if position == 0 or position == 1:
                    stop_loss_price = self.df['EMA20'][i] + 2
                    target_price = self.df['EMA20'][i] - 4
                    side = 'sell'
                    position = -1
            if side:
                orders.append({'time': str(self.df.index[i]) ,'side':side, 'qty':self.qty, 'price': self.df['EMA20'][i], 'sl':stop_loss_price, 'tp':target_price})

        return orders

symbol = 'AAPL'
start_date = '2010-01-01'
end_date = '2023-02-01'

strategy = EMAStrategy(symbol, start_date, end_date)
orders = strategy.backtest(capital=10000)
with open('backtester.json', 'w') as j:
    json.dump(orders, j, indent=4)