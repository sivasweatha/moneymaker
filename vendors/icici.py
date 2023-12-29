import subprocess
from breeze_connect import BreezeConnect
from lib.maps import stockCodes, orderMap
from env import iciciApiKey, iciciApiSecret

class Icici(BreezeConnect):
    response_formatter = lambda self, response: response['Success']

    def __init__(self, sessionToken) -> None:
        self.api_key = iciciApiKey
        self.sessionToken = sessionToken
        self.generate_session(api_secret=iciciApiSecret, session_token=sessionToken)

    def order(self, stock_code, action, quantity, price, stopLoss, target):
        if not self.getPositions():
            order = self.placeOrder(stock_code, action, quantity, price)
            if stopLoss:
                order_id = order['Success']['order_id']
                details = self.orderDetails(orderID = order_id)
                status = details[0]['status']
                print(status)
                if status == 'Executed':
                    positions = self.response_formatter(self.get_portfolio_positions())
                    positions[0] = {k: v for k, v in positions[0].items() if k in self.squareOff.__code__.co_varnames}
                    print(positions[0])
                    squareOff = self.squareOff(slPrice=stopLoss, triggerPrice=stopLoss, **positions[0])
                    order['squareOff'] = squareOff
                elif status != 'Executed':
                    self.checkStatus(order_id, stopLoss)
            if target:
                print(orderMap[action])
                targetOrder = self.placeOrder(stock_code, orderMap[action], quantity, target)
                order['targetOrder'] = targetOrder
            return order
        return {"message": "There is already an order in the order list!"}

    def getISO(self):
        from datetime import datetime as dt, timedelta as td
        return (dt.now().isoformat()[:10] + 'T05:30:00.000Z', (dt.now() - td(days=9)).isoformat()[:10] + 'T05:30:00.000Z')

    def placeOrder(self,stock_code, action, quantity, price):
        return self.place_order(stock_code=stockCodes[stock_code]['icici'],
                        exchange_code="NSE",
                        product="margin",
                        action=action,
                        order_type="limit",
                        quantity=quantity,
                        price=price,
                        validity="Day")

    def checkStatus(self, order_id, stopLoss):
        subprocess.Popen(['python3', 'checkStatus.py', str(order_id), '-st', str(self.sessionToken), '-s', str(stopLoss)])

    def squareOff(self, stock_code, quantity, slPrice, action, triggerPrice, settlement_id, cover_quantity, margin_amount):
        return self.square_off(exchange_code= "NSE",
                        product="margin",
                        stock_code=stock_code,
                        quantity=quantity,
                        price=slPrice,
                        action=orderMap[action],
                        order_type="limit",
                        validity="Day",
                        stoploss=triggerPrice,
                        settlement_id=settlement_id,
                        cover_quantity=cover_quantity,
                        open_quantity=(int(quantity) - int(cover_quantity)),
                        margin_amount=margin_amount)

    def getPositions(self):
        return self.response_formatter(self.get_portfolio_positions())

    def getOrders(self):
        return self.response_formatter(self.get_order_list(exchange_code="NSE",from_date=self.getISO()[0],to_date=self.getISO()[1]))

    def orderDetails(self, orderID, exchangeCode = "NSE"):
        return self.response_formatter(self.get_order_detail(exchange_code=exchangeCode, order_id=orderID))