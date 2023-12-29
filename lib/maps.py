import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'maps.json')
mapJson = json.load(open(json_path))

so = mapJson['so']
orderMap = mapJson['orderMap']
timings = mapJson['timings']
marketHoursMap = mapJson['marketHours']
stockExchangeMap = mapJson['stockToExchange']
stockCodes = mapJson['stockCodes']

strategyOrder = lambda x: so[x] if x in so.keys() else None