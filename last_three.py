# Import yfinance
import yfinance as yf

# Fetch NSE price data, from last 3 one minute candles
data = yf.download('INTC', period='200m', interval='5m')

# Display the data
print(data)