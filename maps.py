import json
mapJson = json.load(open('./maps.json'))

orderMap = mapJson['orderMap']
ordersClosingMap = mapJson['ordersClosingMap']
stockOpeningMap = mapJson['stockOpeningMap']
stockCodes = mapJson['stockCodes']