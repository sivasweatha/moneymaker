from argparse import ArgumentParser
from imports import alphaVantageApiKey
import requests

class AlphaDataDownload:
    def download_to_csv(self, url, header_status = True):
        import csv

        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if header_status:
                writer.writerows(my_list)
            elif not header_status:
                writer.writerows(my_list[1:])

    def download_to_json(self, url):
        import json

        r = requests.get(url)
        data = r.json()
        f = open("data.json", "a")
        json.dump(data, f, indent=4)

    def daily_time_series(self, symbol, method):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={alphaVantageApiKey}&datatype=csv'

        if method == 'json':
            self.download_to_json(url)
        elif method == 'csv':
            self.download_to_csv(url)

    def intraday_time_series(self, symbol, interval, adjusted, years, months):
        import time

        counter = 0
        header_status = True
        while counter < 24:
            years = counter // 12 + 1
            months = counter % 12 + 1

            slice = f'year{str(years)}month{str(months)}'
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval={interval}&slice={slice}&adjusted={adjusted}&apikey={alphaVantageApiKey}'

            self.download_to_csv(url, header_status)

            if header_status:
                header_status = False

            print(f"Downloaded data for year {years} month {months}.")
            counter += 1

            if years == 2 and months == 12:
                break

            if months % 5 == 0 or months == 12:
                print("Waiting...")
                time.sleep(60)

    def conversion_to_dataframe(self):
        import pandas as pd

        df = pd.read_csv('data-csv/aapl-daily.csv')
        df = df.sort_values('timestamp', ascending=True)
        df.to_csv('aapl-sorted_file.csv', index=False)

if __name__ == "__main__":
    def parse_args():
        parser = ArgumentParser()
        parser.add_argument("stock", type=str, help="Stock symbol")
        args = parser.parse_args()
        print(f"Stock: {args.stock}.")
        return args

    args = parse_args()
    symbol = args.stock
    # interval = '5min'
    # adjusted = 'false'
    # years = 1
    # months = 1

    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=nifty&apikey={alphaVantageApiKey}'
    r = requests.get(url)
    data = r.json()

    print(data)

    # ad = AlphaDataDownload()
    # ad.intraday_time_series(symbol, interval, adjusted, years, months)
    # ad.daily_time_series(symbol,method="csv")