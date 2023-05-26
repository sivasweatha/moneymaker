from datetime import datetime as dt
from datetime import timedelta as td
from maps import stockCodes, ordersClosingMap

class Trader:
    vendor: str
    lastOrderId: str
    lastOrder: dict
    def __init__(self, vendor, sessionToken="") -> None:
        self.vendor = vendor
        self.sessionToken = sessionToken
        self.generateSession()

    def generateSession(self):
        if self.vendor == "icici":
            from vendors.icici import Icici
            self.icici = Icici(self.sessionToken)
        elif self.vendor == 'yahoo':
            from vendors.yahoo import YahooFinance
            self.yahoo = YahooFinance()
        elif self.vendor == 'tvPaperTrader':
            from vendors.tradingviewPaperTrader import PaperTrade
            self.pt = PaperTrade()

    def placeOrder(self, stockName, price, action, quantity, stopLoss, target, **kwargs):
        if self.vendor == "icici":
            return self.icici.order(stock_code=stockName,action=action,quantity=quantity,price=price, stopLoss=stopLoss, target=target)
        elif self.vendor == 'tvPaperTrader':
            if kwargs.get('days'):
                exp = dt.now() + td(days=kwargs.get('days'))
            else:
                exp = dt.now() + td(days=1)
            exp = round(exp.timestamp())
            return self.pt.place(symbol=stockCodes[stockName]['tvPaperTrader'], side=action.lower(), type="limit", qty=quantity, price=price, exp=exp, tp=target, sl=stopLoss)

    def subscribeData(self, stock, onticks=lambda ticks: None, onclose=lambda: None, interval='5m', exchange='NSE', product='cash', right=''):
        whenClose = lambda: ordersClosingMap.get(stock) <= dt.now().hour * 100 + dt.now().minute
        if self.vendor == 'icici':
            intervalMap = {
                '5m': '5minute',
                '1m': '1minute',
                '1s': '1second',
                '30m': '30minute'
            }
            self.icici.on_ticks = onticks
            self.icici.subscribe_feeds(interval=intervalMap[interval], stock_code=stockCodes.get(stock)['icici'], exchange_code=exchange, product_type=product, right=right)
        elif self.vendor == 'yahoo':
            self.yahoo.onTicks = onticks
            self.yahoo.onClose = onclose
            self.yahoo.whenClose = whenClose
            self.yahoo.subscribeFeeds(stockCodes.get(stock)['yfinance'], interval)

    def getOrders(self):
        if self.vendor == 'icici':
            return self.icici.response_formatter(self.icici.get_order_list(exchange_code="NSE",from_date=self.icici.getISO()[0],to_date=self.icici.getISO()[1]))
        elif self.vendor == 'tvPaperTrader':
            ...

    def orderDetails(self, orderID, exchangeCode = "NSE"):
        if self.vendor == 'icici':
            return self.icici.response_formatter(self.icici.get_order_detail(exchange_code=exchangeCode, order_id=orderID))
        elif self.vendor == 'tvPaperTrader':
            ...

    def getPositions(self):
        if self.vendor == 'icici':
            return self.icici.response_formatter(self.icici.get_portfolio_positions())
        elif self.vendor == 'tvPaperTrader':
            ...

    def getHoldings(self):
        if self.vendor == 'icici':
            return self.icici.response_formatter(self.icici.get_portfolio_holdings(exchange_code="NSE",from_date=self.icici.getISO()[0],to_date=self.icici.getISO()[1]))
        elif self.vendor == 'tvPaperTrader':
            ...

    def squareOff(self, slPrice, triggerPrice, stock_code, quantity, action, settlement_id, cover_quantity, margin_amount):
        squareOrder = self.icici.squareOff(stock_code=stock_code,
                        quantity=quantity,
                        slPrice=slPrice,
                        action=action,
                        triggerPrice=triggerPrice,
                        settlement_id=settlement_id,
                        cover_quantity=cover_quantity,
                        margin_amount=margin_amount)
        return squareOrder

    def cancelOrder(self, orderID, exchangeCode= "NSE"):
        cancelOrder = self.icici.cancel_order(exchange_code= exchangeCode,
                                order_id= orderID)
        return cancelOrder