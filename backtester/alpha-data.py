from env import alphaVantageApiKey
import requests

class AlphaDataDownload():
    def download_to_csv(self, url):
        import csv

        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(my_list)

    def download_to_json(self, url):
        import json

        r = requests.get(url)
        data = r.json()
        f = open("data.json", "w")
        json.dump(data, f, indent=4)

    def daily_time_series(self, method):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={alphaVantageApiKey}&datatype=csv'

        if method == 'json':
            self.download_to_json(url)
        elif method == 'csv':
            self.download_to_csv(url)

    def intraday_time_series(self, symbol, interval, adjusted, years, months):
        import time

        while months <= 12:
            slice = f'year{str(years)}month{str(months)}'
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval={interval}&slice={slice}&djusted={adjusted}&apikey={alphaVantageApiKey}'

            self.download_to_csv(url)

            print(f"Downloaded month {months}.")
            months = months + 1

            if months % 5 == 0:
                print("Waiting...")
                time.sleep(60)

            if years == 2 and months == 12:
                break

            if months == 12:
                months = 1
                years = 2

    def conversion_to_dataframe(self):
        import pandas as pd

        df = pd.read_csv('data-csv/aapl-daily.csv')
        df = df.sort_values('timestamp', ascending=True)
        df.to_csv('aapl-sorted_file.csv', index=False)

symbol = 'AAPL'
interval = '5min'
adjusted = 'false'
years = 2
months = 12

ad = AlphaDataDownload()