import yfinance as yf
import csv

symbols = []

with open('stocks.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        symbol = row['Symbol']
        try:
            data = yf.download(symbol, period="1d", interval="1d", progress=False)
            daily_return = data['Close'] + data['Open']
            symbols.append(daily_return)
        except Exception as e:
            print(f"Error downloading data for {symbol}: {e}")
print(symbols)