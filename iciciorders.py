import asyncio
from datetime import datetime as dt
import time
from argparse import ArgumentParser
from candle import Candle
from trend import Trend
from strategy import Strategy
from maps import strategyOrder, stockExchangeMap, stockCodes, marketHoursMap
from trader import Trader

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("session_token", type=str, help="Session token for the trader")
    parser.add_argument("stock", type=str, help="Stock symbol")
    parser.add_argument("interval", type=str, help="Interval")
    args = parser.parse_args()
    print(args)
    return args

args = parse_args()
stock = args.stock
savedData = []

receiveData = Trader('yahoo')
trader = Trader('icici', args.session_token)

def duration(stock: str) -> bool:
        current_time = dt.now().hour * 100 + dt.now().minute
        exchange = stockExchangeMap[stock]
        open = marketHoursMap.get(exchange, {}).get("open")
        close = marketHoursMap.get(exchange, {}).get("close")
        if open > close:
            return current_time >= open or current_time <= close
        else:
            return open <= current_time <= close

async def alert(strategy, candle: Candle):
    side = strategyOrder(strategy)
    if side:
        entryPrice = lambda: candle.high if side == "Buy" else candle.low
        round_nearest = lambda x: round(x / 0.05) * 0.05
        entryPrice = round_nearest(entryPrice())
        sl = lambda: candle.low if side == "Buy" else candle.high
        slPrice = round_nearest(sl())
        target = lambda: entryPrice + 0.20 if side == "Buy" else  entryPrice - 0.20
        if trader:
            order = trader.placeOrder(stockName=stock, quantity=1, action=side, price=entryPrice, stopLoss=slPrice, target=target())
            print(f"Order placed at {entryPrice}")
            print(order)
            if order['targetOrder']:
                print(f"Order placed at {target}")
                print(order['targetOrder'])

def onTicks(cur_candle):
    savedData = receiveData.yahoo.getData(stock=stockCodes[stock]['yfinance'])
    cur_time = cur_candle['time']
    cur_dt = dt.strptime(cur_time, "%Y-%m-%d %H:%M:%S")
    candle = Candle(cur_candle['open'], cur_candle['high'], cur_candle['low'], cur_candle['close'])
    trend = Trend(savedData)
    uptrend = trend.isUptrend()

    for category in ['uptrend', 'downtrend', 'sideways']:
        if getattr(trend, f"is{category.capitalize()}")():
            asyncio.run(alert(cur_time, category, candle))

    for category in ['tt', 'bt']:
        if getattr(candle, f"is{category.capitalize()}")():
            if category == "bt" and uptrend:
                print("Buy - BT")
                asyncio.run(alert(category, candle))
            if category == "tt" and not uptrend:
                print("Sell - TT")
                asyncio.run(alert(category, candle))

    if cur_dt.hour * 100 + cur_dt.minute > duration(stock)-5:
        prev_candle = Candle(savedData[-3]['open'], savedData[-3]['high'], savedData[-3]['low'], savedData[-3]['close'])
        strategy = Strategy(candle, prev_candle)
        for category in ['bull180', 'bear180']:
            if getattr(strategy, f"is{category.capitalize()}")():
                if category == "bull180" and uptrend:
                    print("Buy - Bull180")
                    asyncio.run(alert(category, candle))
                if category == "bear180" and not uptrend:
                    print("Sell - Bear180")
                    asyncio.run(alert(category, candle))

    if cur_dt.hour * 100 + cur_dt.minute > duration(stock):
        prev2_candle = Candle(savedData[-4]['open'], savedData[-4]['high'], savedData[-4]['low'], savedData[-4]['close'])
        strategy = Strategy(candle, prev_candle, prev2_candle)
        for category in ['gbi', 'rbi']:
            if getattr(strategy, f"is{category.capitalize()}")():
                if category == "rbi" and uptrend:
                    print("Buy - RBI")
                    asyncio.run(alert(category, candle))
                if category == "gbi" and not uptrend:
                    print("Sell - GBI")
                    asyncio.run(alert(category, candle))

now = dt.now()
waitFor = receiveData.yahoo.waitForNextCandle(now.minute, now.second)
time.sleep(waitFor)

receiveData.subscribeData(stock=stock, onticks=onTicks)