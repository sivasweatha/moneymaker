import multiprocessing
import csv
import logging
from indicators.indicators import Indicators
from vendors.yahoo import YahooFinance
from playsound import playsound
import pandas as pd
import colorama
import argparse
from lib.maps import timings

class StockProcessor:
    def __init__(self, symbols: list, indicators: list, interval: str='30m', day: int=55):
        self.yahoo = YahooFinance()
        self.symbols = symbols
        self.interval = interval
        self.indicators = indicators
        self.day = day

    def process_stock(self, symbol):
        try:
            df1 = self.yahoo.download(symbol, days=self.day, interval=self.interval)
            df2 = self.yahoo.getData(symbol, self.interval, showDF=True)
            df = pd.concat([df1, df2])
            indicators = Indicators(df)
            signal = indicators.decide(self.indicators)

            if signal:
                self.print_in_color("GREEN", f"Buy signal for {symbol}")
                playsound('assets/tada.mp3')
                logging.info(f'Buy signal for {symbol}')
            elif signal == False:
                self.print_in_color("RED",f"Sell signal for {symbol}")
                playsound('assets/tada.mp3')
                logging.info(f'Sell signal for {symbol}')
        except (AttributeError, KeyError):
            print(f"Data not found or symbol may be delisted for {symbol}. Skipping to next symbol.")

    def run(self, offset):
        while True:
            with multiprocessing.Pool() as pool:
                pool.map(self.process_stock, self.symbols)
            self.yahoo.wait_for_interval(self.interval, offset)
            print("The next candle comes...")

    def print_in_color(self, color, text):
        colorama.init()
        print(getattr(colorama.Fore, color) + text + colorama.Fore.RESET)

def read_from_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # Skip header row
        return [row[0] for row in reader]

def process_arguments():
    parser = argparse.ArgumentParser(description="Process stock data.")
    parser.add_argument("-s", "--stocks_csv", type=str, default="stocks.csv",
                        help="Stocks CSV filename (default: stocks.csv)")
    parser.add_argument("-i", "--indicators_csv", type=str, default="1-star.csv",
                        help="Indicators CSV filename (default: 1-star.csv)")
    parser.add_argument("-p", "--period", type=str, default="30m",
                        help="Period value (default: 30m)")
    parser.add_argument("-d", "--days", type=int, default=55,
                        help="Days value (default: 55)")
    return parser.parse_args()

logging.basicConfig(filename=f'logs/{process_arguments().stocks_csv.split(".")[0]}.log', level=logging.INFO, format='%(asctime)s: %(message)s')

if __name__ == '__main__':
    args = process_arguments()

    print("Running scanner with:")
    print(f"Stocks Filename: {args.stocks_csv} \nIndicators CSV: {args.indicators_csv} \nPeriod: {args.period} \nDay: {args.days}")

    symbols = read_from_csv(f"stocks/{args.stocks_csv}")
    indicators = read_from_csv(f"indicator_sets/{args.indicators_csv}")

    processor = StockProcessor(symbols, indicators, interval=args.period, day=args.days)
    processor.run(timings[args.stocks_csv])