import requests
import json
import pandas as pd
import slack
import ssl
from env import slackOauthToken

class BTST:
    def __init__(self, stock="NIFTY 50") -> None:
        self.url = "https://www.nseindia.com/api/equity-stockIndices?index="+stock
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'
        }
        self.sess = requests.Session()
        self.stock = stock

    def set_data(self):
        self.df = self.get_data(self.url)
        self.df = self.format_data(self.df)

    def get_data(self, url):
        response = self.sess.get(url, headers=self.headers, timeout=5)
        if response.status_code == 200:
            return response.text
        return ""

    def format_data(self, data):
        try:
            data = json.loads(data)["data"]
            df = pd.json_normalize(data)
            df = df.drop(['priority','identifier', 'series', 'pChange', 'lastUpdateTime', 'yearHigh', 'ffmc', 'yearLow', 'nearWKH', 'nearWKL', 'perChange365d', 'date365dAgo', 'chart365dPath', 'date30dAgo', 'perChange30d', 'chart30dPath', 'chartTodayPath', 'meta.symbol', 'meta.companyName', 'meta.industry', 'meta.activeSeries', 'meta.debtSeries', 'meta.tempSuspendedSeries', 'meta.isFNOSec', 'meta.isCASec', 'meta.isSLBSec', 'meta.isDebtSec', 'meta.isSuspended', 'meta.isETFSec', 'meta.isDelisted', 'meta.isin', 'meta.quotepreopenstatus.equityTime', 'meta.quotepreopenstatus.preOpenTime', 'meta.quotepreopenstatus.QuotePreOpenFlag'], axis="columns")
            df = df[df['symbol'] != self.stock]
            return df
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error formatting data: {e}")
            return None

    def best_stock(self):
        df = self.df.sort_values(by='totalTradedValue', ascending=False)

        df = df.head(5)
        df = df.sort_values(by='totalTradedVolume', ascending=False)

        df['ltp_open_diff'] = df['lastPrice'] - df['open']

        df = df[df['ltp_open_diff']==df['ltp_open_diff'].max()]

        df = df[df['ltp_open_diff'] > 5]
        if df.empty:
            return "No Stocks Found"
        return df.T

class SendToSlack:
    def __init__(self, token: str):
        self.client = slack.WebClient(token=token, ssl=ssl.SSLContext())

    def send_message(self, message, channel="#auto-trading"):
        self.client.chat_postMessage(channel=channel, text=message)

def slack_print(message, sts: SendToSlack, channel = None):
    print(message)
    sts.send_message(message, channel)

btst = BTST()
btst.set_data()
sts = SendToSlack(slackOauthToken)

if btst.best_stock() is None:
    print("No Stocks Found")
else:
    sts.send_message("3:20 Trade :chart_with_upwards_trend: :\n", "#auto-trading")
    slack_print(btst.best_stock().to_string(), sts, "#auto-trading")