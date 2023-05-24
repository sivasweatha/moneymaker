import csv
from datetime import datetime
import pandas as pd
import numpy as np

class VWAPStrategy:
    def __init__(self):
        self.qty = 100
        self.df = self.get_data()
        self.prev_df = self.get_prevdata()
        self.calculate_vwap()

    def calculate_vwap(self):
        self.df['vwap'] = self.df.groupby('day', as_index=False).apply(self.vwap).reset_index(level=0, drop=True)
        return self.df

    def vwap(self, df):
        prices = (df['high'] + df['low'] + df['close']).div(3)
        vwap_value = (prices * df['volume']).cumsum() / df['volume'].cumsum()
        return vwap_value

    def get_prevdata(self):
        prev_df = pd.read_csv('../data-csv/aapl-daily-asc.csv')
        prev_df.index = prev_df['timestamp']
        prev_df = prev_df.drop(['adjusted_close', 'volume', 'dividend_amount' , 'split_coefficient'], axis='columns')
        prev_df = prev_df.tail(497)
        return prev_df

    def get_data(self):
        df = pd.read_csv('../data-csv/aapl-5min-asc.csv')
        df['time'] = pd.to_datetime(df['time'])
        df['day'] = df['time'].dt.date
        return df

    def calculate_pivots(self, time):
        date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date()
        i = self.prev_df.index.get_loc(str(date))
        pivot = {}
        pivot['prev_close'] = self.prev_df['close'][i-1]
        pivot['prev_high'] = self.prev_df['high'][i-1]
        pivot['prev_low'] = self.prev_df['low'][i-1]
        pivot["p"] = (pivot['prev_close'] + pivot['prev_high'] + pivot['prev_low']) / 3
        pivot["bCPR"] = (pivot['prev_high'] + pivot['prev_low']) / 2
        pivot["tCPR"] = (pivot["p"] - pivot["bCPR"]) + pivot["p"]
        pivot["r1"] = (2 * pivot["p"]) - pivot['prev_low']
        pivot["s1"] = (2 * pivot["p"]) - pivot['prev_high']
        pivot["r2"] = pivot["p"] + (pivot["r1"] - pivot["s1"])
        pivot["s2"] = pivot["p"] - (pivot["r1"] - pivot["s1"])
        pivot["r3"] = pivot['prev_high'] + 2 * (pivot["p"] - pivot['prev_low'])
        pivot["s3"] = pivot['prev_low'] - 2 * (pivot['prev_high'] - pivot["p"])
        pivot["r4"] = pivot["r3"] + (pivot["r2"] - pivot["r1"])
        pivot["s4"] = abs(pivot["s1"] - (pivot["s2"] + pivot["s3"]))
        return pivot

    def set_stoploss(self, side, pivot, vwap):
        stop_loss_price = None
        if side == 'buy':
            ranges = [range for range in pivot.values() if range < vwap]
            if ranges:
                stop_loss_price = max(ranges)
        elif side == 'sell':
            ranges = [range for range in pivot.values() if range > vwap]
            if ranges:
                stop_loss_price = min(ranges)
        return stop_loss_price

    def set_target(self, side, pivot, vwap):
        target_price = None
        if side == 'buy':
            ranges = {key: value for key, value in pivot.items() if key not in ['s1', 's2']}
            if ranges:
                pivot_ranges_above_price = [value for value in ranges.values() if value > vwap]
                if pivot_ranges_above_price:
                    target_price = min(pivot_ranges_above_price)
        elif side == 'sell':
            ranges = {key: value for key, value in pivot.items() if key not in ['r1', 'r2']}
            if ranges:
                pivot_ranges_below_price = [value for value in ranges.values() if value < vwap]
                if pivot_ranges_below_price:
                    target_price = max(pivot_ranges_below_price)
        return target_price

    def trades_check(self, trade, current_price, time):
        sl = trade['sl']
        tp = trade['tp']
        side = trade['side']

        if side == 'buy':
            if current_price <= sl:
                profit = (sl - trade['price']) * trade['qty']
                return {'time': time, 'profit': profit}
            elif current_price >= tp:
                profit = (tp - trade['price']) * trade['qty']
                return {'time': time, 'profit': profit}
        elif side == 'sell':
            if current_price >= sl:
                profit = (trade['price'] - sl) * trade['qty']
                return {'time': time, 'profit': profit}
            elif current_price <= tp:
                profit = (trade['price'] - tp) * trade['qty']
                return {'time': time, 'profit': profit}

    def get_profit(self, profits):
        with open('profits.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time', 'profit'])
            for profit in profits:
                if 'profit' in profit:
                    writer.writerow([profit['time'], profit['profit']])

    def backtest(self):
        orders = []
        profit = []
        for i in range(1, len(self.df)):
            if orders:
                res = self.trades_check(orders[-1], self.df['close'][i], self.df['time'][i])
                if res:
                    profit.append(res)
            pivot = self.calculate_pivots(self.df['time'][i])
            if self.df['close'][i] > self.df['vwap'][i]:
                side = 'buy'
                vwap = self.df['vwap'][i]
                stop_loss_price = self.set_stoploss(side, pivot, vwap)
                target_price = self.set_target(side, pivot, vwap)
            elif self.df['close'][i] < self.df['vwap'][i]:
                side = 'sell'
                stop_loss_price = self.set_stoploss(side, pivot, vwap)
                target_price = self.set_target(side, pivot, vwap)
                orders.append({
                    'time': str(self.df['time'][i]),
                    'side': side,
                    'qty': self.qty,
                    'price': self.df['close'][i],
                    'sl': stop_loss_price,
                    'tp': target_price
                })
        self.get_profit(profit)
        return orders

