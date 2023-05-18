import json
mapJson = json.load(open('./maps.json'))

orderMap = mapJson['orderMap']
stockClosingMap = mapJson['stockClosingMap']
ordersClosingMap = mapJson['ordersClosingMap']
stockOpeningMap = mapJson['stockOpeningMap']
stockCodes = mapJson['stockCodes']