import pandas as pd
from vendors.yahoo import YahooFinance
from lib.maps import stockCodes
from playsound import playsound

interval = '30m'
stock = 'NIFTY50'

yahoo = YahooFinance()

prevdf = yahoo.download(stockCodes[stock]['yfinance'],days=55, interval=interval)

while True:
    df = yahoo.getData(stockCodes[stock]['yfinance'], interval, showDF=True)

    # Calculate the moving averages
    df = pd.concat([prevdf, df])
    print(df)
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()

    # Calculate the trading signals
    df['Buy_Signal'] = (df['SMA_50'] > df['SMA_200']) & (df['SMA_50'].shift(1) < df['SMA_200'].shift(1))
    df['Sell_Signal'] = (df['SMA_50'] < df['SMA_200']) & (df['SMA_50'].shift(1) > df['SMA_200'].shift(1))

    # Check the latest signals
    latest_data = df.iloc[-1]
    print(latest_data)

    if latest_data['Buy_Signal']:
        playsound('assets/tada.mp3')
        print('Buy Signal!')
    elif latest_data['Sell_Signal']:
        playsound('assets/tada.mp3')
        print('Sell Signal!')
    else:
        signal = None

    yahoo.wait_for_interval(interval)