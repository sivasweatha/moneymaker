import yfinance as yf

#Day's 20ma
data = yf.download('KO', start="2021-01-01", end="2022-07-13")

data['20 SMA'] = data['Close'].rolling(window=20).mean()
data['200 SMA'] = data['Close'].rolling(window=200).mean()

print(data.tail())

#5m's ma
data = yf.download('KO', period='10000m', interval='5m')

data['20 SMA'] = data['Close'].rolling(window=20).mean()
data['200 SMA'] = data['Close'].rolling(window=200).mean()

print(data.tail())
