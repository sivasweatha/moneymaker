from trader import Trader
import time
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("order_id", type=str, help="Order")
parser.add_argument("-s", "--stopLoss", type=str, help="Stop Loss")
parser.add_argument("-st", "--sessionToken", nargs=1, type=str, help="Session token for the trader")
args = parser.parse_args()
order_id = args.order_id
stopLoss = args.stopLoss
sessionToken = args.sessionToken[0]
trader = Trader('icici', sessionToken)

details = trader.orderDetails(orderID=order_id)
status = details[0]['status']

while status != 'Executed':
    details = trader.orderDetails(orderID=order_id)
    status = details[0]['status']
    print(status)
    time.sleep(1)

positions = trader.icici.getPositions()
print(positions)
positions[0] = {k: v for k, v in positions[0].items() if k in trader.squareOff.__code__.co_varnames}
print(positions[0])
squareOff = trader.squareOff(slPrice=stopLoss, triggerPrice=stopLoss, **positions[0])
print(squareOff)