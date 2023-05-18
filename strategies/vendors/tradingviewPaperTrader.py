import datetime
import json
import time
from env import paperTradeCookie as cookie
# from keys import paperTradeCookie as cookie
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
        # data = {'start_date': start_date}
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
    pt = PaperTrade()

    # res = pt.place("NSE:IDFCFIRSTB", "buy", "limit", 20, 45.3, 1675925745)
    # print("Dear User Yogi, we have thus placed the order.")
    # id = res['id']
    # time.sleep(2)

    # pt.cancel(id)
    # print("Dear User Yogi, we have thus canceled the order.")

    # dicts = [
    #     {"lang": "Java", "version": "14"},
    #     {"lang": "Python", "version": "3.8"},
    #     {"lang": "C++", "version": "17"},
    # ]

    # key = "lang"
    # val = "C#"

    # d = next((d for d in dicts if d.get(key) == val), None)
    # print(d)

    stock = "HDFCBANK"
    positions = pt.getPositions()
    orders = pt.getOrders()
    funds = pt.getFunds()
    history = pt.history()
    status = pt.checkList("symbol", stock, orders=pt.getOrders())

    # print(positions)
    # print(orders)
    # print(funds)
    # print(status)
    # print(history)
    f = open("history.txt", "w")
    json.dump(history, f, indent=4)
    # id = status['parent']
    # print(id)

    # id = 718776365
    # print(pt.checkList(key="id", item=id, orders=pt.getOrders()))

    # for d in orders:
    #     for i in d.values():
    #         if i == stock:
    #             print(d)
    # for d in orders:
    #     print(d.values())
    # print(status)
    # print(status['id'])
    # exp = datetime.datetime.now() + datetime.timedelta(days=1)
    # exp = round(exp.timestamp())
    # new = pt.place(symbol=stock, price=27, exp=exp, side="sell", type="limit", qty=10, tp=25.50, sl=27.75)

    # id = status['parent']
    # order = pt.modify(id, price=26.40, sl=27, tp=25, qty=10)
    # print(order)


    # key = "symbol"
    # res = next((d for d in orders if d.get(key).endswith(stock)), None)
    # print(res)

    # res = {key:val for key, val in orders.items() if val.endswith(stock)}

    # print(res)

    # print(positions)
    # print(orders)
    # key = "symbol"
    # stock = "NSE:ASIANPAINT"
    # d = next((d for d in orders if d.get(key) == stock), None)
    # print(d)
    # print(funds)
    # print(pt.getOrders()[0]['id'])

    # res = []
    # for d in orders:
    #     for k, v in d.items():
    #         if k != key:
    #             continue
    #         if v.endswith(stock):
    #             res.append(d)