strategy = VWAPStrategy()
result = strategy.backtest()

# Calculate profits
for result in result:
    f = open("data-new.txt", "a")
    f.write(str(result)+"\n")
    f.close()

total = 0
with open('profits-new.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        total += float(row[1])
print(total)


# Plot data
# import plotly.graph_objs as go

# df = pd.read_csv('vwap.csv').head(400)

# fig = go.Figure(data=[go.Candlestick(x=df['time'],
#                 open=df['open'], high=df['high'],
#                 low=df['low'], close=df['close'])])

# fig.add_trace(go.Scatter(x=df['time'], y=df['vwap'],
#                 mode='lines', name='VWAP'))

# fig.show()


    # def set_stoploss(self, side, price):
    #     stop_loss_price = None
    #     if side == 'buy':
    #         stop_loss_price = price - 2
    #     elif side == 'sell':
    #         stop_loss_price = price + 2
    #     return stop_loss_price

    # def set_target(self, side, price):
    #     target_price = None
    #     if side == 'buy':
    #         target_price = price + 4
    #     elif side == 'sell':
    #         target_price = price - 4
    #     return target_price


# def set_stoploss(self, side, pivot, vwap):
#         stop_loss_price = None
#         if side == 'buy':
#             ranges = [range for range in pivot.values() if range < vwap]
#             if ranges:
#                 stop_loss_price = max(ranges)
#         elif side == 'sell':
#             ranges = [range for range in pivot.values() if range > vwap]
#             if ranges:
#                 stop_loss_price = min(ranges)
#         return stop_loss_price

#     def set_target(self, side, pivot, vwap):
#         target_price = None
#         if side == 'buy':
#             ranges = {key: value for key, value in pivot.items() if key not in ['s1', 's2']}
#             if ranges:
#                 pivot_ranges_above_price = [value for value in ranges.values() if value > vwap]
#                 if pivot_ranges_above_price:
#                     target_price = min(pivot_ranges_above_price)
#         elif side == 'sell':
#             ranges = {key: value for key, value in pivot.items() if key not in ['r1', 'r2']}
#             if ranges:
#                 pivot_ranges_below_price = [value for value in ranges.values() if value < vwap]
#                 if pivot_ranges_below_price:
#                     target_price = max(pivot_ranges_below_price)
#         return target_price