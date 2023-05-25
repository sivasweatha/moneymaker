import json
import questionary as q

class AddStocks:
    def __init__(self, mapJson) -> None:
        self.mapJson = mapJson
        self.get_stock_data()

    def get_stock_data(self):
        stockName = q.text("Please enter the stock name: ").ask()
        stockOpening = int(q.text('Please enter the stock opening [eg. 920]: ').ask())
        ordersClosing = int(q.text('Please enter the orders closing [eg. 1500]: ').ask())
        stockCodes = {}
        vendors = list(self.mapJson['stockCodes'].values())[0].keys()
        for vendor in vendors:
            stockCodes[vendor] = q.text('Please enter the the stock code for {}: '.format(vendor.capitalize())).ask()
        self.post_stock_data(stockName, stockOpening, ordersClosing, stockCodes)

    def post_stock_data(self, stockName, stockOpening, ordersClosing, stockCodes):
        self.mapJson['stockOpeningMap'][stockName] = stockOpening
        self.mapJson['ordersClosingMap'][stockName] = ordersClosing
        self.mapJson['stockCodes'][stockName] = stockCodes
        with open('maps.json', 'w') as fp:
            json.dump(self.mapJson, fp, indent=4)

mapJson = json.load(open('./maps.json'))
add = AddStocks(mapJson)
print('All Set!')