# Money Maker

Money Maker is a quantitative trading system that connects with ICICI Breeze Connect API and TradingView HTTP API. It implements EMA (Exponential Moving Average) strategy and includes event-driven backtesters for VWAP (Volume Weighted Average Price) and EMA strategies. The system also allows downloading data from Alpha Vantage API using a program integrated into the system.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Features](#features)
- [Flowchart Diagram](#flowchart-diagram)
- [Trading Statistics](#trading-statistics)

## Installation

1. Clone the repository: `git clone https://github.com/sivasweatha/moneymaker.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Setup Alpha Vantage, ICICIDIRECT and TradingView credentials.

## Setup

Create a file name "env.py". This file will include all your credentials. Make sure to add them in this format:
```python
paperTradeCookie = ""
iciciApiKey = ""
iciciApiSecret = ""
alphaVantageApiKey = ""
```

## Usage

1. Run the main application: `python3 ordersplacer.py <symbol> <interval>`. You would need to provide the symbol and interval in which the trading should occur. Consult the maps.json file for stock symbols and values timings. For example, you can try: `python3 ordersplacer.py HDFCBANK 5m`.
2. The program would start trading.
3. Check your TradingView account history for details on the trades.
4. Use the backtesters to analyze VWAP and EMA strategies. You can tweak the metrics until profitable.
5. You can design your own strategy with the backtester template.

Going live through your ICICIDIRECT account:
1. Run `python iciciplacer.py`. You would need to provide stock and the session token that can be found here: [https://api.icicidirect.com/apiuser/login?api_key=your_public_key](https://api.icicidirect.com/apiuser/login?api_key=your_public_key). Replace "your_public_key" with your public key.
2. You may provide the interval and exchange. By default it is set to, "30minute" and "NSE".
NOTE: When choosing interval, you have to provide with the full name, as in, "5minute", "1hour".
3. Login to your ICICIDIRECT account to find your trades.

## Features

- Integration with ICICI Breeze Connect API and TradingView HTTP API.
- Support for EMA (Exponential Moving Average) strategy and VWAP.
- Backtester for evaluating strategy performance.
- Downloading data from Alpha Vantage API integrated into the system.

## Flowchart Diagram

![Flowchart](https://github.com/sivasweatha/moneymaker/assets/8729837/5c53ac8a-3477-4c85-8605-323e123df061)

This flowchart outlines the step-by-step process of how the trading system executes trades. At the core of the system is the algorithm that receives market data, analyzes it and generates trading signals. These signals are then processed by the strategy module, which applies predefined trading strategies such as exponential moving averages (EMA). Once the strategies identify favorable trading opportunities, the execution module interacts with the vendor API to place trades based on the generated signals. The flowchart is a visual representation of the system's workflow.

## Trading Statistics

These are the trading statistics from backtesting on AAPL and TESLA for the past 2 years (March 2021 - March 2023).

| Strategy | Stoploss and Target | Profitability Ratio (Profit:Total Trades)|
|-----------------|-----------------|-----------------|
| Buy above, Short below VWAP | 1:2 stoploss and target | approx. 15:27209 |
| Buy above, Short below EMA | nearest CPR as stoploss and target | 4178:27209 |

These results aren't enough to overcome the losses.
