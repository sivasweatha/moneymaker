import json
import questionary as q

class AddStocks:
    def __init__(self, mapJson) -> None:
        self.mapJson = mapJson
        self.get_stock_data()

    def get_stock_data(self):
        stockName = q.text("Please enter the stock name (all caps): ").ask()
        stockToExchange = q.text("Please enter the market [eg. IN, US, 24h]: ").ask()
        stockCodes = {}
        vendors = list(self.mapJson['stockCodes'].values())[0].keys()
        for vendor in vendors:
            stockCodes[vendor] = q.text('Please enter the the stock code for {}: '.format(vendor.capitalize())).ask()
        self.post_stock_data(stockName, stockToExchange, stockCodes)

    def post_stock_data(self, stockName, stockToExchange, stockCodes):
        self.mapJson['stockToExchange'][stockName] = stockToExchange
        self.mapJson['stockCodes'][stockName] = stockCodes
        with open('maps.json', 'w') as fp:
            json.dump(self.mapJson, fp, indent=4)

mapJson = json.load(open('./maps.json'))
add = AddStocks(mapJson)
print('All Set!')