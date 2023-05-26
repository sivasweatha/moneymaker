import yfinance as yf
import csv

class Scanner:
    def near_20_EMA():
        symbols = []

        with open('stocks.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row['Symbol']
                try:
                    data = yf.download(symbol, period="30d", interval="1d", progress=False)
                    ema_20 = data['Close'].ewm(span=20, adjust=False).mean()
                    if ema_20[-1] - 10 < data['Close'][-1] > ema_20[-1] + 10 :
                        symbols.append(symbol)
                except Exception as e:
                    print(f"Error downloading data for {symbol}: {e}")

scanner = Scanner()
print(scanner.near_20_EMA())