import json
from env import paperTradeCookie as cookie
import requests

class PaperTrade:
    baseUrl = "https://papertrading.tradingview.com/trading"
    def __init__(self, paperTradeCookie: str = cookie) -> None:
        self.paperTradeCookie = paperTradeCookie

    def post(self, url, data, cookie = ""):
        response = requests.post(url, json=data, headers={'Cookie': cookie, 'Origin': 'https://in.tradingview.com'})
        return response

    def place(self, symbol, side, type, qty, price, exp, tp, sl) -> dict:
        data = {'symbol': symbol, 'side': side, 'type': type, 'qty': qty, 'price': price, 'expiration': exp, 'tp': tp, 'sl': sl}
        res = self.post(url=f"{self.baseUrl}/place", data=data, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res

    def modify(self, id, price, sl, tp, qty="") -> dict:
        data = {'id': id, 'price': price, 'sl': sl, 'tp': tp, 'qty': qty}
        res = self.post(url=f"{self.baseUrl}/modify", data=data, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res

    def cancel(self, id):
        data = {'id': id}
        res = self.post(url=f"{self.baseUrl}/cancel", data=data, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res

    def getOrders(self):
        res = self.post(url=f"{self.baseUrl}/account", data={}, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res['orders']

    def getPositions(self):
        res = self.post(url=f"{self.baseUrl}/account", data={}, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res['positions']

    def history(self):
        res = self.post(url=f"{self.baseUrl}/orders_history", data={}, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res

    def getAccHistory(self):
        res = self.post(url=f"{self.baseUrl}/get_account_history", data={}, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res

    def checkList(self, key, item, orders):
        res = next((d for d in orders if d.get(key) == item), None)
        return res

    def getFunds(self):
        res = self.post(url=f"{self.baseUrl}/account", data={}, cookie=self.paperTradeCookie)
        res = json.loads(res.content.decode("utf8"))
        return res['account']['balance']


if __name__ == "__main__":
    ...