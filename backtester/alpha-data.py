import csv
import json
import time
from env import alphaVantageApiKey
import requests

symbol = 'AAPL'
interval = '5min'
adjusted = 'false'
years = 2
months = 12

slice = f'year{str(years)}month{str(months)}'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={alphaVantageApiKey}&datatype=csv'

with requests.Session() as s:
    download = s.get(url)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(my_list)

# r = requests.get(url)
# data = r.json()
# f = open("data.json", "w")
# json.dump(data, f, indent=4)

# print(data)

while months <= 12:
    slice = f'year{str(years)}month{str(months)}'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={symbol}&interval={interval}&slice={slice}&djusted={adjusted}&apikey={alphaVantageApiKey}'

    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

    with open('data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(my_list)

    print(f"Downloaded month {months}.")
    months = months + 1
    if months % 5 == 0:
        print("Waiting to not sussify Alpha Vantage...\n<.<....>.>")
        time.sleep(60)

    if years == 2 and months == 12:
        break
        # years = 1
        # symbol =

    if months == 12:
        months = 1
        years = 2

import pandas as pd

df = pd.read_csv('data-csv/aapl-daily.csv')

df = df.sort_values('timestamp', ascending=True)

df.to_csv('aapl-sorted_file.csv', index=False)
