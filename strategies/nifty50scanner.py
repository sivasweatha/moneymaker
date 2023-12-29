from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
import csv
from vendors.yahoo import YahooFinance
from playsound import playsound
import concurrent.futures

yahoo = YahooFinance()
interval = '30m'

with open('stocks/stocks.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader, None)
    nifty_50 = []
    for row in reader:
        symbol = row[0]
        nifty_50.append(symbol)

def process_stock(symbol):
    # Download data
    print(symbol)
    data = yahoo.download(symbol, days=55, interval = interval)
    print(data)
    # Calculate Bollinger Bands and RSI
    bb = BollingerBands(data['Close'], window=20, window_dev=2)
    data['bb_high'] = bb.bollinger_hband()
    data['bb_low'] = bb.bollinger_lband()
    rsi = RSIIndicator(data['Close'], window=14)
    data['rsi'] = rsi.rsi()

    # Check the latest data
    latest_data = data.iloc[-1]
    print(latest_data)
    if latest_data['Close'] > latest_data['bb_high'] or latest_data['rsi'] > 70:
        playsound('assets/tada.mp3')
        print(f"Sell signal for {symbol}")
    elif latest_data['Close'] < latest_data['bb_low'] or latest_data['rsi'] < 30:
        playsound('assets/tada.mp3')
        print(f"Buy signal for {symbol}")

while True:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_stock, nifty_50)

    yahoo.wait_for_interval(interval)