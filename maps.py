import json
mapJson = json.load(open('./maps.json'))

so = mapJson['so']
orderMap = mapJson['orderMap']
ordersClosingMap = mapJson['ordersClosingMap']
stockOpeningMap = mapJson['stockOpeningMap']
stockCodes = mapJson['stockCodes']

strategyOrder = lambda x: so[x] if x in so.keys() else None